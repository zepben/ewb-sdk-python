#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional, List, Generator

from zepben.evolve import nlen, ngen, get_by_mrid, safe_remove, require
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, WireInfo
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance, PerLengthImpedance
from zepben.evolve.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance

__all__ = ["AcLineSegment", "Conductor"]


class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.
    """

    length: Optional[float] = None
    """Segment length for calculating line section capabilities."""

    design_temperature: Optional[int] = None
    """[ZBEX] The temperature in degrees Celsius for the network design of this conductor."""

    design_rating: Optional[float] = None
    """[ZBEX] The current rating in Amperes at the specified design temperature that can be used without the conductor breaching physical network"""

    @property
    def wire_info(self):
        """The `WireInfo` for this `Conductor`"""
        return self.asset_info

    @wire_info.setter
    def wire_info(self, wi: Optional[WireInfo]):
        """
        Set the `WireInfo` for this `Conductor`
        :param wi: The `WireInfo` for this `Conductor`
        """
        self.asset_info = wi

    def is_underground(self):
        """
        :return: True if this `Conductor` is underground.
        """
        return isinstance(self.wire_info, CableInfo)


class AcLineSegment(Conductor):
    """
    A wire or combination of wires, with consistent electrical characteristics, building a single electrical system,
    used to carry alternating current between points in the power system.

    For symmetrical, transposed 3ph lines, it is sufficient to use attributes of the line segment, which describe
    impedances and admittances for the entire length of the segment. Additionally impedances can be computed by
    using length and associated per length impedances.

    The BaseVoltage at the two ends of ACLineSegments in a Line shall have the same BaseVoltage.nominalVoltage.
    However, boundary lines  may have slightly different BaseVoltage.nominalVoltages and variation is allowed.
    Larger voltage difference in general requires use of an equivalent branch.
    """
    max_terminals = 2

    per_length_impedance: Optional[PerLengthImpedance] = None
    """A `zepben.evolve.PerLengthImpedance` describing this AcLineSegment"""

    _cuts: Optional[List[Cut]] = None
    _clamps: Optional[List[Clamp]] = None

    @property
    def per_length_sequence_impedance(self) -> Optional[PerLengthSequenceImpedance]:
        """
        Per-length sequence impedance of this line segment.
        :return: A PerLengthSequenceImpedance if one is set, otherwise None.
        """
        if self.per_length_impedance:
            if isinstance(self.per_length_impedance, PerLengthSequenceImpedance):
                return self.per_length_impedance
        return None

    @per_length_sequence_impedance.setter
    def per_length_sequence_impedance(self, value: Optional[PerLengthSequenceImpedance]):
        self.per_length_impedance = value

    @property
    def per_length_phase_impedance(self) -> Optional[PerLengthPhaseImpedance]:
        """
        Per-length phase impedance of this line segment.
        :return: A PerLengthPhaseImpedance if one is set, otherwise None.
        """
        if self.per_length_impedance:
            if isinstance(self.per_length_impedance, PerLengthPhaseImpedance):
                return self.per_length_impedance
        return None

    @per_length_phase_impedance.setter
    def per_length_phase_impedance(self, value: Optional[PerLengthPhaseImpedance]):
        self.per_length_impedance = value

    @property
    def cuts(self) -> Generator[Cut, None, None]:
        """The `Cut`s for this `AcLineSegment`."""
        return ngen(self._cuts)

    def num_cuts(self):
        """
        Get the number of `Cut`s for this `AcLineSegment`.
        """
        return nlen(self._cuts)

    def get_cut(self, mrid: str) -> Cut:
        """
        Get the `Cut` for this `AcLineSegment` identified by `mrid`

        :param mrid: The mRID of the required `Cut`
        :return: The `Cut` with the specified `mrid` if it exists
        :raise KeyError: If the `mrid` wasn't present.
        """
        return get_by_mrid(self._cuts, mrid)

    def add_cut(self, cut: Cut) -> 'AcLineSegment':
        """
        Associate a `Cut` with this `AcLineSegment`.

        :param cut: the `Cut` to associate with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        :raise ValueError: If another `Cut` with the same `mrid` already exists for this `AcLineSegment`.
        """
        if self._validate_cut(cut):
            return self

        self._cuts = list() if self._cuts is None else self._cuts
        self._cuts.append(cut)
        return self

    def remove_cut(self, cut: Cut) -> 'AcLineSegment':
        """
        :param cut: The `Cut` to disassociate from this `AcLineSegment`.
        :raise ValueError: If `cut` was not associated with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self._cuts = safe_remove(self._cuts, cut)
        return self

    def clear_cuts(self) -> 'AcLineSegment':
        """
        Clear all `Cut`s.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self._cuts.clear()
        return self

    @property
    def clamps(self) -> Generator[Clamp, None, None]:
        """The `Clamp`s for this `AcLineSegment`."""
        return ngen(self._clamps)

    def num_clamps(self):
        """
        Get the number of `Clamp`s for this `AcLineSegment`.
        """
        return nlen(self._clamps)

    def get_clamp(self, mrid: str) -> Clamp:
        """
        Get the `Clamp` for this `AcLineSegment` identified by `mrid`

        :param mrid: The mRID of the required `Clamp`
        :return: The `Clamp` with the specified `mrid` if it exists
        :raise KeyError: If the `mrid` wasn't present.
        """
        return get_by_mrid(self._clamps, mrid)

    def add_clamp(self, clamp: Clamp) -> 'AcLineSegment':
        """
        Associate a `Clamp` with this `AcLineSegment`.

        :param clamp: the `Clamp` to associate with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        :raise ValueError: If another `Clamp` with the same `mrid` already exists for this `AcLineSegment`.
        """
        if self._validate_clamp(clamp):
            return self

        self._clamps = list() if self._clamps is None else self._clamps
        self._clamps.append(clamp)
        return self

    def remove_clamp(self, clamp: Clamp) -> 'AcLineSegment':
        """
        :param clamp: The `Clamp` to disassociate from this `AcLineSegment`.
        :raise ValueError: If `clamp` was not associated with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self._clamps = safe_remove(self._clamps, clamp)
        return self

    def clear_clamps(self) -> 'AcLineSegment':
        """
        Clear all `Clamp`s.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self._clamps.clear()
        return self

    def _validate_cut(self, cut: Cut) -> bool:
        """
        Validate a cut against this `AcLineSegment`'s `Cut`s.

        :param cut: The `Cut` to validate.
        :return: True if `cut` is already associated with this `AcLineSegment`, otherwise False.
        :raise ValueError: If `cut.ac_line_segment` is not this `AcLineSegment`, or if this `AcLineSegment` has a different `Cut` with the same mRID.
        """
        if self._validate_reference(cut, self.get_cut, "A Cut"):
            return True

        if not cut.ac_line_segment:
            cut.ac_line_segment = self

        require(cut.ac_line_segment is self,
                lambda: f"Cut {cut} references another AcLineSegment {cut.ac_line_segment}, expected {str(self)}.")
        return False

    def _validate_clamp(self, clamp: Clamp) -> bool:
        """
        Validate a clamp against this `AcLineSegment`'s `Clamp`s.

        :param clamp: The `Clamp` to validate.
        :return: True if `clamp` is already associated with this `AcLineSegment`, otherwise False.
        :raise ValueError: If `clamp.ac_line_segment` is not this `AcLineSegment`, or if this `AcLineSegment` has a different `Clamp` with the same mRID.
        """
        if self._validate_reference(clamp, self.get_clamp, "A Clamp"):
            return True

        if not clamp.ac_line_segment:
            clamp.ac_line_segment = self

        require(clamp.ac_line_segment is self,
                lambda: f"Clamp {clamp} references another AcLineSegment {clamp.ac_line_segment}, expected {str(self)}.")
        return False
