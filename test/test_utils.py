#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.tracing.util import normally_open, currently_open


class TestUtils(object):
    def test_normally_open(self, conducting_equipment, switch):
        # Test with core = None
        normally_open(conducting_equipment)

        # Test with cond equip, legit core

        # test with cond equip, incorrect core

        # Test with switch, core = None
        normally_open(switch)

        # Test with switch, legit core

        # test with switch, incorrect core

        # Test non-equipment raises error



