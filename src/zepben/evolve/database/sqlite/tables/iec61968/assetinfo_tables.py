#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import TableAssetInfo

__all__ = ["TablePowerTransformerInfo", "TableTransformerEndInfo", "TableTransformerTankInfo", "TableWireInfo", "TableCableInfo", "TableAssetInfo",
           "TableOverheadWireInfo"]


class TablePowerTransformerInfo(TableAssetInfo):

    def name(self) -> str:
        return "power_transformer_info"


class TableTransformerEndInfo(TableAssetInfo):
    connection_kind: Column = None
    emergency_s: Column = None
    end_number: Column = None
    insulation_u: Column = None
    phase_angle_clock: Column = None
    r: Column = None
    rated_s: Column = None
    rated_u: Column = None
    short_term_s: Column = None
    transformer_tank_info_mrid: Column = None

    def __init__(self):
        super(TableTransformerEndInfo, self).__init__()
        self.column_index += 1
        self.connection_kind = Column(self.column_index, "connection_kind", "TEXT", Nullable.NOT_NULL)
        self.column_index += 1
        self.emergency_s = Column(self.column_index, "emergency_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.end_number = Column(self.column_index, "end_number", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.insulation_u = Column(self.column_index, "insulation_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.phase_angle_clock = Column(self.column_index, "phase_angle_clock", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.r = Column(self.column_index, "r", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_s = Column(self.column_index, "rated_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.rated_u = Column(self.column_index, "rated_u", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.short_term_s = Column(self.column_index, "short_term_s", "INTEGER", Nullable.NOT_NULL)
        self.column_index += 1
        self.transformer_tank_info_mrid = Column(self.column_index, "transformer_tank_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "transformer_end_info"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerEndInfo, self).non_unique_index_columns()
        cols.append([self.transformer_tank_info_mrid])
        return cols


class TableTransformerTankInfo(TableAssetInfo):
    power_transformer_info_mrid: Column = None

    def __init__(self):
        super(TableTransformerTankInfo, self).__init__()
        self.column_index += 1
        self.power_transformer_info_mrid = Column(self.column_index, "power_transformer_info_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "transformer_tank_info"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableTransformerTankInfo, self).non_unique_index_columns()
        cols.append([self.power_transformer_info_mrid])
        return cols


class TableWireInfo(TableAssetInfo):
    rated_current: Column = None
    material: Column = None

    def __init__(self):
        super(TableWireInfo, self).__init__()
        self.column_index += 1
        self.rated_current = Column(self.column_index, "rated_current", "NUMBER", Nullable.NOT_NULL)
        self.column_index += 1
        self.material = Column(self.column_index, "material", "TEXT", Nullable.NOT_NULL)


class TableCableInfo(TableWireInfo):

    def name(self) -> str:
        return "cable_info"


class TableOverheadWireInfo(TableWireInfo):

    def name(self) -> str:
        return "overhead_wire_info"


