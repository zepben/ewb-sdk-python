#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Substation"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import nlen, get_by_mrid, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import Loop
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


@dataslot
@boilermaker
class Substation(EquipmentContainer):
    """
    A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk
    is passed for the purposes of switching or modifying its characteristics.
    """

    sub_geographical_region: SubGeographicalRegion | None = None
    """The SubGeographicalRegion containing the substation."""

    normal_energized_feeders: List[Feeder] | None = MRIDListAccessor()

    loops: List[Loop] | None = MRIDListAccessor()

    energized_loops: List[Loop] | None = MRIDListAccessor()

    circuits: List[Circuit] | None = MRIDListAccessor()

    def _retype(self):
        self.normal_energized_feeders: MRIDListRouter = ...
        self.loops: MRIDListRouter = ...
        self.energized_loops: MRIDListRouter = ...
        self.circuits: MRIDListRouter = ...

    @property
    def feeders(self) -> Generator[Feeder, None, None]:
        """
        The normal energized feeders of the substation. Also used for naming purposes.
        """
        return self.normal_energized_feeders

    @deprecated("BOILERPLATE: Use len(normal_energized_feeders) instead")
    def num_feeders(self):
        return len(self.normal_energized_feeders)

    @deprecated("BOILERPLATE: Use normal_energized_feeders.get_by_mrid(mrid) instead")
    def get_feeder(self, mrid: str) -> Feeder:
        return self.normal_energized_feeders.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use normal_energized_feeders.append(feeder) instead")
    def add_feeder(self, feeder: Feeder) -> Substation:
        return self.normal_energized_feeders.append(feeder)

    @deprecated("BOILERPLATE: Use normal_energized_feeders.remove(feeder) instead")
    def remove_feeder(self, feeder: Feeder) -> Substation:
        return self.normal_energized_feeders.remove(feeder)

    @deprecated("BOILERPLATE: Use normal_energized_feeders.clear() instead")
    def clear_feeders(self) -> Substation:
        return self.normal_energized_feeders.clear()

    @deprecated("BOILERPLATE: Use len(loops) instead")
    def num_loops(self):
        return len(self.loops)

    @deprecated("BOILERPLATE: Use loops.get_by_mrid(mrid) instead")
    def get_loop(self, mrid: str) -> Loop:
        return self.loops.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use loops.append(loop) instead")
    def add_loop(self, loop: Loop) -> Substation:
        return self.loops.append(loop)

    @deprecated("BOILERPLATE: Use loops.remove(loop) instead")
    def remove_loop(self, loop: Loop) -> Substation:
        return self.loops.remove(loop)

    @deprecated("BOILERPLATE: Use loops.clear() instead")
    def clear_loops(self) -> Substation:
        return self.loops.clear()

    @deprecated("BOILERPLATE: Use len(energized_loops) instead")
    def num_energized_loops(self):
        return len(self.energized_loops)

    @deprecated("BOILERPLATE: Use energized_loops.get_by_mrid(mrid) instead")
    def get_energized_loop(self, mrid: str) -> Loop:
        return self.energized_loops.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use energized_loops.append(loop) instead")
    def add_energized_loop(self, loop: Loop) -> Substation:
        return self.energized_loops.append(loop)

    @deprecated("BOILERPLATE: Use energized_loops.remove(loop) instead")
    def remove_energized_loop(self, loop: Loop) -> Substation:
        return self.energized_loops.remove(loop)

    @deprecated("BOILERPLATE: Use energized_loops.clear() instead")
    def clear_energized_loops(self) -> Substation:
        return self.energized_loops.clear()

    @deprecated("BOILERPLATE: Use len(circuits) instead")
    def num_circuits(self):
        return len(self.circuits)

    @deprecated("BOILERPLATE: Use circuits.get_by_mrid(mrid) instead")
    def get_circuit(self, mrid: str) -> Circuit:
        return self.circuits.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use circuits.append(circuit) instead")
    def add_circuit(self, circuit: Circuit) -> Substation:
        return self.circuits.append(circuit)

    @deprecated("BOILERPLATE: Use circuits.remove(circuit) instead")
    def remove_circuit(self, circuit: Circuit) -> Substation:
        return self.circuits.remove(circuit)

    @deprecated("BOILERPLATE: Use circuits.clear() instead")
    def clear_circuits(self) -> Substation:
        return self.circuits.clear()
        return self
