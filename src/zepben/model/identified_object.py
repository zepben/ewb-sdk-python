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


from zepben.model.util import snake2camelback, iter_but_not_str
from abc import abstractmethod, ABCMeta
from typing import List
import inspect

# Global state for ignored attributes - used when building protobuf args. Any keys in here will not be included
_ignored_attribute_cache = set()


class IdentifiedObject(object, metaclass=ABCMeta):
    """
    Root class to provide common identification for all classes needing identification and naming attributes.
    Everything should extend this class, however it's not mandated that every subclass must use all the fields
    defined here.

    All names of attributes of classes extending this class *must* directly reflect CIM properties if they have a direct
    relation, however must be in snake case to keep the model PEP compliant.
    If you need to add extra attributes to a class that *ARE NOT* in the corresponding protobuf type the name
    must start with at least 2 underscores, for example __upstream in :class:`zepben.model.Terminal`, and you should
    define this attribute as a property in the class using @property and @<property>.setter.
    Failure to do this will result in the conversion to a protobuf type failing. Long Live PEP8

    Attributes:
        mrid : Master resource identifier issued by a model authority. The mRID is unique within an exchange context.
               Global uniqueness is easily achieved by using a UUID, as specified in RFC 4122, for the mRID.
               The use of UUID is strongly recommended.
        name : The name is any free human readable and possibly non unique text naming the object.
        diagram_objects : The :class:`zepben.model.DiagramObject`'s related to this object.
    """
    def __init__(self, mrid: str = "", name: str = "", diagram_objects: List = None):
        """

        :param mrid: The Master Resource Identifier for this object.
        :param name: Any free human readable text naming this object.
        :param diagram_objects: The :class:`zepben.model.DiagramObject`'s related to this object.
        """
        # It's really horrible to use the snake form of mRID, so we define a property + setter for it below as "mrid".
        self._m_r_i_d = mrid
        self.name = name
        self.__diagram_objects_by_diagram = dict()
        if diagram_objects is not None:
            for obj in diagram_objects:
                self.add_diagram_object(obj)

    def __str__(self):
        return f"mrid: {self.mrid}, name: {self.name.strip() if self.name else 'UNKNOWN'} point: {self.diagram_objects}"

    def __repr__(self):
        return f"mrid: {self.mrid}, name: {self.name.strip() if self.name else 'UNKNOWN'} {self.diagram_objects}"

    def add_diagram_object(self, diagram_object):
        if diagram_object.diagram is not None:
            diagram_objects = self.diagram_objects_by_diagram.get(diagram_object.diagram.mrid, [])
            diagram_objects.append(diagram_object)
            self.diagram_objects_by_diagram[diagram_object.diagram.mrid] = diagram_objects

    @property
    def mrid(self):
        return self._m_r_i_d

    @mrid.setter
    def mrid(self, mrid):
        self._m_r_i_d = mrid

    def diagram_objects(self, diagram_mrid=""):
        """Get the objects for a diagram. If diagram_mrid is None will use default diagram"""
        return self.diagram_objects_by_diagram[diagram_mrid]

    @property
    def diagram_objects_by_diagram(self):
        return self.__diagram_objects_by_diagram

    @abstractmethod
    def to_pb(self):
        """
        This method should be defined for any :mod:`zepben.model` type that can be converted to a
        :mod:`zepben.cim` protobuf message.
        :return: The corresponding protobuf message
        """
        raise NotImplementedError("Conversion to protobuf is not supported.")

    @staticmethod
    @abstractmethod
    def from_pb(*args, **kwargs):
        """
        This method should be defined for all types that can be transformed from a Protobuf message.
        :param args: First arg should always be the protobuf message to convert
        :param kwargs: All other args are implementation dependent, anything you need to build your
                       type should be passed in as another parameter. Typical example is network: EquipmentContainer,
                       used for fetching references from an associated network.
        :return: The corresponding type from :mod:`zepben.model`
        """
        raise NotImplementedError("Conversion from protobuf is not supported.")

    @classmethod
    def from_pbs(cls, pb, *args, **kwargs):
        return [cls.from_pb(x, *args, **kwargs) for x in pb]

    def get_all_diagram_object_points(self):
        points = []
        for diag_obj in self.diagram_objects_by_diagram.values():
            points.extend(diag_obj.diagram_object_points)
        return points

    def _is_from_bases(self, k):
        """Check if a certain key is an attribute from a base class."""
        for c in inspect.getmro(self.__class__):
            if k.startswith(f'_{c.__name__}'):
                return True
        return False

    def _should_ignore_key(self, k, v, exclude):
        if k in _ignored_attribute_cache:
            return True
        # No point adding any attributes that don't have a value
        if v is None:
            return True
        if exclude:
            if k in exclude:
                return True
        # attributes starting with _<classname> are properties and should always be excluded
        if self._is_from_bases(k) or k.startswith('__'):
            _ignored_attribute_cache.add(k)
            return True

        return False

    def _pb_args(self, exclude=None):
        """
        Protobuf CIM objects are in camelback form, but we want to keep the CIM model PEP compliant;
        to convert between a CIM object and a PB object, we should simply be able to convert the attributes between
        snake case and camelback and use the corresponding PB constructor to build the protobuf form.
        :param exclude: List of properties to exclude from the resulting dictionary
        :return: A dictionary representing all the properties of this object with camelback keys. Where a property is
        another CIM type, or is a collection of a CIM type, to_pb() should be called for each and the result returned
        as the key to the dictionary. As an example, see self.diagram_points below or terminals in
        ConductingEquipment._pb_args()
        """
        exclude = {} if exclude is None else exclude
        pb_dict = {"diagramObjects": []}
        for diagram_id, diag_objs in self.diagram_objects_by_diagram.items():
            pb_dict["diagramObjects"].extend([obj.to_pb() for obj in diag_objs])

        for k, v in self.__dict__.items():
            if self._should_ignore_key(k, v, exclude):
                continue

            # Remove any leading underscores and convert to camelback casing
            key = snake2camelback(k.lstrip('_'))
            try:
                pb_dict[key] = v.to_pb()
            except AttributeError:
                # Any sequence must stay a sequence, except for strings, bytes, and bytearrays.
                if iter_but_not_str(v):
                    try:
                        # Handle repeated sub-message
                        pb_dict[key] = [x.to_pb() for x in v]
                    except AttributeError:
                        # Handle repeated scalar
                        pb_dict[key] = v
                else:
                    # Strings + every other scalar
                    pb_dict[key] = v
            except NotImplementedError:
                continue
        return pb_dict

    def has_xy(self):
        return self.diagram_objects is not None

