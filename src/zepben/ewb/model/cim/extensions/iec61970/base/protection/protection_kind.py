#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ProtectionKind"]

from enum import Enum

from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class ProtectionKind(Enum):
    """
    [ZBEX]
    The kind of protection being provided by this protection equipment.
    """

    UNKNOWN = 0
    """[ZBEX] Unknown"""

    JG = 1
    """[ZBEX] Overcurrent"""

    JGG = 2
    """[ZBEX] Instantaneous"""

    JGGG = 3
    """[ZBEX] Instantaneous"""

    JT = 4
    """[ZBEX] Thermal overload"""

    J0 = 5
    """[ZBEX] Ground overcurrent"""

    J0GG = 6
    """[ZBEX] Instantaneous ground overcurrent"""

    SEF = 7
    """[ZBEX] Sensitive earth fault"""

    VG = 8
    """[ZBEX] Overvoltage"""

    VGG = 9
    """[ZBEX] Instantaneous overvoltage"""

    VL = 10
    """[ZBEX] Undervoltage"""

    VLL = 11
    """[ZBEX] Instantaneous"""

    V0G = 12
    """[ZBEX] Zero-sequence overvoltage"""

    V0GG = 13
    """[ZBEX] Instantaneous zero-sequence overvoltage"""

    JDIFF = 14
    """[ZBEX] Differential Current"""

    FREQ = 15
    """[ZBEX] Under frequency"""

    FREQG = 16
    """[ZBEX] Over frequency"""

    ZL = 17
    """[ZBEX] Phase distance"""

    Z0L = 18
    """[ZBEX] Ground distance"""

    LE = 19
    """[ZBEX] Load encroachment"""

    J2G = 20
    """[ZBEX] Negative-sequence overcurrent"""

    MULTI_FUNCTION = 21
    """[ZBEX] A multifunctional relay for universal usages"""

    GROUND_CURRENT = 22
    """[ZBEX] A device used to monitor and protect electrical equipment from damage caused by ground faults"""

    GROUND_VOLTAGE = 23
    """[ZBEX] A device used to detect contact accidents between an electric path and ground caused by arc ground faults"""

    NETWORK_PROTECTOR = 24
    """[ZBEX] Is a special self-contained air breaker or switching unit having a full complement of current, potential and control transformers, as well as relay functionality."""

    DISTANCE = 25
    """[ZBEX] A device used to detect faults on long-distance lines, pinpointing not only the fault condition but also measuring the distance between the current sensing mechanism and the fault location in the wire."""

    NEGATIVE_OVERCURRENT = 26
    """[ZBEX] A device used to protect generators from the unbalanced load by detecting negative sequence current."""

    POWER = 27
    """[ZBEX] A device that uses an electromagnet to open or close a circuit when the input (coil) is correctly excited"""

    SECTIONALIZER = 28
    """[ZBEX] A device that automatically isolates a faulted section of line from the rest of the distribution system"""

    AUTO_TRANSFORMER = 29
    """[ZBEX] A device used to regulate the voltage of transmission lines and can also be used to transform voltages."""

    @property
    def short_name(self):
        return str(self)[15:]
