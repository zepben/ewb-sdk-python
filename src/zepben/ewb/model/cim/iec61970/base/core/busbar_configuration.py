#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum


class BreakerConfiguration(Enum):
    """Switching arrangement for a bay."""

    SINGLE_BREAKER = 0
    """Single breaker."""

    BREAKER_AND_A_HALF = 1
    """Breaker and a half."""

    DOUBLE_BREAKER = 2
    """Double breaker."""

    NO_BREAKER = 3
    """No breaker."""

    @property
    def short_name(self) -> str:
        return self.name


class BusbarConfiguration(Enum):
    """Busbar layout for a bay."""

    SINGLE_BUS = 0
    """Single bus."""

    DOUBLE_BUS = 1
    """Double bus."""

    MAIN_WITH_TRANSFER_BUS = 2
    """Main bus with transfer bus."""

    RING_BUS = 3
    """Ring bus."""

    @property
    def short_name(self) -> str:
        return self.name
