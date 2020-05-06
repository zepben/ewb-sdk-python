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


from dataclasses import dataclass

from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource

from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.cim.iec61970.base.meas.iopoint import IoPoint
from zepben.cimbend.cim.iec61970 import Control
from zepben.cimbend.cim.iec61970 import Measurement
from zepben.cimbend.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.cimbend.cim.iec61970 import RemotePoint
from zepben.cimbend.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.cimbend.measurement.measurements import MeasurementService

__all__ = ["MeasurementProtoToCim", "set_remotepoint", "set_iopoint"]


def set_iopoint(pb: PBIoPoint, cim: IoPoint):
    set_identifiedobject(pb.io, cim)


def set_remotepoint(pb: PBRemotePoint, cim: RemotePoint):
    set_identifiedobject(pb.io, cim)


@dataclass
class MeasurementProtoToCim(BaseProtoToCim):
    service: MeasurementService

    def add_control(self, pb: PBControl):
        cim = Control(pb.mrid())
        set_iopoint(pb.ip, cim)
        cim.remote_control = self._ensure_get(pb.remoteControlMRID, RemoteControl, cim)
        self.service.add(cim)

    def add_measurement(self, pb: PBMeasurement):
        cim = Measurement(pb.mrid())
        set_identifiedobject(pb.io, cim)
        cim.remote_source = self._ensure_get(pb.remoteSourceMRID, RemoteSource, cim)
        self.service.add(cim)

    def add_remotecontrol(self, pb: PBRemoteControl):
        cim = RemoteControl(pb.mrid())
        set_remotepoint(pb.rp, cim)
        self.service.add(cim)

    def add_remotesource(self, pb: PBRemoteSource):
        cim = RemoteSource(pb.mrid())
        set_remotepoint(pb.rp, cim)
        self.service.add(cim)