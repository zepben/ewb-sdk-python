#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

__all__ = ["Switch", "Breaker", "Disconnector", "Jumper", "Fuse", "ProtectedSwitch", "Recloser", "LoadBreakSwitch"]

from zepben.evolve.util import require


def _calculate_open_state(current_state: int, is_open: bool, phase: SinglePhaseKind = None) -> int:
    require(phase != SinglePhaseKind.NONE and phase != SinglePhaseKind.INVALID,
            lambda: f"Invalid phase {phase} specified")
    if phase is None:
        return 0b1111 if is_open else 0
    else:
        return current_state | phase.bit_mask if is_open else current_state & ~phase.bit_mask


def _check_open(current_state: int, phase: SinglePhaseKind = None) -> bool:
    require(phase != SinglePhaseKind.NONE and phase != SinglePhaseKind.INVALID,
            lambda: f"Invalid phase {phase} specified")
    if phase is None:
        return current_state != 0
    else:
        return (current_state & phase.bit_mask) != 0


class Switch(ConductingEquipment):
    """
    A generic device designed to close, or open, or both, one or more electric circuits.
    All switches are two terminal devices including grounding switches.

    NOTE: The normal and currently open properties are implemented as an integer rather than a boolean to allow for the caching of
      measurement values if the switch is operating un-ganged. These values will cache the latest values from the measurement
      value for each phase of the switch.
    """

    _open: int = 0
    """Tells if the switch is considered open when used as input to topology processing."""

    _normally_open: int = 0
    """The attribute is used in cases when no Measurement for the status value is present. If the Switch has a status measurement the Discrete.normalValue 
    is expected to match with the Switch.normalOpen."""

    def is_normally_open(self, phase: SinglePhaseKind = None):
        """
        Check if the switch is normally open on `phase`.

        `phase` The `single_phase_kind.SinglePhaseKind` to check the normal status. A `phase` of `None` (default) checks if any phase is open.
        Returns True if `phase` is open in its normal state, False if it is closed
        """
        return _check_open(self._normally_open, phase)

    def get_normal_state(self) -> int:
        """
        Get the underlying normal open states. Stored as 4 bits, 1 per phase.
        """
        return self._normally_open

    def is_open(self, phase: SinglePhaseKind = None):
        """
        Check if the switch is currently open on `phase`.

        `phase` The `SinglePhaseKind` to check the current status. A `phase` of `None` (default) checks
        if any phase is open.
        Returns True if `phase` is open in its current state, False if it is closed
        """
        return _check_open(self._open, phase)

    def get_state(self) -> int:
        """
        The attribute tells if the switch is considered open when used as input to topology processing.
        Get the underlying open states. Stored as 4 bits, 1 per phase.
        """
        return self._open

    def set_normally_open(self, is_normally_open: bool, phase: SinglePhaseKind = None) -> Switch:
        """
        `is_normally_open` indicates if the phase(s) should be opened.
        `phase` the phase to set the normal status. If set to None will default to all phases.
        Returns This `Switch` to be used fluently.
        """
        self._normally_open = _calculate_open_state(self._normally_open, is_normally_open, phase)
        return self

    def set_open(self, is_open: bool, phase: SinglePhaseKind = None) -> Switch:
        """
        `is_open` indicates if the phase(s) should be opened.
        `phase` the phase to set the current status. If set to None will default to all phases.
        Returns This `Switch` to be used fluently.
        """
        self._open = _calculate_open_state(self._open, is_open, phase)
        return self


class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by ProtectionEquipment.
    """
    pass


class Breaker(ProtectedSwitch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions
    and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions
    e.g. those of short circuit.
    """

    def is_substation_breaker(self):
        """Convenience function for detecting if this breaker is part of a substation. Returns true if this Breaker is associated with a Substation."""
        return self.num_substations() > 0


class Disconnector(Switch):
    """
    A manually operated or motor operated mechanical switching device used for changing the connections in a circuit,
    or for isolating a circuit or equipment from a source of power. It is required to open or close circuits when
    negligible current is broken or made.
    """
    pass


class Fuse(Switch):
    """
    An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of
    overcurrent through it. A fuse is considered a switching device because it breaks current.
    """
    pass


class Jumper(Switch):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is de-energized.
    Note that zero-impedance branches can potentially be modeled by other equipment types.
    """
    pass


class Recloser(ProtectedSwitch):
    """
    Pole-mounted fault interrupter with built-in phase and ground relays, current transformer (CT), and supplemental controls.
    """
    pass


class LoadBreakSwitch(ProtectedSwitch):
    """A mechanical switching device capable of making, carrying, and breaking currents under normal operating
    conditions. """
    pass
