#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["AcLineSegment"]

from functools import singledispatchmethod
from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.conductor import Conductor
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment_phase import AcLineSegmentPhase
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove, require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
    from zepben.ewb.model.cim.iec61970.base.wires.cut import Cut
    from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import WireInfo
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance


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

    per_length_impedance: 'PerLengthImpedance | None' = None
    """A `zepben.ewb.model.cim.iec61970.base.wires.PerLengthImpedance` describing this AcLineSegment"""

    _cuts: list['Cut'] | None= None
    _clamps: list['Clamp'] | None = None
    _phases: list['AcLineSegmentPhase'] | None = None

    @property
    def per_length_sequence_impedance(self) -> Optional['PerLengthSequenceImpedance']:
        """
        Per-length sequence impedance of this line segment.
        :return: A PerLengthSequenceImpedance if one is set, otherwise None.
        """
        if self.per_length_impedance:
            from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance
            if isinstance(self.per_length_impedance, PerLengthSequenceImpedance):
                return self.per_length_impedance
        return None

    @per_length_sequence_impedance.setter
    def per_length_sequence_impedance(self, value: Optional['PerLengthSequenceImpedance']):
        self.per_length_impedance = value

    @property
    def per_length_phase_impedance(self) -> Optional['PerLengthPhaseImpedance']:
        """
        Per-length phase impedance of this line segment.
        :return: A PerLengthPhaseImpedance if one is set, otherwise None.
        """
        if self.per_length_impedance:
            from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
            if isinstance(self.per_length_impedance, PerLengthPhaseImpedance):
                return self.per_length_impedance
        return None

    @per_length_phase_impedance.setter
    def per_length_phase_impedance(self, value: Optional['PerLengthPhaseImpedance']):
        self.per_length_impedance = value

    @property
    def cuts(self) -> Generator['Cut', None, None]:
        """The `Cut`s for this `AcLineSegment`."""
        return ngen(self._cuts)

    def num_cuts(self):
        """
        Get the number of `Cut`s for this `AcLineSegment`.
        """
        return nlen(self._cuts)

    def get_cut(self, mrid: str) -> 'Cut':
        """
        Get the `Cut` for this `AcLineSegment` identified by `mrid`

        :param mrid: The mRID of the required `Cut`
        :return: The `Cut` with the specified `mrid` if it exists
        :raise KeyError: If the `mrid` wasn't present.
        """
        return get_by_mrid(self._cuts, mrid)

    def add_cut(self, cut: 'Cut') -> 'AcLineSegment':
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

    def remove_cut(self, cut: 'Cut') -> 'AcLineSegment':
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
    def clamps(self) -> Generator['Clamp', None, None]:
        """The `Clamp`s for this `AcLineSegment`."""
        return ngen(self._clamps)

    def num_clamps(self):
        """
        Get the number of `Clamp`s for this `AcLineSegment`.
        """
        return nlen(self._clamps)

    def get_clamp(self, mrid: str) -> 'Clamp':
        """
        Get the `Clamp` for this `AcLineSegment` identified by `mrid`

        :param mrid: The mRID of the required `Clamp`
        :return: The `Clamp` with the specified `mrid` if it exists
        :raise KeyError: If the `mrid` wasn't present.
        """
        return get_by_mrid(self._clamps, mrid)

    def add_clamp(self, clamp: 'Clamp') -> 'AcLineSegment':
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

    def remove_clamp(self, clamp: 'Clamp') -> 'AcLineSegment':
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

    def _validate_cut(self, cut: 'Cut') -> bool:
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

    def _validate_clamp(self, clamp: 'Clamp') -> bool:
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

    @property
    def phases(self) -> Generator['Phase', None, None]:
        """
        The individual phase models for this AcLineSegment. The returned collection is read only.
        """
        return ngen(self._phases)

    def num_phases(self) -> int:
        """
        Get the number of entries in the [AcLineSegmentPhase] collection.
        """
        return nlen(self._phases)

    def get_phase(self, identifier: 'str | SinglePhaseKind') -> 'AcLineSegmentPhase | None':
        """
        The individual phase models for this AcLineSegment.

        :param identifier: the mRID or ``SinglePhaseKind`` of the required [AcLineSegmentPhase]
        :returns: The [AcLineSegmentPhase] with the specified [mRID] if it exists, otherwise null
        """
        if isinstance(identifier, str):
            if self._phases is not None:
                return get_by_mrid(self._phases, identifier)

        elif isinstance(identifier, SinglePhaseKind):
            for it in self._phases:
                if it == identifier:
                    return it

        raise KeyError(identifier)

    def add_phase(self, phase: AcLineSegmentPhase) -> 'AcLineSegment':
        """
        Add an [AcLineSegmentPhase] to this [AcLineSegment].

        :param phase: The [AcLineSegmentPhase] to add.
        :returns: This [AcLineSegment] for fluent use.
        """
        if self._validate_reference(phase, self.get_phase, "An AcLineSegmentPhase"):
            return self

        if phase.ac_line_segment is None:
            phase.ac_line_segment = self

        require(phase.ac_line_segment is self, lambda: f"${phase} `acLineSegment` property references ${phase.ac_line_segment}, expected ${self}.")

        if self._phases is None:
            self._phases = list()
        self._phases.append(phase)
        self._phases.sort(key=lambda it: getattr(it, 'sequence_number') or 0)
        return self

    def remove_phase(self, phase: AcLineSegmentPhase) -> 'AcLineSegment':
        """
        Remove an [AcLineSegmentPhase] from this [AcLineSegment].

        :param phase: The [AcLineSegmentPhase] to remove.
        :returns: true if [phase] is removed from the collection.
        """
        self._phases = safe_remove(self._phases, phase)
        return self

    def clear_phases(self) -> 'AcLineSegment':
        """
        Clear all [AcLineSegmentPhase]'s from this [AcLineSegment].

        :returns: This [AcLineSegment] for fluent use.
        """
        self._phases = None
        return self

    def wire_info_for_phase(self, phase: SinglePhaseKind) -> 'WireInfo | None':
        """
        Retrieve the WireInfo associated with the requested [phase]. If no specific [WireInfo] is available for the given [phase], [AcLineSegment.assetInfo] will be returned.

        :param phase: the phase to retrieve [WireInfo] for.
        """
        for it in self._phases:
            if it.phase == phase:
                return it.asset_info
        return self.wire_info
