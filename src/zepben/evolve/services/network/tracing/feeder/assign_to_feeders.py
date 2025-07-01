#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from collections.abc import Collection
from logging import Logger
from typing import Iterable, Union, List, Dict, Any, Set, Type, Generator, TYPE_CHECKING

from zepben.evolve import Switch, ProtectedSwitch, PowerElectronicsConnection
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.networktrace.conditions.conditions import stop_at_open
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

if TYPE_CHECKING:
    from zepben.evolve import AuxiliaryEquipment, Equipment, LvFeeder, ConductingEquipment, EquipmentContainer, Terminal

__all__ = ["AssignToFeeders", "BaseFeedersInternal"]


class AssignToFeeders:
    """
    Convenience class that provides methods for assigning HV/MV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `NetworkTrace`.
    """

    def __init__(self, debug_logger: Logger = None):
        self._debug_logger = debug_logger

    async def run(
        self,
        network: NetworkService,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL,
        start_terminal: Terminal = None
    ):
        """
        Assign equipment to feeders in the specified network, given an optional start terminal.

        :param network: The [NetworkService] to process.
        :param network_state_operators: operator interfaces relating to the network state we are operating on
        :param start_terminal: An optional [Terminal] to start from:
        * When a start terminal is provided, the trace will assign all feeders associated with the terminals equipment to all connected equipment.
        * If no start terminal is provided, all feeder head terminals in the network will be used instead, assigning their associated feeder.
        """

        await AssignToFeedersInternal(
            network_state_operators,
            self._debug_logger
        ).run(network, start_terminal)


class BaseFeedersInternal:
    def __init__(self, network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL, debug_logger: Logger = None):
        self.network_state_operators = network_state_operators
        self._debug_logger = debug_logger

    def _feeders_from_terminal(self, terminal: Terminal) -> Generator[Feeder, None, None]:
        return terminal.conducting_equipment.feeders(self.network_state_operators)

    def _associate_equipment_with_containers(self, equipment_containers: Iterable[EquipmentContainer], equipment: Iterable[Equipment]):
        for feeder in equipment_containers:
            for it in equipment:
                if it is not None:
                    self.network_state_operators.associate_equipment_and_container(it, feeder)

    def _associate_relay_systems_with_containers(self, equipment_containers: Iterable[EquipmentContainer], to_equipment: ProtectedSwitch):
        self._associate_equipment_with_containers(
            equipment_containers,
            [scheme.system for relayFunction in to_equipment.relay_functions for scheme in relayFunction.schemes if scheme.system is not None]
        )

    def _associate_power_electronic_units(self, equipment_containers: Iterable[EquipmentContainer], to_equipment: PowerElectronicsConnection):
        self._associate_equipment_with_containers(equipment_containers, to_equipment.units)

    def _feeder_energizes(self, feeders: Iterable[Union[LvFeeder, Feeder]], lv_feeders: Iterable[LvFeeder]):
        for feeder in feeders:
            for lv_feeder in lv_feeders:
                self.network_state_operators.associate_energizing_feeder(feeder, lv_feeder)

    def _feeder_try_energize_lv_feeders(self, feeders: Iterable[Feeder], lv_feeder_start_points: Set[ConductingEquipment], to_equipment: PowerTransformer):

        lv_feeders = []
        if len(sites := list(to_equipment.sites)) > 0:
            for s in sites:
                lv_feeders.extend(lv_f for lv_f in s.find_lv_feeders(lv_feeder_start_points, self.network_state_operators))
        else:
            for eq in to_equipment:
                lv_feeders.extend(eq.lv_feeders(self.network_state_operators))

        self._feeder_energizes(feeders, lv_feeders)


