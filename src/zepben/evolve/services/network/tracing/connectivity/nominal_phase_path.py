#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass


__all__ = ["NominalPhasePath"]

from zepben.evolve import SinglePhaseKind


@dataclass(frozen=True)
class NominalPhasePath(object):
    """
    Defines how a nominal phase is wired through a connectivity node between two terminals
    """

    from_phase: SinglePhaseKind
    """The nominal phase where the path comes from."""

    to_phase: SinglePhaseKind
    """The nominal phase where the path goes to."""


