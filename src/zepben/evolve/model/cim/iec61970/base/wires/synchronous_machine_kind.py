#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import unique, Enum


@unique
class SynchronousMachineKind(Enum):
    """
    Synchronous machine type.
    """

    UNKNOWN = 0
    """UNKNOWN"""

    generator = 1
    """Indicates the synchronous machine can operate as a generator."""

    condenser = 2
    """Indicates the synchronous machine can operate as a condenser."""

    generatorOrCondenser = 3
    """Indicates the synchronous machine can operate as a generator or as a condenser."""

    motor = 4
    """Indicates the synchronous machine can operate as a motor."""

    generatorOrMotor = 5
    """Indicates the synchronous machine can operate as a generator or as a motor."""

    motorOrCondenser = 6
    """Indicates the synchronous machine can operate as a motor or as a condenser."""

    generatorOrCondenserOrMotor = 7
    """Indicates the synchronous machine can operate as a generator or as a condenser or as a motor."""

    @property
    def short_name(self) -> str:
        """Get the name of this `SynchronousMachineKind` without the class qualifier"""
        return str(self)[23:]
