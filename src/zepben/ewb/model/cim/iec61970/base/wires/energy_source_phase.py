#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EnergySourcePhase"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.energy_source import EnergySource


@dataslot
class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.
    """

    energy_source: Optional['EnergySource'] = ValidatedDescriptor(None)
    """The `zepben.ewb.model.cim.iec61970.wires.EnergySource` with this `EnergySourcePhase`"""

    phase: SinglePhaseKind = SinglePhaseKind.NONE
    """A `zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind.SinglePhaseKind` Phase of this energy source component. If the energy source is wye connected, 
    the connection is from the indicated phase to the central ground or neutral point. If the energy source is delta connected, the phase indicates an energy 
    source connected from the indicated phase to the next logical non-neutral phase."""

    @validate(energy_source)
    def _energy_source_validate(self, es):
        if self._energy_source is None or self._energy_source is es:
            return es
        else:
            raise ValueError(f"energy_source for {str(self)} has already been set to {self._energy_source}, cannot reset this field to {es}")
