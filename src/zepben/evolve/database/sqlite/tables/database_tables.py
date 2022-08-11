#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Cursor
from typing import Dict, TypeVar, Type, Any

from dataclassy import dataclass

from zepben.evolve.database.sqlite.tables.associations.assetorganisationroles_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.circuit_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.customeragreements_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.equipment_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.loop_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.pricingstructure_association_tables import *
from zepben.evolve.database.sqlite.tables.associations.usagepoints_association_tables import *
from zepben.evolve.database.sqlite.tables.exceptions import MissingTableConfigException, SqlException
from zepben.evolve.database.sqlite.tables.iec61968.asset_tables import *
from zepben.evolve.database.sqlite.tables.iec61968.assetinfo_tables import *
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import *
from zepben.evolve.database.sqlite.tables.iec61968.customer_tables import *
from zepben.evolve.database.sqlite.tables.iec61968.metering_tables import *
from zepben.evolve.database.sqlite.tables.iec61968.operations_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.auxiliaryequipment_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.diagramlayout_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.equivalent_tables import TableEquivalentBranches
from zepben.evolve.database.sqlite.tables.iec61970.base.infiec61970.feeder_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.meas_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.scada_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.conductor_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.connector_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.energyconnection_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.generation.production_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.perlength_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.switch_tables import *
from zepben.evolve.database.sqlite.tables.iec61970.base.wires.transformer_tables import *
from zepben.evolve.database.sqlite.tables.metadata_tables import *
from zepben.evolve.database.sqlite.tables.sqlite_table import *

__all__ = ["DatabaseTables", "PreparedStatement"]


T = TypeVar("T", bound=SqliteTable)


def _create_tables() -> Dict[Type[T], T]:
    return {
        TableAcLineSegments: TableAcLineSegments(),
        TableAccumulators: TableAccumulators(),
        TableAnalogs: TableAnalogs(),
        TableAssetOrganisationRolesAssets: TableAssetOrganisationRolesAssets(),
        TableAssetOwners: TableAssetOwners(),
        TableBaseVoltages: TableBaseVoltages(),
        TableBatteryUnit: TableBatteryUnit(),
        TableBreakers: TableBreakers(),
        TableBusbarSections: TableBusbarSections(),
        TableCableInfo: TableCableInfo(),
        TableCircuits: TableCircuits(),
        TableCircuitsSubstations: TableCircuitsSubstations(),
        TableCircuitsTerminals: TableCircuitsTerminals(),
        TableConnectivityNodes: TableConnectivityNodes(),
        TableControls: TableControls(),
        TableCustomerAgreements: TableCustomerAgreements(),
        TableCustomerAgreementsPricingStructures: TableCustomerAgreementsPricingStructures(),
        TableCustomers: TableCustomers(),
        TableDiagramObjectPoints: TableDiagramObjectPoints(),
        TableDiagramObjects: TableDiagramObjects(),
        TableDiagrams: TableDiagrams(),
        TableDisconnectors: TableDisconnectors(),
        TableDiscretes: TableDiscretes(),
        TableEnergyConsumerPhases: TableEnergyConsumerPhases(),
        TableEnergyConsumers: TableEnergyConsumers(),
        TableEnergySourcePhases: TableEnergySourcePhases(),
        TableEnergySources: TableEnergySources(),
        TableEquipmentEquipmentContainers: TableEquipmentEquipmentContainers(),
        TableEquipmentOperationalRestrictions: TableEquipmentOperationalRestrictions(),
        TableEquipmentUsagePoints: TableEquipmentUsagePoints(),
        TableEquivalentBranches: TableEquivalentBranches(),
        TableFaultIndicators: TableFaultIndicators(),
        TableFeeders: TableFeeders(),
        TableFuses: TableFuses(),
        TableGeographicalRegions: TableGeographicalRegions(),
        TableJumpers: TableJumpers(),
        TableJunctions: TableJunctions(),
        TableLinearShuntCompensators: TableLinearShuntCompensators(),
        TableLoadBreakSwitches: TableLoadBreakSwitches(),
        TableLocationStreetAddresses: TableLocationStreetAddresses(),
        TableLocations: TableLocations(),
        TableLoops: TableLoops(),
        TableLoopsSubstations: TableLoopsSubstations(),
        TableLvFeeders: TableLvFeeders(),
        TableMetadataDataSources: TableMetadataDataSources(),
        TableMeters: TableMeters(),
        TableNameTypes: TableNameTypes(),
        TableNames: TableNames(),
        TableNoLoadTests: TableNoLoadTests(),
        TableOpenCircuitTests: TableOpenCircuitTests(),
        TableOperationalRestrictions: TableOperationalRestrictions(),
        TableOrganisations: TableOrganisations(),
        TableOverheadWireInfo: TableOverheadWireInfo(),
        TablePerLengthSequenceImpedances: TablePerLengthSequenceImpedances(),
        TablePhotoVoltaicUnit: TablePhotoVoltaicUnit(),
        TablePoles: TablePoles(),
        TablePositionPoints: TablePositionPoints(),
        TablePowerElectronicsConnection: TablePowerElectronicsConnection(),
        TablePowerElectronicsConnectionPhases: TablePowerElectronicsConnectionPhases(),
        TablePowerElectronicsWindUnit: TablePowerElectronicsWindUnit(),
        TablePowerTransformerEnds: TablePowerTransformerEnds(),
        TablePowerTransformerInfo: TablePowerTransformerInfo(),
        TablePowerTransformers: TablePowerTransformers(),
        TablePricingStructures: TablePricingStructures(),
        TablePricingStructuresTariffs: TablePricingStructuresTariffs(),
        TableRatioTapChangers: TableRatioTapChangers(),
        TableReclosers: TableReclosers(),
        TableRemoteControls: TableRemoteControls(),
        TableRemoteSources: TableRemoteSources(),
        TableShortCircuitTests: TableShortCircuitTests(),
        TableShuntCompensatorInfo: TableShuntCompensatorInfo(),
        TableSites: TableSites(),
        TableStreetlights: TableStreetlights(),
        TableSubGeographicalRegions: TableSubGeographicalRegions(),
        TableSubstations: TableSubstations(),
        TableTariffs: TableTariffs(),
        TableTerminals: TableTerminals(),
        TableTransformerEndInfo: TableTransformerEndInfo(),
        TableTransformerStarImpedance: TableTransformerStarImpedance(),
        TableTransformerTankInfo: TableTransformerTankInfo(),
        TableUsagePoints: TableUsagePoints(),
        TableUsagePointsEndDevices: TableUsagePointsEndDevices(),
        TableVersion: TableVersion(),
    }


