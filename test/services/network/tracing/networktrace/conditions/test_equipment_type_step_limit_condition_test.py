#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

from zepben.evolve import StepContext, Switch, NetworkTraceStep, Breaker, Junction
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_type_step_limit_condition import EquipmentTypeStepLimitCondition


def mock_ctx(value: int):
    ctx = MagicMock(spec=StepContext)
    ctx.get_value = lambda key: value
    return ctx

class TestEquipmentStepLimitCondition:
    def test_should_stop_when_matched_count_is_equal_to_limit(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)
        context = mock_ctx(2)
        assert condition.should_stop(MagicMock(), context)

    def test_should_stop_when_matched_type_count_is_greater_than_limit(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)
        context = mock_ctx(3)
        assert condition.should_stop(MagicMock(), context)

    def test_should_not_stop_when_matched_type_count_is_less_than_limit(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)
        context = mock_ctx(1)
        assert not condition.should_stop(MagicMock(), context)

    def test_always_returns_0_for_initial_value(self):
        step = MagicMock(spec=NetworkTraceStep)
        result = EquipmentTypeStepLimitCondition(2, Switch).compute_initial_value(step)
        assert result == 0

    def test_computes_correct_next_value_on_internal_step(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)

        current_step = MagicMock(spec=NetworkTraceStep)
        path = MagicMock(spec=NetworkTraceStep.Path)
        path.traced_internally = True
        step = MagicMock(spec=NetworkTraceStep)
        step.path = path

        result = condition.compute_next_value(step, current_step, 1)
        assert result == 1

    def test_computes_correct_next_value_on_matching_external_step(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)

        current_step = MagicMock(spec=NetworkTraceStep)
        path = MagicMock(spec=NetworkTraceStep.Path)
        path.traced_internally = False
        path.to_equipment = MagicMock(spec=Breaker)
        step = MagicMock(spec=NetworkTraceStep)
        step.path = path

        result = condition.compute_next_value(step, current_step, 1)
        assert result == 2

    def test_computes_correct_next_value_on_non_matching_external_step(self):
        condition = EquipmentTypeStepLimitCondition(2, Switch)

        current_step = MagicMock(spec=NetworkTraceStep)
        path = MagicMock(spec=NetworkTraceStep.Path)
        path.traced_internally = False
        path.to_equipment = MagicMock(spec=Junction)
        step = MagicMock(spec=NetworkTraceStep)
        step.path = path

        result = condition.compute_next_value(step, current_step, 1)
        assert result == 1

