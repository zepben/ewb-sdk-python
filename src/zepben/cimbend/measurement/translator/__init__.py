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


from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource
from zepben.cimbend.measurement.translator.measurement_proto2cim import *
import zepben.cimbend.common

__all__ = ["measurement_proto2cim.py"]

Control.mrid = lambda self: self.ip.mrid()
IoPoint.mrid = lambda self: self.io.mRID
Measurement.mrid = lambda self: self.io.mRID
RemoteControl.mrid = lambda self: self.rp.mrid()
RemotePoint.mrid = lambda self: self.io.mRID
RemoteSource.mrid = lambda self: self.rp.mrid()

