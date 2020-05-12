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
from __future__ import annotations

from dataclasses import dataclass, InitVar, field
from typing import List, Optional, Generator, Tuple

from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.wires.vector_group import VectorGroup
from zepben.cimbend.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.cimbend.util import require, nlen, get_by_mrid, contains_mrid, ngen

__all__ = ["TapChanger", "RatioTapChanger", "PowerTransformer", "PowerTransformerEnd", "TransformerEnd"]


@dataclass
class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.

    Attributes -
        control_enabled : Specifies the regulation status of the equipment.  True is regulating, false is not regulating.
        _high_step : Highest possible tap step position, advance from neutral. The attribute shall be greater than lowStep.
        _low_step : Lowest possible tap step position, retard from neutral
        _step : Tap changer position. Starting step for a steady state solution. Non integer values are allowed to
               support continuous tap variables.
               The reasons for continuous value are to support study cases where no discrete tap changers has yet been
               designed, a solutions where a narrow voltage band force the tap step to oscillate or accommodate for a
               continuous solution as input.
               The attribute shall be equal or greater than lowStep and equal or less than highStep.
        _neutral_step : The neutral tap step position for this winding.
                      The attribute shall be equal or greater than lowStep and equal or less than highStep.
        neutral_u : Voltage at which the winding operates at the neutral tap setting.
        _normal_step : The tap step position used in "normal" network operation for this winding. For a "Fixed" tap changer
                     indicates the current physical tap setting. The attribute shall be equal or greater than lowStep
                     and equal or less than highStep.
    """
    control_enabled: bool = True
    highstep: InitVar[int] = 1
    _high_step: int = field(default=1, init=False)
    lowstep: InitVar[int] = 0
    _low_step: int = field(default=0, init=False)
    neutralstep: InitVar[int] = 0
    _neutral_step: int = field(default=0, init=False)
    neutral_u: int = 0
    normalstep: InitVar[int] = 0
    _normal_step: int = field(default=0, init=False)
    step_: InitVar[float] = 0.0
    _step: float = field(default=0.0, init=False)

    def __post_init__(self, highstep: int, lowstep: int, neutralstep: int, normalstep: int, step_: float):
        super().__post_init__()
        self._high_step = highstep
        self._low_step = lowstep
        self._neutral_step = neutralstep
        self._normal_step = normalstep
        self._step = step_
        self._validate_steps()

    @property
    def high_step(self):
        return self._high_step

    @high_step.setter
    def high_step(self, val):
        require(val > self._low_step, lambda: f"High step {val} must be greater than low step {self._low_step}")
        self._check_steps(self.low_step, val)
        self._high_step = val

    @property
    def low_step(self):
        return self._low_step

    @low_step.setter
    def low_step(self, val):
        require(val < self._high_step, lambda: f"Low step {val} must be less than high step {self._high_step}")
        self._check_steps(val, self.high_step)
        self._low_step = val

    @property
    def neutral_step(self):
        return self._neutral_step

    @neutral_step.setter
    def neutral_step(self, val):
        require(self._low_step <= val <= self._high_step,
                lambda: f"Neutral step {val} must be between high step {self._high_step} and low step {self._low_step}")
        self._neutral_step = val

    @property
    def normal_step(self):
        return self._normal_step

    @normal_step.setter
    def normal_step(self, val):
        require(self._low_step <= val <= self._high_step,
                lambda: f"Normal step {val} must be between high step {self._high_step} and low step {self._low_step}")
        self._normal_step = val

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, val):
        require(self._low_step <= val <= self._high_step,
                lambda: f"Step {val} must be between high step {self._high_step} and low step {self._low_step}")
        self._step = val

    def _check_steps(self, low, high):
        require(low <= self.step <= high, lambda: f"New value would invalidate current step of {self.step}")
        require(low <= self.normal_step <= high,
                lambda: f"New value would invalidate current normal_step of {self.normal_step}")
        require(low <= self.neutral_step <= high,
                lambda: f"New value would invalidate current neutral_step of {self.neutral_step}")

    def _validate_steps(self):
        require(self.high_step > self.low_step,
                lambda: f"High step [{self.high_step}] must be greater than low step [{self.low_step}]")
        require(self.low_step <= self.neutral_step <= self.high_step,
                lambda: f"Neutral step [{self.neutral_step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        require(self._low_step <= self.normal_step <= self._high_step,
                lambda: f"Normal step [{self.normal_step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        require(self._low_step <= self.step <= self._high_step,
                lambda: f"Step [{self.step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")


@dataclass
class RatioTapChanger(TapChanger):
    """
    A tap changer that changes the voltage ratio impacting the voltage magnitude but not the phase angle across the
    transformer.

    Attributes -
        transformer_end : Transformer end to which this ratio tap changer belongs.
        step_voltage_increment : Tap step increment, in per cent of neutral voltage, per step position.
    """

    transformer_end: Optional[TransformerEnd] = None
    step_voltage_increment: float = 0.0


@dataclass
class TransformerEnd(IdentifiedObject):
    """
    A conducting connection point of a power transformer. It corresponds to a physical transformer winding terminal.
    In earlier CIM versions, the TransformerWinding class served a similar purpose, but this class is more flexible
    because it associates to terminal but is not a specialization of ConductingEquipment.

    Attributes -
        grounded : (for Yn and Zn connections) True if the neutral is solidly grounded.
        rGround : (for Yn and Zn connections) Resistance part of neutral impedance where 'grounded' is true
        xGround : (for Yn and Zn connections) Reactive part of neutral impedance where 'grounded' is true
        baseVoltage : Base voltage of the transformer end.  This is essential for PU calculation.
        ratioTapChanger : Ratio tap changer associated with this transformer end.
        terminal : The terminal of the transformer that this end is associated with
    """
    grounded: bool = False
    r_ground: float = 0.0
    x_ground: float = 0.0
    ratio_tap_changer: Optional[RatioTapChanger] = None
    terminal: Optional[Terminal] = None
    base_voltage: Optional[BaseVoltage] = None


@dataclass
class PowerTransformerEnd(TransformerEnd):
    """
    A PowerTransformerEnd is associated with each Terminal of a PowerTransformer.
    The impedance values r, r0, x, and x0 of a PowerTransformerEnd represents a star equivalent as follows
    1) for a two Terminal PowerTransformer the high voltage PowerTransformerEnd has non zero values on r, r0, x, and x0
    while the low voltage PowerTransformerEnd has zero values for r, r0, x, and x0.
    2) for a three Terminal PowerTransformer the three PowerTransformerEnds represents a star equivalent with each leg
    in the star represented by r, r0, x, and x0 values.
    3) for a PowerTransformer with more than three Terminals the PowerTransformerEnd impedance values cannot be used.
    Instead use the TransformerMeshImpedance or split the transformer into multiple PowerTransformers.

    Attributes -
        power_transformer : The power transformer of this power transformer end.
        rated_s : Normal apparent power rating.
                  The attribute shall be a positive value. For a two-winding transformer the values for the high and
                  low voltage sides shall be identical.
        rated_u : Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for
                  single-phase windings. A high voltage side, as given by TransformerEnd.endNumber, shall have a ratedU
                  that is greater or equal than ratedU for the lower voltage sides.
        r : Resistance (star-phases) of the transformer end. The attribute shall be equal or greater than zero
            for non-equivalent transformers.
        x : Positive sequence series reactance (star-phases) of the transformer end.
        r0 : Zero sequence series resistance (star-phases) of the transformer end.
        x0 : Zero sequence series reactance of the transformer end.
        connection_kind : Kind of :class:`zepben.protobuf.cim.iec61970.base.wires.WindingConnection` for this end.
        ratio_tap_changer : :class:`RatioTapChanger` attached to this end.
        b : Magnetizing branch susceptance (B mag).  The value can be positive or negative.
        b0 : Zero sequence magnetizing branch susceptance.
        g : Magnetizing branch conductance.
        g0 : Zero sequence magnetizing branch conductance (star-phases).
        phase_angle_clock : Terminal voltage phase angle displacement where 360 degrees are represented with
                            clock hours. The valid values are 0 to 11. For example, for the secondary side end of a transformer with
                            vector group code of 'Dyn11', specify the connection kind as wye with neutral and specify the phase angle of
                            the clock as 11.  The clock value of the transformer end number specified as 1, is assumed to be zero.
    """
    power_transformer: Optional[PowerTransformer] = None
    rated_s: int = 0
    rated_u: int = 0
    r: float = 0.0
    x: float = 0.0
    r0: float = 0.0
    x0: float = 0.0
    g: float = 0.0
    g0: float = 0.0
    b: float = 0.0
    b0: float = 0.0
    connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING
    phase_angle_clock: int = 0

    def has_tap_changer(self):
        return self.ratio_tap_changer is not None

    def get_tap_changer_step(self):
        if self.has_tap_changer():
            return self.ratio_tap_changer.step


@dataclass
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

    Attributes -
        vector_group : :class:`zepben.protobuf.cim.iec61970.base.wires.VectorGroup` of the transformer for protective relaying.
        power_transformer_ends : A list of the :class:`PowerTransformerEnd` for each winding in this Transformer.
                                 The ordering of the list is important, and reflects which
                                 :class:`zepben.cimbend.Terminal` each end is associated with.
    """
    vector_group: VectorGroup = VectorGroup.UNKNOWN
    powertransformerends: InitVar[List[PowerTransformerEnd]] = field(default=list())
    _power_transformer_ends: Optional[List[PowerTransformerEnd]] = field(init=False, default=None)

    def __post_init__(self, usagepoints: Optional[List[UsagePoint]],
                      equipmentcontainers: Optional[List[EquipmentContainer]],
                      operationalrestrictions: Optional[List[OperationalRestriction]],
                      currentfeeders: Optional[List[Feeder]],
                      terminals_: List[Terminal],
                      powertransformerends: List[PowerTransformerEnd]):
        super().__post_init__(usagepoints, equipmentcontainers, operationalrestrictions, currentfeeders, terminals_)
        for end in powertransformerends:
            self.add_end(end)

    @property
    def num_ends(self):
        """
        Get the number of :class:`PowerTransformerEnd`s for this ``PowerTransformer``.
        """
        return nlen(self._power_transformer_ends)

    @property
    def ends(self) -> Generator[Tuple[int, PowerTransformerEnd], None, None]:
        """
        :return: Generator over the ``PowerTransformerEnd``s of this ``PowerTransformer``.
        """
        for i, end in enumerate(ngen(self._power_transformer_ends)):
            yield i, end

    def get_end_by_mrid(self, mrid: str) -> PowerTransformerEnd:
        """
        Get the ``PowerTransformerEnd`` for this ``PowerTransformer`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`PowerTransformerEnd`
        :return: The :class:`PowerTransformerEnd` with the specified ``mrid`` if it
        exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._power_transformer_ends, mrid)

    def get_end_by_num(self, end_number: int):
        """
        Get a ``PowerTransformerEnd`` by its sequenceNumber.
        :param end_number: The sequenceNumber of the `PowerTransformerEnd` in relation to this ``PowerTransformer``.
        :raises: IndexError if this ``PowerTransformer`` does not have ``sequence_number`` ``PowerTransformerEnd``'s.
        :return: The ``PowerTransformerEnd`` referred to by ``sequenceNumber``
        """
        return self._power_transformer_ends[end_number]

    def add_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        :param end: the :class:`PowerTransformerEnd` to add to this ``PowerTransformer``, assigning it a sequence_number
                    of ``num_ends``.
        :return: A reference to this ``PowerTransformer`` to allow fluent use.
        """
        self.insert_end(end)
        return self

    def insert_end(self, end: PowerTransformerEnd, end_number: int = None) -> PowerTransformer:
        """
        :param end: the :class:`PowerTransformerEnd` to associate with this ``PowerTransformer``.
        :param end_number: The ``sequenceNumber`` for ``end``. You should aim to always insert
        ``PowerTransformerEnd``s in order.
        :return: A reference to this ``PowerTransformer`` to allow fluent use.
        """
        if end_number is None:
            end_number = self.num_terminals
        require(not contains_mrid(self._power_transformer_ends, end.mrid),
                lambda: f"A PowerTransformerEnd with mRID {end.mrid} already exists in {str(self)}.")
        require(0 <= end_number <= self.num_ends,
                lambda: f"Unable to add PowerTransformerEnd to {str(self)}. End number {end_number} is invalid. "
                        f"Expected a value between 0 and {self.num_ends}. Make sure you are adding the ends in the "
                        f"correct order and there are no missing sequence numbers.")
        self._power_transformer_ends = list() if self._power_transformer_ends is None else self._power_transformer_ends
        self._power_transformer_ends.insert(end_number, end)
        return self

    def remove_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        :param end: the :class:`PowerTransformerEnd` to disassociate from this ``PowerTransformer``.
        :raises: ValueError if ``end`` was not associated with this ``PowerTransformer``.
        :return: A reference to this ``PowerTransformer`` to allow fluent use.
        """
        if self._power_transformer_ends is not None:
            self._power_transformer_ends.remove(end)
            if not self._power_transformer_ends:
                self._power_transformer_ends = None
        else:
            raise KeyError(end)

        return self

    def clear_ends(self) -> PowerTransformer:
        """
        Clear all ``PowerTransformerEnd``s.
        :return: A reference to this ``PowerTransformer`` to allow fluent use.
        """
        self._power_transformer_ends.clear()
        return self

    def get_nominal_voltage(self, terminal: Terminal = None):
        """
        Return nominal voltage, ideally corresponding to a specific terminal.
        :param terminal:
        :return: Nominal voltage of the PowerTransformerEnd corresponding to the terminal,
                 or potentially None if no terminal is specified
        """
        if terminal is None:
            return self.nominal_voltage
        else:
            return self.get_end_by_num(self.terminal_sequence_number(terminal))
