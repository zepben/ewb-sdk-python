#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Set, Union, Optional

from typing_extensions import TypeVar

from zepben.evolve import NetworkService, ConductingEquipment, Feeder, PowerTransformer, Switch, Terminal, Traversal

__all__ = ["FindSwerEquipment"]

from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

T = TypeVar

from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace

from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing


class FindSwerEquipment:
    """
    A class which can be used for finding the SWER equipment in a [NetworkService] or [Feeder].
    """

    async def find(self, to_process: Union[NetworkService, Feeder], network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL) -> Set[ConductingEquipment]:
        """
        Convenience method to call out to `find_all` or `find_on_feeder` based on the class type of `to_process`

        :param to_process: the object to process
        :param network_state_operators: The `NetworkStateOperators` to be used when finding SWER equipment

        :return: A `Set` of `ConductingEquipment` on `Feeder` that is SWER, or energised via SWER.
        """
        if isinstance(to_process, Feeder):
            return await self.find_on_feeder(to_process, network_state_operators)
        elif isinstance(to_process, NetworkService):
            return await self.find_all(to_process, network_state_operators)

    async def find_all(self, network_service: NetworkService, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL) -> Set[ConductingEquipment]:
        """
        Find the `ConductingEquipment` on any `Feeder` in a `NetworkService` which is SWER. This will include any equipment on the LV network that is energised
        via SWER.

        :param network_service: The `NetworkService` to process.
        :param network_state_operators: The `NetworkStateOperators` to be used when finding SWER equipment

        :return: A `Set` of `ConductingEquipment` on `Feeder` that is SWER, or energised via SWER.
        """
        return {it for feeder in network_service.objects(Feeder) for it in await self.find_on_feeder(feeder, network_state_operators)}

    async def find_on_feeder(self, feeder: Feeder, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL) -> Set[ConductingEquipment]:
        """
        Find the `ConductingEquipment` on a `Feeder` which is SWER. This will include any equipment on the LV network that is energised via SWER.

        :param feeder: The `Feeder` to process.

        :return: A `Set` of `ConductingEquipment` on `feeder` that is SWER, or energised via SWER.
        """
        to_process = [it for it in network_state_operators.get_equipment(feeder)
                      if isinstance(it, PowerTransformer) and it.has_swer_terminal and it.has_non_swer_terminal]

        # We will add all the SWER transformers to the swer_equipment list before starting any traces to prevent tracing though them by accident. In
        # order to do this, we collect the sequence to a list to change the iteration order.
        swer_equipment = set(to_process)

        for it in to_process:
            await self._trace_from(network_state_operators, it, swer_equipment)

        return swer_equipment

    def _create_trace(self, state_operators: NetworkStateOperators) -> NetworkTrace[T]:
        return Tracing.network_trace(state_operators).add_condition(state_operators.stop_at_open())

    async def _trace_from(self, state_operators: NetworkStateOperators, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):
        # Trace from any SWER terminals.
        await self._trace_swer_from(state_operators, transformer, swer_equipment)

        # Trace from any LV terminals.
        await self._trace_lv_from(state_operators, transformer, swer_equipment)

    async def _trace_swer_from(self, state_operators: NetworkStateOperators, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):

        def condition(step, *args):
            if step.path.to_terminal.is_swer_terminal or isinstance(step.path.to_equipment, Switch):
                return step.path.to_equipment not in swer_equipment

        def step_action(step: NetworkTraceStep, context):
            swer_equipment.add(step.path.to_equipment)

        trace = self._create_trace(state_operators)
        trace.add_queue_condition(Traversal.queue_condition(condition))

        trace.add_step_action(Traversal.step_action(step_action))


        for it in [t for t in transformer.terminals if t.is_swer_terminal()]:
            trace.reset()
            trace.run(it, None)


    async def _trace_lv_from(self, state_operators: NetworkStateOperators,  transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):

        def condition(step, *args):
            if 1 < step.path.to_equipment.base_voltage_value < 1000:
                return step.path.to_equipment not in swer_equipment

        def step_action(step: NetworkTraceStep, context):
            swer_equipment.add(step.path.to_equipment)

        trace = self._create_trace(state_operators)
        trace.add_stop_condition(Traversal.stop_condition(condition))
        trace.add_step_action(Traversal.step_action(step_action))

        for it in [t for t in transformer.terminals for ct in t.connected_terminals() if t.not_swer_terminal()]:
            trace.reset()
            trace.run(it, None)

    """
    @staticmethod
    def _is_swer_terminal(terminal: Terminal) -> bool:
        return terminal.phases.num_phases == 1

    @staticmethod
    def _is_non_swer_terminal(terminal: Terminal) -> bool:
        return terminal.phases.num_phases > 1

    def _has_swer_terminal(self, ce: ConductingEquipment) -> bool:
        return any(self._is_swer_terminal(it) for it in ce.terminals)

    def _has_non_swer_terminal(self, ce: ConductingEquipment) -> bool:
        return any(self._is_non_swer_terminal(it) for it in ce.terminals)
    """

Terminal.is_swer_terminal = lambda self: self.phases.num_phases == 1
Terminal.not_swer_terminal = lambda self: self.phases.num_phases > 1
ConductingEquipment.has_swer_terminal = lambda self: any(t.is_swer_terminal() for t in self.terminals)
ConductingEquipment.has_non_swer_terminal = lambda self: any(t.not_swer_terminal() for t in self.terminals)
