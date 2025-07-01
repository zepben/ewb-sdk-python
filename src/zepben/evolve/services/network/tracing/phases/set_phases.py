#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections.abc import Sequence
from functools import singledispatchmethod
from typing import Union, Set, Iterable, List, Type, TYPE_CHECKING, Optional, Callable

from zepben.evolve import PhaseStatus, add_neutral
from zepben.evolve.exceptions import TracingException, PhaseException
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_connected import TerminalConnectivityConnected
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_internal import TerminalConnectivityInternal
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue

if TYPE_CHECKING:
    from logging import Logger

__all__ = ["SetPhases"]


class SetPhases:
    """
    Convenience class that provides methods for setting phases on a `NetworkService`.
    This class is backed by a `NetworkTrace`.
    """

    def __init__(self, debug_logger: Logger = None):
        self._debug_logger = debug_logger

    class PhasesToFlow:
        def __init__(self, nominal_phase_paths: Iterable[NominalPhasePath], step_flowed_phases: bool = False):
            self.nominal_phase_paths = nominal_phase_paths
            self.step_flowed_phases = step_flowed_phases

        def __str__(self):
            return f'PhasesToFlow(nominal_phase_paths={self.nominal_phase_paths}, step_flowed_phases={self.step_flowed_phases})'

    @singledispatchmethod
    async def run(
        self,
        target: Union[NetworkService, Terminal],
        phases: Union[PhaseCode, Iterable[SinglePhaseKind]] = None,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL
    ):
        """

        :param target:
        :param phases:
        :param network_state_operators: The `NetworkStateOperators` to be used when setting phases.
        """

        raise ValueError('INTERNAL ERROR: incorrect params')

    @run.register
    async def _(
        self,
        network: NetworkService,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL
    ):
        """
        Apply phases and flow from all energy sources in the network.
        This will apply `Terminal.phases` to all terminals on each `EnergySource` and then flow along the connected network.

        :param network: The network in which to apply phases.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting phases.
        """

        def _terminals_from_network():
            for energy_source in network.objects(EnergySource):
                for terminal in energy_source.terminals:
                    self._apply_phases(terminal.phases.single_phases, terminal, network_state_operators)
                    yield terminal

        await self._run_terminals(_terminals_from_network(), network_state_operators=network_state_operators)

    @run.register
    async def _(
        self,
        start_terminal: Terminal,
        phases: Union[PhaseCode, List[SinglePhaseKind], Set[SinglePhaseKind]] = None,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL,
        seed_terminal: Terminal = None
    ):
        """
        Apply phases to the `start_terminal` and flow, optionally specifying a `seed_terminal`. If specified, the `seed_terminal`
        and `start_terminal` must have the same `Terminal.conducting_equipment`

        :param start_terminal: The terminal to start applying phases from.
        :param phases: The phases to apply. Must only contain ABCN, if None, `SetPhases` will flow phases already set on `start_terminal`.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting phases.
        :param seed_terminal: The terminal from which to spread the phases from.
        """

        if phases is None:
            # Flow phases already set on the given Terminal
            await self._run_terminals([start_terminal], network_state_operators=network_state_operators)

        elif isinstance(phases, PhaseCode):
            await self.run(start_terminal, phases=phases.single_phases, network_state_operators=network_state_operators)

        elif isinstance(phases, (List, Set)):
            if seed_terminal:
                nominal_phase_paths = self._get_nominal_phase_paths(network_state_operators, seed_terminal, start_terminal, list(phases))

                if self._flow_phases(network_state_operators, seed_terminal, start_terminal, nominal_phase_paths):
                    await self.run(start_terminal, network_state_operators=network_state_operators)

            else:
                if len(phases) != len(start_terminal.phases.single_phases):
                    raise TracingException(
                        f"Attempted to apply phases [{', '.join(phase.name for phase in phases)}] to {start_terminal} with nominal phases {start_terminal.phases.name}. "
                        f"Number of phases to apply must match the number of nominal phases. Found {len(phases)}, expected {len(start_terminal.phases.single_phases)}"
                    )
                self._apply_phases(phases, start_terminal, network_state_operators)
                await self._run_terminals([start_terminal], network_state_operators=network_state_operators)

        else:
            raise ValueError('ERROR: phases must either be a PhaseCode, or Union[List, Set]')

    def spread_phases(
        self,
        from_terminal: Terminal,
        to_terminal: Terminal,
        phases: List[SinglePhaseKind] = None,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL
    ):
        """
        Apply nominal phases from the `from_terminal` to the `to_terminal`.

        :param from_terminal: The terminal to from which to spread phases.
        :param to_terminal: The terminal to spread phases to.
        :param phases: The nominal phases on which to spread phases, if None, `SetPhases` will use phases from `from_terminal`.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting phases.
        """

        paths = self._get_nominal_phase_paths(network_state_operators, from_terminal, to_terminal, phases or from_terminal.phases.single_phases)
        self._flow_phases(network_state_operators, from_terminal, to_terminal, paths)

    async def _run_terminals(self, terminals: Iterable[Terminal], network_state_operators: Type[NetworkStateOperators]):

        partially_energised_transformers: Set[PowerTransformer] = set()
        trace = self._create_network_trace(network_state_operators, partially_energised_transformers)

        for terminal in terminals:
            await self._run_terminal_trace(terminal, trace)

        # Go back and add any missing phases to transformers that were energised from a downstream side with fewer phases
        #  when they were in parallel, that successfully energised all the upstream side phases. This setup stops the spread
        #  from coming back down the upstream (it is fully energised) and processing the transformer correctly.

        if self._debug_logger:
            self._debug_logger.info('Reprocessing partially energised transformers...')

        for tx in partially_energised_transformers:
            terminals_by_energisation = [(terminal, _not_fully_energised(network_state_operators, terminal)) for terminal in tx.terminals]
            if any(energised for _, energised in terminals_by_energisation):

                partially_energised = []
                fully_energised = []
                for terminal, energised in terminals_by_energisation:
                    if energised:
                        partially_energised.append(terminal)
                    else:
                        fully_energised.append(terminal)

                for partial in partially_energised:
                    for full in fully_energised:
                        self._flow_transformer_phases(network_state_operators, full, partial, allow_suspect_flow=True)
                    await self._run_terminal_trace(partial, trace)

        if self._debug_logger:
            self._debug_logger.info("Reprocessing complete.")

    async def _run_terminal_trace(self, terminal: Terminal, network_trace: NetworkTrace[PhasesToFlow]):
        await network_trace.run(
            terminal,
            self.PhasesToFlow(
                [NominalPhasePath(SinglePhaseKind.NONE, it) for it in terminal.phases]
            ), can_stop_on_start_item=False
        )

        # This is called in a loop so we need to reset it for each call. We choose to do this after to release the memory
        #  used by the trace once it is finished, rather than before, which has would be marginally quicker on the first
        #  call, but would hold onto the memory as long as the `SetPhases` instance is referenced.

        network_trace.reset()

    @staticmethod
    def _nominal_phase_path_to_phases(nominal_phase_paths: list[NominalPhasePath]) -> list[SinglePhaseKind]:
        return [it.to_phase for it in nominal_phase_paths]

    def _create_network_trace(
        self,
        state_operators: Type[NetworkStateOperators],
        partially_energised_transformers: Set[PowerTransformer]
    ) -> NetworkTrace[PhasesToFlow]:

        def step_action(nts, ctx):
            path, phases_to_flow = nts
            #  We always assume the first step terminal already has the phases applied, so we don't do anything on the first step
            phases_to_flow.step_flowed_phases = True if ctx.is_start_item else (
                self._flow_phases(state_operators, path.from_terminal, path.to_terminal, phases_to_flow.nominal_phase_paths)
            )

            # If we flowed phases but failed to completely energise a transformer, keep track of it for reprocessing later.
            if (phases_to_flow.step_flowed_phases
                and isinstance(path.to_equipment, PowerTransformer)
                and _not_fully_energised(state_operators, path.to_terminal)
            ):
                partially_energised_transformers.add(path.to_equipment)

        return (
            Tracing.network_trace_branching(
                network_state_operators=state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                debug_logger=self._debug_logger,
                name=f'SetPhases({state_operators.description})',
                queue_factory=lambda: WeightedPriorityQueue.process_queue(lambda it: it.path.to_terminal.phases.num_phases),
                branch_queue_factory=lambda: WeightedPriorityQueue.branch_queue(lambda it: it.path.to_terminal.phases.num_phases),
                compute_data=self._compute_next_phases_to_flow(state_operators)
            )
            .add_queue_condition(
                lambda next_step, x, y, z: len(next_step.data.nominal_phase_paths) > 0
            )
            .add_step_action(step_action)
        )

    def _compute_next_phases_to_flow(self, state_operators: Type[NetworkStateOperators]) -> ComputeData[PhasesToFlow]:
        def inner(step, _, next_path):
            if not step.data.step_flowed_phases:
                return self.PhasesToFlow([])

            return self.PhasesToFlow(
                self._get_nominal_phase_paths(
                    state_operators,
                    next_path.from_terminal,
                    next_path.to_terminal,
                    self._nominal_phase_path_to_phases(step.data.nominal_phase_paths)
                )
            )

        return ComputeData(inner)

    @staticmethod
    def _apply_phases(
        phases: List[SinglePhaseKind],
        terminal: Terminal,
        state_operators: Type[NetworkStateOperators]
    ):
        traced_phases = state_operators.phase_status(terminal)
        for i, nominal_phase in enumerate(terminal.phases.single_phases):
            traced_phases[nominal_phase] = phases[i] if phases[i] not in PhaseCode.XY else SinglePhaseKind.NONE

    def _get_nominal_phase_paths(
        self,
        state_operators: Type[NetworkStateOperators],
        from_terminal: Terminal,
        to_terminal: Terminal,
        phases: Sequence[SinglePhaseKind] = None
    ) -> List[NominalPhasePath]:

        if phases is None:
            phases = from_terminal.phases.single_phases

        traced_internally = from_terminal.conducting_equipment == to_terminal.conducting_equipment
        phases_to_flow = self._get_phases_to_flow(state_operators, from_terminal, phases, traced_internally)

        if traced_internally:
            return list(TerminalConnectivityInternal().between(from_terminal, to_terminal, phases_to_flow).nominal_phase_paths)
        else:
            return list(TerminalConnectivityConnected().terminal_connectivity(from_terminal, to_terminal, phases_to_flow).nominal_phase_paths)

    @staticmethod
    def _get_phases_to_flow(
        state_operators: Type[NetworkStateOperators],
        terminal: Terminal,
        phases: Sequence[SinglePhaseKind],
        internal_flow: bool
    ) -> Set[SinglePhaseKind]:

        if internal_flow:
            if ce := terminal.conducting_equipment:
                return set(p for p in phases if not state_operators.is_open(ce, p))
            return set()
        return set(phases)

    def _flow_phases(
        self,
        state_operators: Type[NetworkStateOperators],
        from_terminal: Terminal,
        to_terminal: Terminal,
        nominal_phase_paths: List[NominalPhasePath]
    ) -> bool:

        if (from_terminal.conducting_equipment == to_terminal.conducting_equipment
            and isinstance(from_terminal.conducting_equipment, PowerTransformer)
        ):
            return self._flow_transformer_phases(state_operators, from_terminal, to_terminal, nominal_phase_paths, allow_suspect_flow=False)
        else:
            return self._flow_straight_phases(state_operators, from_terminal, to_terminal, nominal_phase_paths)

    def _flow_straight_phases(
        self,
        state_operators: Type[NetworkStateOperators],
        from_terminal: Terminal,
        to_terminal: Terminal,
        nominal_phase_paths: List[NominalPhasePath]
    ) -> bool:

        from_phases = state_operators.phase_status(from_terminal)
        to_phases = state_operators.phase_status(to_terminal)

        updated_phases = []

        for from_, to_ in ((p.from_phase, p.to_phase) for p in nominal_phase_paths):
            self._try_set_phase(from_phases[from_], from_terminal, from_phases, from_, to_terminal, to_phases, to_, lambda: updated_phases.append(True))

        return any(updated_phases)

    def _flow_transformer_phases(
        self,
        state_operators: Type[NetworkStateOperators],
        from_terminal: Terminal,
        to_terminal: Terminal,
        nominal_phase_paths: List[NominalPhasePath] = None,
        allow_suspect_flow: bool = False
    ) -> bool:

        paths = nominal_phase_paths or self._get_nominal_phase_paths(state_operators, from_terminal, to_terminal)

        # If this transformer doesn't mess with phases (or only adds or removes a neutral), just use the straight
        #  processor. We use the number of phases rather than the phases themselves to correctly handle the shift
        #  from known to unknown phases. e.g. AB -> XY.

        if from_terminal.phases.without_neutral.num_phases == to_terminal.phases.without_neutral.num_phases:
            return self._flow_transformer_phases_adding_neutral(state_operators, from_terminal, to_terminal, paths)

        from_phases = state_operators.phase_status(from_terminal)
        to_phases = state_operators.phase_status(to_terminal)

        updated_phases = []

        # Split the phases into ones we need to flow directly, and ones that have been added by a transformer. In
        #  the case of an added Y phase (SWER -> LV2 transformer) we need to flow the phases before we can calculate
        #  the missing phase.
        flow_phases = (p for p in paths if p.from_phase == SinglePhaseKind.NONE)
        add_phases = (p for p in paths if p.from_phase != SinglePhaseKind.NONE)
        for p in flow_phases:
            self._try_add_phase(from_terminal, from_phases, to_terminal, to_phases, p.to_phase, allow_suspect_flow,
                                lambda: updated_phases.append(True))

        for p in add_phases:
            self._try_set_phase(from_phases[p.from_phase], from_terminal, from_phases, p.from_phase,
                                to_terminal, to_phases, p.to_phase, lambda: updated_phases.append(True))

        return any(updated_phases)

    def _flow_transformer_phases_adding_neutral(
        self,
        state_operators: Type[NetworkStateOperators],
        from_terminal: Terminal,
        to_terminal: Terminal,
        paths: List[NominalPhasePath]
    ) -> bool:

        updated_phases = self._flow_straight_phases(state_operators, from_terminal, to_terminal,
                                                    [it for it in paths if it != add_neutral])

        # Only add the neutral if we added a phases to the transformer, otherwise you will flag an energised neutral
        #  with no active phases. We check to see if we need to add the neutral to prevent adding it when we traverse
        #  through the transformer in the opposite direction.

        if updated_phases and (add_neutral in paths):
            state_operators.phase_status(to_terminal)[SinglePhaseKind.N] = SinglePhaseKind.N

        return updated_phases

    def _try_set_phase(
        self,
        phase: SinglePhaseKind,
        from_terminal: Terminal,
        from_phases: PhaseStatus,
        from_: SinglePhaseKind,
        to_terminal: Terminal,
        to_phases: PhaseStatus,
        to_: SinglePhaseKind,
        on_success: Callable[[], None]
    ):
        try:
            if phase != SinglePhaseKind.NONE and to_phases.__setitem__(to_, phase):
                if self._debug_logger:
                    self._debug_logger.info(f'   {from_terminal.mrid}[{from_}] -> {to_terminal.mrid}[{to_}]: set to {phase}')
                on_success()
        except PhaseException:
            self._throw_cross_phase_exception(from_terminal, from_phases, from_, to_terminal, to_phases, to_)

    def _try_add_phase(
        self,
        from_terminal: Terminal,
        from_phases: PhaseStatus,
        to_terminal: Terminal,
        to_phases: PhaseStatus,
        to_: SinglePhaseKind,
        allow_suspect_flow: bool,
        on_success: Callable[[], None]
    ):
        # The phases that can be added are ABCN and Y, so for all cases other than Y we can just use the added phase. For
        #   Y we need to look at what the phases on the other side of the transformer are to determine what has been added.

        phase = _unless_none(
            to_phases[to_], _to_y_phase(from_phases[from_terminal.phases.single_phases[0]], allow_suspect_flow)
        ) if to_ == SinglePhaseKind.Y else to_

        self._try_set_phase(phase, from_terminal, from_phases, SinglePhaseKind.NONE, to_terminal, to_phases, to_, on_success)

    @staticmethod
    def _throw_cross_phase_exception(
        from_terminal: Terminal,
        from_phases: PhaseStatus,
        from_: SinglePhaseKind,
        to_terminal: Terminal,
        to_phases: PhaseStatus,
        to_: SinglePhaseKind
    ):
        phase_desc = f'{from_.name}' if from_ == to_ else f'path {from_.name} to {to_.name}'

        def get_ce_details(terminal: Terminal):
            if terminal.conducting_equipment:
                return terminal.conducting_equipment
            return ''

        if from_terminal.conducting_equipment == to_terminal.conducting_equipment:
            terminal_desc = f'from {from_terminal} to {to_terminal} through {from_terminal.conducting_equipment}'
        else:
            terminal_desc = f'between {from_terminal} on {get_ce_details(from_terminal)} and {to_terminal} on {get_ce_details(to_terminal)}'

        raise PhaseException(
            f"Attempted to flow conflicting phase {from_phases[from_].name} onto {to_phases[to_].name} on nominal phase {phase_desc}. This occurred while " +
            f"flowing {terminal_desc}. This is often caused by missing open points, or incorrect phases in upstream equipment that should be " +
            "corrected in the source data."
        )


