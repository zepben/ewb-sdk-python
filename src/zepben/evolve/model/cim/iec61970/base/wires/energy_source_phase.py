#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import EnergySource

from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["EnergySourcePhase"]


class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.
    """

    _energy_source: Optional[EnergySource] = None
    """The `zepben.evolve.cim.iec61970.wires.EnergySource` with this `EnergySourcePhase`"""

    phase: SinglePhaseKind = SinglePhaseKind.NONE
    """A `zepben.evolve.iec61970.base.wires.single_phase_kind.SinglePhaseKind` Phase of this energy source component. If the energy source is wye connected, 
    the connection is from the indicated phase to the central ground or neutral point. If the energy source is delta connected, the phase indicates an energy 
    source connected from the indicated phase to the next logical non-neutral phase."""

    def __init__(self, energy_source: EnergySource = None, **kwargs):
        super(EnergySourcePhase, self).__init__(**kwargs)
        if energy_source:
            self.energy_source = energy_source

    @property
    def energy_source(self):
        """The `EnergySource` with this `EnergySourcePhase`"""
        return self._energy_source

    @energy_source.setter
    def energy_source(self, es):
        if self._energy_source is None or self._energy_source is es:
            self._energy_source = es
        else:
            raise ValueError(f"energy_source for {str(self)} has already been set to {self._energy_source}, cannot reset this field to {es}")
