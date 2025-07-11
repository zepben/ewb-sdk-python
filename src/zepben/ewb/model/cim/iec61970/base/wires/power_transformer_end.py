#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformerEnd"]

import warnings
from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_cooling_type import TransformerCoolingType
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_end_rated_s import TransformerEndRatedS
from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import TransformerEnd
from zepben.ewb.model.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.util import ngen, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import PowerTransformer


class PowerTransformerEnd(TransformerEnd):
    """
    A PowerTransformerEnd is associated with each Terminal of a PowerTransformer.

    The impedance values r, r0, x, and x0 of a PowerTransformerEnd represents a star equivalent as follows

    1) for a two Terminal PowerTransformer the high voltage PowerTransformerEnd has non-zero values on r, r0, x, and x0
    while the low voltage PowerTransformerEnd has zero values for r, r0, x, and x0.
    2) for a three Terminal PowerTransformer the three PowerTransformerEnds represents a star equivalent with each leg
    in the star represented by r, r0, x, and x0 values.
    3) For a three Terminal transformer each PowerTransformerEnd shall have g, g0, b and b0 values corresponding the no load losses
    distributed on the three PowerTransformerEnds. The total no load loss shunt impedances may also be placed at one of the
    PowerTransformerEnds, preferably the end numbered 1, having the shunt values on end 1 is the preferred way.
    4) for a PowerTransformer with more than three Terminals the PowerTransformerEnd impedance values cannot be used.
    Instead use the TransformerMeshImpedance or split the transformer into multiple PowerTransformers.
    """

    _power_transformer: Optional[PowerTransformer] = None
    """The power transformer of this power transformer end."""
    _rated_s: Optional[int] = None

    rated_u: Optional[int] = None
    """Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings. A high voltage side, as given by 
    TransformerEnd.endNumber, shall have a ratedU that is greater or equal than ratedU for the lower voltage sides."""

    r: Optional[float] = None
    """Resistance (star-phases) of the transformer end. The attribute shall be equal or greater than zero for non-equivalent transformers."""

    x: Optional[float] = None
    """Positive sequence series reactance (star-phases) of the transformer end."""

    r0: Optional[float] = None
    """Zero sequence series resistance (star-phases) of the transformer end."""

    x0: Optional[float] = None
    """Zero sequence series reactance of the transformer end."""

    g: Optional[float] = None
    """Magnetizing branch conductance."""

    g0: Optional[float] = None
    """Zero sequence magnetizing branch conductance (star-phases)."""

    b: Optional[float] = None
    """Magnetizing branch susceptance (B mag).  The value can be positive or negative."""

    b0: Optional[float] = None
    """Zero sequence magnetizing branch susceptance."""

    connection_kind: WindingConnection = WindingConnection.UNKNOWN
    """Kind of `zepben.protobuf.cim.iec61970.base.wires.winding_connection.WindingConnection` for this end."""

    phase_angle_clock: Optional[int] = None
    """Terminal voltage phase angle displacement where 360 degrees are represented with clock hours. The valid values are 0 to 11. For example, for the 
    secondary side end of a transformer with vector group code of 'Dyn11', specify the connection kind as wye with neutral and specify the phase angle of the 
    clock as 11. The clock value of the transformer end number specified as 1, is assumed to be zero."""

    _s_ratings: Optional[List[TransformerEndRatedS]] = None
    """
    Backing list for storing transformer ratings. Placed here to not mess with __init__ param order. Must always be placed at the end.
    Should not be used directly, instead use add_rating and get_rating functions. 
    """

    def __init__(self, power_transformer: PowerTransformer = None, rated_s: int = None, **kwargs):
        super(PowerTransformerEnd, self).__init__(**kwargs)
        if power_transformer:
            self.power_transformer = power_transformer
        if self._s_ratings:
            raise ValueError("Do not directly set s_ratings through the constructor. You have one more constructor parameter than expected.")
        if rated_s and self._rated_s:
            raise ValueError(f"Cannot specify both rated_s and _rated_s properties when constructing {self}. Check your constructor parameters.")
        if rated_s is not None:
            warnings.warn(
                "`rated_s` has been replaced by `s_ratings`. Please use `add_rating()` to add one of more ratings and their related [TransformerCoolingType].",
                DeprecationWarning,
                stacklevel=3
            )
            self.rated_s = rated_s
        if self._rated_s is not None:
            self.rated_s = self._rated_s
            self._rated_s = None

    @property
    def power_transformer(self):
        """The power transformer of this power transformer end."""
        return self._power_transformer

    @power_transformer.setter
    def power_transformer(self, pt):
        if self._power_transformer is None or self._power_transformer is pt:
            self._power_transformer = pt
        else:
            raise ValueError(f"power_transformer for {str(self)} has already been set to {self._power_transformer}, cannot reset this field to {pt}")

    @property
    def nominal_voltage(self):
        return self.base_voltage.nominal_voltage if self.base_voltage else self.rated_u

    @property
    def rated_s(self) -> Optional[int]:
        """
        Normal apparent power rating. The attribute shall be a positive value. For a two-winding transformer the values for the high and low voltage sides
        shall be identical.
        """
        if self._s_ratings:
            return self._s_ratings[0].rated_s if len(self._s_ratings) > 0 else None
        return None

    @rated_s.setter
    def rated_s(self, rated_s: Optional[int]):
        warnings.warn(
            "`rated_s` has been replaced by `s_ratings` and is only for backward compatibility. Setting `rated_s`, will clear any other ratings.",
            DeprecationWarning,
            stacklevel=2
        )
        self.clear_ratings()
        if rated_s is not None:
            self.add_transformer_end_rated_s(TransformerEndRatedS(TransformerCoolingType.UNKNOWN, rated_s))

    @property
    def s_ratings(self) -> Generator[TransformerEndRatedS, None, None]:
        return ngen(self._s_ratings)

    def num_ratings(self) -> int:
        return nlen(self._s_ratings)

    def get_rating(self, cooling_type: TransformerCoolingType) -> TransformerEndRatedS:
        if self._s_ratings:
            for s_rating in self._s_ratings:
                if s_rating.cooling_type == cooling_type:
                    return s_rating
        raise KeyError(cooling_type)

    def add_rating(self, rated_s: int, cooling_type: TransformerCoolingType = TransformerCoolingType.UNKNOWN) -> PowerTransformerEnd:
        self._s_ratings = self._s_ratings if self._s_ratings else list()

        for s_rating in self._s_ratings:
            if s_rating.cooling_type == cooling_type:
                raise ValueError(f"A rating for coolingType {cooling_type.name} already exists, please remove it first.")

        self._s_ratings.append(TransformerEndRatedS(cooling_type, rated_s))

        def sort_by_rated_s(t: TransformerEndRatedS) -> int:
            return t.rated_s

        self._s_ratings.sort(key=sort_by_rated_s, reverse=True)

        return self

    def add_transformer_end_rated_s(self, transformer_end_rated_s: TransformerEndRatedS) -> PowerTransformerEnd:
        return self.add_rating(transformer_end_rated_s.rated_s, transformer_end_rated_s.cooling_type)

    def remove_rating(self, transformer_end_rated_s: TransformerEndRatedS) -> PowerTransformerEnd:
        self._s_ratings = safe_remove(self._s_ratings, transformer_end_rated_s)
        return self

    def remove_rating_by_cooling_type(self, cooling_type: TransformerCoolingType) -> TransformerEndRatedS:
        if self._s_ratings:
            for transformer_end_rated_s in self._s_ratings:
                if transformer_end_rated_s.cooling_type == cooling_type:
                    self._s_ratings.remove(transformer_end_rated_s)
                    self._s_ratings = self._s_ratings if self._s_ratings else None
                    return transformer_end_rated_s
        raise IndexError(cooling_type)

    def clear_ratings(self) -> PowerTransformerEnd:
        self._s_ratings = None
        return self

    def resistance_reactance(self):
        """
        Get the `ResistanceReactance` for this `PowerTransformerEnd` from either:
        1. directly assigned values or
        2. the pre-calculated `starImpedance` or
        3. from the datasheet information of the associated `powerTransformer`

        If the data is not complete in any of the above it will merge in the missing values from the subsequent sources.
        :return:
        """
        ResistanceReactance(self.r, self.x, self.r0, self.x0).merge_if_incomplete(
            lambda: self.star_impedance.resistance_reactance() if self.star_impedance is not None else None
        ).merge_if_incomplete(
            lambda: self.power_transformer.power_transformer_info.resistance_reactance(self.end_number) if self.power_transformer.asset_info is not None
            else None
        )
