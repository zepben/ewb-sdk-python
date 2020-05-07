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
from __future__ import annotations

import logging
# from zepben.cimbend.util import snake2camelback, iter_but_not_str
from abc import ABCMeta
from dataclasses import dataclass
from typing import Union
from uuid import uuid4, UUID

__all__ = ["IdentifiedObject"]

# Global state for ignored attributes - used when building protobuf args. Any keys in here will not be included
_ignored_attribute_cache = set()

logger = logging.getLogger(__name__)


@dataclass
class IdentifiedObject(object, metaclass=ABCMeta):
    """
    Root class to provide common identification for all classes needing identification and naming attributes.
    Everything should extend this class, however it's not mandated that every subclass must use all the fields
    defined here.

    All names of attributes of classes extending this class *must* directly reflect CIM properties if they have a direct
    relation, however must be in snake case to keep the phases PEP compliant.
    If you need to add extra attributes to a class that *ARE NOT* in the corresponding protobuf type the name
    must start with at least 2 underscores, for example __upstream in :class:`zepben.cimbend.Terminal`, and you should
    define this attribute as a property in the class using @property and @<property>.setter.
    Failure to do this will result in the conversion to a protobuf type failing. Long Live PEP8

    Attributes -
        mrid : Master resource identifier issued by a model authority. The mRID is unique within an exchange context.
               Global uniqueness is easily achieved by using a UUID, as specified in RFC 4122, for the mRID.
               The use of UUID is strongly recommended.
        name : The name is any free human readable and possibly non unique text naming the object.
        num_diagram_objects : The number of diagram objects associated with this object. Used to tell clients whether
                              they can fetch diagram objects from a related DiagramService
    """
    # TODO: requires rework of _pb_args
    # __slots__ = "_m_r_i_d", "name", "__diagram_objects_by_diagram"

    mrid: Union[str, UUID] = ""
    name: str = ""
    num_diagram_objects: int = 0

    def __post_init__(self):
        if not self.mrid:
            self.mrid = uuid4()

    def __str__(self):
        return f"{self.__class__.__name__}{{{'|'.join(a for a in (str(self.mrid), self.name) if a)}}}"

    def __repr__(self):
        return f"mrid='{self.mrid}', name='{self.name}', num_diagram_objects={self.num_diagram_objects}"

    @property
    def has_diagram_objects(self):
        return self.num_diagram_objects > 0

    # @classmethod
    # def from_pbs(cls, pb, *args, **kwargs):
    #     return [cls.from_pb(x, *args, **kwargs) for x in pb]

    # def _is_from_bases(self, k):
    #     """Check if a certain key is an attribute from a base class."""
    #     for c in inspect.getmro(self.__class__):
    #         if k.startswith(f'_{c.__name__}'):
    #             return True
    #     return False
    #
    # def _should_ignore_key(self, k, v, exclude):
    #     if k in _ignored_attribute_cache:
    #         return True
    #     # No point adding any attributes that don't have a value
    #     if v is None:
    #         return True
    #     if exclude:
    #         if k in exclude:
    #             return True
    #     # attributes starting with _<classname> are properties and should always be excluded
    #     if self._is_from_bases(k) or k.startswith('__'):
    #         _ignored_attribute_cache.add(k)
    #         return True
    #
    #     return False

    # def _pb_args(self, exclude=None):
    #     """
    #     Protobuf CIM objects are in camelcase, but we want to keep the CIM phases PEP compliant;
    #     to convert between a CIM object and a PB object, we should simply be able to convert the attributes between
    #     snake case and camelback and use the corresponding PB constructor to build the protobuf form.
    #     :param exclude: List of properties to exclude from the resulting dictionary
    #     :return: A dictionary representing all the properties of this object with camelback keys. Where a property is
    #     another CIM type, or is a collection of a CIM type, to_pb() should be called for each and the result returned
    #     as the key to the dictionary. As an example, see self.diagram_points below or terminals in
    #     ConductingEquipment._pb_args()
    #     # TODO: use __slots__
    #     """
    #     exclude = {} if exclude is None else exclude
    #     pb_dict = {"diagramObjects": []}
    #     for diagram_id, diag_objs in self.diagram_objects_by_diagram.items():
    #         pb_dict["diagramObjects"].extend([obj.to_pb() for obj in diag_objs])
    #
    #     for k, v in self.__dict__.items():
    #         if self._should_ignore_key(k, v, exclude):
    #             continue
    #
    #         # Remove any leading underscores and convert to camelback casing
    #         key = snake2camelback(k.lstrip('_'))
    #         try:
    #             if v is not None:
    #                 pb_dict[key] = v.to_pb()
    #         except AttributeError:
    #             # Any sequence must stay a sequence, except for strings, bytes, and bytearrays.
    #             if iter_but_not_str(v):
    #                 try:
    #                     # Handle repeated sub-message
    #                     pb_dict[key] = []
    #                     for x in v:
    #                         pb_dict[key].append(x.to_pb())
    #                 except AttributeError as ae:
    #                     if x:
    #                         if hasattr(x, 'to_pb'):
    #                             logger.warning(f"Converting repeated field '{key}' caused: ", exc_info=ae)
    #                     # Handle repeated scalar
    #                     pb_dict[key] = v
    #             else:
    #                 # Strings + every other scalar
    #                 pb_dict[key] = v
    #         except NotImplementedError:
    #             continue
    #
    #     #        for k, v in zip(self.__slots__, map(self.__getattribute__, self.__slots__)):
    #     #            if self._should_ignore_key(k, v, exclude):
    #     #                continue
    #     #
    #     #            # Remove any leading underscores and convert to camelback casing
    #     #            key = snake2camelback(k.lstrip('_'))
    #     #            try:
    #     #                pb_dict[key] = v.to_pb()
    #     #            except AttributeError:
    #     #                # Any sequence must stay a sequence, except for strings, bytes, and bytearrays.
    #     #                if iter_but_not_str(v):
    #     #                    try:
    #     #                        # Handle repeated sub-message
    #     #                        pb_dict[key] = [x.to_pb() for x in v]
    #     #                    except AttributeError:
    #     #                        # Handle repeated scalar
    #     #                        pb_dict[key] = v
    #     #                else:
    #     #                    # Strings + every other scalar
    #     #                    pb_dict[key] = v
    #     #            except NotImplementedError:
    #     #                continue
    #
    #     return pb_dict

