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


from zepben.cim.iec61970 import PhaseShuntConnectionKind, SinglePhaseKind, EnergyConsumer as PBEnergyConsumer, EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.model.equipment import ConductingEquipment
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.identified_object import IdentifiedObject
from typing import List


class EnergyConsumerPhase(IdentifiedObject):
    def __init__(self, pfixed: float, qfixed: float, phase: SinglePhaseKind, mrid: str = None, name: str = None,
                 diag_objs: List[DiagramObject] = None):
        self.pfixed = pfixed
        self.qfixed = qfixed
        self.phase = phase
        super().__init__(mrid, name, diag_objs)

    def to_pb(self):
        return PBEnergyConsumerPhase(**self._pb_args())


class EnergyConsumer(ConductingEquipment):
    def __init__(self, mrid: str, p: float = None, q: float = None, in_service: bool = True, base_voltage: BaseVoltage = BV_UNKNOWN,
                 phs_shunt_conn_kind: PhaseShuntConnectionKind = None, ecp: List[EnergyConsumerPhase] = None, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        self.p = p
        self.q = q
        self.phaseConnection = phs_shunt_conn_kind
        self.energy_consumer_phases = ecp
        super().__init__(mrid, in_service, base_voltage, name, terminals, diag_objs, location)

    def __str__(self):
        return f"{super().__str__()} p: {self.p}, q: {self.q}"

    def __repr__(self):
        return f"{super().__repr__()} p: {self.p}, q: {self.q}"

    def to_pb(self):
        args = self._pb_args()
        return PBEnergyConsumer(**args)
