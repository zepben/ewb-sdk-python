#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

from zepben.ewb import Switch, SinglePhaseKind
from zepben.ewb.services.network.tracing.networktrace.operators.open_state_operators import OpenStateOperators


class FlipFlopper:
    def __init__(self, state):
        self.state = state

    def __call__(self, *args, **kwargs):
        _state = self.state
        self.state = not _state
        return _state

class TestOpenStateOperators:

    normal = OpenStateOperators.NORMAL
    current = OpenStateOperators.CURRENT

    def test_is_open_check_swith_open_state(self):
        for operators, attr in ((self.normal, 'is_normally_open'), (self.current, 'is_open')):
            switch = MagicMock(Switch)
            flopper = FlipFlopper(False)
            setattr(switch, attr, lambda spk: flopper())

            assert not operators.is_open(switch, SinglePhaseKind.A)
            assert operators.is_open(switch, SinglePhaseKind.A)

    def test_set_open(self):
        for operators, attr in ((self.normal, 'is_normally_open'), (self.current, 'is_open')):
            switch = MagicMock(Switch)
            operators.set_open(switch, True, SinglePhaseKind.A)
            assert getattr(switch, attr)
