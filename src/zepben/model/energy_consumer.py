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


from zepben.cim.IEC61970.wires_pb2 import PhaseShuntConnectionKind, SinglePhaseKind, EnergyConsumer as PBEnergyConsumer, EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.model.equipment import ConductingEquipment
from zepben.model.diagram_layout import DiagramObjectPoints
from zepben.model.common import PositionPoints
from zepben.model.identified_object import IdentifiedObject
from typing import Set, List


class EnergyConsumerPhase(IdentifiedObject):
    def __init__(self, pfixed: float, qfixed: float, phase: SinglePhaseKind, mrid: str = None, name: str = None,
                 desc: str = None, diag_points: DiagramObjectPoints = None):
        self.pfixed = pfixed
        self.qfixed = qfixed
        self.phase = phase
        super().__init__(mrid, name, diag_points, desc)

    def to_pb(self):
        return PBEnergyConsumerPhase(**self._pb_args())


class EnergyConsumer(ConductingEquipment):
    def __init__(self, mrid: str, p: float = None, q: float = None, in_service: bool = True, nom_volts: float = 0.0,
                 phs_shunt_conn_kind: PhaseShuntConnectionKind = None, ecp: List[EnergyConsumerPhase] = None, name: str = "", description: str = "",
                 terminals: Set = None, diag_point: DiagramObjectPoints = None, pos_points: PositionPoints = None):
        self.p = p
        self.q = q
        self.connection_kind = phs_shunt_conn_kind
        self.energy_consumer_phase = ecp
        super().__init__(mrid, in_service, nom_volts, name, description, terminals, diag_point, pos_points)

    def __str__(self):
        return f"{super().__str__()} p: {self.p}, q: {self.q}"

    def __repr__(self):
        return f"{super().__repr__()} p: {self.p}, q: {self.q}"

    def to_pb(self):
        args = self._pb_args()
        return PBEnergyConsumer(**args)
