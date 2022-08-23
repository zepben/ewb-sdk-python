#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Substation, Terminal, Loop
from zepben.evolve.model.cim.iec61970.base.wires.line import Line
from zepben.evolve.util import ngen, get_by_mrid, safe_remove, nlen

__all__ = ["Circuit"]


class Circuit(Line):
    """Missing description"""

    loop: Optional[Loop] = None
    _end_terminals: Optional[List[Terminal]] = None
    _end_substations: Optional[List[Substation]] = None

    def __init__(self, end_terminals: List[Terminal] = None, end_substations: List[Substation] = None, **kwargs):
        super(Circuit, self).__init__(**kwargs)
        if end_terminals:
            for term in end_terminals:
                self.add_end_terminal(term)

        if end_substations:
            for sub in end_substations:
                self.add_end_substation(sub)

    @property
    def end_terminals(self) -> Generator[Terminal, None, None]:
        """
        The `Terminal`s representing the ends for this `Circuit`.
        """
        return ngen(self._end_terminals)

    @property
    def end_substations(self) -> Generator[Substation, None, None]:
        """
        The `Substations`s representing the ends for this `Circuit`.
        """
        return ngen(self._end_substations)

    def num_end_terminals(self):
        """Return the number of end `Terminal`s associated with this `Circuit`"""
        return nlen(self._end_terminals)

    def get_end_terminal(self, mrid: str) -> Terminal:
        """
        Get the `Terminal` for this `Circuit` identified by `mrid`

        `mrid` the mRID of the required `Terminal`
        Returns The `Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._end_terminals, mrid)

    def add_end_terminal(self, terminal: Terminal) -> Circuit:
        """
        Associate an `Terminal` with this `Circuit`

        `terminal` the `Terminal` to associate with this `Circuit`.
        Returns A reference to this `Circuit` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `Circuit`.
        """
        if self._validate_reference(terminal, self.get_end_terminal, "An Terminal"):
            return self
        self._end_terminals = list() if self._end_terminals is None else self._end_terminals
        self._end_terminals.append(terminal)
        return self

    def remove_end_terminal(self, terminal: Terminal) -> Circuit:
        """
        Disassociate `terminal` from this `Circuit`

        `terminal` the `Terminal` to disassociate from this `Circuit`.
        Returns A reference to this `Circuit` to allow fluent use.
        Raises `ValueError` if `terminal` was not associated with this `Circuit`.
        """
        self._end_terminals = safe_remove(self._end_terminals, terminal)
        return self

    def clear_end_terminals(self) -> Circuit:
        """
        Clear all end terminals.
        Returns A reference to this `Circuit` to allow fluent use.
        """
        self._end_terminals = None
        return self

    def num_end_substations(self):
        """Return the number of end `Substation`s associated with this `Circuit`"""
        return nlen(self._end_substations)

    def get_end_substation(self, mrid: str) -> Substation:
        """
        Get the `Substation` for this `Circuit` identified by `mrid`

        `mrid` the mRID of the required `Substation`
        Returns The `Substation` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._end_substations, mrid)

    def add_end_substation(self, substation: Substation) -> Circuit:
        """
        Associate an `Substation` with this `Circuit`

        `substation` the `Substation` to associate with this `Circuit`.
        Returns A reference to this `Circuit` to allow fluent use.
        Raises `ValueError` if another `Substation` with the same `mrid` already exists for this `Circuit`.
        """
        if self._validate_reference(substation, self.get_end_substation, "An Substation"):
            return self
        self._end_substations = list() if self._end_substations is None else self._end_substations
        self._end_substations.append(substation)
        return self

    def remove_end_substation(self, substation: Substation) -> Circuit:
        """
        Disassociate `substation` from this `Circuit`

        `substation` the `Substation` to disassociate from this `Circuit`.
        Returns A reference to this `Circuit` to allow fluent use.
        Raises `ValueError` if `substation` was not associated with this `Circuit`.
        """
        self._end_substations = safe_remove(self._end_substations, substation)
        return self

    def clear_end_substations(self) -> Circuit:
        """
        Clear all end substations.
        Returns A reference to this `Circuit` to allow fluent use.
        """
        self._end_substations = None
        return self
