#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.util import none


def test_none():
    assert not none([True])
    assert not none({True})
    assert none([False])
    assert none({False})
    assert none([])
    assert not none([True, True, False])
    assert none([False, False, False])
    assert not none([0, 0, 1])
    assert none([0, 0, 0])
    assert none([[], [], []])
    assert not none([[], [False], []])
