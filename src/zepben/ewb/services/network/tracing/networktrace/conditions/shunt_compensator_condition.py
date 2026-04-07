#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import Generic, cast, TypeVar

from zepben.ewb.model.cim.iec61970.base.wires.shunt_compensator import ShuntCompensator
from zepben.ewb.services.network.tracing.networktrace.conditions.network_trace_queue_condition import NetworkTraceQueueCondition
from zepben.ewb.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.ewb.services.network.tracing.traversal.step_context import StepContext

T = TypeVar('T')


class _ShuntCompensatorCondition(ABC):
    class _StopOnGround(NetworkTraceQueueCondition[T], Generic[T]):
        """
        A `NetworkTraceQueueCondition` that prevents the network trace from queueing between the normal and grounding terminals
        of a `ShuntCompensator`.
        """

        def __init__(self):
            super().__init__(NetworkTraceStep.Type.INTERNAL)

        # noinspection PyUnusedLocal
        def should_queue_matched_step(
            self,
            next_item: NetworkTraceStep[T],
            next_context: StepContext,
            current_item: NetworkTraceStep[T],
            current_context: StepContext
        ) -> bool:
            # Queue everything that isn't an internal traversal across a `ShuntCompensator` involving its `grounding_terminal`.
            if not isinstance(next_item.path.to_equipment, ShuntCompensator):
                return True
            sc = cast(ShuntCompensator, next_item.path.to_equipment)

            return next_item.path.traced_externally or (
                    (next_item.path.to_terminal != sc.grounding_terminal) and (next_item.path.from_terminal != sc.grounding_terminal))
