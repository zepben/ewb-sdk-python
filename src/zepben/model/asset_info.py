from zepben.model.identified_object import IdentifiedObject
from zepben.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind
from zepben.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.cim.iec61970.base.domain.CurrentFlow_pb2 import CurrentFlow as PBCurrentFlow


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
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = ""):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci):
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
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = ""):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci):
        """
        Convert a Protobuf OverheadWireInfo
        :param pb_ci: :class:`zepben.cim.iec61968.assetinfo.OverheadWireInfo`
        :return: A CableInfo
        """
        return OverheadWireInfo(mrid=pb_ci.mRID, rated_current=CurrentFlow.from_pb(pb_ci.ratedCurrent), material=pb_ci.material, name=pb_ci.name)

    def to_pb(self):
        args = self._pb_args()
        return PBOverheadWireInfo(**args)


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
    def from_pb(pb_cf):
        return CurrentFlow(pb_cf.value)


class TransformerEndInfo(AssetInfo):
    """
    TODO: Implement
    """
    def __init__(self, mrid, name: str = ""):
        super().__init__(mrid, name)

    @staticmethod
    def from_pb(pb_te):
        """
        Convert a Protobuf TransformerEndInfo. Currently Unused.
        :param pb_ci: :class:`zepben.cim.iec61968.assetinfo.TransformerEndInfo`
        :return: A TransformerEndInfo
        """
        raise NotImplementedError()
