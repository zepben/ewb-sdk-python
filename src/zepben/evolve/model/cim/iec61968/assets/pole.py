#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Optional, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Streetlight

from zepben.evolve.model.cim.iec61968.assets.structure import Structure
from zepben.evolve.util import get_by_mrid, ngen, nlen, safe_remove

__all__ = ["Pole"]


class Pole(Structure):
    """A Pole Asset"""

    classification: str = ""
    """Pole class: 1, 2, 3, 4, 5, 6, 7, H1, H2, Other, Unknown."""

    _streetlights: Optional[List[Streetlight]] = None

    def __init__(self, streetlights: List[Streetlight] = None, **kwargs):
        super(Pole, self).__init__(**kwargs)
        if streetlights:
            for light in streetlights:
                self.add_streetlight(light)

    def num_streetlights(self) -> int:
        """
        Get the number of `Streetlight`s associated with this `Pole`.
        """
        return nlen(self._streetlights)

    @property
    def streetlights(self) -> Generator[Streetlight, None, None]:
        """
        The `Streetlight`s of this `Pole`.
        """
        return ngen(self._streetlights)

    def get_streetlight(self, mrid: str) -> Streetlight:
        """
        Get the `Streetlight` for this asset identified by `mrid`.

        `mrid` the mRID of the required `Streetlight`
        Returns The `Streetlight` with the specified `mrid`.
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._streetlights, mrid)

    def add_streetlight(self, streetlight: Streetlight) -> Pole:
        """
        Associate a `Streetlight` with this `Pole`

        `streetlight` the `Streetlight` to associate with this `Pole`.
        Returns A reference to this `Pole` to allow fluent use.
        Raises `ValueError` if another `Streetlight` with the same `mrid` already exists in this `Pole`
        """
        if self._validate_reference(streetlight, self.get_streetlight, "A Streetlight"):
            return self

        self._streetlights = list() if self._streetlights is None else self._streetlights
        self._streetlights.append(streetlight)
        return self

    def remove_streetlight(self, streetlight: Streetlight) -> Pole:
        """
        Disassociate `streetlight` from this `Pole`
        `streetlight` the `Streetlight` to disassociate from this `Pole`.
        Raises `ValueError` if `streetlight` was not associated with this `Pole`.
        Returns A reference to this `Pole` to allow fluent use.
        """
        self._streetlights = safe_remove(self._streetlights, streetlight)
        return self

    def clear_streetlights(self) -> Pole:
        """
        Clear all Streetlights.
        Returns self
        """
        self._streetlights = None
        return self
