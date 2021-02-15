#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import BusbarSection



def test_constructor():
    bbs = BusbarSection()
    assert bbs.mrid
    bbs = BusbarSection(mrid="test")
    assert bbs.mrid == "test"
    bbs = BusbarSection("test2")
    assert bbs.mrid == "test2"


