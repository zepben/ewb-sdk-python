"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Generator

from zepben.cimbend.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.cimbend.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.cimbend.util import nlen, get_by_mrid, contains_mrid, require, ngen

__all__ = ["EnergySource"]


@dataclass
class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.

    Attributes -
        active_power : High voltage source active injection. Load sign convention is used, i.e. positive sign means flow
                       out from a node. Starting value for steady state solutions
        r : Positive sequence Thevenin resistance.
        x : Positive sequence Thevenin reactance.
        reactive_power : High voltage source reactive injection. Load sign convention is used, i.e. positive sign means
                         flow out from a node. Starting value for steady state solutions.
        voltage_angle : Phase angle of a-phase open circuit.
        voltage_magnitude : Phase-to-phase open circuit voltage magnitude.
        energy_source_phases : An optional list of :class:`EnergySourcePhase`'s describing the phases for this source.
                    The existence of this attribute indicates this is a primary EnergySource and thus will be used as a
                    source point for calculating `Direction`'s.
    """

    energysourcephases: InitVar[List[EnergySourcePhase]] = field(default=list())
    _energy_source_phases: Optional[List[EnergySourcePhase]] = field(init=False, default=None)
    active_power: float = 0.0
    r: float = 0.0
    x: float = 0.0
    reactive_power: float = 0.0
    voltage_angle: float = 0.0
    voltage_magnitude: float = 0.0
    p_max: float = 0.0
    p_min: float = 0.0
    r0: float = 0.0
    rn: float = 0.0
    x0: float = 0.0
    xn: float = 0.0

    def __post_init__(self, usagepoints: Optional[List[UsagePoint]],
                      equipmentcontainers: Optional[List[EquipmentContainer]],
                      operationalrestrictions: Optional[List[OperationalRestriction]],
                      currentfeeders: Optional[List[Feeder]],
                      terminals_: List[Terminal],
                      energysourcephases: List[EnergySourcePhase]):
        super().__post_init__(usagepoints, equipmentcontainers, operationalrestrictions, currentfeeders, terminals_)
        for phase in energysourcephases:
            phase.energy_consumer = self
            self.add_phase(phase)

    @property
    def has_phases(self):
        """
        Check if this source has any associated :class:`EnergySourcePhases`
        :return: True if there is at least one `EnergySourcePhase`, otherwise False
        """
        return nlen(self._energy_source_phases) > 0

    @property
    def phases(self) -> Generator[EnergySourcePhase, None, None]:
        """
        :return: Generator over the ``EnergySourcePhase``s of this ``EnergySource``.
        """
        return ngen(self._energy_source_phases)

    @property
    def num_phases(self):
        return nlen(self._energy_source_phases)

    def get_container(self, mrid: str) -> EnergySource:
        """
        Get the ``EnergySourcePhase`` for this ``EnergySource`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`EnergySourcePhase`
        :return: The :class:`EnergySourcePhase` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._energy_source_phases, mrid)

    def add_phase(self, phase: EnergySourcePhase) -> EnergySource:
        """
        Associate an ``EnergySourcePhase`` with this ``EnergySource``
        :param phase: the :class:`EnergySourcePhase` to associate with this ``EnergySource``.
        :return: A reference to this ``EnergySource`` to allow fluent use.
        """
        require(not contains_mrid(self._energy_source_phases, phase.mrid),
                lambda: f"An EnergySourcePhase with mRID {phase.mrid} already exists in {str(self)}")

        self._energy_source_phases = list() if self._energy_source_phases is None else self._energy_source_phases
        self._energy_source_phases.append(phase)
        return self

    def remove_phases(self, phase: EnergySourcePhase) -> EnergySource:
        """
        :param phase: the :class:`EnergySourcePhase` to disassociate with this ``EnergySource``.
        :raises: KeyError if ``phase`` was not associated with this ``EnergySource``.
        :return: A reference to this ``EnergySource`` to allow fluent use.
        """
        if self._energy_source_phases is not None:
            self._energy_source_phases.remove(phase)
            if not self._energy_source_phases:
                self._energy_source_phases = None
        else:
            raise KeyError(phase)

        return self

    def clear_phases(self) -> EnergySource:
        """
        Clear all phases.
        :return: A reference to this ``EnergySource`` to allow fluent use.
        """
        self._energy_source_phases = None
        return self
