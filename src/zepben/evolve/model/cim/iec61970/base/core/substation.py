#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Loop, Circuit, Feeder

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.evolve.model.cim.iec61970.base.core.regions import SubGeographicalRegion
from zepben.evolve.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["Substation"]


class Substation(EquipmentContainer):
    """
    A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk
    is passed for the purposes of switching or modifying its characteristics.
    """

    sub_geographical_region: Optional[SubGeographicalRegion] = None
    """The SubGeographicalRegion containing the substation."""

    _normal_energized_feeders: Optional[List[Feeder]] = None

    _loops: Optional[List[Loop]] = None

    _energized_loops: Optional[List[Loop]] = None

    _circuits: Optional[List[Circuit]] = None

    def __init__(self, normal_energized_feeders: List[Feeder] = None, loops: List[Loop] = None, energized_loops: List[Loop] = None,
                 circuits: List[Circuit] = None, **kwargs):
        super(Substation, self).__init__(**kwargs)
        if normal_energized_feeders:
            for feeder in normal_energized_feeders:
                self.add_feeder(feeder)
        if loops:
            for loop in loops:
                self.add_loop(loop)
        if energized_loops:
            for loop in energized_loops:
                self.add_energized_loop(loop)
        if circuits:
            for circuit in circuits:
                self.add_circuit(circuit)

    @property
    def circuits(self) -> Generator[Circuit, None, None]:
        """
        The `Circuit`s originating from this substation.
        """
        return ngen(self._circuits)

    @property
    def loops(self) -> Generator[Loop, None, None]:
        """
        The `Loop` originating from this substation.
        """
        return ngen(self._loops)

    @property
    def energized_loops(self) -> Generator[Loop, None, None]:
        """
        The `Loop`s originating from this substation that are energised.
        """
        return ngen(self._energized_loops)

    @property
    def feeders(self) -> Generator[Feeder, None, None]:
        """
        The normal energized feeders of the substation. Also used for naming purposes.
        """
        return ngen(self._normal_energized_feeders)

    def num_feeders(self):
        """
        Returns The number of `Feeder`s associated with this `Substation`
        """
        return nlen(self._normal_energized_feeders)

    def get_feeder(self, mrid: str) -> Feeder:
        """
        Get the `Feeder` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Feeder`
        Returns The `Feeder` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._normal_energized_feeders, mrid)

    def add_feeder(self, feeder: Feeder) -> Substation:
        """
        Associate a `Feeder` with this `Substation`

        `feeder` The `Feeder` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Feeder` with the same `mrid` already exists for this `Substation`.
        """
        if self._validate_reference(feeder, self.get_feeder, "A Feeder"):
            return self
        self._normal_energized_feeders = list() if self._normal_energized_feeders is None else self._normal_energized_feeders
        self._normal_energized_feeders.append(feeder)
        return self

    def remove_feeder(self, feeder: Feeder) -> Substation:
        """
        Disassociate `feeder` from this `Substation`

        `feeder` The `Feeder` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `feeder` was not associated with this `Substation`.
        """
        self._normal_energized_feeders = safe_remove(self._normal_energized_feeders, feeder)
        return self

    def clear_feeders(self) -> Substation:
        """
        Clear all current `Feeder`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self._normal_energized_feeders = None
        return self

    def num_loops(self):
        """
        Returns The number of `Loop`s associated with this `Substation`
        """
        return nlen(self._loops)

    def get_loop(self, mrid: str) -> Loop:
        """
        Get the `Loop` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Loop`
        Returns The `Loop` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._loops, mrid)

    def add_loop(self, loop: Loop) -> Substation:
        """
        Associate a `Loop` with this `Substation`

        `loop` The `Loop` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Loop` with the same `mrid` already exists for this `Substation`.
        """
        if self._validate_reference(loop, self.get_loop, "A Loop"):
            return self
        self._loops = list() if self._loops is None else self._loops
        self._loops.append(loop)
        return self

    def remove_loop(self, loop: Loop) -> Substation:
        """
        Disassociate `loop` from this `Substation`

        `loop` The `Loop` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `loop` was not associated with this `Substation`.
        """
        self._loops = safe_remove(self._loops, loop)
        return self

    def clear_loops(self) -> Substation:
        """
        Clear all current `Loop`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self._loops = None
        return self

    def num_energized_loops(self):
        """
        Returns The number of `Loop`s associated with this `Substation`
        """
        return nlen(self._energized_loops)

    def get_energized_loop(self, mrid: str) -> Loop:
        """
        Get the `Loop` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Loop`
        Returns The `Loop` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._energized_loops, mrid)

    def add_energized_loop(self, loop: Loop) -> Substation:
        """
        Associate a `Loop` with this `Substation`

        `loop` The `Loop` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Loop` with the same `mrid` already exists for this `Substation`.
        """
        if self._validate_reference(loop, self.get_energized_loop, "A Loop"):
            return self
        self._energized_loops = list() if self._energized_loops is None else self._energized_loops
        self._energized_loops.append(loop)
        return self

    def remove_energized_loop(self, loop: Loop) -> Substation:
        """
        Disassociate `loop` from this `Substation`

        `loop` The `Loop` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `loop` was not associated with this `Substation`.
        """
        self._energized_loops = safe_remove(self._energized_loops, loop)
        return self

    def clear_energized_loops(self) -> Substation:
        """
        Clear all current `Loop`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self._energized_loops = None
        return self

    def num_circuits(self):
        """
        Returns The number of `Circuit`s associated with this `Substation`
        """
        return nlen(self._circuits)

    def get_circuit(self, mrid: str) -> Circuit:
        """
        Get the `Circuit` for this `Substation` identified by `mrid`

        `mrid` The mRID of the required `Circuit`
        Returns The `Circuit` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._circuits, mrid)

    def add_circuit(self, circuit: Circuit) -> Substation:
        """
        Associate a `Circuit` with this `Substation`

        `circuit` The `Circuit` to associate with this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if another `Circuit` with the same `mrid` already exists for this `Substation`.
        """
        if self._validate_reference(circuit, self.get_circuit, "A Circuit"):
            return self
        self._circuits = list() if self._circuits is None else self._circuits
        self._circuits.append(circuit)
        return self

    def remove_circuit(self, circuit: Circuit) -> Substation:
        """
        Disassociate `circuit` from this `Substation`

        `circuit` The `Circuit` to disassociate from this `Substation`.
        Returns A reference to this `Substation` to allow fluent use.
        Raises `ValueError` if `circuit` was not associated with this `Substation`.
        """
        self._circuits = safe_remove(self._circuits, circuit)
        return self

    def clear_circuits(self) -> Substation:
        """
        Clear all current `Circuit`s.
        Returns A reference to this `Substation` to allow fluent use.
        """
        self._circuits = None
        return self
