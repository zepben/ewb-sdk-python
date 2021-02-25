#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableConductingEquipment

__all__ = ["TableConnectors", "TableBusbarSections", "TableJunctions"]


# noinspection PyAbstractClass
class TableConnectors(TableConductingEquipment):
    pass


class TableBusbarSections(TableConnectors):
    def name(self) -> str:
        return "busbar_sections"


class TableJunctions(TableConnectors):
    def name(self) -> str:
        return "junctions"
