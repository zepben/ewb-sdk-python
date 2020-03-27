from __future__ import annotations
from zepben.model.identified_object import IdentifiedObject
from typing import List
__all__ = ['PowerSystemResource']


class PowerSystemResource(IdentifiedObject):
    """
    Abstract class, should only be used through subclasses.
    A power system resource can be an item of equipment such as a switch, an equipment container containing many individual
    items of equipment such as a substation, or an organisational entity such as sub-control area. Power system resources
    can have measurements associated.

    Attributes:
        - location : A :class:`zepben.model.Location` for this resource.
        - asset_info : A subclass of :class:`zepben.model.AssetInfo` providing information about the asset associated
                       with this PowerSystemResource.
    """
    def __init__(self, mrid: str, name: str = "", asset_info: AssetInfo = None, diag_objs: List[DiagramObject] = None,
                 location: Location = None):
        """
        Create a PowerSystemResource
        :param mrid: mRID for this object
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        :param asset_info: A subclass of :class:`zepben.model.AssetInfo` providing information about the asset associated
                           with this PowerSystemResource.
        """
        self.location = location
        self.asset_info = asset_info
        super().__init__(mrid=mrid, name=name, diagram_objects=diag_objs)

