#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Callable, Optional

from zepben.evolve import MetadataCollection, NetworkService, DiagramService, CustomerService, MetadataEntryReader, DiagramCIMReader, CustomerCIMReader, \
    TableVersion, MetadataCollectionReader, DiagramServiceReader, CustomerServiceReader, Feeder, EnergySource, ConductingEquipment, connected_equipment
from zepben.evolve.database.sqlite.readers.network_cim_reader import NetworkCIMReader
from zepben.evolve.database.sqlite.readers.network_service_reader import NetworkServiceReader
from zepben.evolve.services.network.tracing import tracing

logger = logging.getLogger(__name__)
__all__ = ["DatabaseReader"]


class DatabaseReader:

    def __init__(
        self,
        database_file: str,
        get_connection: Callable[[str], Connection] = lambda database: sqlite3.connect(database),
        get_cursor: Callable[[Connection], Cursor] = lambda conn: conn.cursor()
    ):
        """
        :param database_file: the filename of the database to write.
        :param get_connection: provider of the connection to the specified database.
        :param get_cursor: provider of statements for the connection.
        """
        self._database_file = database_file
        self._get_connection = get_connection
        self._get_cursor = get_cursor

    _connection: Optional[Connection] = None
    _has_been_used = False

    def load(
        self,
        metadata_collection: MetadataCollection,
        network_service: NetworkService,
        diagram_service: DiagramService,
        customer_service: CustomerService
    ) -> bool:
        if not self._connect_database():
            self._close_connection()
            return False

        metadata_reader = MetadataEntryReader(metadata_collection)
        network_service_reader = NetworkCIMReader(network_service)
        diagram_service_reader = DiagramCIMReader(diagram_service)
        customer_service_reader = CustomerCIMReader(customer_service)

        def get_cursor() -> Cursor:
            return self._get_cursor(self._connection)

        try:
            status = MetadataCollectionReader(get_cursor).load(metadata_reader) \
                     and NetworkServiceReader(get_cursor).load(network_service_reader) \
                     and DiagramServiceReader(get_cursor).load(diagram_service_reader) \
                     and CustomerServiceReader(get_cursor).load(customer_service_reader)
        except Exception as e:
            logger.error(f"Unable to load database: {str(e)}")
            self._close_connection()
            return False

        return status and self._post_load(network_service)

    def _connect_database(self) -> bool:
        if self._has_been_used:
            logger.error("You can only use the database reader once.")
            return False

        self._has_been_used = True

        try:
            self._connection = self._get_connection(self._database_file)

            cur = self._get_cursor(self._connection)
            cur.execute("SELECT version FROM version")
            rows = cur.fetchall()
            if len(rows) == 1:
                version = int(rows[0][0])
                if version == TableVersion.SUPPORTED_VERSION:
                    return True

                logger.error(f"Invalid database version. Found {version}, expected {TableVersion.SUPPORTED_VERSION}.")
            else:
                logger.error("Unable to read version from database. Please make sure the database is a valid EWB database.")
        except Exception as e:
            logger.error(f"Failed to connect to the database for reading: {str(e)}")

        return False

    def _close_connection(self):
        if self._connection is None:
            return

        try:
            self._connection.close()
        except Exception as e:
            logger.error(f"Failed to close connection to database: {str(e)}")
        finally:
            self._connection = None

    def _post_load(self, network_service: NetworkService) -> bool:
        #
        # NOTE: phase and direction tracing is not yet supported
        #

        logger.info("Applying feeder direction to network...")
        tracing.set_direction().run(network_service)
        logger.info("Feeder direction applied to network.")

        logger.info("Applying phases to network...")
        tracing.set_phases().run(network_service)
        tracing.phase_inferrer().run(network_service)
        logger.info("Phasing applied to network.")

        logger.info("Assigning equipment to feeders...")
        tracing.assign_equipment_to_feeders().run(network_service)
        logger.info("Equipment assigned to feeders.")

        logger.info("Assigning equipment to LV feeders...")
        tracing.assign_equipment_to_lv_feeders().run(network_service)
        logger.info("Equipment assigned to LV feeders.")

        logger.info("Validating primary sources vs feeders...")
        self._validate_sources(network_service)
        logger.info("Sources vs feeders validated.")

        self._close_connection()
        return True

    def _validate_sources(self, network_service: NetworkService):
        def get_head_equipment(feeder: Feeder) -> Optional[ConductingEquipment]:
            if feeder.normal_head_terminal is not None:
                return feeder.normal_head_terminal.conducting_equipment
            else:
                return None

        # We do not want to warn about sources attached directly to the feeder start point.
        feeder_start_points = set(filter(lambda it: it is not None, map(get_head_equipment, network_service.objects(Feeder))))

        def has_been_assigned_to_feeder(energy_source: EnergySource) -> bool:
            return energy_source.is_external_grid \
                   and self._is_on_feeder(energy_source) \
                   and feeder_start_points.isdisjoint(set(connected_equipment(energy_source)))

        for es in filter(has_been_assigned_to_feeder, network_service.objects(EnergySource)):
            logger.warning(f"External grid source {es} has been assigned to the following feeders: normal {es.normal_feeders}, current {es.current_feeders}")

    @staticmethod
    def _is_on_feeder(energy_source: EnergySource) -> bool:
        return bool(list(energy_source.normal_feeders)) or bool(list(energy_source.current_feeders))
