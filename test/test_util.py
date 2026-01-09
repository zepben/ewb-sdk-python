#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from uuid import UUID

from zepben.ewb.util import none, generate_id


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

def test_generate_id():
    # make sure our generated ID is a valid UUID.
    UUID(generate_id())

    # Make sure each call gives a new UUID.
    assert generate_id() != generate_id()
