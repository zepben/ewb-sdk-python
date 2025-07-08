#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import Terminal
from zepben.ewb.services.network.tracing.networktrace.operators.phase_state_operators import PhaseStateOperators


class TestPhaseStateOperators:

    normal = PhaseStateOperators.NORMAL
    current = PhaseStateOperators.CURRENT

    def test_phase_status(self):
        for operators, attr in ((self.normal, 'normal_phases'), (self.current, 'current_phases')):
            terminal = Terminal()
            # FIXME: should be comparing the actual PhaseStatus object, but Terminal makes a new one on every call
            assert operators.phase_status(terminal).terminal is getattr(terminal, attr).terminal
