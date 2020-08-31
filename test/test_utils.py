"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


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



