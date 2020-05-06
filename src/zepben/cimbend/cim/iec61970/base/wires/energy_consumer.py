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

from dataclasses import dataclass
from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.cimbend.cim.iec61970.base.wires.energy_connection import EnergyConnection
from zepben.cimbend.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.cimbend.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["EnergyConsumer", "EnergyConsumerPhase"]

from zepben.cimbend.util import nlen, require, contains_mrid, get_by_mrid, ngen


@dataclass
class EnergyConsumerPhase(PowerSystemResource):
    """
    A single phase of an energy consumer.

    Attributes:
        energy_consumer : The :class:`zepben.cimbend.iec61970.base.wires.EnergyConsumer` to which this phase belongs.
        phase : Phase of this energy consumer component. If the energy consumer is wye connected, the connection is
                from the indicated phase to the central ground or neutral point.  If the energy consumer is delta
                connected, the phase indicates an energy consumer connected from the indicated phase to the next
                logical non-neutral phase.
        p : Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        q : Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        pfixed : Active power of the load that is a fixed quantity. Load sign convention is used,
                 i.e. positive sign means flow out from a node.
        qfixed : Reactive power of the load that is a fixed quantity. Load sign convention is used,
                 i.e. positive sign means flow out from a node.
        phase : A :class:`zepben.cimbend.SinglePhaseKind` Phase of this energy consumer component. If the energy
                consumer is wye connected, the connection is from the indicated phase to the central ground or neutral point.
                If the energy consumer is delta connected, the phase indicates an energy consumer connected from the
                indicated phase to the next logical non-neutral phase.
    """

    energy_consumer: Optional[EnergyConsumer] = None
    phase: SinglePhaseKind = SinglePhaseKind.NONE
    p: float = 0.0
    q: float = 0.0
    p_fixed: float = 0.0
    q_fixed: float = 0.0


@dataclass
class EnergyConsumer(EnergyConnection):
    """
    Generic user of energy - a point of consumption on the power system phases. May also represent a pro-sumer with
    negative p/q values.

    Attributes:
        p : Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        q : Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        phase_connection : :class:`zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind` - The type of phase
                          connection, such as wye, delta, I (single phase).
        energy_consumer_phases : The individual phase models for this energy consumer.
        customer_count : Number of individual customers represented by this demand.
        grounded : Used for Yn and Zn connections. True if the neutral is solidly grounded.
        p_fixed : Active power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign
                  means flow out from a node.
        q_fixed : power of the load that is a fixed quantity. Load sign convention is used, i.e. positive sign means
                  flow out from a node.
    """

    _energy_consumer_phases: Optional[List[EnergyConsumerPhase]] = None
    grounded: bool = False
    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.D
    p: float = 0.0
    p_fixed: float = 0.0
    q: float = 0.0
    q_fixed: float = 0.0
    customer_count: int = 0

    def __post_init__(self):
        for phase in self._energy_consumer_phases:
            phase.energy_consumer = self

    @property
    def has_phases(self):
        """
        Check if this source has any associated :class:`EnergySourcePhases`
        :return: True if there is at least one `EnergySourcePhase`, otherwise False
        """
        return nlen(self._energy_consumer_phases) > 0

    @property
    def num_phases(self):
        return nlen(self._energy_consumer_phases)

    @property
    def phases(self) -> Generator[EnergyConsumerPhase, None, None]:
        """
        :return: Generator over the ``EnergyConsumerPhase``s of this ``EnergyConsumer``.
        """
        return ngen(self._energy_consumer_phases)

    def get_container(self, mrid: str) -> EnergyConsumer:
        """
        Get the ``EnergyConsumerPhase`` for this ``EnergyConsumer`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`EnergyConsumerPhase`
        :return: The :class:`EnergyConsumerPhase` with the specified ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._energy_consumer_phases, mrid)

    def add_phase(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        """
        Associate an ``EnergyConsumerPhase`` with this ``EnergyConsumer``
        :param phase: the :class:`EnergyConsumerPhase` to associate with this ``EnergyConsumer``.
        :return: A reference to this ``EnergyConsumer`` to allow fluent use.
        """
        require(not contains_mrid(self._energy_consumer_phases, phase.mrid),
                lambda: f"An EnergyConsumerPhase with mRID {phase.mrid} already exists in {str(self)}")

        self._energy_consumer_phases = set() if self._energy_consumer_phases is None else self._energy_consumer_phases
        self._energy_consumer_phases.add(phase)
        return self

    def remove_phases(self, phase: EnergyConsumerPhase) -> EnergyConsumer:
        """
        :param phase: the :class:`EnergyConsumerPhase` to disassociate with this ``EnergyConsumer``.
        :raises: KeyError if ``phase`` was not associated with this ``EnergyConsumer``.
        :return: A reference to this ``EnergyConsumer`` to allow fluent use.
        """
        if self._energy_consumer_phases is not None:
            self._energy_consumer_phases.remove(phase)
            if not self._energy_consumer_phases:
                self._energy_consumer_phases = None
        else:
            raise KeyError(phase)

        return self

    def clear_phases(self) -> EnergyConsumer:
        """
        Clear all phases.
        :return: A reference to this ``EnergyConsumer`` to allow fluent use.
        """
        self._energy_consumer_phases = None
        return self
