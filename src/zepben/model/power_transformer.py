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
from zepben.model.terminal import Terminal
from zepben.model.identified_object import IdentifiedObject
from zepben.model.equipment import ConductingEquipment, PowerSystemResource
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.exceptions import NoTerminalException
from zepben.cim.iec61970 import PowerTransformer as PBPowerTransformer, PowerTransformerEnd as PBPowerTransformerEnd, \
    RatioTapChanger as PBRatioTabChanger, WindingConnection
from zepben.cim.iec61970 import VectorGroup
from typing import List


class InvalidTransformerError(Exception):
    pass


class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.

    Attributes:
        high_step : Highest possible tap step position, advance from neutral. The attribute shall be greater than lowStep.
        low_step : Lowest possible tap step position, retard from neutral
        step : Tap changer position. Starting step for a steady state solution. Non integer values are allowed to
               support continuous tap variables.
               The reasons for continuous value are to support study cases where no discrete tap changers has yet been
               designed, a solutions where a narrow voltage band force the tap step to oscillate or accommodate for a
               continuous solution as input.
               The attribute shall be equal or greater than lowStep and equal or less than highStep.
    """
    def __init__(self, high_step: float = 0.0, low_step: float = 0.0, step: float = 0.0, mrid: str = "", name: str = "",
                 diag_objs: List[DiagramObject] = None):
        """
        Create a TapChanger
        :param high_step: Highest possible tap step position, advance from neutral. Must be greater than lowStep.
        :param low_step: Lowest possible tap step position, retard from neutral
        :param step: Tap changer position. Starting step for a steady state solution. Non integer values are allowed to
                     support continuous tap variables. Must be >= low_step and <= high_step.
        :param mrid: mRID for this object. Optional and not typically used.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs)
        if high_step < low_step:
            raise InvalidTransformerError(f"high_step ({high_step}) for TapChanger {mrid} must be greater than low_step ({low_step})")
        self.high_step = high_step
        self.low_step = low_step
        self.step = step


class RatioTapChanger(TapChanger):
    """
    A tap changer that changes the voltage ratio impacting the voltage magnitude but not the phase angle across the
    transformer.

    Attributes:
        step_voltage_increment : Tap step increment, in per cent of neutral voltage, per step position.
    """
    def __init__(self, high_step: float = 0.0, low_step: float = 0.0, step: float = 0.0, step_voltage_increment: float = 0.0,
                 mrid: str = "", name: str = "", diag_objs: List[DiagramObject] = None):
        """
        Create a RatioTapChanger
        :param high_step: Highest possible tap step position, advance from neutral. Must be greater than lowStep.
        :param low_step: Lowest possible tap step position, retard from neutral
        :param step: Tap changer position. Starting step for a steady state solution. Non integer values are allowed to
                     support continuous tap variables. Must be >= low_step and <= high_step.
        :param step_voltage_increment: Tap step increment, in percent of neutral voltage, per step position.
        :param mrid: mRID for this object. Optional and not typically used.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.step_voltage_increment = step_voltage_increment
        super().__init__(mrid=mrid, high_step=high_step, low_step=low_step, step=step, name=name, diag_objs=diag_objs)

    def to_pb(self):
        args = self._pb_args()
        return PBRatioTabChanger(**args)

    @staticmethod
    def from_pb(pb_rtc):
        """
        Convert a :class:`zepben.cim.iec61970.base.wires.RatioTapChanger`
        :param pb_rtc: :class:`zepben.cim.iec61970.base.wires.RatioTapChanger`
        :return: :class:`RatioTapChanger`
        """
        return RatioTapChanger(high_step=pb_rtc.highStep, low_step=pb_rtc.lowStep, step=pb_rtc.step,
                               step_voltage_increment=pb_rtc.stepVoltageIncrement)


class PowerTransformerEnd(IdentifiedObject):
    """
    A PowerTransformerEnd is associated with each Terminal of a PowerTransformer.
    The impedance values r, r0, x, and x0 of a PowerTransformerEnd represents a star equivalent as follows
    1) for a two Terminal PowerTransformer the high voltage PowerTransformerEnd has non zero values on r, r0, x, and x0
    while the low voltage PowerTransformerEnd has zero values for r, r0, x, and x0.
    2) for a three Terminal PowerTransformer the three PowerTransformerEnds represents a star equivalent with each leg
    in the star represented by r, r0, x, and x0 values.
    3) for a PowerTransformer with more than three Terminals the PowerTransformerEnd impedance values cannot be used.
    Instead use the TransformerMeshImpedance or split the transformer into multiple PowerTransformers.

    Attributes:
        rated_s : Normal apparent power rating.
                  The attribute shall be a positive value. For a two-winding transformer the values for the high and
                  low voltage sides shall be identical.
        rated_u : Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for
                  single-phase windings. A high voltage side, as given by TransformerEnd.endNumber, shall have a ratedU
                  that is greater or equal than ratedU for the lower voltage sides.
        r : Resistance (star-model) of the transformer end. The attribute shall be equal or greater than zero
            for non-equivalent transformers.
        x : Positive sequence series reactance (star-model) of the transformer end.
        r0 : Zero sequence series resistance (star-model) of the transformer end.
        x0 : Zero sequence series reactance of the transformer end.
        connection_kind : Kind of :class:`zepben.cim.iec61970.base.wires.WindingConnection` for this end.
        ratio_tap_changer : :class:`RatioTapChanger` attached to this end.
    """
    def __init__(self, rated_s: float = None, rated_u: float = None, r: float = None, x: float = None, r0: float = None,
                 x0: float = None, winding: WindingConnection = None, tap_changer: RatioTapChanger = None,
                 mrid: str = "", name: str = "", diag_objs: List[DiagramObject] = None):
        """
        Create a PowerTransformerEnd
        :param rated_s: Normal apparent power rating.
                        The attribute shall be a positive value. For a two-winding transformer the values for the high and
                        low voltage sides shall be identical.
        :param rated_u: Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for
                        single-phase windings. A high voltage side, as given by TransformerEnd.endNumber, shall have a ratedU
                        that is greater or equal than ratedU for the lower voltage sides.
        :param r: Resistance (star-model) of the transformer end. The attribute shall be equal or greater than zero
                  for non-equivalent transformers.
        :param x: Positive sequence series reactance (star-model) of the transformer end.
        :param r0: Zero sequence series resistance (star-model) of the transformer end.
        :param x0: Zero sequence series reactance of the transformer end.
        :param winding: Kind of :class:`zepben.cim.iec61970.base.wires.WindingConnection` for this end.
        :param tap_changer: :class:`RatioTapChanger` attached to this end.
        :param mrid: mRID for this object. Optional and not typically used.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
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

    @staticmethod
    def from_pb(pb_tfe):
        """
        Convert a :class:`zepben.cim.iec61970.base.wires.PowerTransformerEnd`
        :param pb_rtc: :class:`zepben.cim.iec61970.base.wires.PowerTransformerEnd`
        :return: :class:`PowerTransformerEnd`
        """
        tap_changer = RatioTapChanger.from_pb(pb_tfe.ratioTapChanger)
        return PowerTransformerEnd(rated_s=pb_tfe.ratedS, rated_u=pb_tfe.ratedU, r=pb_tfe.r, x=pb_tfe.x, r0=pb_tfe.r0,
                                   x0=pb_tfe.x0, winding=pb_tfe.connectionKind, tap_changer=tap_changer)


