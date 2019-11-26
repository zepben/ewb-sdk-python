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


from zepben.cim.iec61970 import EnergySource as PBEnergySource
from zepben.model.terminal import Terminal
from zepben.model.equipment import ConductingEquipment
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from typing import List


class EnergySource(ConductingEquipment):
    def __init__(self, mrid: str, active_power: float = 0.0, r: float = 0.0, x: float = 0.0, base_voltage: BaseVoltage = BV_UNKNOWN,
                 reactive_power: float = 0.0, voltage_angle: float = 0.0, voltage_magnitude: float = 0.0,
                 in_service: bool = True, name: str = "", terminals: List = None,
                 diag_objs: List[DiagramObject] = None, location: Location = None):
        self.active_power = active_power
        self.r = r
        self.x = x
        self.reactive_power = reactive_power
        self.voltage_angle = voltage_angle
        self.voltage_magnitude = voltage_magnitude
        super().__init__(mrid, in_service, base_voltage, name, terminals, diag_objs, location)

    def __str__(self):
        return f"{super().__str__()} active_power: {self.active_power}, r: {self.r}, x: {self.x}, reactive_power: {self.reactive_power}, voltage_angle: {self.voltage_angle}, voltage_mag: {self.voltage_magnitude}"

    def __repr__(self):
        return f"{super().__repr__()} active_power: {self.active_power}, r: {self.r}, x: {self.x}, reactive_power: {self.reactive_power}, voltage_angle: {self.voltage_angle}, voltage_mag: {self.voltage_magnitude}"

    def to_pb(self):
        args = self._pb_args()
        return PBEnergySource(**args)

    @staticmethod
    def from_pb(pb_es, network):
        """
        Convert a protobuf EnergySource to a :class:`zepben.model.EnergySource`
        :param pb_es: :class:`zepben.cim.iec61970.base.wires.EnergySource`
        :param network: EquipmentContainer to extract BaseVoltage
        :raises: NoBaseVoltageException when BaseVoltage isn't found in network
        :return: A :class:`zepben.model.EnergySource`
        """
        terms = Terminal.from_pbs(pb_es.terminals, network)
        location = Location.from_pb(pb_es.location)
        diag_objs = DiagramObject.from_pbs(pb_es.diagramObjects)
        base_voltage = network.get_base_voltage(pb_es.baseVoltageMRID)
        return EnergySource(mrid=pb_es.mRID,
                            name=pb_es.name,
                            active_power=pb_es.activePower,
                            r=pb_es.r,
                            x=pb_es.x,
                            base_voltage=base_voltage,
                            reactive_power=pb_es.reactivePower,
                            voltage_angle=pb_es.voltageAngle,
                            voltage_magnitude=pb_es.voltageMagnitude,
                            in_service=pb_es.inService,
                            terminals=terms,
                            diag_objs=diag_objs,
                            location=location)


