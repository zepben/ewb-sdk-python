#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Optional, Awaitable, Any, Collection, Iterable

from zepben.evolve import Switch, AuxiliaryEquipment, ProtectedSwitch, Traversal
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.services.common.resolver import normal_head_terminal
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import BaseFeedersInternal
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.step_context import StepContext

__all__ = ["AssignToLvFeeders"]


class AssignToLvFeeders:
    async def run(self,
                  network: NetworkService,
                  network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL,
                  start_terminal: Terminal=None):
        await AssignToLvFeedersInternal(network_state_operators).run(network, start_terminal)


class AssignToLvFeedersInternal(BaseFeedersInternal):
    """
    Convenience class that provides methods for assigning LV feeders on a `NetworkService`.
    Requires that a Feeder have a normalHeadTerminal with associated ConductingEquipment.
    This class is backed by a `BasicTraversal`.
    """

    async def run(self,
                  network: NetworkService,
                  start_terminal: Terminal=None):
        """
        Assign equipment to each feeder in the specified network.

        :param network: The network containing the feeders to process
        """
        self.network_state_operators = self.network_state_operators

        lv_feeder_start_points = network.lv_feeder_start_points
        terminal_to_aux_equipment = network.aux_equipment_by_terminal

        if start_terminal is None:
            for lv_feeder in network.objects(LvFeeder):
                head_terminal = lv_feeder.normal_head_terminal
                if head_terminal is None:
                    continue
                head_equipment = head_terminal.conducting_equipment
                if head_equipment is None:
                    continue
                for feeder in head_equipment.get_filtered_containers(Feeder, self.network_state_operators):
                    self.network_state_operators.associate_energizing_feeder(feeder, lv_feeder)
                await self.run_with_feeders(lv_feeder.normal_head_terminal,
                                            lv_feeder_start_points,
                                            terminal_to_aux_equipment,
                                            [lv_feeder])

        else:
            await self.run_with_feeders(normal_head_terminal,
                                        lv_feeder_start_points,
                                        terminal_to_aux_equipment,
                                        self._lv_feeders_from_terminal(start_terminal))

    async def run_with_feeders(self,
                               terminal: Terminal,
                               lv_feeder_start_points: Set[ConductingEquipment],
                               terminal_to_aux_equipment: dict[Terminal, list[AuxiliaryEquipment]],
                               lv_feeders_to_assign: list[LvFeeder]):

        if terminal is None or len(lv_feeders_to_assign) == 0:
            return

        start_ce = terminal.conducting_equipment

        if isinstance(start_ce, Switch) and self.network_state_operators.is_open(start_ce):
            lv_feeders_to_assign.associate_equipment(start_ce)
        else:
            traversal = await self._create_trace(terminal_to_aux_equipment, lv_feeder_start_points, lv_feeders_to_assign)
            traversal.run(terminal, False)

    async def _create_trace(self,
                      terminal_to_aux_equipment: dict[Terminal, list[AuxiliaryEquipment]],
                      lv_feeder_start_points: Set[ConductingEquipment],
                      lv_feeders_to_assign: list[LvFeeder]) -> NetworkTrace[...]:

        def _reached_hv(ce: ConductingEquipment):
            return True if ce.base_voltage and ce.base_voltage.nominal_voltage >= 1000 else False

        def stop_condition(nts: NetworkTraceStep, context):
            return nts.data

        def queue_condition(nts: NetworkTraceStep, *args):
            assert isinstance(nts, NetworkTraceStep)
            return nts.data or not _reached_hv(nts.path.to_equipment)

        def step_action(nts: NetworkTraceStep, context):
            self._process(nts.path, nts.data, context, terminal_to_aux_equipment, lv_feeder_start_points, lv_feeders_to_assign)

        return (Tracing.network_trace(self.network_state_operators, NetworkTraceActionType.ALL_STEPS, compute_data=(
                        lambda _, __, next_path: next_path.to_equipment in lv_feeder_start_points)
                    )
                .add_condition(self.network_state_operators.stop_at_open())
                .add_stop_condition(Traversal.stop_condition(stop_condition))
                .add_queue_condition(Traversal.queue_condition(queue_condition))
                .add_step_action(Traversal.step_action(step_action))
            )


    def _process(self,
                       step_path: NetworkTraceStep.Path,
                       found_lv_feeder: bool,
                       step_context: StepContext,
                       terminal_to_aux_equipment: dict[Terminal, Collection[AuxiliaryEquipment]],
                       lv_feeder_start_points: Set[ConductingEquipment],
                       lv_feeders_to_assign: list[LvFeeder]):
        if step_path.traced_internally and not step_context.is_start_item:
            return

        if found_lv_feeder:
            found_lv_feeders = self._find_lv_feeders(step_path.to_equipment, lv_feeder_start_points)

            self._energized_by(lv_feeders_to_assign, list(map(lambda it: self.network_state_operators.get_energizing_feeders(it), found_lv_feeders)))
            self._energized_by(found_lv_feeders, list(map(lambda it: self.network_state_operators.get_energizing_feeders(it), found_lv_feeders)))

        try:
            aux_equip_for_this_terminal = terminal_to_aux_equipment[step_path.to_terminal]
        except KeyError:
            aux_equip_for_this_terminal = []

        self._associate_equipment_with_containers(lv_feeders_to_assign, aux_equip_for_this_terminal)
        self._associate_equipment_with_containers(lv_feeders_to_assign, [step_path.to_equipment])

        if isinstance(step_path.to_equipment, ProtectedSwitch):
            self._associate_relay_systems_with_containers(lv_feeders_to_assign, step_path.to_equipment)



    def _find_lv_feeders(self, ce: ConductingEquipment, lv_feeder_start_points: list[ConductingEquipment]) -> list[LvFeeder]:
        sites = list(ce.get_filtered_containers(Site, self.network_state_operators))
        if len(sites) == 1:
            return sites[0].find_lv_feeders(lv_feeder_start_points, self.network_state_operators)
        elif len(sites) == 0:
            return list(ce.get_filtered_containers(LvFeeder, self.network_state_operators))
        raise Exception("HURR DURR")  # TODO: remove this when locig is confirmed

    def _lv_feeders_from_terminal(self, terminal: Terminal):
        return terminal.conducting_equipment.get_filtered_containers(LvFeeder)(self.network_state_operators)

    def _energized_by(self, lv_feeders: list[LvFeeder], feeders: list[Feeder]):
        for lv_feeder in lv_feeders:
            map(lambda it: self.network_state_operators.associate_energizing_feeder(it, lv_feeder), feeders)

