#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Substation"]

from typing import Optional, List, TYPE_CHECKING

from zepben.ewb.collections.autoslot import autoslot_dataclass
from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import Loop
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


@autoslot_dataclass
class Substation(EquipmentContainer):
    """
    A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk
    is passed for the purposes of switching or modifying its characteristics.
    """

    sub_geographical_region: Optional[SubGeographicalRegion] = None
    """The SubGeographicalRegion containing the substation."""

    normal_energized_feeders: Optional[List[Feeder]] = None

    loops: Optional[List[Loop]] = None

    energized_loops: Optional[List[Loop]] = None

    circuits: Optional[List[Circuit]] = None

    def __post_init__(self):
        self.normal_energized_feeders: MRIDList[Feeder] = MRIDList(self.normal_energized_feeders)
        self.loops: MRIDList[Feeder] = MRIDList(self.loops)
        self.energized_loops: MRIDList[Feeder] = MRIDList(self.energized_loops)
        self.circuits: MRIDList[Feeder] = MRIDList(self.circuits)

    @property
    def feeders(self):
        """
        The normal energized feeders of the substation. Also used for naming purposes.
        """
        return self.normal_energized_feeders

    def num_feeders(self):
        """
        Returns The number of `Feeder`s associated with this `Substation`
        """
        return len(self.normal_energized_feeders)

    def get_feeder(self, mrid: str) -> Feeder:
        """
        Get the `Feeder` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Feeder`
        Returns The `Feeder` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.normal_energized_feeders.get_by_mrid(mrid)

    def add_feeder(self, feeder: Feeder) -> Substation:
        """
        Associate a `Feeder` with this `Substation`

        `feeder` The `Feeder` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Feeder` with the same `mrid` already exists for this `Substation`.
        """
        self.normal_energized_feeders.add(feeder)
        return self

    def remove_feeder(self, feeder: Feeder) -> Substation:
        """
        Disassociate `feeder` from this `Substation`

        `feeder` The `Feeder` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `feeder` was not associated with this `Substation`.
        """
        self.normal_energized_feeders.remove(feeder)
        return self

    def clear_feeders(self) -> Substation:
        """
        Clear all current `Feeder`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self.normal_energized_feeders.clear()
        return self

    def num_loops(self):
        """
        Returns The number of `Loop`s associated with this `Substation`
        """
        return len(self.loops)

    def get_loop(self, mrid: str) -> Loop:
        """
        Get the `Loop` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Loop`
        Returns The `Loop` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.loops.get_by_mrid(mrid)

    def add_loop(self, loop: Loop) -> Substation:
        """
        Associate a `Loop` with this `Substation`

        `loop` The `Loop` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Loop` with the same `mrid` already exists for this `Substation`.
        """
        self.loops.add(loop)
        return self

    def remove_loop(self, loop: Loop) -> Substation:
        """
        Disassociate `loop` from this `Substation`

        `loop` The `Loop` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `loop` was not associated with this `Substation`.
        """
        self.loops.remove(loop)
        return self

    def clear_loops(self) -> Substation:
        """
        Clear all current `Loop`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self.loops.clear()
        return self

    def num_energized_loops(self):
        """
        Returns The number of `Loop`s associated with this `Substation`
        """
        return len(self.energized_loops)

    def get_energized_loop(self, mrid: str) -> Loop:
        """
        Get the `Loop` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Loop`
        Returns The `Loop` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.energized_loops.get_by_mrid(mrid)

    def add_energized_loop(self, loop: Loop) -> Substation:
        """
        Associate a `Loop` with this `Substation`

        `loop` The `Loop` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Loop` with the same `mrid` already exists for this `Substation`.
        """
        self.energized_loops.add(loop)
        return self

    def remove_energized_loop(self, loop: Loop) -> Substation:
        """
        Disassociate `loop` from this `Substation`

        `loop` The `Loop` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `loop` was not associated with this `Substation`.
        """
        self.energized_loops.remove(loop)
        return self

    def clear_energized_loops(self) -> Substation:
        """
        Clear all current `Loop`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self.energized_loops.clear()
        return self

    def num_circuits(self):
        """
        Returns The number of `Circuit`s associated with this `Substation`
        """
        return len(self.circuits)

    def get_circuit(self, mrid: str) -> Circuit:
        """
        Get the `Circuit` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Circuit`
        Returns The `Circuit` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.circuits.get_by_mrid(mrid)

    def add_circuit(self, circuit: Circuit) -> Substation:
        """
        Associate a `Circuit` with this `Substation`

        `circuit` The `Circuit` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Circuit` with the same `mrid` already exists for this `Substation`.
        """
        self.circuits.add(circuit)
        return self

    def remove_circuit(self, circuit: Circuit) -> Substation:
        """
        Disassociate `circuit` from this `Substation`

        `circuit` The `Circuit` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `circuit` was not associated with this `Substation`.
        """
        self.circuits.remove(circuit)
        return self

    def clear_circuits(self) -> Substation:
        """
        Clear all current `Circuit`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self.circuits.clear()
        return self
