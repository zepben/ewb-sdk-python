#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetServiceWriter"]

from zepben.ewb.database.sqlite.changeset.change_set_cim_writer import ChangeSetCimWriter
from zepben.ewb.database.sqlite.changeset.change_set_database_tables import ChangeSetDatabaseTables
from zepben.ewb.database.sqlite.common.base_service_writer import BaseServiceWriter
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetServiceWriter(BaseServiceWriter):
    """
    A class for writing a `VariantService` into the database.

    :param service: The `VariantService` to save to the database.
    :param database_tables: The `ChangeSetDatabaseTables` to add to the database.
    """

    def __init__(
        self,
        service: VariantService,
        database_tables: ChangeSetDatabaseTables,
        writer: ChangeSetCimWriter = None
    ):
        writer = writer if writer is not None else ChangeSetCimWriter(database_tables)
        super().__init__(service, writer)

        # This is not strictly necessary, it is just to update the type of the writer. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._writer: ChangeSetCimWriter = writer

    def _do_save(self) -> bool:
        return all([
            self._save_each_object(ChangeSet, self._writer.save_change_set),
            self._save_each_object(ObjectCreation, self._writer.save_object_creation),
            self._save_each_object(ObjectDeletion, self._writer.save_object_deletion),
            self._save_each_object(ObjectModification, self._writer.save_object_modification)
        ])
