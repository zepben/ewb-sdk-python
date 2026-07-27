#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Substation"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb import Alias
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, LazyMridList, Backfill, internal

from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import Loop
    from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


@zb_dataclass
class Substation(EquipmentContainer):
    """
    A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk
    is passed for the purposes of switching or modifying its characteristics.
    """

    _sub_geographical_region: Optional[SubGeographicalRegion] = field(default=None)

    _normal_energized_feeders: Optional[List[Feeder]] = field(default=None)

    feeders: MridCollection[Feeder] = LazyMridList(
        _normal_energized_feeders,
        "A Feeder",
        backfill=Backfill(Feeder.normal_energizing_substation)
    )
    normal_energized_feeders = Alias(feeders)

    _loops: Optional[List[Loop]] = field(default=None)

    loops: MridCollection[Loop] = LazyMridList(
        _loops,
        "A Loop",
    )

    _energized_loops: Optional[List[Loop]] = field(default=None)

    energized_loops: MridCollection[Loop] = LazyMridList(
        _energized_loops,
        "A Loop",
    )

    _circuits: Optional[List[Circuit]] = field(default=None)

    circuits: MridCollection[Circuit] = LazyMridList(
        _circuits,
        "A Circuit",
    )

    @property
    @internal(_sub_geographical_region)
    def sub_geographical_region(self):
        """The SubGeographicalRegion containing the substation."""
        return self._sub_geographical_region



    @sub_geographical_region.setter
    @deprecated("sub_geographical_region should never be set directly - it is automatically set when adding it to the `substations` list")
    def sub_geographical_region(self, value):
        self._sub_geographical_region = value

    # region deprecated list boilerplate
    # region circuits boilerplate

    @deprecated("Use len(obj.circuits) instead.")
    def num_circuits(self):
        return len(self.circuits)

    @deprecated("Use obj.circuits.get_by_mrid(mrid) instead.")
    def get_circuit(self, mrid: str) -> Circuit:
        return self.circuits.get_by_mrid(mrid)

    @deprecated("Use obj.circuits.append(circuit) instead.")
    def add_circuit(self, circuit: Circuit) -> Substation:
        self.circuits.append(circuit)
        return self

    @deprecated("Use obj.circuits.remove(circuit) instead.")
    def remove_circuit(self, circuit: Circuit) -> Substation:
        self.circuits.remove(circuit)
        return self

    @deprecated("Use obj.circuits.clear() instead.")
    def clear_circuits(self) -> Substation:
        self.circuits.clear()
        return self

    # endregion circuits boilerplate

    # region loops boilerplate

    @deprecated("Use len(obj.loops) instead.")
    def num_loops(self):
        return len(self.loops)

    @deprecated("Use obj.loops.get_by_mrid(mrid) instead.")
    def get_loop(self, mrid: str) -> Loop:
        return self.loops.get_by_mrid(mrid)

    @deprecated("Use obj.loops.append(loop) instead.")
    def add_loop(self, loop: Loop) -> Substation:
        self.loops.append(loop)
        return self

    @deprecated("Use obj.loops.remove(loop) instead.")
    def remove_loop(self, loop: Loop) -> Substation:
        self.loops.remove(loop)
        return self

    @deprecated("Use obj.loops.clear() instead.")
    def clear_loops(self) -> Substation:
        self.loops.clear()
        return self

    # endregion loops boilerplate

    # region energized_loops boilerplate

    @deprecated("Use len(obj.energized_loops) instead.")
    def num_energized_loops(self):
        return len(self.energized_loops)

    @deprecated("Use obj.energized_loops.get_by_mrid(mrid) instead.")
    def get_energized_loop(self, mrid: str) -> Loop:
        return self.energized_loops.get_by_mrid(mrid)

    @deprecated("Use obj.energized_loops.append(loop) instead.")
    def add_energized_loop(self, loop: Loop) -> Substation:
        self.energized_loops.append(loop)
        return self

    @deprecated("Use obj.energized_loops.remove(loop) instead.")
    def remove_energized_loop(self, loop: Loop) -> Substation:
        self.energized_loops.remove(loop)
        return self

    @deprecated("Use obj.energized_loops.clear() instead.")
    def clear_energized_loops(self) -> Substation:
        self.energized_loops.clear()
        return self

    # endregion energized_loops boilerplate

    # region feeders boilerplate

    @deprecated("Use len(obj.feeders) instead.")
    def num_feeders(self):
        return len(self.feeders)

    @deprecated("Use obj.feeders.get_by_mrid(mrid) instead.")
    def get_feeder(self, mrid: str) -> Feeder:
        return self.feeders.get_by_mrid(mrid)

    @deprecated("Use obj.feeders.append(feeder) instead.")
    def add_feeder(self, feeder: Feeder) -> Substation:
        self.feeders.append(feeder)
        return self

    @deprecated("Use obj.feeders.remove(feeder) instead.")
    def remove_feeder(self, feeder: Feeder) -> Substation:
        self.feeders.remove(feeder)
        return self

    @deprecated("Use obj.feeders.clear() instead.")
    def clear_feeders(self) -> Substation:
        self.feeders.clear()
        return self

    # endregion feeders boilerplate

    # endregion deprecated list boilerplate
