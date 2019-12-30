"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


import pytest
from zepben.model.tracing import SetPhases
from zepben.model import Direction
from zepben.cim.iec61970 import SinglePhaseKind
from test.util import get_terminal, check_expected_current_phases, check_expected_normal_phases

A = SinglePhaseKind.A
B = SinglePhaseKind.B
C = SinglePhaseKind.C
N = SinglePhaseKind.N

OUT = Direction.OUT
IN = Direction.IN
BOTH = Direction.BOTH
NONE = Direction.NONE

class TestSetPhase(object):
    @pytest.mark.asyncio
    async def test_set_phase(self, network1):
        assert network1 is not None
        set_phases = SetPhases()
        await set_phases.run(network1)
        assert len(network1.energy_sources) == 1
        assert len(network1.energy_consumers) == 1

        check_expected_current_phases(get_terminal(network1, "default-acls-1", 0), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_expected_current_phases(get_terminal(network1, "default-acls-1", 1), [A, B, C, N], [IN, IN, IN, IN])
        check_expected_current_phases(get_terminal(network1, "acls-1", 1), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_expected_current_phases(get_terminal(network1, "acls-1", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_expected_current_phases(get_terminal(network1, "default-es", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_expected_current_phases(get_terminal(network1, "default-cb", 0), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_expected_current_phases(get_terminal(network1, "trafo-1", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_expected_current_phases(get_terminal(network1, "trafo-1", 1), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_expected_current_phases(get_terminal(network1, "ec-1", 0), [A, B, C, N], [IN, IN, IN, IN])


