#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Callable

from zepben.evolve import NetworkStateOperators, FeederDirection, SinglePhaseKind, Switch, PowerTransformer
from zepben.evolve.services.network.tracing.networktrace.conditions.conditions import limit_equipment_steps
from zepben.evolve.services.network.tracing.networktrace.conditions.direction_condition import DirectionCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_step_limit_condition import EquipmentStepLimitCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.equipment_type_step_limit_condition import EquipmentTypeStepLimitCondition
from zepben.evolve.services.network.tracing.networktrace.conditions.open_condition import OpenCondition


class TestCondition:
    def test_state_operators_with_direction(self):
        state_operators = NetworkStateOperators.NORMAL
        condition = state_operators.with_direction(FeederDirection.BOTH)
        assert isinstance(condition, DirectionCondition)
        assert condition.state_operators is state_operators
        assert condition.direction is FeederDirection.BOTH

    def test_state_operators_upstream(self):
        state_operators = NetworkStateOperators.NORMAL
        condition = state_operators.upstream()
        assert isinstance(condition, DirectionCondition)
        assert condition.state_operators is state_operators
        assert condition.direction is FeederDirection.UPSTREAM

    def test_state_operators_downstream(self):
        state_operators = NetworkStateOperators.NORMAL
        condition = state_operators.downstream()
        assert isinstance(condition, DirectionCondition)
        assert condition.state_operators is state_operators
        assert condition.direction is FeederDirection.DOWNSTREAM

    def test_stop_at_open(self):
        is_open: Callable[[Switch, Optional[SinglePhaseKind]], bool] = Switch.is_open
        state_operators = NetworkStateOperators.NORMAL
        condition = state_operators.stop_at_open(is_open, SinglePhaseKind.A)
        assert isinstance(condition, OpenCondition)
        assert condition._phase is SinglePhaseKind.A

    def test_open_operators_stop_at_open(self):
        state_operators = NetworkStateOperators.NORMAL
        condition = state_operators.stop_at_open(phase=SinglePhaseKind.A)
        assert isinstance(condition, OpenCondition)
        assert condition._is_open == state_operators.is_open
        assert condition._phase is SinglePhaseKind.A

    def test_limit_equipment_steps(self):
        condition = limit_equipment_steps(1)
        assert isinstance(condition, EquipmentStepLimitCondition)
        assert condition.limit == 1

    def test_limit_equipment_type_steps(self):
        condition = limit_equipment_steps(1, PowerTransformer)
        assert isinstance(condition, EquipmentTypeStepLimitCondition)
        assert condition.limit == 1
        assert condition.equipment_type is PowerTransformer
