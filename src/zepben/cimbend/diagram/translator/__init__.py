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


import zepben.cimbend.common
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram
from zepben.cimbend.diagram.translator.diagram_proto2cim import *

__all__ = ["diagram_proto2cim.py"]


Diagram.mrid = lambda self: self.io.mRID
DiagramObject.mrid = lambda self: self.io.mRID
