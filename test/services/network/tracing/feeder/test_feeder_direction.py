#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import FeederDirection


class TestFeederDirection:

    def test_contains(self):
        assert FeederDirection.NONE in FeederDirection.NONE
        assert FeederDirection.UPSTREAM not in FeederDirection.NONE
        assert FeederDirection.DOWNSTREAM not in FeederDirection.NONE
        assert FeederDirection.BOTH not in FeederDirection.NONE

        assert FeederDirection.NONE not in FeederDirection.UPSTREAM
        assert FeederDirection.UPSTREAM in FeederDirection.UPSTREAM
        assert FeederDirection.DOWNSTREAM not in FeederDirection.UPSTREAM
        assert FeederDirection.BOTH not in FeederDirection.UPSTREAM

        assert FeederDirection.NONE not in FeederDirection.DOWNSTREAM
        assert FeederDirection.UPSTREAM not in FeederDirection.DOWNSTREAM
        assert FeederDirection.DOWNSTREAM in FeederDirection.DOWNSTREAM
        assert FeederDirection.BOTH not in FeederDirection.DOWNSTREAM

        assert FeederDirection.NONE not in FeederDirection.BOTH
        assert FeederDirection.UPSTREAM in FeederDirection.BOTH
        assert FeederDirection.DOWNSTREAM in FeederDirection.BOTH
        assert FeederDirection.BOTH in FeederDirection.BOTH

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

    def test_not(self):
        assert ~FeederDirection.NONE == FeederDirection.BOTH
        assert ~FeederDirection.UPSTREAM == FeederDirection.DOWNSTREAM
        assert ~FeederDirection.DOWNSTREAM == FeederDirection.UPSTREAM
        assert ~FeederDirection.BOTH == FeederDirection.NONE
