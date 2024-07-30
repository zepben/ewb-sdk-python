#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pytest import raises

from zepben.evolve import Tracker


def test_methods_are_abstract():
    tracker = Tracker()

    with raises(NotImplementedError):
        tracker.has_visited(0)

    with raises(NotImplementedError):
        tracker.visit(0)

    with raises(NotImplementedError):
        tracker.clear()

    with raises(NotImplementedError):
        tracker.copy()
