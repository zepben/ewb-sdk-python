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
from zepben.model.diagram_layout import DiagramObjectPoints
from zepben.model.common import PositionPoints
from zepben.cim.IEC61970.winding.winding_pb2 import WindingConnection
from zepben.cim.IEC61970.wires_pb2 import PowerTransformer as PBPowerTransformer, PowerTransformerEnd as PBPowerTransformerEnd, \
    RatioTapChanger as PBRatioTabChanger
from google.protobuf.field_mask_pb2 import FieldMask
from typing import Set


class InvalidTransformerError(Exception):
    pass


class RatioTapChanger(IdentifiedObject):
    def __init__(self, high_step: float = 0.0, low_step: float = 0.0, step: float = 0.0, step_voltage_increment: float = 0.0,
                 mrid: str = None, name: str = None, desc: str = None, diag_points: DiagramObjectPoints = None):
        self.high_step = high_step
        self.low_step = low_step
        self.step = step
        self.step_voltage_increment = step_voltage_increment
        super().__init__(mrid, name, diag_points, desc)

    def to_pb(self):
        args = self._pb_args()
        return PBRatioTabChanger(**args)


class PowerTransformerEnd(IdentifiedObject):
    def __init__(self, rated_s: float = None, rated_u: float = None, r: float = None, x: float = None, r0: float = None,
                 x0: float = None, winding: WindingConnection = None, terminals: Set = None, end_number: int = 0,
                 tap_changer: RatioTapChanger = None, mrid: str = None, name: str = None, desc: str = None,
                 diag_points: DiagramObjectPoints = None):
        self.rated_s = rated_s
        self.rated_u = rated_u
        self.r = r
        self.x = x
        self.r0 = r0
        self.x0 = x0
        self.connection_kind = winding
        self.terminals = terminals
        self.end_number = end_number
        self.tap_changer = tap_changer
        super().__init__(mrid, name, diag_points, desc)

    def has_tap_changer(self):
        return self.tap_changer is not None

    def get_tap_changer_step(self):
        if self.has_tap_changer():
            return self.tap_changer.step

    def _pb_args(self):
        """
        Temporary override to add in mask
        :return:
        """
        args = super()._pb_args()
        # TODO: This can be moved to IdentifiedObject if we mandate mask on all messages
        args["mask"] = FieldMask(paths=args.keys())
        return args

    def to_pb(self):
        args = self._pb_args()
        return PBPowerTransformerEnd(**args)


class PowerTransformer(ConductingEquipment):

    def __init__(self, mrid: str, vector_group: float = None, in_service: bool = True, name: str = "",
                 description: str = "", terminals: Set = None, diag_point: DiagramObjectPoints = None,
                 pos_points: PositionPoints = None):
        """
        :param mrid:
        :param vector_group:  TODO: change to vector?
        :param in_service:
        """
        self.vector_group = vector_group
        self.ends = []

        super().__init__(mrid, in_service, None, name, description, terminals, diag_point, pos_points)

    def add_end(self, end: PowerTransformerEnd):
        for e in self.ends:
            if e.end_number == end.end_number:
                raise InvalidTransformerError(f"Transformer {self.mrid} already has an end with number {e.end_number}")
        else:
            self.ends.append(end)

    def get_end(self, end_number: int):
        for end in self.ends:
            if end.end_number == end_number:
                return end
        else:
            raise InvalidTransformerError(f"Transformer {self.mrid} does not have end {end_number}")

    @property
    def endCount(self):
        return len(self.ends)

    def __str__(self):
        return f"{super().__str__()} vector_group: {self.vector_group}"

    def __repr__(self):
        return f"{super().__repr__()} vector_group: {self.vector_group}"

    def _pb_args(self):
        """
        Temporary
        # TODO: This can be moved to IdentifiedObject if we mandate mask on all messages
        :return:
        """
        args = super()._pb_args()
        args["mask"] = FieldMask(paths=args.keys())

        return args

    def to_pb(self):
        args = self._pb_args()
        return PBPowerTransformer(**args)
