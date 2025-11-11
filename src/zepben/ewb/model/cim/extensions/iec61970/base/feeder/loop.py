#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Loop"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import safe_remove, ngen, nlen, get_by_mrid

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


@zbex
@dataslot
@boilermaker
class Loop(IdentifiedObject):
    """
    [ZBEX]
    Sub-transmission circuits are usually arranged in loops so that a single line failure does not cut off service
    to many customers for more than a short time.
    """

    circuits: List[Circuit] | None = MRIDListAccessor()
    substations: List[Substation] | None = MRIDListAccessor()
    energizing_substations: List[Substation] | None = MRIDListAccessor()

    def _retype(self):
        self.circuits: MRIDListRouter = ...
        self.substations: MRIDListRouter = ...
        self.energizing_substations: MRIDListRouter = ...

    @deprecated("BOILERPLATE: Use len(circuits) instead")
    def num_circuits(self):
        return len(self.circuits)

    @deprecated("BOILERPLATE: Use circuits.get_by_mrid(mrid) instead")
    def get_circuit(self, mrid: str) -> Circuit:
        return self.circuits.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use circuits.append(circuit) instead")
    def add_circuit(self, circuit: Circuit) -> Loop:
        self.circuits.append(circuit)
        return self

    @deprecated("Boilerplate: Use circuits.remove(circuit) instead")
    def remove_circuit(self, circuit: Circuit) -> Loop:
        self.circuits.remove(circuit)
        return self

    @deprecated("BOILERPLATE: Use circuits.clear() instead")
    def clear_circuits(self) -> Loop:
        return self.circuits.clear()

    @deprecated("BOILERPLATE: Use len(substations) instead")
    def num_substations(self):
        return len(self.substations)

    @deprecated("BOILERPLATE: Use substations.get_by_mrid(mrid) instead")
    def get_substation(self, mrid: str) -> Substation:
        return self.substations.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use substations.append(substation) instead")
    def add_substation(self, substation: Substation) -> Loop:
        self.substations.append(substation)
        return self

    @deprecated("Boilerplate: Use substations.remove(substation) instead")
    def remove_substation(self, substation: Substation) -> Loop:
        self.substations.remove(substation)
        return self

    @deprecated("BOILERPLATE: Use substations.clear() instead")
    def clear_substations(self) -> Loop:
        return self.substations.clear()

    @deprecated("BOILERPLATE: Use len(energizing_substations) instead")
    def num_energizing_substations(self):
        return len(self.energizing_substations)

    @deprecated("BOILERPLATE: Use energizing_substations.get_by_mrid(mrid) instead")
    def get_energizing_substation(self, mrid: str) -> Substation:
        return self.energizing_substations.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use energizing_substations.append(substation) instead")
    def add_energizing_substation(self, substation: Substation) -> Loop:
        self.energizing_substations.append(substation)
        return self

    @deprecated("Boilerplate: Use energizing_substations.remove(substation) instead")
    def remove_energizing_substation(self, substation: Substation) -> Loop:
        self.energizing_substations.remove(substation)
        return self

    @deprecated("BOILERPLATE: Use energizing_substations.clear() instead")
    def clear_energizing_substations(self) -> Loop:
        self.energizing_substations.clear()
        return self

