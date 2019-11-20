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


from zepben.model.identified_object import IdentifiedObject
from zepben.model.equipment import ConductingEquipment
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.cim.iec61970 import PowerTransformer as PBPowerTransformer, PowerTransformerEnd as PBPowerTransformerEnd, \
    RatioTapChanger as PBRatioTabChanger, WindingConnection
from zepben.cim.iec61970 import VectorGroup
from typing import List


class InvalidTransformerError(Exception):
    pass


class RatioTapChanger(IdentifiedObject):
    def __init__(self, high_step: float = 0.0, low_step: float = 0.0, step: float = 0.0, step_voltage_increment: float = 0.0,
                 mrid: str = None, name: str = None, diag_objs: List[DiagramObject] = None):
        self.high_step = high_step
        self.low_step = low_step
        self.step = step
        self.step_voltage_increment = step_voltage_increment
        super().__init__(mrid, name, diag_objs)

    def to_pb(self):
        args = self._pb_args()
        return PBRatioTabChanger(**args)


class PowerTransformerEnd(IdentifiedObject):
    def __init__(self, rated_s: float = None, rated_u: float = None, r: float = None, x: float = None, r0: float = None,
                 x0: float = None, winding: WindingConnection = None, tap_changer: RatioTapChanger = None,
                 mrid: str = None, name: str = None, diag_objs: List[DiagramObject] = None):
        """
        :param rated_s:
        :param rated_u:
        :param r:
        :param x:
        :param r0:
        :param x0:
        :param winding:
        :param tap_changer:
        :param mrid:
        :param name:
        :param desc:
        :param diag_objs:
        """
        self.rated_s = rated_s
        self.rated_u = rated_u
        self.r = r
        self.x = x
        self.r0 = r0
        self.x0 = x0
        self.connection_kind = winding
        self.ratio_tap_changer = tap_changer
        super().__init__(mrid, name, diag_objs)

    def has_tap_changer(self):
        return self.ratio_tap_changer is not None

    def get_tap_changer_step(self):
        if self.has_tap_changer():
            return self.ratio_tap_changer.step

    def to_pb(self):
        args = self._pb_args()
        return PBPowerTransformerEnd(**args)


class PowerTransformer(ConductingEquipment):

    def __init__(self, mrid: str, vector_group: VectorGroup = None, in_service: bool = True, name: str = "",
                 ends: List[PowerTransformerEnd] = None, terminals: List = None, diag_objs: List[DiagramObject] = None,
                 location: Location = None):
        """
        :param mrid:
        :param vector_group:
        :param in_service:
        """
        self.vector_group = vector_group
        self.powerTransformerEnds = ends if ends is not None else []

        super().__init__(mrid, in_service, None, name, terminals, diag_objs, location)

    def add_end(self, end: PowerTransformerEnd):
        self.powerTransformerEnds.append(end)

    def get_end(self, end_number: int):
        return self.powerTransformerEnds[end_number]

    def get_nominal_voltage(self, terminal=None):
        """
        Return nominal voltage, ideally corresponding to a specific terminal.
        :param terminal:
        :return: Nominal voltage of the PowerTransformerEnd corresponding to the terminal,
                 or potentially None if no terminal is specified
        """
        if terminal is None:
            return self.nominal_voltage
        else:
            for i, term in enumerate(self.terminals):
                if term is terminal:
                    return self.get_end(i).rated_u
        raise NoSuchEquipmentException(f"PowerTransformer {self.mrid} had no terminal {terminal.mrid}")

    @property
    def end_count(self):
        return len(self.powerTransformerEnds)

    def __str__(self):
        return f"{super().__str__()} vector_group: {self.vector_group}"

    def __repr__(self):
        return f"{super().__repr__()} vector_group: {self.vector_group}"

    def to_pb(self):
        args = self._pb_args()
        return PBPowerTransformer(**args)
