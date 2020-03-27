from __future__ import annotations
from zepben.model.power_system_resource import PowerSystemResource
from typing import List


class ConnectivityNodeContainer(PowerSystemResource):
    """
    This class is currently unused in our CIM profile, but may be extended in the future
    """
    def __init__(self, mrid: str, name: str = "", diag_objs: List[DiagramObject] = None, location: Location = None):
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs, location=location)

