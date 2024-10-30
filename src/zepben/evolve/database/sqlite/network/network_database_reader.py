#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from sqlite3 import Connection
from typing import Optional

from zepben.evolve.database.sqlite.common.base_database_reader import BaseDatabaseReader
from zepben.evolve.database.sqlite.common.metadata_collection_reader import MetadataCollectionReader
from zepben.evolve.database.sqlite.network.network_database_tables import NetworkDatabaseTables
from zepben.evolve.database.sqlite.network.network_service_reader import NetworkServiceReader
from zepben.evolve.database.sqlite.tables.table_version import TableVersion
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.services.network.network_service import NetworkService, connected_equipment

__all__ = ["NetworkDatabaseReader"]

from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import AssignToFeeders
from zepben.evolve.services.network.tracing.feeder.assign_to_lv_feeders import AssignToLvFeeders

from zepben.evolve.services.network.tracing.feeder.set_direction import SetDirection
from zepben.evolve.services.network.tracing.phases.phase_inferrer import PhaseInferrer
from zepben.evolve.services.network.tracing.phases.set_phases import SetPhases


class NetworkDatabaseReader(BaseDatabaseReader):
    """
    A class for reading the `NetworkService` objects and `MetadataCollection` from our network database.

    NOTE: The network database must be loaded first if you are using a pre-split database you wish to upgrade as it was the only database at the time
      and will create the other databases as part of the upgrade. This warning can be removed once we set a new minimum version of the database and
      remove the split database logic - Check `UpgradeRunner` to see if this is still required.

    :param connection: The connection to the database.
    :param service: The `NetworkService` to populate with CIM objects from the database.
    :param database_description: The description of the database for logging (e.g. filename).
    """

    def __init__(
        self,
        connection: Connection,
        service: NetworkService,
        database_description: str,
        tables: NetworkDatabaseTables = NetworkDatabaseTables(),
        metadata_reader: MetadataCollectionReader = None,
        service_reader: NetworkServiceReader = None,
        table_version: TableVersion = TableVersion(),
        set_direction: SetDirection = SetDirection(),
        set_phases: SetPhases = SetPhases(),
        phase_inferrer: PhaseInferrer = PhaseInferrer(),
        assign_to_feeders: AssignToFeeders = AssignToFeeders(),
        assign_to_lv_feeders: AssignToLvFeeders = AssignToLvFeeders()
    ):
        super().__init__(
            connection,
            metadata_reader if metadata_reader else MetadataCollectionReader(service, tables, connection),
            service_reader if service_reader else NetworkServiceReader(service, tables, connection),
            service,
            database_description,
            table_version
        )
        self.service = service
        self.set_direction = set_direction
        self.set_phases = set_phases
        self.phase_inferrer = phase_inferrer
        self.assign_to_feeders = assign_to_feeders
        self.assign_to_lv_feeders = assign_to_lv_feeders

    async def _post_load(self) -> bool:
        status = await super()._post_load()

        self._logger.info("Applying feeder direction to network...")
        await self.set_direction.run(self.service)
        self._logger.info("Feeder direction applied to network.")

        self._logger.info("Applying phases to network...")
        await self.set_phases.run(self.service)
        await self.phase_inferrer.run(self.service)
        self._logger.info("Phasing applied to network.")

        self._logger.info("Assigning equipment to feeders...")
        await self.assign_to_feeders.run(self.service)
        self._logger.info("Equipment assigned to feeders.")

        self._logger.info("Assigning equipment to LV feeders...")
        await self.assign_to_lv_feeders.run(self.service)
        self._logger.info("Equipment assigned to LV feeders.")

        self._logger.info("Validating that each equipment is assigned to a container...")
        self._validate_equipment_containers()
        self._logger.info("Equipment containers validated.")

        self._logger.info("Validating primary sources vs feeders...")
        self._validate_sources()
        self._logger.info("Sources vs feeders validated.")

        return status

    def _validate_equipment_containers(self):
        missing_containers = [it for it in self.service.objects(Equipment) if not it.containers]
        count_by_class = Counter()

        for it in missing_containers:
            count_by_class[type(it).__name__] += 1

        for (className, count) in count_by_class:
            self._logger.warning(f"{count} {className}s were missing an equipment container.")

        if count_by_class:
            self._logger.warning(f"A total of {len(missing_containers)} equipment had no associated equipment container. Debug logging will show more details.")

        for equipment in missing_containers:
            self._logger.debug(f"{equipment} was not assigned to any equipment container.")

    def _validate_sources(self):
        def head_conducting_equipment_mrid(feeder: Feeder) -> Optional[str]:
            if feeder.normal_head_terminal and feeder.normal_head_terminal.conducting_equipment:
                return feeder.normal_head_terminal.conducting_equipment.mrid
            else:
                return None

        # We do not want to warn about sources attached directly to the feeder start point.
        feeder_start_points = set(map(head_conducting_equipment_mrid, self.service.objects(Feeder)))

        def has_been_assigned_to_feeder(energy_source: EnergySource) -> bool:
            return energy_source.is_external_grid \
                and self._is_on_feeder(energy_source) \
                and feeder_start_points.isdisjoint({it.to_equip.mrid for it in connected_equipment(energy_source) if it.to_equip})

        for es in self.service.objects(EnergySource):
            if has_been_assigned_to_feeder(es):
                self._logger.warning(
                    f"External grid source {es.name} [{es.mrid}] has been assigned to the following feeders: normal [{[it.mrid for it in es.normal_feeders]}], "
                    f"current [{[it.mrid for it in es.current_feeders]}]"
                )

    @staticmethod
    def _is_on_feeder(energy_source: EnergySource) -> bool:
        if energy_source.normal_feeders or energy_source.current_feeders:
            return True
        else:
            return False
