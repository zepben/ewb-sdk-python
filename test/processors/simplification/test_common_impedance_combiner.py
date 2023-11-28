#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import PerLengthSequenceImpedance, TestNetworkBuilder, AcLineSegment
from zepben.evolve.processors.simplification.common_impedance_combiner import CommonImpedanceCombiner


@pytest.mark.timeout(324234)
@pytest.mark.asyncio
async def test_combine_common_impedance_lines():
    plsi = PerLengthSequenceImpedance()
    plsi.r = 0.001
    plsi.x = 0.0012

    test_network = (await TestNetworkBuilder()
                    .from_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .to_acls(action=lambda c: setattr(c, "per_length_sequence_impedance", plsi))
                    .build())
    test_network.add(plsi)

    what_it_did = await CommonImpedanceCombiner().process(test_network)

    test = list(test_network.objects(AcLineSegment))
