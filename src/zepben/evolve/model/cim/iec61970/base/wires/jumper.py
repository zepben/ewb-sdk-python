#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve import Switch

__all__ = ["Jumper"]


class Jumper(Switch):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is de-energized.
    Note that zero-impedance branches can potentially be modeled by other equipment types.
    """
    pass
