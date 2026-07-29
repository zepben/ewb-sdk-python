#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformerEnd"]

import warnings
from dataclasses import field
from typing import Optional, List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.boilerplate.backfill import internal
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_cooling_type import TransformerCoolingType
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_end_rated_s import TransformerEndRatedS
from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import TransformerEnd
from zepben.ewb.model.cim.iec61970.base.wires.winding_connection import WindingConnection
from zepben.ewb.boilerplate.relations.transformer_end_rated_s_list import TransformerEndRatedSList
from zepben.ewb.model.resistance_reactance import ResistanceReactance
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import PowerTransformer


@zb_dataclass
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

    _power_transformer: Optional[PowerTransformer] = field(default=None)
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

    _s_ratings: Optional[List[TransformerEndRatedS]] = field(default=None)
    """
    Backing list for storing transformer ratings. Placed here to not mess with __init__ param order. Must always be placed at the end.
    Should not be used directly, instead use add_rating and get_rating functions. 
    """

    def __init__(self, *args, rated_s: int = None, ratings=None, **kwargs):
        super(PowerTransformerEnd, self).__init__(*args, **kwargs)
        self.s_ratings.extend(ratings)
        if "_s_ratings" in kwargs:
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
    @internal(_power_transformer)
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
        if self._s_ratings and len(self._s_ratings) > 0:
            return self._s_ratings[0].rated_s
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

    s_ratings: TransformerEndRatedSList = TransformerEndRatedSList(
        _s_ratings,
        validate=lambda self, it: self._validate_rating(it),
        sort_by=lambda it: -it.rated_s
    )

    def _validate_rating(self, rating: TransformerEndRatedS):
        if any(it.cooling_type == rating.cooling_type for it in self.s_ratings):
            raise ValueError(f"A rating for coolingType {rating.cooling_type.name} already exists, please remove it first.")

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

    # region deprecated list methods

    # region s_ratings boilerplate

    @deprecated("Use len(s_ratings) instead.")
    def num_ratings(self) -> int:
        return len(self.s_ratings)

    @deprecated("Use s_ratings.get_by_cooling_type(cooling_type) instead.")
    def get_rating(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS:
        rating = self.s_ratings.get_by_cooling_type(cooling_type)

        if rating is None:
            raise KeyError(cooling_type)

        return rating

    @deprecated("Use s_ratings.append(TransformerEndRatedS(cooling_type, rated_s)) instead.")
    def add_rating(
        self,
        rated_s: int,
        cooling_type: TransformerCoolingType = TransformerCoolingType.UNKNOWN,
    ) -> PowerTransformerEnd:
        self.s_ratings.append(TransformerEndRatedS(cooling_type, rated_s))
        return self

    @deprecated("Use s_ratings.append(transformer_end_rated_s) instead.")
    def add_transformer_end_rated_s(
        self,
        transformer_end_rated_s: TransformerEndRatedS,
    ) -> PowerTransformerEnd:
        self.s_ratings.append(transformer_end_rated_s)
        return self

    @deprecated("Use s_ratings.remove(transformer_end_rated_s) instead.")
    def remove_rating(
        self,
        transformer_end_rated_s: TransformerEndRatedS,
    ) -> PowerTransformerEnd:
        self.s_ratings.remove(transformer_end_rated_s)
        return self

    @deprecated("Use s_ratings.remove_by_cooling_type(cooling_type) instead.")
    def remove_rating_by_cooling_type(
        self,
        cooling_type: TransformerCoolingType,
    ) -> TransformerEndRatedS:
        rating = self.s_ratings.remove_by_cooling_type(cooling_type)

        if rating is None:
            raise IndexError(cooling_type)

        return rating

    @deprecated("Use s_ratings.clear() instead.")
    def clear_ratings(self) -> PowerTransformerEnd:
        self.s_ratings.clear()
        return self

    # endregion

    # endregion