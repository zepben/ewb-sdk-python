#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Circuit, Substation

__all__ = ["Loop"]

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.util import safe_remove, ngen, nlen, get_by_mrid


class Loop(IdentifiedObject):
    """Missing description"""

    _circuits: Optional[List[Circuit]] = None
    _substations: Optional[List[Substation]] = None
    _energizing_substations: Optional[List[Substation]] = None

    def __init__(self, circuits: List[Circuit] = None, substations: List[Substation] = None, energizing_substations: List[Substation] = None, **kwargs):
        super(Loop, self).__init__(**kwargs)
        if circuits:
            for term in circuits:
                self.add_circuit(term)

        if substations:
            for sub in substations:
                self.add_substation(sub)

        if energizing_substations:
            for sub in energizing_substations:
                self.add_energizing_substation(sub)

    @property
    def circuits(self) -> Generator[Circuit, None, None]:
        """
        Sub-transmission `Circuit`s that form part of this loop.
        """
        return ngen(self._circuits)

    @property
    def substations(self) -> Generator[Substation, None, None]:
        """
        The `Substation`s that are powered by this `Loop`.
        """
        return ngen(self._substations)

    @property
    def energizing_substations(self) -> Generator[Substation, None, None]:
        """
        The `Substation`s that normally energize this `Loop`.
        """
        return ngen(self._energizing_substations)

    def num_circuits(self):
        """Return the number of end `Circuit`s associated with this `Loop`"""
        return nlen(self._circuits)

    def get_circuit(self, mrid: str) -> Circuit:
        """
        Get the `Circuit` for this `Loop` identified by `mrid`

        `mrid` the mRID of the required `Circuit`
        Returns The `Circuit` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._circuits, mrid)

    def add_circuit(self, circuit: Circuit) -> Loop:
        """
        Associate an `Circuit` with this `Loop`

        `circuit` the `Circuit` to associate with this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if another `Circuit` with the same `mrid` already exists for this `Loop`.
        """
        if self._validate_reference(circuit, self.get_circuit, "An Circuit"):
            return self
        self._circuits = list() if self._circuits is None else self._circuits
        self._circuits.append(circuit)
        return self

    def remove_circuit(self, circuit: Circuit) -> Loop:
        """
        Disassociate `circuit` from this `Loop`

        `circuit` the `Circuit` to disassociate from this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if `circuit` was not associated with this `Loop`.
        """
        self._circuits = safe_remove(self._circuits, circuit)
        return self

    def clear_circuits(self) -> Loop:
        """
        Clear all end circuits.
        Returns A reference to this `Loop` to allow fluent use.
        """
        self._circuits = None
        return self

    def num_substations(self):
        """Return the number of end `Substation`s associated with this `Loop`"""
        return nlen(self._substations)

    def get_substation(self, mrid: str) -> Substation:
        """
        Get the `Substation` for this `Loop` identified by `mrid`

        `mrid` the mRID of the required `Substation`
        Returns The `Substation` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._substations, mrid)

    def add_substation(self, substation: Substation) -> Loop:
        """
        Associate an `Substation` with this `Loop`

        `substation` the `Substation` to associate with this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if another `Substation` with the same `mrid` already exists for this `Loop`.
        """
        if self._validate_reference(substation, self.get_substation, "An Substation"):
            return self
        self._substations = list() if self._substations is None else self._substations
        self._substations.append(substation)
        return self

    def remove_substation(self, substation: Substation) -> Loop:
        """
        Disassociate `substation` from this `Loop`

        `substation` the `Substation` to disassociate from this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if `substation` was not associated with this `Loop`.
        """
        self._substations = safe_remove(self._substations, substation)
        return self

    def clear_substations(self) -> Loop:
        """
        Clear all end substations.
        Returns A reference to this `Loop` to allow fluent use.
        """
        self._substations = None
        return self

    def num_energizing_substations(self):
        """Return the number of end `Substation`s associated with this `Loop`"""
        return nlen(self._energizing_substations)

    def get_energizing_substation(self, mrid: str) -> Substation:
        """
        Get the `Substation` for this `Loop` identified by `mrid`

        `mrid` the mRID of the required `Substation`
        Returns The `Substation` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._energizing_substations, mrid)

    def add_energizing_substation(self, substation: Substation) -> Loop:
        """
        Associate an `Substation` with this `Loop`

        `substation` the `Substation` to associate with this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if another `Substation` with the same `mrid` already exists for this `Loop`.
        """
        if self._validate_reference(substation, self.get_energizing_substation, "An Substation"):
            return self
        self._energizing_substations = list() if self._energizing_substations is None else self._energizing_substations
        self._energizing_substations.append(substation)
        return self

    def remove_energizing_substation(self, substation: Substation) -> Loop:
        """
        Disassociate `substation` from this `Loop`

        `substation` the `Substation` to disassociate from this `Loop`.
        Returns A reference to this `Loop` to allow fluent use.
        Raises `ValueError` if `substation` was not associated with this `Loop`.
        """
        self._energizing_substations = safe_remove(self._energizing_substations, substation)
        return self

    def clear_energizing_substations(self) -> Loop:
        """
        Clear all end energizing_substations.
        Returns A reference to this `Loop` to allow fluent use.
        """
        self._energizing_substations = None
        return self
