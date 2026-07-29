#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["AcLineSegment"]

from dataclasses import field
from typing import Optional, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection
from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment_phase import AcLineSegmentPhase
from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.ewb.model.cim.iec61970.base.wires.conductor import Conductor
from zepben.ewb.model.cim.iec61970.base.wires.cut import Cut
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.boilerplate.relations.ac_line_segment_phase_list import AcLineSegmentPhaseList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
    from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance


@zb_dataclass
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

    _cuts: list[Cut] | None = field(default=None)
    _clamps: list[Clamp] | None = field(default=None)
    _phases: list[AcLineSegmentPhase] | None = field(default=None)

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


    cuts: MridCollection[Cut] = LazyMridList(
        _cuts,
        "A Cut",
        backfill=Backfill(Cut.ac_line_segment)
    )


    clamps: MridCollection[Clamp] = LazyMridList(
        _clamps,
        "A Clamp",
        backfill=Backfill(Clamp.ac_line_segment)
    )

    phases: AcLineSegmentPhaseList = AcLineSegmentPhaseList(
        _phases,
        "An AcLineSegmentPhase",
        backfill=Backfill(AcLineSegmentPhase.ac_line_segment),
        sort_by=lambda it: it.sequence_number or 0
    )


    def wire_info_for_phase(self, phase: SinglePhaseKind) -> 'WireInfo | None':
        """
        Retrieve the WireInfo associated with the requested [phase]. If no specific [WireInfo] is available for the given [phase], [AcLineSegment.assetInfo] will be returned.

        :param phase: the phase to retrieve [WireInfo] for.
        """
        if self._phases:
            for it in self._phases:
                if it.phase == phase:
                    return it.asset_info
            return self.asset_info
        else:
            return self.asset_info

    # region deprecated list boilerplate
    # region cuts boilerplate

    @deprecated("Use len(obj.cuts) instead.")
    def num_cuts(self):
        return len(self.cuts)

    @deprecated("Use obj.cuts.get_by_mrid(mrid) instead.")
    def get_cut(self, mrid: str) -> Cut:
        return self.cuts.get_by_mrid(mrid)

    @deprecated("Use obj.cuts.append(cut) instead.")
    def add_cut(self, cut: Cut) -> 'AcLineSegment':
        self.cuts.append(cut)
        return self

    @deprecated("Use obj.cuts.remove(cut) instead.")
    def remove_cut(self, cut: Cut) -> 'AcLineSegment':
        self.cuts.remove(cut)
        return self

    @deprecated("Use obj.cuts.clear() instead.")
    def clear_cuts(self) -> 'AcLineSegment':
        self.cuts.clear()
        return self

    # endregion cuts boilerplate

    # region clamps boilerplate

    @deprecated("Use len(obj.clamps) instead.")
    def num_clamps(self):
        return len(self.clamps)

    @deprecated("Use obj.clamps.get_by_mrid(mrid) instead.")
    def get_clamp(self, mrid: str) -> Clamp:
        return self.clamps.get_by_mrid(mrid)

    @deprecated("Use obj.clamps.append(clamp) instead.")
    def add_clamp(self, clamp: Clamp) -> 'AcLineSegment':
        self.clamps.append(clamp)
        return self

    @deprecated("Use obj.clamps.remove(clamp) instead.")
    def remove_clamp(self, clamp: Clamp) -> 'AcLineSegment':
        self.clamps.remove(clamp)
        return self

    @deprecated("Use obj.clamps.clear() instead.")
    def clear_clamps(self) -> 'AcLineSegment':
        self.clamps.clear()
        return self

    # endregion clamps boilerplate

    # region phases boilerplate

    @deprecated("Use len(obj.phases) instead.")
    def num_phases(self) -> int:
        return len(self.phases)

    @deprecated("Use obj.phases.get_by_mrid(identifier) or obj.phases.get_by_phase(identifier) instead.")
    def get_phase(self, identifier: 'str | SinglePhaseKind') -> 'AcLineSegmentPhase | None':
        if isinstance(identifier, str):
            return self.phases.get_by_mrid(identifier)
        elif isinstance(identifier, SinglePhaseKind):
            return self.phases.get_by_phase(identifier)
        raise KeyError(identifier) # Wrong error, but consistent with previous functionality - deprecated regardless.

    @deprecated("Use obj.phases.append(phase) instead.")
    def add_phase(self, phase: AcLineSegmentPhase) -> 'AcLineSegment':
        self.phases.append(phase)
        return self

    @deprecated("Use obj.phases.remove(phase) instead.")
    def remove_phase(self, phase: AcLineSegmentPhase) -> 'AcLineSegment':
        self.phases.remove(phase)
        return self

    @deprecated("Use obj.phases.clear() instead.")
    def clear_phases(self) -> 'AcLineSegment':
        self.phases.clear()
        return self

    # endregion phases boilerplate

    # endregion deprecated list boilerplate
