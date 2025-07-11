#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

from zepben.ewb import Equipment
from zepben.ewb.services.network.tracing.networktrace.operators.in_service_state_operators import InServiceStateOperators


class TestInServiceStateOperators:
    normal = InServiceStateOperators.NORMAL
    current = InServiceStateOperators.CURRENT

    def test_is_in_service(self):
        for operator, attr in ((self.normal, 'normally_in_service'), (self.current, 'in_service')):
            for _bool in (True, False):
                equipment = MagicMock(Equipment)
                setattr(equipment, attr, _bool)

                assert operator.is_in_service(equipment) == _bool

    def test_set_in_service(self):
        for operator, attr in ((self.normal, 'normally_in_service'), (self.current, 'in_service')):
            for _bool in (True, False):
                equipment = MagicMock(Equipment)
                assert getattr(equipment, attr)

                operator.set_in_service(equipment, False)

                assert not getattr(equipment, attr)