class AssignToFeedersInternal(BaseFeedersInternal):

    async def run(
        self,
        network: NetworkService,
        start_terminal: Terminal = None
    ):
        feeder_start_points = network.feeder_start_points
        lv_feeder_start_points = network.lv_feeder_start_points
        terminal_to_aux_equipment = network.aux_equipment_by_terminal

        if start_terminal is None:
            for it in list(it for it in network.objects(Feeder)):
                await self.run_with_feeders(it.normal_head_terminal,
                                            feeder_start_points,
                                            lv_feeder_start_points,
                                            terminal_to_aux_equipment,
                                            [it])

        else:
            await self.run_with_feeders(start_terminal,
                                        feeder_start_points,
                                        lv_feeder_start_points,
                                        terminal_to_aux_equipment,
                                        list(self._feeders_from_terminal(start_terminal)))

    async def run_with_feeders(self,
                               terminal: Terminal,
                               feeder_start_points: Set[ConductingEquipment],
                               lv_feeder_start_points: Set[ConductingEquipment],
                               terminal_to_aux_equipment: Dict[Terminal, List[AuxiliaryEquipment]],
                               feeders_to_assign: List[Feeder]):

        if terminal is None or len(feeders_to_assign) == 0:
            return

        if isinstance(start_ce := terminal.conducting_equipment, Switch) and self.network_state_operators.is_open(start_ce):
            self._associate_equipment_with_containers(feeders_to_assign, [start_ce])
        else:
            traversal = await self._create_trace(terminal_to_aux_equipment, feeder_start_points, lv_feeder_start_points, feeders_to_assign)
            await traversal.run(terminal, False, can_stop_on_start_item=False)

    async def _create_trace(self,
                            terminal_to_aux_equipment: Dict[Terminal, List[AuxiliaryEquipment]],
                            feeder_start_points: Set[ConductingEquipment],
                            lv_feeder_start_points: Set[ConductingEquipment],
                            feeders_to_assign: List[Feeder]
                            ) -> NetworkTrace[Any]:

        def _reached_lv(ce: ConductingEquipment):
            return True if ce.base_voltage and ce.base_voltage.nominal_voltage < 1000 else False

        def _reached_substation_transformer(ce: ConductingEquipment):
            return True if isinstance(ce, PowerTransformer) and len(list(ce.substations)) > 0 else False

        async def step_action(nts: NetworkTraceStep, context: StepContext):
            await self._process(nts.path, context, terminal_to_aux_equipment, lv_feeder_start_points, feeders_to_assign)

        return (
            Tracing.network_trace(
                network_state_operators=self.network_state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                debug_logger=self._debug_logger,
                name=f'AssignToFeeders({self.network_state_operators.description})'
            )
            .add_condition(stop_at_open())
            .add_stop_condition(
                lambda step, ctx: step.path.to_equipment in feeder_start_points
            )
            .add_queue_condition(
                lambda step, ctx, x, y: not _reached_substation_transformer(step.path.to_equipment)
            )
            .add_queue_condition(
                lambda step, ctx, x, y: not _reached_lv(step.path.to_equipment)
            )
            .add_step_action(step_action)
        )

    async def _process(self,
                       step_path: NetworkTraceStep.Path,
                       step_context: StepContext,
                       terminal_to_aux_equipment: Dict[Terminal, Collection[AuxiliaryEquipment]],
                       lv_feeder_start_points: Set[ConductingEquipment],
                       feeders_to_assign: List[Feeder]):

        if step_path.traced_internally and not step_context.is_start_item:
            return

        self._associate_equipment_with_containers(feeders_to_assign, terminal_to_aux_equipment.get(step_path.to_terminal, {}))
        self._associate_equipment_with_containers(feeders_to_assign, [step_path.to_equipment])

        to_equip = step_path.to_equipment
        if isinstance(to_equip, PowerTransformer):
            self._feeder_try_energize_lv_feeders(feeders_to_assign, lv_feeder_start_points, to_equip)
        elif isinstance(to_equip, ProtectedSwitch):
            self._associate_relay_systems_with_containers(feeders_to_assign, to_equip)
        elif isinstance(to_equip, PowerElectronicsConnection):
            self._associate_power_electronic_units(feeders_to_assign, to_equip)
