#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import zepben.cimbend.common
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram
from zepben.cimbend.diagram.translator.diagram_proto2cim import *
from zepben.cimbend.diagram.translator.diagram_cim2proto import *

__all__ = []


Diagram.mrid = lambda self: self.io.mRID
DiagramObject.mrid = lambda self: self.io.mRID