@dataclass(slots=True)
class PreparedStatement(object):
    statement: str
    _values: Dict[int, Any] = dict()
    _num_cols: int = None

    def __init__(self):
        self._num_cols = self.statement.count('?')

    @property
    def num_columns(self):
        return self._num_cols

    @property
    def parameters(self):
        """
        Get the string representation of the current parameters set on this PreparedStatement.
        '(unset)' means this index has not yet been set.
        This function should be used for error handling and debugging only.

        Returns the string representation of all parameters that have been set on this PreparedStatement, separated by commas.
        """
        pm = []
        for i in range(1, self.num_columns + 1):
            try:
                pm.append(str(self._values[i]))
            except KeyError:
                pm.append("(unset)")
        return ", ".join(pm)

    def execute(self, cursor: Cursor):
        """
        Execute this PreparedStatement using the given `cursor`.

        Throws any exception possible from cursor.execute, typically `sqlite3.DatabaseError`
        """
        parameters = []
        missing = []
        for i in range(1, self.num_columns + 1):
            try:
                parameters.append(self._values[i])
            except KeyError:
                missing.append(str(i))

        if missing:
            raise SqlException(f"Missing values for indices {', '.join(missing)}. Ensure all ?'s have a corresponding value in the prepared statement.")

        cursor.execute(self.statement, parameters)

    def add_value(self, index: int, value: Any):
        if 0 < index <= self._num_cols:
            self._values[index] = value
        else:
            raise SqlException(f"index must be between 1 and {self.num_columns} for this statement, got {index}")


@dataclass(slots=True)
class DatabaseTables(object):
    _tables: Dict[Type[T], T] = _create_tables()
    _insert_statements: Dict[Type[T], PreparedStatement] = dict()

    def __init__(self):
        self._insert_statements.clear()
        for t, table in self._tables.items():
            self._insert_statements[t] = PreparedStatement(table.prepared_insert_sql())

    def get_table(self, clazz: Type[T]) -> T:
        try:
            return self._tables[clazz]
        except KeyError:
            raise MissingTableConfigException(f"No table has been registered for {clazz}. Add the table to database_tables.py")

    def get_insert(self, clazz: Type[T]) -> PreparedStatement:
        try:
            return self._insert_statements[clazz]
        except KeyError:
            raise MissingTableConfigException(f"No prepared insert statement has been registered for {clazz}. Add the to database_tables.py")

    @property
    def tables(self):
        for t in self._tables.values():
            yield t

    @staticmethod
    def copy():
        return DatabaseTables()
