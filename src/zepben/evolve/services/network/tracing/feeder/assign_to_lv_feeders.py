#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from functools import singledispatchmethod
from typing import Collection, List, Generator, TypeVar, Dict, Set, Type, TYPE_CHECKING

from zepben.evolve import Switch, ProtectedSwitch, PowerElectronicsConnection, Terminal, ConductingEquipment, AuxiliaryEquipment, LvFeeder
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import BaseFeedersInternal
from zepben.evolve.services.network.tracing.networktrace.conditions.conditions import stop_at_open
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

if TYPE_CHECKING:
    from logging import Logger

T = TypeVar("T")

__all__ = ["AssignToLvFeeders"]


class AssignToLvFeeders:
    """
    Convenience class that provides methods for assigning LV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `BasicTraversal`.
    """

    def __init__(self, debug_logger: Logger = None):
        self._debug_logger = debug_logger

    @singledispatchmethod
    async def run(
        self,
        network: NetworkService,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL,
        start_terminal: Terminal = None
    ):
        """
        Assign equipment to each feeder in the specified network.

        :param network: The network containing the feeders to process.
        :param network_state_operators: `NetworkStateOperators` to use for stateful operations.
        :param start_terminal: get the lv feeders for this `Terminal`s `ConductingEquipment`.
        """

        await AssignToLvFeedersInternal(
            network_state_operators,
            self._debug_logger
        ).run(network, start_terminal)

    @run.register
    async def _(
        self,
        terminal: Terminal,
        lv_feeder_start_points: Set[ConductingEquipment],
        terminal_to_aux_equipment: Dict[Terminal, List[AuxiliaryEquipment]],
        lv_feeders_to_assign: List[LvFeeder],
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL
    ):
        await AssignToLvFeedersInternal(
            network_state_operators,
            self._debug_logger
        ).run_with_feeders(
            terminal,
            lv_feeder_start_points,
            terminal_to_aux_equipment,
            lv_feeders_to_assign
        )


class AssignToLvFeedersInternal(BaseFeedersInternal):

    async def run(
        self,
        network: NetworkService,
        start_terminal: Terminal = None
    ):
        lv_feeder_start_points = network.lv_feeder_start_points
        terminal_to_aux_equipment = network.aux_equipment_by_terminal

        if start_terminal is None:
            for lv_feeder in network.objects(LvFeeder):

                head_terminal = lv_feeder.normal_head_terminal
                if head_terminal is not None:

                    head_equipment = head_terminal.conducting_equipment
                    if head_equipment is not None:

                        for feeder in head_equipment.feeders(self.network_state_operators):
                            self.network_state_operators.associate_energizing_feeder(feeder, lv_feeder)

                #  We can run from each LV feeder as we process them, as being associated with their energizing feeders is not a requirement of the trace.
                await self.run_with_feeders(lv_feeder.normal_head_terminal,
                                            lv_feeder_start_points,
                                            terminal_to_aux_equipment,
                                            [lv_feeder])

        else:
            await self.run_with_feeders(start_terminal,
                                        lv_feeder_start_points,
                                        terminal_to_aux_equipment,
                                        self._lv_feeders_from_terminal(start_terminal))

    async def run_with_feeders(
        self,
        terminal: Terminal,
        lv_feeder_start_points: Set[ConductingEquipment],
        terminal_to_aux_equipment: Dict[Terminal, List[AuxiliaryEquipment]],
        lv_feeders_to_assign: List[LvFeeder]
    ):
        if terminal is None or len(lv_feeders_to_assign) == 0:
            return

        if isinstance(start_ce := terminal.conducting_equipment, Switch) and self.network_state_operators.is_open(start_ce):
            self._associate_equipment_with_containers(lv_feeders_to_assign, [start_ce])
        else:
            traversal = self._create_trace(terminal_to_aux_equipment, lv_feeder_start_points, lv_feeders_to_assign)
            await traversal.run(terminal, False)

    def _create_trace(
        self,
        terminal_to_aux_equipment: Dict[Terminal, List[AuxiliaryEquipment]],
        lv_feeder_start_points: Set[ConductingEquipment],
        lv_feeders_to_assign: List[LvFeeder]
    ) -> NetworkTrace[T]:
        def _reached_hv(ce: ConductingEquipment):
            return True if ce.base_voltage and ce.base_voltage.nominal_voltage >= 1000 else False

        async def step_action(nts: NetworkTraceStep, context):
            await self._process(nts.path, nts.data, context, terminal_to_aux_equipment, lv_feeder_start_points, lv_feeders_to_assign)

        return (
            Tracing.network_trace(
                network_state_operators=self.network_state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                debug_logger=self._debug_logger,
                name=f'AssignToLvFeeders({self.network_state_operators.description})',
                compute_data=(lambda x, y, next_path: next_path.to_equipment in lv_feeder_start_points)
            )
            .add_condition(stop_at_open())
            .add_stop_condition(lambda step, ctx: step.data)
            .add_queue_condition(
                lambda next_step, *args: next_step.data or not _reached_hv(next_step.path.to_equipment)
            )
            .add_step_action(step_action)
        )

    async def _process(
        self,
        step_path: NetworkTraceStep.Path,
        found_lv_feeder: bool,
        step_context: StepContext,
        terminal_to_aux_equipment: Dict[Terminal, Collection[AuxiliaryEquipment]],
        lv_feeder_start_points: Set[ConductingEquipment],
        lv_feeders_to_assign: List[LvFeeder]
    ):
        if step_path.traced_internally and not step_context.is_start_item:
            return

        # It might be tempting to check `stepContext.isStopping`, but that would also pick up open points between LV feeders which is not good.
        if found_lv_feeder:

            for it in (found_lv_feeders := list(self._find_lv_feeders(step_path.to_equipment, lv_feeder_start_points))):
                # Energize the LV feeders that we are processing by the energizing feeders of what we found
                self._feeder_energizes(self.network_state_operators.get_energizing_feeders(it), lv_feeders_to_assign)

            for it in lv_feeders_to_assign:
                # Energize the LV feeders we found by the energizing feeders we are processing
                self._feeder_energizes(self.network_state_operators.get_energizing_feeders(it), found_lv_feeders)

        aux_equip_for_this_terminal = terminal_to_aux_equipment.get(step_path.to_terminal, {})

        self._associate_equipment_with_containers(lv_feeders_to_assign, [step_path.to_equipment])
        self._associate_equipment_with_containers(lv_feeders_to_assign, aux_equip_for_this_terminal)

        to_equip = step_path.to_equipment
        if isinstance(to_equip, ProtectedSwitch):
            self._associate_relay_systems_with_containers(lv_feeders_to_assign, to_equip)
        elif isinstance(to_equip, PowerElectronicsConnection):
            self._associate_power_electronic_units(lv_feeders_to_assign, to_equip)

    def _find_lv_feeders(self, ce: ConductingEquipment, lv_feeder_start_points: Set[ConductingEquipment]) -> Generator[LvFeeder, None, None]:
        if sites := list(ce.sites):
            for site in sites:
                for feeder in site.find_lv_feeders(lv_feeder_start_points, self.network_state_operators):
                    yield feeder
        else:
            for feeder in ce.lv_feeders(self.network_state_operators):
                yield feeder

    def _lv_feeders_from_terminal(self, terminal: Terminal) -> List[LvFeeder]:
        return list(terminal.conducting_equipment.lv_feeders(self.network_state_operators))
