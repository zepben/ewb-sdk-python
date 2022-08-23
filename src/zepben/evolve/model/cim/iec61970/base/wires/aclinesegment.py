#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, WireInfo
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance

__all__ = ["AcLineSegment", "Conductor"]


class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.
    """

    length: Optional[float] = None
    """Segment length for calculating line section capabilities."""

    @property
    def wire_info(self):
        """The `WireInfo` for this `Conductor`"""
        return self.asset_info

    @wire_info.setter
    def wire_info(self, wi: Optional[WireInfo]):
        """
        Set the `WireInfo` for this `Conductor`
        `wi` The `WireInfo` for this `Conductor`
        """
        self.asset_info = wi

    def is_underground(self):
        """
        Returns True if this `Conductor` is underground.
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
    per_length_sequence_impedance: Optional[PerLengthSequenceImpedance] = None
    """A `zepben.evolve.PerLengthSequenceImpedance` describing this ACLineSegment"""

