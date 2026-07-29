#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerTransformer"]

import sys
from dataclasses import field
from typing import List, Optional, TYPE_CHECKING

from zepben.ewb import Alias
from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.boilerplate.relations.power_transformer_end_list import PowerTransformerEndList

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.extensions.iec61970.base.wires.vector_group import VectorGroup
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import TransformerConstructionKind
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import TransformerFunctionKind
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@zb_dataclass
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

    asset_info: PowerTransformerInfo | None = None

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

    _power_transformer_ends: List[PowerTransformerEnd] | None = field(default=None)

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


    ends: PowerTransformerEndList = PowerTransformerEndList(
        _power_transformer_ends,
        "A PowerTransformerEnd",
        backfill=Backfill(PowerTransformerEnd.power_transformer),
        validate=lambda self, it: self._validate_end(it),
        sort_by=lambda it: it.end_number
    )
    power_transformer_ends = Alias(ends)

    def _validate_end(self, end: PowerTransformerEnd):
        self._validate_reference_by_field(end, end.end_number, self.ends.get_by_num, "end_number")

        if end.end_number == 0:
            end.end_number = self.num_ends() + 1


    @property
    @deprecated("use asset_info instead.")
    def power_transformer_info(self) -> Optional[PowerTransformerInfo]:
        """The `PowerTransformerInfo` for this `PowerTransformer`"""
        return self.asset_info

    @power_transformer_info.setter
    @deprecated("use asset_info instead.")
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


    # region deprecated list boilerplate
    #
    # ("region/endregion" is an IntelliJ feature letting you hide the entire thing)
    # This boilerplate exists solely to enable backwards compatibility.
    # It will be removed eventually.
    # Every single method simply forwards the call to the corresponding list.

    # ends boilerplate

    @deprecated("Use `len(power_transformer.ends)` instead.")
    def num_ends(self):
        return len(self.ends)

    @deprecated("Use `power_transformer.ends.get_by_mrid(mrid)` instead.")
    def get_end_by_mrid(self, mrid: str) -> PowerTransformerEnd:
        return self.ends.get_by_mrid(mrid)

    @deprecated("Use `power_transformer.ends.get_by_num(end_number)` instead.")
    def get_end_by_num(self, end_number: int) -> PowerTransformerEnd:
        return self.ends.get_by_num(end_number)

    @deprecated("Use `power_transformer.ends.get_by_terminal(terminal)` instead.")
    def get_end_by_terminal(self, terminal: Terminal) -> PowerTransformerEnd:
        return self.ends.get_by_terminal(terminal)

    @deprecated("Use `power_transformer.ends.append(end)` instead.")
    def add_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        self.ends.append(end)
        return self

    @deprecated("Use `power_transformer.ends.remove(end)` instead.")
    def remove_end(self, end: PowerTransformerEnd) -> PowerTransformer:
        self.ends.remove(end)
        return self

    @deprecated("Use `power_transformer.ends.clear()` instead.")
    def clear_ends(self) -> PowerTransformer:
        self.ends.clear()
        return self

    # endregion

    # endregion
