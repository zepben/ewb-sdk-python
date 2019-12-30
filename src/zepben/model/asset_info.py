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


from zepben.model.identified_object import IdentifiedObject
from zepben.model.exceptions import NoAssetInfoException
from zepben.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind
from zepben.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.cim.iec61970.base.domain.CurrentFlow_pb2 import CurrentFlow as PBCurrentFlow


class CurrentFlow(object):
    """
    Electrical current with sign convention: positive flow is out of the conducting equipment into the connectivity
    node. Can be both AC and DC.

    Attributes :
        value : The rate of current.
    """
    def __init__(self, value):
        self.value = value

    def to_pb(self):
        return PBCurrentFlow(value=self.value)

    @staticmethod
    def from_pb(pb_cf, **kwargs):
        return CurrentFlow(pb_cf.value)


class AssetInfo(IdentifiedObject):
    """
    Set of attributes of an asset, representing typical datasheet information of a physical device that can be
    instantiated and shared in different data exchange contexts:
        - as attributes of an asset instance (installed or in stock)
        - as attributes of an asset model (product by a manufacturer)
        - as attributes of a type asset (generic type of an asset as used in designs/extension planning).
    """
    def __init__(self, mrid, name):
        super().__init__(mrid, name)

    @staticmethod
    def from_pb(pb_ai, **kwargs):
        if pb_ai.HasField("cableInfo"):
            return CableInfo.from_pb(pb_ai.cableInfo)
        elif pb_ai.HasField("overheadWireInfo"):
            return OverheadWireInfo.from_pb(pb_ai.overheadWireInfo)
        elif pb_ai.HasField("transformerEndInfo"):
            return TransformerEndInfo.from_pb(pb_ai.transformerEndInfo)
        else:
            raise NoAssetInfoException("assetInfo was empty")


class WireInfo(AssetInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics

    Attributes:
        rated_current : Current carrying capacity of the wire under stated thermal conditions.
        material : :class:`zepben.cim.iec61968.assetinfo.WireMaterialKind` - Conductor material.
    """
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = ""):
        self.rated_current = rated_current
        self.material = material
        super().__init__(mrid, name)


class CableInfo(WireInfo):
    """
    Cable data. A cable is an underground conductor.
    """
    def __init__(self, mrid, rated_current: CurrentFlow = None, material: WireMaterialKind = WireMaterialKind.UNKNOWN, name: str = ""):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci, **kwargs):
        """
        Convert a Protobuf CableInfo
        :param pb_ci: :class:`zepben.cim.iec61968.assetinfo.CableInfo`
        :return: A CableInfo
        """
        return CableInfo(mrid=pb_ci.mRID, rated_current=CurrentFlow.from_pb(pb_ci.ratedCurrent), material=pb_ci.material, name=pb_ci.name)

    def to_pb(self):
        args = self._pb_args()
        return PBCableInfo(**args)


class OverheadWireInfo(WireInfo):
    """
    Overhead wire data. A "wire" is an above ground conductor.
    """
    def __init__(self, mrid, rated_current: CurrentFlow = None, material: WireMaterialKind = WireMaterialKind.UNKNOWN, name: str = ""):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci, **kwargs):
        """
        Convert a Protobuf OverheadWireInfo
        :param pb_ci: :class:`zepben.cim.iec61968.assetinfo.OverheadWireInfo`
        :return: A CableInfo
        """
        return OverheadWireInfo(mrid=pb_ci.mRID, rated_current=CurrentFlow.from_pb(pb_ci.ratedCurrent), material=pb_ci.material, name=pb_ci.name)

    def to_pb(self):
        args = self._pb_args()
        return PBOverheadWireInfo(**args)




class TransformerEndInfo(AssetInfo):
    """
    TODO: Implement
    """
    def __init__(self, mrid, name: str = ""):
        super().__init__(mrid, name)

    @staticmethod
    def from_pb(pb_te, **kwargs):
        """
        Convert a Protobuf TransformerEndInfo. Currently Unused.
        :param pb_ci: :class:`zepben.cim.iec61968.assetinfo.TransformerEndInfo`
        :return: A TransformerEndInfo
        """
        raise NotImplementedError()
