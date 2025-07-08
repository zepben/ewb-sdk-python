#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformer"]

from typing import List, Optional, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.extensions.iec61970.base.wires.vector_group import VectorGroup
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import TransformerConstructionKind
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import TransformerFunctionKind
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.util import require, nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd


class PowerTransformer(ConductingEquipment):
    """
    An electrical device consisting of  two or more coupled windings, with or without a magnetic core, for introducing
    mutual coupling between electric circuits.

    Transformers can be used to control voltage and phase shift (active power flow). A power transformer may be composed of separate transformer tanks that
    need not be identical. A power transformer can be modeled with or without tanks and is intended for use in both balanced and unbalanced representations.

    A power transformer typically has two terminals, but may have one (grounding), three or more terminals.

    The inherited association ConductingEquipment.BaseVoltage should not be used.
    The association from TransformerEnd to BaseVoltage should be used instead.

    Attributes -
        vector_group : `zepben.protobuf.cim.iec61970.base.wires.VectorGroup` of the transformer for protective relaying.
        power_transformer_ends : 
                                 
                                 
    """
    vector_group: VectorGroup = VectorGroup.UNKNOWN
    """
    Vector group of the transformer for protective relaying, e.g., Dyn1. For unbalanced transformers, this may not be simply
    determined from the constituent winding connections and phase angle displacements.
                                                                                                                            
    The vectorGroup string consists of the following components in the order listed: high voltage winding connection, mid
    voltage winding connection(for three winding transformers), phase displacement clock number from 0 to 11,  low voltage
    winding connection phase displacement clock number from 0 to 11.   The winding connections are D(delta), Y(wye),
    YN(wye with neutral), Z(zigzag), ZN(zigzag with neutral), A(auto transformer). Upper case means the high voltage,
    lower case mid or low.The high voltage winding always has clock position 0 and is not included in the vector group
    string.  Some examples: YNy0(two winding wye to wye with no phase displacement), YNd11(two winding wye to delta with
    330 degrees phase displacement), YNyn0d5(three winding transformer wye with neutral high voltage, wye with neutral mid
    voltage and no phase displacement, delta low voltage with 150 degrees displacement).
                                                                                                                            
    Phase displacement is defined as the angular difference between the phasors representing the voltages between the
    neutral point(real or imaginary) and the corresponding terminals of two windings, a positive sequence voltage system
    being applied to the high-voltage terminals, following each other in alphabetical sequence if they are lettered, or in
    numerical sequence if they are numbered: the phasors are assumed to rotate in a counter-clockwise sense.
    """

    _power_transformer_ends: Optional[List[PowerTransformerEnd]] = None

    transformer_utilisation: Optional[float] = None
    """
    The fraction of the transformer’s normal capacity (nameplate rating) that is in use. It may be expressed as the
    result of the calculation S/Sn, where S = Load on Transformer (in VA), Sn = Transformer Nameplate Rating (in VA).
    """

    construction_kind: TransformerConstructionKind = TransformerConstructionKind.unknown
    """
    The construction kind of this transformer.
    """

    function: TransformerFunctionKind = TransformerFunctionKind.other
    """
    The function of this transformer.
    """

    def __init__(self, power_transformer_ends: List[PowerTransformerEnd] = None, **kwargs):
        super(PowerTransformer, self).__init__(**kwargs)
        if power_transformer_ends:
            for end in power_transformer_ends:
                if end.power_transformer is None:
                    end.power_transformer = self
                self.add_end(end)

    def num_ends(self):
        """
        Get the number of `PowerTransformerEnd`s for this `PowerTransformer`.
        """
        return nlen(self._power_transformer_ends)

    @property
    def ends(self) -> Generator[PowerTransformerEnd, None, None]:
        """The `PowerTransformerEnd`s for this `PowerTransformer`."""
        return ngen(self._power_transformer_ends)

    @property
    def power_transformer_info(self) -> Optional[PowerTransformerInfo]:
        """The `PowerTransformerInfo` for this `PowerTransformer`"""
        return self.asset_info

    @power_transformer_info.setter
    def power_transformer_info(self, pti: Optional[PowerTransformerInfo]):
        """
        Set the `PowerTransformerInfo` for this `PowerTransformer`
        `pti` The `PowerTransformerInfo` to associate with this `PowerTransformer`
        """
        self.asset_info = pti

    def get_base_voltage(self, terminal: Terminal = None):
        if terminal is None:
            return self.base_voltage
        for end in self.ends:
            if end.terminal is terminal:
                return end.base_voltage
        else:
            return None

    def get_end_by_mrid(self, mrid: str) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` for this `PowerTransformer` identified by `mrid`

        `mrid` the mRID of the required `PowerTransformerEnd`
        Returns The `PowerTransformerEnd` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_transformer_ends, mrid)

    def get_end_by_num(self, end_number: int) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` on this `PowerTransformer` by its `end_number`.

        `end_number` The `end_number` of the `PowerTransformerEnd` in relation to this `PowerTransformer`s VectorGroup.
        Returns The `PowerTransformerEnd` referred to by `end_number`
        Raises IndexError if no `PowerTransformerEnd` was found with end_number `end_number`.
        """
        if self._power_transformer_ends:
            for end in self._power_transformer_ends:
                if end.end_number == end_number:
                    return end
        raise IndexError(f"No TransformerEnd with end_number {end_number} was found in PowerTransformer {str(self)}")

    def get_end_by_terminal(self, terminal: Terminal) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` on this `PowerTransformer` by its `terminal`.

        `terminal` The `terminal` to find a `PowerTransformerEnd` for.
        Returns The `PowerTransformerEnd` connected to the specified `terminal`
        Raises IndexError if no `PowerTransformerEnd` connected to `terminal` was found on this `PowerTransformer`.
        """
        if self._power_transformer_ends:
            for end in self._power_transformer_ends:
                if end.terminal is terminal:
                    return end
        raise IndexError(f"No TransformerEnd with terminal {terminal} was found in PowerTransformer {str(self)}")

    def add_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        Associate a `PowerTransformerEnd` with this `PowerTransformer`. If `end.end_number` == 0, the end will be assigned an end_number of
        `self.num_ends() + 1`.

        `end` the `PowerTransformerEnd` to associate with this `PowerTransformer`.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        Raises `ValueError` if another `PowerTransformerEnd` with the same `mrid` already exists for this `PowerTransformer`.
        """
        if self._validate_end(end):
            return self

        if end.end_number == 0:
            end.end_number = self.num_ends() + 1

        self._power_transformer_ends = list() if self._power_transformer_ends is None else self._power_transformer_ends
        self._power_transformer_ends.append(end)
        self._power_transformer_ends.sort(key=lambda t: t.end_number)
        return self

    def remove_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        """
        `end` the `PowerTransformerEnd` to disassociate from this `PowerTransformer`.
        Raises `ValueError` if `end` was not associated with this `PowerTransformer`.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        """
        self._power_transformer_ends = safe_remove(self._power_transformer_ends, end)
        return self

    def clear_ends(self) -> PowerTransformer:
        """
        Clear all `PowerTransformerEnd`s.
        Returns A reference to this `PowerTransformer` to allow fluent use.
        """
        self._power_transformer_ends.clear()
        return self

    def _validate_end(self, end: PowerTransformerEnd) -> bool:
        """
        Validate an end against this `PowerTransformer`'s `PowerTransformerEnd`s.

        `end` The `PowerTransformerEnd` to validate.
        Returns True if `end` is already associated with this `PowerTransformer`, otherwise False.
        Raises `ValueError` if `end.power_transformer` is not this `PowerTransformer`, or if this `PowerTransformer` has a different `PowerTransformerEnd`
        with the same mRID.
        """
        if self._validate_reference(end, self.get_end_by_mrid, "A PowerTransformerEnd"):
            return True

        if self._validate_reference_by_field(end, end.end_number, self.get_end_by_num, "end_number"):
            return True

        if not end.power_transformer:
            end.power_transformer = self

        require(end.power_transformer is self,
                lambda: f"PowerTransformerEnd {end} references another PowerTransformer {end.power_transformer}, expected {str(self)}.")
        return False
