#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import FeederDirection


class TestFeederDirection:

    def test_has(self):
        assert FeederDirection.NONE.has(FeederDirection.NONE)
        assert not FeederDirection.NONE.has(FeederDirection.UPSTREAM)
        assert not FeederDirection.NONE.has(FeederDirection.DOWNSTREAM)
        assert not FeederDirection.NONE.has(FeederDirection.BOTH)

        assert not FeederDirection.UPSTREAM.has(FeederDirection.NONE)
        assert FeederDirection.UPSTREAM.has(FeederDirection.UPSTREAM)
        assert not FeederDirection.UPSTREAM.has(FeederDirection.DOWNSTREAM)
        assert not FeederDirection.UPSTREAM.has(FeederDirection.BOTH)

        assert not FeederDirection.DOWNSTREAM.has(FeederDirection.NONE)
        assert not FeederDirection.DOWNSTREAM.has(FeederDirection.UPSTREAM)
        assert FeederDirection.DOWNSTREAM.has(FeederDirection.DOWNSTREAM)
        assert not FeederDirection.DOWNSTREAM.has(FeederDirection.BOTH)

        assert not FeederDirection.BOTH.has(FeederDirection.NONE)
        assert FeederDirection.BOTH.has(FeederDirection.UPSTREAM)
        assert FeederDirection.BOTH.has(FeederDirection.DOWNSTREAM)
        assert FeederDirection.BOTH.has(FeederDirection.BOTH)

    def test_plus(self):
        assert FeederDirection.NONE + FeederDirection.NONE == FeederDirection.NONE
        assert FeederDirection.NONE + FeederDirection.UPSTREAM == FeederDirection.UPSTREAM
        assert FeederDirection.NONE + FeederDirection.DOWNSTREAM == FeederDirection.DOWNSTREAM
        assert FeederDirection.NONE + FeederDirection.BOTH == FeederDirection.BOTH

        assert FeederDirection.UPSTREAM + FeederDirection.NONE == FeederDirection.UPSTREAM
        assert FeederDirection.UPSTREAM + FeederDirection.UPSTREAM == FeederDirection.UPSTREAM
        assert FeederDirection.UPSTREAM + FeederDirection.DOWNSTREAM == FeederDirection.BOTH
        assert FeederDirection.UPSTREAM + FeederDirection.BOTH == FeederDirection.BOTH

        assert FeederDirection.DOWNSTREAM + FeederDirection.NONE == FeederDirection.DOWNSTREAM
        assert FeederDirection.DOWNSTREAM + FeederDirection.UPSTREAM == FeederDirection.BOTH
        assert FeederDirection.DOWNSTREAM + FeederDirection.DOWNSTREAM == FeederDirection.DOWNSTREAM
        assert FeederDirection.DOWNSTREAM + FeederDirection.BOTH == FeederDirection.BOTH

        assert FeederDirection.BOTH + FeederDirection.NONE == FeederDirection.BOTH
        assert FeederDirection.BOTH + FeederDirection.UPSTREAM == FeederDirection.BOTH
        assert FeederDirection.BOTH + FeederDirection.DOWNSTREAM == FeederDirection.BOTH
        assert FeederDirection.BOTH + FeederDirection.BOTH == FeederDirection.BOTH

    def test_minus(self):
        assert FeederDirection.NONE - FeederDirection.NONE == FeederDirection.NONE
        assert FeederDirection.NONE - FeederDirection.UPSTREAM == FeederDirection.NONE
        assert FeederDirection.NONE - FeederDirection.DOWNSTREAM == FeederDirection.NONE
        assert FeederDirection.NONE - FeederDirection.BOTH == FeederDirection.NONE

        assert FeederDirection.UPSTREAM - FeederDirection.NONE == FeederDirection.UPSTREAM
        assert FeederDirection.UPSTREAM - FeederDirection.UPSTREAM == FeederDirection.NONE
        assert FeederDirection.UPSTREAM - FeederDirection.DOWNSTREAM == FeederDirection.UPSTREAM
        assert FeederDirection.UPSTREAM - FeederDirection.BOTH == FeederDirection.NONE

        assert FeederDirection.DOWNSTREAM - FeederDirection.NONE == FeederDirection.DOWNSTREAM
        assert FeederDirection.DOWNSTREAM - FeederDirection.UPSTREAM == FeederDirection.DOWNSTREAM
        assert FeederDirection.DOWNSTREAM - FeederDirection.DOWNSTREAM == FeederDirection.NONE
        assert FeederDirection.DOWNSTREAM - FeederDirection.BOTH == FeederDirection.NONE

        assert FeederDirection.BOTH - FeederDirection.NONE == FeederDirection.BOTH
        assert FeederDirection.BOTH - FeederDirection.UPSTREAM == FeederDirection.DOWNSTREAM
        assert FeederDirection.BOTH - FeederDirection.DOWNSTREAM == FeederDirection.UPSTREAM
        assert FeederDirection.BOTH - FeederDirection.BOTH == FeederDirection.NONE
