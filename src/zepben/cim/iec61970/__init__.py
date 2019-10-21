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

from zepben.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import *
from zepben.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2_grpc import *
from zepben.cim.iec61970.base.core.BaseVoltage_pb2 import *
from zepben.cim.iec61970.base.core.BaseVoltage_pb2_grpc import *
from zepben.cim.iec61970.base.core.ConnectivityNode_pb2 import *
from zepben.cim.iec61970.base.core.ConnectivityNode_pb2_grpc import *
from zepben.cim.iec61970.base.core.EquipmentContainer_pb2 import *
from zepben.cim.iec61970.base.core.EquipmentContainer_pb2_grpc import *
from zepben.cim.iec61970.base.core.Feeder_pb2 import *
from zepben.cim.iec61970.base.core.Feeder_pb2_grpc import *
from zepben.cim.iec61970.base.core.GeographicalRegion_pb2 import *
from zepben.cim.iec61970.base.core.GeographicalRegion_pb2_grpc import *
from zepben.cim.iec61970.base.core.SubGeographicalRegion_pb2 import *
from zepben.cim.iec61970.base.core.SubGeographicalRegion_pb2_grpc import *
from zepben.cim.iec61970.base.core.PhaseCode_pb2 import *
from zepben.cim.iec61970.base.core.PhaseCode_pb2_grpc import *
from zepben.cim.iec61970.base.core.Substation_pb2 import *
from zepben.cim.iec61970.base.core.Substation_pb2_grpc import *
from zepben.cim.iec61970.base.core.Terminal_pb2 import *
from zepben.cim.iec61970.base.core.Terminal_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.Diagram_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.Diagram_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObject_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObjectStyle_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.DiagramObjectStyle_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.DiagramStyle_pb2_grpc import *
from zepben.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import *
from zepben.cim.iec61970.base.diagramlayout.OrientationKind_pb2_grpc import *
from zepben.cim.iec61970.base.domain.CurrentFlow_pb2 import *
from zepben.cim.iec61970.base.domain.CurrentFlow_pb2_grpc import *
from zepben.cim.iec61970.base.domain.Voltage_pb2 import *
from zepben.cim.iec61970.base.domain.Voltage_pb2_grpc import *
from zepben.cim.iec61970.base.meas.Control_pb2 import *
from zepben.cim.iec61970.base.meas.Control_pb2_grpc import *
from zepben.cim.iec61970.base.meas.Measurement_pb2 import *
from zepben.cim.iec61970.base.meas.Measurement_pb2_grpc import *
from zepben.cim.iec61970.base.meas.MeasurementValue_pb2 import *
from zepben.cim.iec61970.base.meas.MeasurementValue_pb2_grpc import *
from zepben.cim.iec61970.base.scada.RemoteControl_pb2 import *
from zepben.cim.iec61970.base.scada.RemoteControl_pb2_grpc import *
from zepben.cim.iec61970.base.scada.RemoteSource_pb2 import *
from zepben.cim.iec61970.base.scada.RemoteSource_pb2_grpc import *
from zepben.cim.iec61970.base.wires.EnergySource_pb2 import *
from zepben.cim.iec61970.base.wires.EnergySource_pb2_grpc import *
from zepben.cim.iec61970.base.wires.AcLineSegment_pb2 import *
from zepben.cim.iec61970.base.wires.AcLineSegment_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Breaker_pb2 import *
from zepben.cim.iec61970.base.wires.Breaker_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Direction_pb2 import *
from zepben.cim.iec61970.base.wires.Direction_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Disconnector_pb2 import *
from zepben.cim.iec61970.base.wires.Disconnector_pb2_grpc import *
from zepben.cim.iec61970.base.wires.EnergyConsumer_pb2 import *
from zepben.cim.iec61970.base.wires.EnergyConsumer_pb2_grpc import *
from zepben.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import *
from zepben.cim.iec61970.base.wires.EnergyConsumerPhase_pb2_grpc import *
from zepben.cim.iec61970.base.wires.EnergySourcePhase_pb2 import *
from zepben.cim.iec61970.base.wires.EnergySourcePhase_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Fuse_pb2 import *
from zepben.cim.iec61970.base.wires.Fuse_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Jumper_pb2 import *
from zepben.cim.iec61970.base.wires.Jumper_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Junction_pb2 import *
from zepben.cim.iec61970.base.wires.Junction_pb2_grpc import *
from zepben.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import *
from zepben.cim.iec61970.base.wires.LinearShuntCompensator_pb2_grpc import *
from zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import *
from zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2_grpc import *
from zepben.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import *
from zepben.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2_grpc import *
from zepben.cim.iec61970.base.wires.PowerTransformer_pb2 import *
from zepben.cim.iec61970.base.wires.PowerTransformer_pb2_grpc import *
from zepben.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import *
from zepben.cim.iec61970.base.wires.PowerTransformerEnd_pb2_grpc import *
from zepben.cim.iec61970.base.wires.RatioTapChanger_pb2 import *
from zepben.cim.iec61970.base.wires.RatioTapChanger_pb2_grpc import *
from zepben.cim.iec61970.base.wires.Recloser_pb2 import *
from zepben.cim.iec61970.base.wires.Recloser_pb2_grpc import *
from zepben.cim.iec61970.base.wires.SinglePhaseKind_pb2 import *
from zepben.cim.iec61970.base.wires.SinglePhaseKind_pb2_grpc import *
from zepben.cim.iec61970.base.wires.VectorGroup_pb2 import *
from zepben.cim.iec61970.base.wires.VectorGroup_pb2_grpc import *
from zepben.cim.iec61970.base.wires.WindingConnection_pb2 import *
from zepben.cim.iec61970.base.wires.WindingConnection_pb2_grpc import *
