#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Loop"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


@zb_dataclass
@zbex
class Loop(IdentifiedObject):
    """
    [ZBEX]
    Sub-transmission circuits are usually arranged in loops so that a single line failure does not cut off service
    to many customers for more than a short time.
    """

    _circuits: Optional[List[Circuit]] = field(default=None)
    _substations: Optional[List[Substation]] = field(default=None)
    _energizing_substations: Optional[List[Substation]] = field(default=None)


    circuits: MridCollection[Circuit] = LazyMridList(
        _circuits,
        "A Circuit",
    )

    substations: MridCollection[Substation] = LazyMridList(
        _substations,
        "A Substation",
    )

    energizing_substations: MridCollection[Substation] = LazyMridList(
        _energizing_substations,
        "A Substation",
    )
















    # region deprecated list boilerplate
    # region circuits boilerplate

    @deprecated("Use len(obj.circuits) instead.")
    def num_circuits(self):
        return len(self.circuits)

    @deprecated("Use obj.circuits.get_by_mrid(mrid) instead.")
    def get_circuit(self, mrid: str) -> Circuit:
        return self.circuits.get_by_mrid(mrid)

    @deprecated("Use obj.circuits.append(circuit) instead.")
    def add_circuit(self, circuit: Circuit) -> Loop:
        self.circuits.append(circuit)
        return self

    @deprecated("Use obj.circuits.remove(circuit) instead.")
    def remove_circuit(self, circuit: Circuit) -> Loop:
        self.circuits.remove(circuit)
        return self

    @deprecated("Use obj.circuits.clear() instead.")
    def clear_circuits(self) -> Loop:
        self.circuits.clear()
        return self

    # endregion circuits boilerplate

    # region substations boilerplate

    @deprecated("Use len(obj.substations) instead.")
    def num_substations(self):
        return len(self.substations)

    @deprecated("Use obj.substations.get_by_mrid(mrid) instead.")
    def get_substation(self, mrid: str) -> Substation:
        return self.substations.get_by_mrid(mrid)

    @deprecated("Use obj.substations.append(substation) instead.")
    def add_substation(self, substation: Substation) -> Loop:
        self.substations.append(substation)
        return self

    @deprecated("Use obj.substations.remove(substation) instead.")
    def remove_substation(self, substation: Substation) -> Loop:
        self.substations.remove(substation)
        return self

    @deprecated("Use obj.substations.clear() instead.")
    def clear_substations(self) -> Loop:
        self.substations.clear()
        return self

    # endregion substations boilerplate

    # region energizing_substations boilerplate

    @deprecated("Use len(obj.energizing_substations) instead.")
    def num_energizing_substations(self):
        return len(self.energizing_substations)

    @deprecated("Use obj.energizing_substations.get_by_mrid(mrid) instead.")
    def get_energizing_substation(self, mrid: str) -> Substation:
        return self.energizing_substations.get_by_mrid(mrid)

    @deprecated("Use obj.energizing_substations.append(substation) instead.")
    def add_energizing_substation(self, substation: Substation) -> Loop:
        self.energizing_substations.append(substation)
        return self

    @deprecated("Use obj.energizing_substations.remove(substation) instead.")
    def remove_energizing_substation(self, substation: Substation) -> Loop:
        self.energizing_substations.remove(substation)
        return self

    @deprecated("Use obj.energizing_substations.clear() instead.")
    def clear_energizing_substations(self) -> Loop:
        self.energizing_substations.clear()
        return self

    # endregion energizing_substations boilerplate

    # endregion deprecated list boilerplate
