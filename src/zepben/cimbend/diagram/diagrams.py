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


from dataclasses import dataclass, field
from typing import Dict, List

from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_layout import DiagramObject
from zepben.cimbend.common.base_service import BaseService

__all__ = ["DiagramService"]


@dataclass
class DiagramService(BaseService):
    name: str = "diagram"
    _diagram_objects_by_diagram_mrid: Dict[str, Dict[str, DiagramObject]] = field(default_factory=dict)
    _diagram_objects_by_identified_object_mrid: Dict[str, Dict[str, DiagramObject]] = field(default_factory=dict)
    _diagram_object_indexes: List[Dict[str, Dict[str, DiagramObject]]] = field(default_factory=list)

    def __post_init__(self):
        self._diagram_object_indexes.append(self._diagram_objects_by_identified_object_mrid)
        self._diagram_object_indexes.append(self._diagram_objects_by_diagram_mrid)

    def get_diagram_objects(self, mrid: str) -> List[DiagramObject]:
        """
        Get ``DiagramObject``'s from the service associated with the given mRID.

        ``DiagramObject``'s are indexed by its ``DiagramObject.mrid``, its ``DiagramObject.diagram.mrid``,
        and its ``DiagramObject.identifiedObjectMRID``'s (if present).

        If you request a ``DiagramObject`` by its mRID you will receive a List with a single entry, otherwise
        the list will contain as many ``DiagramObject``'s as have been recorded against the provided mRID.
        :param mrid: The mRID to look up in the service.
        :return: A list of ``DiagramObject``'s associated with ``mrid``.
        """
        obj = self.get(mrid, DiagramObject)
        if obj is not None:
            return [obj]

        for index in self._diagram_object_indexes:
            if mrid in index:
                return list(index[mrid].values())

        return []

    def add_diagram_object(self, diagram_object: DiagramObject):
        """
        Associate a ``DiagramObject`` with this service.
        The ``DiagramObject`` will be indexed by its ``Diagram`` and its ``IdentifiedObject`` (if present).

        :param diagram_object: The ``DiagramObject`` to add.
        :return: True if the ``DiagramObject`` was successfully associated with the service.
        """
        return super().add(diagram_object) and self._add_index(diagram_object)

    def remove(self, diagram_object: DiagramObject) -> bool:
        """
        Disassociate a ``DiagramObject`` with the service. This will remove all indexing of the ``DiagramObject`` and it
        will no longer be able to be found via the service.

        :param diagram_object: The ``DiagramObject`` to disassociate with this service.
        :return: True if the ``DiagramObject`` was removed successfully.
        """
        return super().remove(diagram_object) and self._remove_index(diagram_object)

    def _add_index(self, diagram_object: DiagramObject) -> bool:
        """
        Index a ``DiagramObject`` against its associated [Diagram] and [IdentifiedObject].

        :param diagram_object: The ``DiagramObject`` to remove from the indexes.
        :return: True if the index was updated.
        """
        self._diagram_objects_by_diagram_mrid.setdefault(diagram_object.diagram.mrid, dict())[diagram_object.mrid] = diagram_object
        iomrid = diagram_object.identified_object_mrid
        if iomrid is not None:
            self._diagram_objects_by_identified_object_mrid.setdefault(iomrid, dict())[diagram_object.mrid] = diagram_object

        return True

    def _remove_index(self, diagram_object: DiagramObject) -> bool:
        """
        Remove the indexes of a ``DiagramObject``.

        :param diagram_object: The ``DiagramObject`` to remove from the indexes.
        :return: True if the index was updated.
        """
        diagram_map = self._diagram_objects_by_diagram_mrid[diagram_object.diagram.mrid]
        if diagram_map is not None:
            del diagram_map[diagram_object.mrid]
            if not diagram_map:
                del self._diagram_objects_by_diagram_mrid[diagram_object.diagram.mrid]

        iomrid = diagram_object.identified_object_mrid
        if iomrid is not None:
            io_map = self._diagram_objects_by_identified_object_mrid[iomrid]
            if io_map is not None:
                del io_map[diagram_object.mrid]
                if not io_map:
                    del self._diagram_objects_by_identified_object_mrid[iomrid]

        return True
