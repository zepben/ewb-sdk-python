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

from dataclasses import dataclass, field

from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["Switch", "Breaker", "Disconnector", "Jumper", "Fuse", "ProtectedSwitch", "Recloser"]


@dataclass
class Switch(ConductingEquipment):
    """
    A generic device designed to close, or open, or both, one or more electric circuits.
    All switches are two terminal devices including grounding switches.

    NOTE: The normal and currently open properties are implemented as an integer rather than a boolean to allow for the caching of
      measurement values if the switch is operating un-ganged. These values will cache the latest values from the measurement
      value for each phase of the switch.

    Attributes:

        _open : The attribute tells if the switch is considered open when used as input to topology processing.
        _normal_open : The attribute is used in cases when no Measurement for the status value is present. If the Switch
                       has a status measurement the Discrete.normalValue is expected to match with the Switch.normalOpen.
    """

    _open: int = field(init=False, default=0)
    _normal_open: int = field(init=False, default=0)

    def __post_init__(self):
        self.set_open(False)
        self.set_normally_open(False)

    def normally_open(self, phase: SinglePhaseKind):
        """
        Check if the switch is normally open on ``phase``.

        :param phase: The :class:`single_phase_kind.SinglePhaseKind` to check the normal status
        :return: The status of the ``phase`` in its normal state
        """
        self._check_open(self._normal_open, phase)

    def get_normal_state(self) -> int:
        """
        Get the underlying normal open states. Stored as 4 bits, 1 per phase.
        """
        return self._normal_open

    def is_open(self, phase: SinglePhaseKind):
        """
        Check if the switch is currently open on ``phase``.

        :param phase: The :class:`single_phase_kind.SinglePhaseKind` to check the current status
        :return: The status of the ``phase`` in its current state
        """
        self._check_open(self._open, phase)

    def get_state(self) -> int:
        """
        Get the underlying open states. Stored as 4 bits, 1 per phase.
        """
        return self._open

    def set_normally_open(self, is_normally_open: bool, phase: SinglePhaseKind = SinglePhaseKind.NONE) -> Switch:
        """
        :param is_normally_open: indicates if the phase(s) should be opened.
        :param phase: the phase to set the normal status. If unset will default to all phases.
        :return: This ``Switch`` to be used fluently.
        """
        self._normal_open = self._calculate_open_state(self._normal_open, is_normally_open, phase)
        return self

    def set_open(self, is_open: bool, phase: SinglePhaseKind = SinglePhaseKind.NONE) -> Switch:
        """
        :param is_open: indicates if the phase(s) should be opened.
        :param phase: the phase to set the current status. If unset will default to all phases.
        :return: This ``Switch`` to be used fluently.
        """
        self._open = self._calculate_open_state(self._open, is_open, phase)
        return self

    def _check_open(self, current_state: int, phase: SinglePhaseKind) -> bool:
        if phase == SinglePhaseKind.NONE or self.num_terminals == 0:
            return current_state != 0

        res = None
        for term in self.terminals:
            if res is None and term.phases.single_phases.contains(phase):
                res = current_state & phase.bit_mask() != 0

        if res is None:
            raise ValueError(f"Invalid phase {phase} specified")

        return res

    def _calculate_open_state(self, current_state: int, is_open: bool, phase: SinglePhaseKind) -> int:
        if phase == SinglePhaseKind.NONE or self.num_terminals == 0:
            return 0b1111 if is_open else 0

        new_state = None
        for term in self.terminals:
            if new_state is None and term.phases.single_phases.contains(phase):
                new_state = current_state | phase.bit_mask if is_open else current_state & ~phase.bit_mask

        if new_state is None:
            raise ValueError(f"Invalid phase {phase} specified")

        return new_state


class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by ProtectionEquipment.
    """
    pass


@dataclass
class Breaker(ProtectedSwitch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions
    and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions
    e.g. those of short circuit.

    Attributes:
        Same as :class:`Switch`
    """

    def is_substation_breaker(self):
        return self.num_substations > 0


@dataclass
class Disconnector(Switch):
    """
    A manually operated or motor operated mechanical switching device used for changing the connections in a circuit,
    or for isolating a circuit or equipment from a source of power. It is required to open or close circuits when
    negligible current is broken or made.
    """
    pass


@dataclass
class Fuse(Switch):
    """
    An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of
    overcurrent through it. A fuse is considered a switching device because it breaks current.
    """
    pass


@dataclass
class Jumper(Switch):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is de-energized.
    Note that zero-impedance branches can potentially be modeled by other equipment types.
    """
    pass


@dataclass
class Recloser(ProtectedSwitch):
    """
    Pole-mounted fault interrupter with built-in phase and ground relays, current transformer (CT), and supplemental controls.
    """
    pass
