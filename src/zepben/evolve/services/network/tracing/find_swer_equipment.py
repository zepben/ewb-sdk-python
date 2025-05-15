#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Union, Generator, AsyncGenerator

from typing_extensions import TypeVar

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch

from zepben.evolve import NetworkService

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
            return set(await self.find_on_feeder(to_process, network_state_operators))
        elif isinstance(to_process, NetworkService):
            return set([item async for item in self.find_all(to_process, network_state_operators)])

    async def find_all(self, network_service: NetworkService, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL) -> AsyncGenerator[ConductingEquipment, None]:
        """
        Find the `ConductingEquipment` on any `Feeder` in a `NetworkService` which is SWER. This will include any equipment on the LV network that is energised
        via SWER.

        :param network_service: The `NetworkService` to process.
        :param network_state_operators: The `NetworkStateOperators` to be used when finding SWER equipment

        :return: A `Set` of `ConductingEquipment` on `Feeder` that is SWER, or energised via SWER.
        """
        for feeder in network_service.objects(Feeder):
            for item in await self.find_on_feeder(feeder, network_state_operators):
                yield item

    async def find_on_feeder(self, feeder: Feeder, network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL) -> Set[ConductingEquipment]:
        """
        Find the `ConductingEquipment` on a `Feeder` which is SWER. This will include any equipment on the LV network that is energised via SWER.

        :param feeder: The `Feeder` to process.
        :param network_state_operators: The `NetworkStateOperators` to be used when finding SWER equipment

        :return: A `Set` of `ConductingEquipment` on `feeder` that is SWER, or energised via SWER.
        """
        swer_equipment: Set[ConductingEquipment] = set()

        # We will add all the SWER transformers to the swer_equipment list before starting any traces to prevent tracing though them by accident. In
        # order to do this, we collect the sequence to a list to change the iteration order.
        for equipment in network_state_operators.get_equipment(feeder):
            if isinstance(equipment, PowerTransformer):
                if _has_swer_terminal(equipment) and _has_non_swer_terminal(equipment):
                    swer_equipment.add(equipment)
                    await self._trace_from(network_state_operators, equipment, swer_equipment)
        return swer_equipment

    @staticmethod
    def _create_trace(state_operators: NetworkStateOperators) -> NetworkTrace[T]:
        return Tracing.network_trace(state_operators).add_condition(state_operators.stop_at_open())

    async def _trace_from(self, state_operators: NetworkStateOperators, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):
        # Trace from any SWER terminals.
        await self._trace_swer_from(state_operators, transformer, swer_equipment)

        # Trace from any LV terminals.
        await self._trace_lv_from(state_operators, transformer, swer_equipment)

    async def _trace_swer_from(self, state_operators: NetworkStateOperators, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):

        def condition(next_step, nctx, step, ctx):
            if _is_swer_terminal(next_step.path.to_terminal) or isinstance(next_step.path.to_equipment, Switch):
                return next_step.path.to_equipment not in swer_equipment

        trace = (
            self._create_trace(state_operators)
            .add_queue_condition(condition)
            .add_step_action(lambda step, ctx: swer_equipment.add(step.path.to_equipment))
        )

        for it in (t for t in transformer.terminals if _is_swer_terminal(t)):
            trace.reset()
            await trace.run(it, None)


    async def _trace_lv_from(self, state_operators: NetworkStateOperators,  transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):

        def condition(next_step, nctx, step, ctx):
            if 1 <= next_step.path.to_equipment.base_voltage_value <= 1000:
                return next_step.path.to_equipment not in swer_equipment

        trace = (
            self._create_trace(state_operators)
            .add_queue_condition(condition)
            .add_step_action(lambda step, ctx: swer_equipment.add(step.path.to_equipment))
        )

        for terminal in transformer.terminals:
            if _is_non_swer_terminal(terminal):
                trace.reset()
                await trace.run(terminal, None)

def _is_swer_terminal(terminal: Terminal) -> bool:
    return terminal.phases.num_phases == 1

def _is_non_swer_terminal(terminal: Terminal) -> bool:
    return terminal.phases.num_phases > 1

def _has_swer_terminal(ce: ConductingEquipment) -> bool:
    return any(_is_swer_terminal(it) for it in ce.terminals)

def _has_non_swer_terminal(ce: ConductingEquipment) -> bool:
    return any(_is_non_swer_terminal(it) for it in ce.terminals)
