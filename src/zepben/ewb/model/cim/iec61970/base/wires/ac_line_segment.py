#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AcLineSegment"]

from typing import Optional, List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor, custom_add
from zepben.ewb.model.cim.iec61970.base.wires.conductor import Conductor
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
    from zepben.ewb.model.cim.iec61970.base.wires.cut import Cut
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_impedance import PerLengthImpedance
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance


@dataslot
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

    per_length_impedance: Optional['PerLengthImpedance'] = None
    """A `zepben.ewb.model.cim.iec61970.base.wires.PerLengthImpedance` describing this AcLineSegment"""

    cuts: List['Cut'] | None = MRIDListAccessor()
    clamps: List['Clamp'] | None = MRIDListAccessor()

    def _retype(self):
        self.cuts: MRIDListRouter['Cut'] = ...
        self.clamps: MRIDListRouter['Clamp'] = ...
    
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

    @deprecated("BOILERPLATE: Use len(cuts) instead")
    def num_cuts(self):
        return len(self.cuts)

    @deprecated("BOILERPLATE: Use cuts.get_by_mrid(mrid) instead")
    def get_cut(self, mrid: str) -> 'Cut':
        return self.cuts.get_by_mrid(mrid)

    @custom_add(cuts)
    def add_cut(self, cut: 'Cut') -> 'AcLineSegment':
        """
        Associate a `Cut` with this `AcLineSegment`.

        :param cut: the `Cut` to associate with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        :raise ValueError: If another `Cut` with the same `mrid` already exists for this `AcLineSegment`.
        """
        if self._validate_cut(cut):
            return self

        self.cuts.append_unchecked(cut)
        return self

    @deprecated("Boilerplate: Use cuts.remove(cut) instead")
    def remove_cut(self, cut: 'Cut') -> 'AcLineSegment':
        self.cuts.remove(cut)
        return self

    @deprecated("Boilerplate: Use cuts.clear() instead")
    def clear_cuts(self) -> 'AcLineSegment':
        """
        Clear all `Cut`s.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self.cuts.clear()
        return self

    @deprecated("BOILERPLATE: Use len(clamps) instead")
    def num_clamps(self):
        return len(self.clamps)

    @deprecated("BOILERPLATE: Use clamps.get_by_mrid(mrid) instead")
    def get_clamp(self, mrid: str) -> 'Clamp':
        return self.clamps.get_by_mrid(mrid)

    @custom_add(clamps)
    def add_clamp(self, clamp: 'Clamp') -> 'AcLineSegment':
        """
        Associate a `Clamp` with this `AcLineSegment`.

        :param clamp: the `Clamp` to associate with this `AcLineSegment`.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        :raise ValueError: If another `Clamp` with the same `mrid` already exists for this `AcLineSegment`.
        """
        if self._validate_clamp(clamp):
            return self

        self.clamps.append_unchecked(clamp)
        return self

    @deprecated("Boilerplate: Use clamps.remove(clamp) instead")
    def remove_clamp(self, clamp: 'Clamp') -> 'AcLineSegment':
        self.clamps.remove(clamp)
        return self

    @deprecated("Boilerplate: clamps.clear() instead")
    def clear_clamps(self) -> 'AcLineSegment':
        """
        Clear all `Clamp`s.
        :return: A reference to this `AcLineSegment` to allow fluent use.
        """
        self.clamps.clear()
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
