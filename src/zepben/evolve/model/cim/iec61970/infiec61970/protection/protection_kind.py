#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ["ProtectionKind"]


class ProtectionKind(Enum):
    """The kind of protection being provided by this protection equipment."""

    UNKNOWN = 0
    """Unknown"""

    JG = 1
    """Overcurrent"""

    JGG = 2
    """Instantaneous"""

    JGGG = 3
    """Instantaneous"""

    JT = 4
    """Thermal overload"""

    J0 = 5
    """Ground overcurrent"""

    J0GG = 6
    """Instantaneous ground overcurrent"""

    SEF = 7
    """Sensitive earth fault"""

    VG = 8
    """Overvoltage"""

    VGG = 9
    """Instantaneous overvoltage"""

    VL = 10
    """Undervoltage"""

    VLL = 11
    """Instantaneous"""

    V0G = 12
    """Zero-sequence overvoltage"""

    V0GG = 13
    """Instantaneous zero-sequence overvoltage"""

    JDIFF = 14
    """Differential Current"""

    FREQ = 15
    """Under frequency"""

    FREQG = 16
    """Over frequency"""

    ZL = 17
    """Phase distance"""

    Z0L = 18
    """Ground distance"""

    LE = 19
    """Load encroachment"""

    J2G = 20
    """Negative-sequence overcurrent"""

    MULTI_FUNCTION = 21
    """A multifunctional relay for universal usages"""

    GROUND_CURRENT = 22
    """A device used to monitor and protect electrical equipment from damage caused by ground faults"""

    GROUND_VOLTAGE = 23
    """A device used to detect contact accidents between an electric path and ground caused by arc ground faults"""

    NETWORK_PROTECTOR = 24
    """Is a special self-contained air breaker or switching unit having a full complement of current, potential and control transformers, as well as relay functionality."""

    DISTANCE = 25
    """A device used to detect faults on long-distance lines, pinpointing not only the fault condition but also measuring the distance between the current sensing mechanism and the fault location in the wire."""

    NEGATIVE_OVERCURRENT = 26
    """A device used to protect generators from the unbalanced load by detecting negative sequence current."""

    POWER = 27
    """A device that uses an electromagnet to open or close a circuit when the input (coil) is correctly excited"""

    SECTIONALIZER = 28
    """A device that automatically isolates a faulted section of line from the rest of the distribution system"""

    AUTO_TRANSFORMER = 29
    """A device used to regulate the voltage of transmission lines and can also be used to transform voltages."""

    @property
    def short_name(self):
        return str(self)[15:]
