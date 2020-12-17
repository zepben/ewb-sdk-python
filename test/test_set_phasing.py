#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from zepben.evolve import SetPhases, phase_log, PhaseDirection, SinglePhaseKind
from test.util import get_terminal, check_phases

A = SinglePhaseKind.A
B = SinglePhaseKind.B
C = SinglePhaseKind.C
N = SinglePhaseKind.N
SPK_NONE = SinglePhaseKind.NONE

OUT = PhaseDirection.OUT
IN = PhaseDirection.IN
BOTH = PhaseDirection.BOTH
NONE = PhaseDirection.NONE


class TestSetPhase(object):
    @pytest.mark.asyncio
    @pytest.mark.skip
    async def test_set_phase(self, network1):
        assert network1 is not None
        set_phases = SetPhases()
        await set_phases.run(network1)
        assert len(network1.energy_sources) == 1
        assert len(network1.energy_consumers) == 1

        check_phases(get_terminal(network1, "default-acls-1", 0), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network1, "default-acls-1", 1), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network1, "acls-1", 1), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network1, "acls-1", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network1, "default-es", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network1, "default-cb", 0), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network1, "default-cb", 1), [SPK_NONE, SPK_NONE, SPK_NONE, SPK_NONE], [NONE, NONE, NONE, NONE])
        check_phases(get_terminal(network1, "trafo-1", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network1, "trafo-1", 1), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network1, "ec-1", 0), [A, B, C, N], [IN, IN, IN, IN])

    @pytest.mark.asyncio
    @pytest.mark.skip
    async def test_set_phase_multi_branch(self, network2):
        assert network2 is not None
        set_phases = SetPhases()
        await set_phases.run(network2)
        breakers = []
        for br in network2.breakers.values():
            try:
                if br.is_substation_breaker():
                    breakers.append(br)
            except:
                pass

        await phase_log(breakers)
        check_phases(get_terminal(network2, "acls0", 0), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network2, "acls0", 1), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network2, "es", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network2, "acls1", 0), [A, B, C, N], [IN, IN, IN, IN])
        check_phases(get_terminal(network2, "acls1", 1), [A, B, C, N], [OUT, OUT, OUT, OUT])
        check_phases(get_terminal(network2, "acls4", 0), [A, B], [IN, IN])
        check_phases(get_terminal(network2, "acls4", 1), [A, B], [OUT, OUT])
        check_phases(get_terminal(network2, "acls7", 1), [A, B], [OUT, OUT])
        check_phases(get_terminal(network2, "acls8", 0), [B, C], [OUT, OUT])
        check_phases(get_terminal(network2, "acls9", 0), [B, C], [OUT, OUT])
        check_phases(get_terminal(network2, "acls9", 1), [B, C], [IN, IN])
        check_phases(get_terminal(network2, "br0", 0), [A, B], [IN, IN])
        check_phases(get_terminal(network2, "br0", 1), [B, C], [IN, IN])
        check_phases(get_terminal(network2, "junc7", 0), [B], [IN])


