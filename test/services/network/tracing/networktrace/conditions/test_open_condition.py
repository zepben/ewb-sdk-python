#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable
from unittest.mock import MagicMock

from zepben.evolve import Switch, SinglePhaseKind, NetworkTraceStep, ConductingEquipment, StepContext
from zepben.evolve.services.network.tracing.networktrace.conditions.open_condition import OpenCondition



def mock_nts(type: NetworkTraceStep.Type=None, path:NetworkTraceStep.Path=None) -> NetworkTraceStep:
    next_step = MagicMock(spec=NetworkTraceStep)
    if type:
        next_step.type = lambda: type

    if path:
        next_step.path = path

    return next_step

def mock_nts_path(to_equipment: ConductingEquipment=None) -> NetworkTraceStep.Path:
    next_path = MagicMock(spec=NetworkTraceStep.Path)
    if to_equipment:
        next_path.to_equipment = to_equipment

    return next_path

def should_queue_params(next_step, next_context=None, current_step=None, current_context=None
                        ) -> (NetworkTraceStep, StepContext, NetworkTraceStep, StepContext):
    return next_step, next_context or MagicMock(), current_step or MagicMock(), current_context or MagicMock()

class TestOpenCondition:
    def test_always_queues_external_steps(self):
        is_open = Callable[[Switch, SinglePhaseKind], bool]
        spk = MagicMock(spec=SinglePhaseKind)
        next_step = mock_nts(type=NetworkTraceStep.Type.EXTERNAL)

        assert OpenCondition(is_open, spk).should_queue(*should_queue_params(next_step))

    def test_always_queues_non_switch_equipment(self):
        is_open = Callable[[Switch, SinglePhaseKind], bool]
        spk = MagicMock(spec=SinglePhaseKind)

        next_path = mock_nts_path(to_equipment=MagicMock(spec=ConductingEquipment))
        next_step = mock_nts(
            type=NetworkTraceStep.Type.INTERNAL,
            path=next_path)

        assert OpenCondition(MagicMock(spec=is_open), spk).should_queue(*should_queue_params(next_step))

    def test_queues_closed_switch_equipment(self):
        switch = MagicMock(spec=Switch)
        spk = MagicMock(spec=SinglePhaseKind)

        is_open = lambda switch, _spk: False

        next_path = mock_nts_path(to_equipment=switch)
        next_step = mock_nts(
            type=NetworkTraceStep.Type.INTERNAL,
            path=next_path
        )

        assert OpenCondition(is_open, spk).should_queue(*should_queue_params(next_step))

    def test_does_not_queue_open_switch_equipment(self):
        switch = MagicMock(spec=Switch)
        spk = MagicMock(spec=SinglePhaseKind)

        is_open = lambda switch, _spk: True

        next_path = mock_nts_path(to_equipment=switch)
        next_step = mock_nts(
            type=NetworkTraceStep.Type.INTERNAL,
            path=next_path
        )

        assert not OpenCondition(is_open, spk).should_queue(*should_queue_params(next_step))

