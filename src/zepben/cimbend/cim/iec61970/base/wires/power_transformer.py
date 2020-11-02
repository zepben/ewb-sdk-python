#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Generator

from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.wires.vector_group import VectorGroup
from zepben.cimbend.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.cimbend.util import require, nlen, get_by_mrid, ngen, safe_remove

__all__ = ["TapChanger", "RatioTapChanger", "PowerTransformer", "PowerTransformerEnd", "TransformerEnd"]


class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.
    """

    control_enabled: bool = True
    """Specifies the regulation status of the equipment.  True is regulating, false is not regulating."""

    neutral_u: int = 0
    """Voltage at which the winding operates at the neutral tap setting."""

    _high_step: int = 1
    _low_step: int = 0
    _neutral_step: int = 0
    _normal_step: int = 0
    _step: float = 0.0

    def __init__(self, high_step: int = 1, low_step: int = 0, neutral_step: int = 0, normal_step: int = 0, step: float = 0.0):
        self._high_step = high_step
        self._low_step = low_step
        self._neutral_step = neutral_step
        self._normal_step = normal_step
        self._step = step
        self._validate_steps()

    @property
    def high_step(self):
        """Highest possible tap step position, advance from neutral. The attribute shall be greater than lowStep."""
        return self._high_step

    @high_step.setter
    def high_step(self, val):
        require(val > self._low_step, lambda: f"High step {val} must be greater than low step {self._low_step}")
        self._check_steps(self.low_step, val)
        self._high_step = val

    @property
    def low_step(self):
        """Lowest possible tap step position, retard from neutral"""
        return self._low_step

    @low_step.setter
    def low_step(self, val):
        require(val < self._high_step, lambda: f"Low step {val} must be less than high step {self._high_step}")
        self._check_steps(val, self.high_step)
        self._low_step = val

    @property
    def neutral_step(self):
        """The neutral tap step position for this winding. The attribute shall be equal or greater than lowStep and equal or less than highStep."""
        return self._neutral_step

    @neutral_step.setter
    def neutral_step(self, val):
        require(self._low_step <= val <= self._high_step, lambda: f"Neutral step {val} must be between high step {self._high_step} and low step {self._low_step}")
        self._neutral_step = val

    @property
    def normal_step(self):
        """
        The tap step position used in "normal" network operation for this winding. For a "Fixed" tap changer indicates the current physical tap setting.
        The attribute shall be equal or greater than lowStep and equal or less than highStep.
        """
        return self._normal_step

    @normal_step.setter
    def normal_step(self, val):
        require(self._low_step <= val <= self._high_step, lambda: f"Normal step {val} must be between high step {self._high_step} and low step {self._low_step}")
        self._normal_step = val

    @property
    def step(self):
        """
        Tap changer position. Starting step for a steady state solution. Non integer values are allowed to support continuous tap variables.
        The reasons for continuous value are to support study cases where no discrete tap changers has yet been designed, a solutions where a narrow voltage
        band force the tap step to oscillate or accommodate for a continuous solution as input.
        The attribute shall be equal or greater than lowStep and equal or less than highStep.
        """
        return self._step

    @step.setter
    def step(self, val):
        require(self._low_step <= val <= self._high_step, lambda: f"Step {val} must be between high step {self._high_step} and low step {self._low_step}")
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


class RatioTapChanger(TapChanger):
    """
    A tap changer that changes the voltage ratio impacting the voltage magnitude but not the phase angle across the transformer.

    Angle sign convention (general): Positive value indicates a positive phase shift from the winding where the tap is located to the other winding
    (for a two-winding transformer).
    """

    transformer_end: Optional[TransformerEnd] = None
    """`TransformerEnd` to which this ratio tap changer belongs."""

    step_voltage_increment: float = 0.0
    """Tap step increment, in per cent of neutral voltage, per step position."""


class TransformerEnd(IdentifiedObject):
    """
    A conducting connection point of a power transformer. It corresponds to a physical transformer winding terminal.
    In earlier CIM versions, the TransformerWinding class served a similar purpose, but this class is more flexible
    because it associates to terminal but is not a specialization of ConductingEquipment.
    """
    grounded: bool = False
    """(for Yn and Zn connections) True if the neutral is solidly grounded."""

    r_ground: float = 0.0
    """(for Yn and Zn connections) Resistance part of neutral impedance where 'grounded' is true"""

    x_ground: float = 0.0
    """(for Yn and Zn connections) Reactive part of neutral impedance where 'grounded' is true"""

    ratio_tap_changer: Optional[RatioTapChanger] = None
    """Ratio tap changer associated with this transformer end."""

    terminal: Optional[Terminal] = None
    """The terminal of the transformer that this end is associated with"""

    base_voltage: Optional[BaseVoltage] = None
    """Base voltage of the transformer end.  This is essential for PU calculation."""

    end_number: int = 0
    """Number for this transformer end, corresponding to the end’s order in the power transformer vector group or phase angle clock number. 
    Highest voltage winding should be 1. Each end within a power transformer should have a unique subsequent end number. 
    Note the transformer end number need not match the terminal sequence number."""


class PowerTransformerEnd(TransformerEnd):
    """
    A PowerTransformerEnd is associated with each Terminal of a PowerTransformer.

    The impedance values r, r0, x, and x0 of a PowerTransformerEnd represents a star equivalent as follows

    1) for a two Terminal PowerTransformer the high voltage PowerTransformerEnd has non zero values on r, r0, x, and x0
    while the low voltage PowerTransformerEnd has zero values for r, r0, x, and x0.
    2) for a three Terminal PowerTransformer the three PowerTransformerEnds represents a star equivalent with each leg
    in the star represented by r, r0, x, and x0 values.
    3) For a three Terminal transformer each PowerTransformerEnd shall have g, g0, b and b0 values corresponding the no load losses
    distributed on the three PowerTransformerEnds. The total no load loss shunt impedances may also be placed at one of the
    PowerTransformerEnds, preferably the end numbered 1, having the shunt values on end 1 is the preferred way.
    4) for a PowerTransformer with more than three Terminals the PowerTransformerEnd impedance values cannot be used.
    Instead use the TransformerMeshImpedance or split the transformer into multiple PowerTransformers.
    """

    _power_transformer: Optional[PowerTransformer] = None
    """The power transformer of this power transformer end."""

    rated_s: int = 0
    """Normal apparent power rating. The attribute shall be a positive value. For a two-winding transformer the values for the high and low voltage sides 
    shall be identical."""

    rated_u: int = 0
    """Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings. A high voltage side, as given by 
    TransformerEnd.endNumber, shall have a ratedU that is greater or equal than ratedU for the lower voltage sides."""

    r: float = 0.0
    """Resistance (star-phases) of the transformer end. The attribute shall be equal or greater than zero for non-equivalent transformers."""

    x: float = 0.0
    """Positive sequence series reactance (star-phases) of the transformer end."""

    r0: float = 0.0
    """Zero sequence series resistance (star-phases) of the transformer end."""

    x0: float = 0.0
    """Zero sequence series reactance of the transformer end."""

    g: float = 0.0
    """Magnetizing branch conductance."""

    g0: float = 0.0
    """Zero sequence magnetizing branch conductance (star-phases)."""

    b: float = 0.0
    """Magnetizing branch susceptance (B mag).  The value can be positive or negative."""

    b0: float = 0.0
    """Zero sequence magnetizing branch susceptance."""

    connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING
    """Kind of `zepben.protobuf.cim.iec61970.base.wires.winding_connection.WindingConnection` for this end."""

    phase_angle_clock: int = 0
    """Terminal voltage phase angle displacement where 360 degrees are represented with clock hours. The valid values are 0 to 11. For example, for the 
    secondary side end of a transformer with vector group code of 'Dyn11', specify the connection kind as wye with neutral and specify the phase angle of the 
    clock as 11. The clock value of the transformer end number specified as 1, is assumed to be zero."""

    def __init__(self, power_transformer: PowerTransformer = None):
        if power_transformer:
            self.power_transformer = power_transformer

    @property
    def power_transformer(self):
        """The power transformer of this power transformer end."""
        return self._power_transformer

    @power_transformer.setter
    def power_transformer(self, pt):
        if self._power_transformer is None or self._power_transformer is pt:
            self._power_transformer = pt
        else:
            raise ValueError(f"power_transformer for {str(self)} has already been set to {self._power_transformer}, cannot reset this field to {pt}")


class PowerTransformer(ConductingEquipment):
    """
    An electrical device consisting of  two or more coupled windings, with or without a magnetic core, for introducing
    mutual coupling between electric circuits.

    Transformers can be used to control voltage and phase shift (active power flow). A power transformer may be composed of separate transformer tanks that
    need not be identical. A power transformer can be modeled with or without tanks and is intended for use in both balanced and unbalanced representations.

    A power transformer typically has two terminals, but may have one (grounding), three or more terminals.

    The inherited association ConductingEquipment.BaseVoltage should not be used.
    The association from TransformerEnd to BaseVoltage should be used instead.

    Attributes -
        vector_group : `zepben.protobuf.cim.iec61970.base.wires.VectorGroup` of the transformer for protective relaying.
        power_transformer_ends : 
                                 
                                 
    """
    vector_group: VectorGroup = VectorGroup.UNKNOWN
    """
    Vector group of the transformer for protective relaying, e.g., Dyn1. For unbalanced transformers, this may not be simply
    determined from the constituent winding connections and phase angle displacements.
                                                                                                                            
    The vectorGroup string consists of the following components in the order listed: high voltage winding connection, mid
    voltage winding connection(for three winding transformers), phase displacement clock number from 0 to 11,  low voltage
    winding connection phase displacement clock number from 0 to 11.   The winding connections are D(delta), Y(wye),
    YN(wye with neutral), Z(zigzag), ZN(zigzag with neutral), A(auto transformer). Upper case means the high voltage,
    lower case mid or low.The high voltage winding always has clock position 0 and is not included in the vector group
    string.  Some examples: YNy0(two winding wye to wye with no phase displacement), YNd11(two winding wye to delta with
    330 degrees phase displacement), YNyn0d5(three winding transformer wye with neutral high voltage, wye with neutral mid
    voltage and no phase displacement, delta low voltage with 150 degrees displacement).
                                                                                                                            
    Phase displacement is defined as the angular difference between the phasors representing the voltages between the
    neutral point(real or imaginary) and the corresponding terminals of two windings, a positive sequence voltage system
    being applied to the high-voltage terminals, following each other in alphabetical sequence if they are lettered, or in
    numerical sequence if they are numbered: the phasors are assumed to rotate in a counter-clockwise sense.
    """

    _power_transformer_ends: Optional[List[PowerTransformerEnd]] = None

    def __init__(self, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                 operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None, terminals: List[Terminal] = None,
                 power_transformer_ends: List[PowerTransformerEnd] = None):
        super().__init__(usage_points=usage_points, equipment_containers=equipment_containers, operational_restrictions=operational_restrictions,
                         current_feeders=current_feeders, terminals=terminals)
        if power_transformer_ends:
            for end in power_transformer_ends:
                self.add_end(end)

    def num_ends(self):
        """
        Get the number of `PowerTransformerEnd`s for this `PowerTransformer`.
        """
        return nlen(self._power_transformer_ends)

    @property
    def ends(self) -> Generator[PowerTransformerEnd, None, None]:
        """The `PowerTransformerEnd`s for this `PowerTransformer`."""
        return ngen(self._power_transformer_ends)

    def get_end_by_mrid(self, mrid: str) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` for this `PowerTransformer` identified by `mrid`

        `mrid` the mRID of the required `PowerTransformerEnd`
        Returns The `PowerTransformerEnd` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_transformer_ends, mrid)

    def get_end_by_num(self, end_number: int):
        """
        Get the `PowerTransformerEnd` on this `PowerTransformer` by its `end_number`.

        `end_number` The `end_number` of the `PowerTransformerEnd` in relation to this `PowerTransformer`s VectorGroup.
        Returns The `PowerTransformerEnd` referred to by `end_number`
        Raises IndexError if no `PowerTransformerEnd` was found with end_number `end_number`.
        """
        if self._power_transformer_ends:
            for end in self._power_transformer_ends:
                if end.end_number == end_number:
                    return end
        raise IndexError(f"No TransformerEnd with end_number {end_number} was found in PowerTransformer {str(self)}")

    def add_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        Associate a `PowerTransformerEnd` with this `PowerTransformer`. If `end.end_number` == 0, the end will be assigned an end_number of
        `self.num_ends() + 1`.

        `end` the `PowerTransformerEnd` to associate with this `PowerTransformer`.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        Raises `ValueError` if another `PowerTransformerEnd` with the same `mrid` already exists for this `PowerTransformer`.
        """
        if self._validate_end(end):
            return self

        if end.end_number == 0:
            end.end_number = self.num_ends() + 1

        self._power_transformer_ends = list() if self._power_transformer_ends is None else self._power_transformer_ends
        self._power_transformer_ends.append(end)
        self._power_transformer_ends.sort(key=lambda t: t.end_number)
        return self

    def remove_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        `end` the `PowerTransformerEnd` to disassociate from this `PowerTransformer`.
        Raises `ValueError` if `end` was not associated with this `PowerTransformer`.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        """
        self._power_transformer_ends = safe_remove(self._power_transformer_ends, end)
        return self

    def clear_ends(self) -> PowerTransformer:
        """
        Clear all `PowerTransformerEnd`s.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        """
        self._power_transformer_ends.clear()
        return self

    def _validate_end(self, end: PowerTransformerEnd) -> bool:
        """
        Validate an end against this `PowerTransformer`'s `PowerTransformerEnd`s.

        `end` The `PowerTransformerEnd` to validate.
        Returns True if `end` is already associated with this `PowerTransformer`, otherwise False.
        Raises `ValueError` if `end.power_transformer` is not this `PowerTransformer`, or if this `PowerTransformer` has a different `PowerTransformerEnd`
        with the same mRID.
        """
        if self._validate_reference(end, self.get_end_by_mrid, "A PowerTransformerEnd"):
            return True

        if self._validate_reference_by_sn(end.end_number, end, self.get_end_by_num, "A PowerTransformerEnd", "end_number"):
            return True

        require(end.power_transformer is self,
                lambda: f"PowerTransformerEnd {end} references another PowerTransformer {end.power_transformer}, expected {str(self)}.")
        return False
