#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

from zepben.ewb import NetworkTraceStep
from zepben.ewb.services.network.tracing.networktrace.conditions.equipment_step_limit_condition import EquipmentStepLimitCondition


def mock_nts(num_terminal_steps=0, num_equipment_steps=0):
    return NetworkTraceStep(MagicMock(spec=NetworkTraceStep.Path), num_terminal_steps, num_equipment_steps, None)

class TestEquipmentStepLimitCondition:

    def test_should_stop_when_step_number_is_equal_to_limit(self):
        assert EquipmentStepLimitCondition(2).should_stop(mock_nts(0, 2), MagicMock())

    def test_should_stop_when_step_number_is_greater_than_limit(self):
        assert EquipmentStepLimitCondition(2).should_stop(mock_nts(0, 3), MagicMock())

    def test_should_not_stop_when_step_number_is_less_than_limit(self):
        assert not EquipmentStepLimitCondition(2).should_stop(mock_nts(3, 1), MagicMock())
