#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict, List

from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import DiagramObject
from zepben.evolve.services.common.base_service import BaseService

__all__ = ["DiagramService"]


class DiagramService(BaseService):
    name: str = "diagram"
    _diagram_objects_by_diagram_mrid: Dict[str, Dict[str, DiagramObject]] = dict()
    _diagram_objects_by_identified_object_mrid: Dict[str, Dict[str, DiagramObject]] = dict()
    _diagram_object_indexes: List[Dict[str, Dict[str, DiagramObject]]] = list()

    def __init__(self):
        self._diagram_object_indexes.append(self._diagram_objects_by_identified_object_mrid)
        self._diagram_object_indexes.append(self._diagram_objects_by_diagram_mrid)

    def get_diagram_objects(self, mrid: str) -> List[DiagramObject]:
        """
        Get `DiagramObject`'s from the service associated with the given mRID.

        `DiagramObject`'s are indexed by its `DiagramObject.mrid`, its `DiagramObject.diagram.mrid`,
        and its `DiagramObject.identifiedObjectMRID`'s (if present).

        If you request a `DiagramObject` by its mRID you will receive a List with a single entry, otherwise
        the list will contain as many `DiagramObject`'s as have been recorded against the provided mRID.
        `mrid` The mRID to look up in the service.
        Returns A list of `DiagramObject`'s associated with `mrid`.
        """
        obj = self.get(mrid, DiagramObject, None)
        if obj is not None:
            return [obj]

        for index in self._diagram_object_indexes:
            if mrid in index:
                return list(index[mrid].values())

        return []

    def add_diagram_object(self, diagram_object: DiagramObject):
        """
        Associate a `DiagramObject` with this service.
        The `DiagramObject` will be indexed by its `Diagram` and its `IdentifiedObject` (if present).

        `diagram_object` The `DiagramObject` to add.
        Returns True if the `DiagramObject` was successfully associated with the service.
        """
        return self.add(diagram_object) and self._add_index(diagram_object)

    def remove(self, diagram_object: DiagramObject) -> bool:
        """
        Disassociate a `DiagramObject` with the service. This will remove all indexing of the `DiagramObject` and it
        will no longer be able to be found via the service.

        `diagram_object` The `DiagramObject` to disassociate with this service.
        Returns True if the `DiagramObject` was removed successfully.
        """
        return super(DiagramService, self).remove(diagram_object) and self._remove_index(diagram_object)

    def _add_index(self, diagram_object: DiagramObject) -> bool:
        """
        Index a `DiagramObject` against its associated [Diagram] and [IdentifiedObject].

        `diagram_object` The `DiagramObject` to remove from the indexes.
        Returns True if the index was updated.
        """
        if diagram_object.diagram:
            self._diagram_objects_by_diagram_mrid.setdefault(diagram_object.diagram.mrid, dict())[diagram_object.mrid] = diagram_object

        io_mrid = diagram_object.identified_object_mrid
        if io_mrid:
            self._diagram_objects_by_identified_object_mrid.setdefault(io_mrid, dict())[diagram_object.mrid] = diagram_object

        return True

    def _remove_index(self, diagram_object: DiagramObject) -> bool:
        """
        Remove the indexes of a `DiagramObject`.

        `diagram_object` The `DiagramObject` to remove from the indexes.
        Returns True if the index was updated.
        """
        if diagram_object.diagram.mrid:
            diagram_map = self._diagram_objects_by_diagram_mrid[diagram_object.diagram.mrid]
            if diagram_map is not None:
                del diagram_map[diagram_object.mrid]
                if not diagram_map:
                    del self._diagram_objects_by_diagram_mrid[diagram_object.diagram.mrid]

        io_mrid = diagram_object.identified_object_mrid
        if io_mrid is not None:
            io_map = self._diagram_objects_by_identified_object_mrid[io_mrid]
            if io_map is not None:
                del io_map[diagram_object.mrid]
                if not io_map:
                    del self._diagram_objects_by_identified_object_mrid[io_mrid]

        return True
