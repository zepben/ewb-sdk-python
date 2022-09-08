#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https:#mozilla.org/MPL/2.0/.
from typing import Callable, Set, Union, Optional

from zepben.evolve import ConnectedEquipmentTraversal, ConductingEquipmentStep, NetworkService, ConductingEquipment, Feeder, PowerTransformer, Switch, \
    new_normal_connected_equipment_trace

__all__ = ["FindSwerEquipment"]


class FindSwerEquipment:
    """
    A class which can be used for finding the SWER equipment in a [NetworkService] or [Feeder].
    """

    create_trace: Callable[[], ConnectedEquipmentTraversal]

    def __init__(self, create_trace: Optional[Callable[[], ConnectedEquipmentTraversal]] = None) -> None:
        super().__init__()
        self.create_trace = create_trace or new_normal_connected_equipment_trace

    async def find_all(self, network_service: NetworkService) -> Set[ConductingEquipment]:
        """
        Find the `ConductingEquipment` on any `Feeder` in a `NetworkService` which is SWER. This will include any equipment on the LV network that is energised
        via SWER.

        :param network_service: The `NetworkService` to process.

        :return: A `Set` of `ConductingEquipment` on any `Feeder` in `network_service` that is SWER, or energised via SWER.
        """
        return {it for feeder in network_service.objects(Feeder) for it in await self.find_on_feeder(feeder)}

    async def find_on_feeder(self, feeder: Feeder) -> Set[ConductingEquipment]:
        """
        Find the `ConductingEquipment` on a `Feeder` which is SWER. This will include any equipment on the LV network that is energised via SWER.

        :param feeder: The `Feeder` to process.

        :return: A `Set` of `ConductingEquipment` on `feeder` that is SWER, or energised via SWER.
        """
        to_process = [it for it in feeder.equipment if isinstance(it, PowerTransformer) and self._has_swer_terminal(it) and self._has_non_swer_terminal(it)]

        # We will add all the SWER transformers to the swer_equipment list before starting any traces to prevent tracing though them by accident. In
        # order to do this, we collect the sequence to a list to change the iteration order.
        swer_equipment = set(to_process)

        for it in to_process:
            await self._trace_from(it, swer_equipment)

        return swer_equipment

    async def _trace_from(self, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):
        # Trace from any SWER terminals.
        await self._trace_swer_from(transformer, swer_equipment)

        # Trace from any LV terminals.
        await self._trace_lv_from(transformer, swer_equipment)

    async def _trace_swer_from(self, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):
        async def is_in_swer_equipment(step: ConductingEquipmentStep) -> bool:
            return step.conducting_equipment in swer_equipment

        async def has_no_swer_terminals(step: ConductingEquipmentStep) -> bool:
            return not self._has_swer_terminal(step)

        async def add_swer_equipment(step: ConductingEquipmentStep, is_stopping: bool):
            # To make sure we include any open points on a SWER network (unlikely) we include stop equipment if it is a `Switch`.
            if not is_stopping or isinstance(step.conducting_equipment, Switch):
                swer_equipment.add(step.conducting_equipment)

        trace = self.create_trace()
        trace.add_stop_condition(is_in_swer_equipment)
        trace.add_stop_condition(has_no_swer_terminals)
        trace.add_step_action(add_swer_equipment)

        # We start from the connected equipment to prevent tracing in the wrong direction, as we are using the connected equipment trace.
        to_process = [ct.conducting_equipment for t in transformer.terminals for ct in t.connected_terminals() if
                      t.phases.num_phases == 1 and ct.conducting_equipment]

        for it in to_process:
            trace.reset()
            await trace.run_from(it)

    async def _trace_lv_from(self, transformer: PowerTransformer, swer_equipment: Set[ConductingEquipment]):
        async def is_in_swer_equipment(step: ConductingEquipmentStep) -> bool:
            return step.conducting_equipment in swer_equipment

        async def add_swer_equipment(step: ConductingEquipmentStep, _: bool):
            swer_equipment.add(step.conducting_equipment)

        trace = self.create_trace()
        trace.add_stop_condition(is_in_swer_equipment)
        trace.add_step_action(add_swer_equipment)

        # We start from the connected equipment to prevent tracing in the wrong direction, as we are using the connected equipment trace.
        to_process = [ct.conducting_equipment for t in transformer.terminals for ct in t.connected_terminals() if
                      t.phases.num_phases > 1 and ct.conducting_equipment and 1 <= ct.conducting_equipment.base_voltage_value <= 1000]

        for it in to_process:
            trace.reset()
            await trace.run_from(it)

    @staticmethod
    def _has_swer_terminal(item: Union[ConductingEquipmentStep, ConductingEquipment]) -> bool:
        if isinstance(item, ConductingEquipmentStep):
            item = item.conducting_equipment

        return any(t.phases.num_phases == 1 for t in item.terminals)

    @staticmethod
    def _has_non_swer_terminal(ce: ConductingEquipment) -> bool:
        return any(t.phases.num_phases > 1 for t in ce.terminals)
