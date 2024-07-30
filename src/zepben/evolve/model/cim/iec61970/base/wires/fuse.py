#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional

from zepben.evolve import Switch

from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

__all__ = ["Fuse"]


class Fuse(Switch):
    """
    An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of
    overcurrent through it. A fuse is considered a switching device because it breaks current.
    """

    function: Optional[ProtectionRelayFunction] = None
    """The function implemented by this Fuse"""
