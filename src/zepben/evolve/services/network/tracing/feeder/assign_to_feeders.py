#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections.abc import Collection
from typing import Set, Callable, Optional, Awaitable, Any, Iterable

from zepben.evolve import Switch, AuxiliaryEquipment, ProtectedSwitch, Equipment, LvFeeder
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, EquipmentContainer, Site
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.services.network.network_service import NetworkService

__all__ = ["AssignToFeeders"]

from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing

from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext


class AssignToFeeders:
    """
    Convenience class that provides methods for assigning HV/MV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `NetworkTrace`.
    """

    async def run(self,
                  network: NetworkService,
                  network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL,
                  start_terminal: Terminal=None):
        """
        Assign equipment to feeders in the specified network, given an optional start terminal.

        :param network: The [NetworkService] to process.
        :param network_state_operators: operator interfaces relating to the network state we are operating on
        :param start_terminal: An optional [Terminal] to start from:
        * When a start terminal is provided, the trace will assign all feeders associated with the terminals equipment to all connected equipment.
        * If no start terminal is provided, all feeder head terminals in the network will be used instead, assigning their associated feeder.
        """
        await AssignToFeedersInternal(network_state_operators).run(network, start_terminal)


class BaseFeedersInternal:
    def __init__(self, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        self.network_state_operators = network_state_operators

    def _feeders_from_terminal(self, terminal: Terminal):
        return terminal.conducting_equipment.get_filtered_containers(Feeder)(self.network_state_operators)

    def _associate_equipment_with_containers(self, equipment_containers: Iterable[EquipmentContainer], equipment: Iterable[Equipment]):
        for item in equipment_containers:
            for feeder in equipment:
                self.network_state_operators.associate_equipment_and_container(item, feeder)

    def _associate_relay_systems_with_containers(self, equipment_containers: Iterable[EquipmentContainer], to_equipment: ProtectedSwitch):
        self._associate_equipment_with_containers(equipment_containers, [
            scheme.system
            for relayFunction in to_equipment.relay_functions
            for scheme in relayFunction.schemes
            if scheme.system is not None]
                                                  )

    def _feeder_energizes(self, feeders: Iterable[Feeder], lv_feeders: Iterable[LvFeeder]):
        for feeder in feeders:
            for lv_feeder in lv_feeders:
                self.network_state_operators.associate_energizing_feeder(feeder, lv_feeder)

    def _feeder_try_energize_lv_feeders(self, to_equipment: PowerTransformer, lv_feeder_start_points: Set[ConductingEquipment]):
        sites = to_equipment.get_filtered_containers(Site, self.network_state_operators)
        if len(sites) > 0:
            self._feeder_energizes(sites.find_lv_feeders(lv_feeder_start_points, self.network_state_operators))
        else:
            self._feeder_energizes(to_equipment.get_filtered_containers(LvFeeder, self.network_state_operators))


class AssignToFeedersInternal(BaseFeedersInternal):

    async def run(self,
                  network: NetworkService,
                  start_terminal: Terminal=None):
        self.network_state_operators = self.network_state_operators

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
                                        self._feeders_from_terminal(start_terminal))

    async def run_with_feeders(self,
                               terminal: Terminal,
                               feeder_start_points: Set[ConductingEquipment],
                               lv_feeder_start_points: Set[ConductingEquipment],
                               terminal_to_aux_equipment: dict[Terminal, list[AuxiliaryEquipment]],
                               feeders_to_assign: list[Feeder]):

        if terminal is None or len(feeders_to_assign) == 0:
            return

        start_ce = terminal.conducting_equipment

        if isinstance(start_ce, Switch) and self.network_state_operators.is_open(start_ce):
            feeders_to_assign.associate_equipment(start_ce)
        else:
            traversal = self._create_trace(terminal_to_aux_equipment, feeder_start_points, lv_feeder_start_points, feeders_to_assign)
            traversal.run(terminal, False, can_stop_on_start_item=False)

    def _create_trace(self,
                      terminal_to_aux_equipment: dict[Terminal, list[AuxiliaryEquipment]],
                      feeder_start_points: Set[ConductingEquipment],
                      lv_feeder_start_points: Set[ConductingEquipment],
                      feeders_to_assign: list[Feeder]) -> NetworkTrace[...]:

        def _reached_lv(ce: ConductingEquipment):
            return True if ce.base_voltage and ce.base_voltage.nominal_voltage < 1000 else False

        def _reached_substation_transformer(ce: ConductingEquipment):
            return True if isinstance(ce, PowerTransformer) and len(list(ce.substations)) > 0 else False

        def stop_condition(_in, *args):
            path, *_ = _in
            return path.to_equipment in feeder_start_points

        def queue_condition_a(_in, *args):
            path, *_ = _in
            return not _reached_substation_transformer(path.to_equipment)

        def queue_condition_b(_in, *args):
            path, *_ = _in
            return not _reached_lv(path.to_equipment)

        def step_action(_in, context):
            path, found_lv_feeder = _in
            return self._process(path, context, terminal_to_aux_equipment, lv_feeder_start_points, feeders_to_assign)


        return (
            Tracing.network_trace(self.network_state_operators, NetworkTraceActionType.ALL_STEPS)
                .add_condition(self.network_state_operators.stop_at_open())
                .add_stop_condition(Traversal.stop_condition(stop_condition))
                .add_queue_condition(Traversal.queue_condition(queue_condition_a))
                .add_queue_condition(Traversal.queue_condition(queue_condition_b))
                .add_step_action(Traversal.step_action(step_action))
        )

    async def _process(self,
                 step_path: NetworkTraceStep.Path,
                 step_context: StepContext,
                 terminal_to_aux_equipment: dict[Terminal, Collection[AuxiliaryEquipment]],
                 lv_feeder_start_points: Set[ConductingEquipment],
                 feeders_to_assign: list[Feeder]):
        if step_path.traced_internally and not step_context.is_start_item:
            return

        self._associate_equipment_with_containers(feeders_to_assign, terminal_to_aux_equipment[step_path.to_terminal])
        self._associate_equipment_with_containers(feeders_to_assign, step_path.to_equipment)

        if isinstance(step_path.to_equipment, PowerTransformer):
            feeders_to_assign._try_energize_lv_feeders(step_path.to_equipment, lv_feeder_start_points)
        elif isinstance(step_path.to_equipment, ProtectedSwitch):
            feeders_to_assign._associate_relay_systems(step_path.to_equipment)