def _not_fully_energised(network_state_operators: Type[NetworkStateOperators], terminal: Terminal) -> bool:
    phase_status = network_state_operators.phase_status(terminal)
    return any(phase_status[it] == SinglePhaseKind.NONE for it in terminal.phases.single_phases)


def _unless_none(single_phase_kind: SinglePhaseKind, default: SinglePhaseKind) -> Optional[SinglePhaseKind]:
    if single_phase_kind == SinglePhaseKind.NONE:
        return default
    return single_phase_kind


def _to_y_phase(phase: SinglePhaseKind, allow_suspect_flow: bool) -> SinglePhaseKind:
    # NOTE: If we are adding Y to a C <-> XYN transformer we will leave it de-energised to prevent cross-phase energisation
    #       when there is a parallel C to XN transformer. This can be changed if the entire way XY mappings are reworked to
    #       use traced phases instead of the X and Y, which includes in straight paths to prevent cross-phase wiring.
    #
    #       Due to both AB and AC energising X with A, until the above is fixed we don't know which one we are using, so if
    #       we aren't allowing suspect flows we will also leave it de-energised to prevent cross-phase energisation when you
    #       have parallel XY <-> XN transformers on an AC line (adds B to the Y "C wire"). If we are allowing suspect flows
    #       for partially energised transformers on a second pass we will default these to use AB.

    if phase == SinglePhaseKind.A:
        if allow_suspect_flow:
            return SinglePhaseKind.B
        else:
            return SinglePhaseKind.NONE
    elif phase == SinglePhaseKind.B:
        return SinglePhaseKind.C
    elif phase == SinglePhaseKind.C:
        return SinglePhaseKind.NONE
    else:
        return SinglePhaseKind.NONE
