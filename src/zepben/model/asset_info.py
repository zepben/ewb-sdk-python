from zepben.model.identified_object import IdentifiedObject
from zepben.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind
from zepben.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.cim.iec61970.base.domain.CurrentFlow_pb2 import CurrentFlow as PBCurrentFlow


class AssetInfo(IdentifiedObject):
    def __init__(self, mrid, name):
        super().__init__(mrid, name)


class WireInfo(AssetInfo):
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = None):
        self.rated_current = rated_current
        self.material = material
        super().__init__(mrid, name)


class CableInfo(WireInfo):
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = None):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci):
        return CableInfo(mrid=pb_ci.mRID, rated_current=CurrentFlow.from_pb(pb_ci.ratedCurrent), material=pb_ci.material, name=pb_ci.name)

    def to_pb(self):
        args = self._pb_args()
        return PBCableInfo(**args)


class OverheadWireInfo(WireInfo):
    def __init__(self, mrid, rated_current, material: WireMaterialKind, name: str = None):
        super().__init__(mrid, rated_current, material, name)

    @staticmethod
    def from_pb(pb_ci):
        return OverheadWireInfo(mrid=pb_ci.mRID, rated_current=CurrentFlow.from_pb(pb_ci.ratedCurrent), material=pb_ci.material, name=pb_ci.name)

    def to_pb(self):
        args = self._pb_args()
        return PBOverheadWireInfo(**args)


class CurrentFlow(object):
    def __init__(self, value):
        self.value = value

    def to_pb(self):
        return PBCurrentFlow(value=self.value)

    @staticmethod
    def from_pb(pb_cf):
        return CurrentFlow(pb_cf.value)


class TransformerEndInfo(AssetInfo):
    def __init__(self, mrid, name: str = None):
        super().__init__(mrid, name)

    @staticmethod
    def from_pb(pb_te):
        raise NotImplementedError()
