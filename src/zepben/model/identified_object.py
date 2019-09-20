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


from zepben.model.diagram_layout import DiagramObjectPoints
from zepben.model.util import snake2camelback, iter_but_not_str
from abc import abstractmethod


class IdentifiedObject(object):
    """
    All names of attributes *must* directly reflect CIM properties if they have a direct relation, however must be in
    snake case to keep the model PEP compliant.
    If you need to add extra attributes to a class that *ARE NOT* in the corresponding protobuf type the name
    must start with at least 2 underscores, for example __upstream in terminal, and you should define this attribute
    as a property in the class using @property and @<property>.setter. Failure to do this will result in the conversion
    to a protobuf type failing. Long Live PEP8
    """
    def __init__(self, mrid: str, name: str = None, diagram_points: DiagramObjectPoints = None, description: str = None):
        # It's really horrible to use the snake form of mRID, so we define a property + setter for it below as "mrid".
        self._m_r_i_d = mrid
        self.name = name
        self.description = description
        self.diagram_points = diagram_points

    def __str__(self):
        return f"mrid: {self.mrid}, name: {self.name.strip() if self.name else 'UNKNOWN'} point: {self.diagram_points}"

    def __repr__(self):
        return f"mrid: {self.mrid}, name: {self.name.strip() if self.name else 'UNKNOWN'} {self.diagram_points}"

    @property
    def mrid(self):
        return self._m_r_i_d

    @mrid.setter
    def mrid(self, mrid):
        self._m_r_i_d = mrid

    @abstractmethod
    def to_pb(self):
        raise NotImplementedError("Conversion to protobuf is not supported.")

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
        pb_dict = {}
        for k, v in self.__dict__.items():
            # No point adding any attributes that don't have a value
            if v is None:
                continue
            if k in exclude:
                continue
            # attributes starting with _<classname> are properties and should always be excluded
            if k.startswith(f'_{self.__class__.__name__}'):
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

        return pb_dict

    def has_xy(self):
        return self.diagram_points is not None

    def set_diagram_points(self, diagram_points):
        self.diagram_points = diagram_points