class PowerTransformer(ConductingEquipment):
    """
    An electrical device consisting of  two or more coupled windings, with or without a magnetic core, for introducing
    mutual coupling between electric circuits.
    Transformers can be used to control voltage and phase shift (active power flow).
    A power transformer may be composed of separate transformer tanks that need not be identical.
    A power transformer can be modeled with or without tanks and is intended for use in both balanced and
    unbalanced representations.
    A power transformer typically has two terminals, but may have one (grounding), three or more terminals.
    The inherited association ConductingEquipment.BaseVoltage should not be used.
    The association from TransformerEnd to BaseVoltage should be used instead.

    Attributes:
        vector_group : :class:`zepben.cim.iec61970.base.wires.VectorGroup` of the transformer for protective relaying.
        power_transformer_ends : A list of the :class:`PowerTransformerEnd` for each winding in this Transformer.
                                 The ordering of the list is important, and reflects which
                                 :class:`zepben.model.Terminal` each end is associated with.
    """
    def __init__(self, mrid: str, ends: List[PowerTransformerEnd], vector_group: VectorGroup = VectorGroup.UNKNOWN,
                 in_service: bool = True, name: str = "", terminals: List = None, diag_objs: List[DiagramObject] = None,
                 location: Location = None):
        """
        Create a PowerTransformer
        :param mrid: mRID for this object
        :param vector_group: :class:`zepben.cim.iec61970.base.wires.VectorGroup` of the transformer for protective relaying
        :param in_service: If True, the equipment is in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param ends: A list of the :class:`PowerTransformerEnd` for each winding in this Transformer.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        """
        self.vector_group = vector_group
        self.power_transformer_ends = ends if ends is not None else []

        super().__init__(mrid=mrid, base_voltage=None, in_service=in_service, name=name,
                         terminals=terminals, diag_objs=diag_objs, location=location)

    def add_end(self, end: PowerTransformerEnd):
        self.power_transformer_ends.append(end)

    def get_end(self, end_number: int):
        return self.power_transformer_ends[end_number]

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
        raise NoTerminalException(f"PowerTransformer {self.mrid} had no terminal {terminal.mrid}")

    @property
    def end_count(self):
        return len(self.power_transformer_ends)

    def __str__(self):
        return f"{super().__str__()} vector_group: {self.vector_group}"

    def __repr__(self):
        return f"{super().__repr__()} vector_group: {self.vector_group}"

    def to_pb(self):
        args = self._pb_args()
        return PBPowerTransformer(**args)

    @staticmethod
    def from_pb(pb_tf, network):
        """
        Convert a protobuf PowerTransformer to a :class:`zepben.model.PowerTransformer`
        :param pb_tf: :class:`zepben.cim.iec61970.base.wires.PowerTransformer`
        :param network: EquipmentContainer associated with this transformer.
        :return: A :class:`zepben.model.PowerTransformer`
        """
        terms = Terminal.from_pbs(pb_tf.terminals, network)
        location = Location.from_pb(pb_tf.location)
        diag_objs = DiagramObject.from_pbs(pb_tf.diagramObjects)
        ends = PowerTransformerEnd.from_pbs(pb_tf.powerTransformerEnds)
        return PowerTransformer(mrid=pb_tf.mRID,
                                name=pb_tf.name,
                                vector_group=pb_tf.vectorGroup,
                                in_service=pb_tf.inService,
                                terminals=terms,
                                ends=ends,
                                diag_objs=diag_objs,
                                location=location)
