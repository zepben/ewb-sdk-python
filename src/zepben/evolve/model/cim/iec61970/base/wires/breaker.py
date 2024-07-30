#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch

__all__ = ["Breaker"]


class Breaker(ProtectedSwitch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions
    and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions
    e.g. those of short circuit.
    """

    in_transit_time: Optional[float] = None
    """The transition time from open to close in seconds."""

    @property
    def is_substation_breaker(self) -> bool:
        """Convenience function for detecting if this breaker is part of a substation. Returns true if this Breaker is associated with a Substation."""
        return self.num_substations() > 0

    @property
    def is_feeder_head_breaker(self) -> bool:
        """Convenience function for detecting if this breaker is at the head of a feeder."""
        terminals = list(self.terminals)
        return any(fdr.normal_head_terminal in terminals for fdr in self.normal_feeders)
