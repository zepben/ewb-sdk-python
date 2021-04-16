#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import TableBusbarSections, TableJunctions


def test_table_busbarsection():
    t = TableBusbarSections()
    assert t.name() == "busbar_sections"


def test_table_junctions():
    t = TableJunctions()
    assert t.name() == "junctions"
