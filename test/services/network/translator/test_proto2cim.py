#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from zepben.evolve import NetworkService, BusbarSection

from test.pb_creators import busbarsection


@given(bbs=busbarsection())
def test_busbar_to_cim(bbs):
    cim = bbs.to_cim(NetworkService())
    assert cim.mrid == bbs.mrid()
    assert isinstance(cim, BusbarSection)
