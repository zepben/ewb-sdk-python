#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_equipment import EquivalentEquipment

__all__ = ["EquivalentBranch"]


class EquivalentBranch(EquivalentEquipment):
    """
    The class represents equivalent branches. In cases where a transformer phase shift is modelled and the EquivalentBranch
    is spanning the same nodes, the impedance quantities for the EquivalentBranch shall consider the needed phase shift.
    """

    negative_r12: Optional[float] = None
    """"
    Negative sequence series resistance from terminal sequence 1 to terminal sequence 2. Used for short circuit data exchange according
    to IEC 60909. EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    negative_r21: Optional[float] = None
    """"
    Negative sequence series resistance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according
    to IEC 60909. EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    negative_x12: Optional[float] = None
    """"
    Negative sequence series reactance from terminal sequence 1 to terminal sequence 2. Used for short circuit data exchange according
    to IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    negative_x21: Optional[float] = None
    """"
    Negative sequence series reactance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according
    to IEC 60909. Usage: EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    positive_r12: Optional[float] = None
    """"
    Positive sequence series resistance from terminal sequence 1 to terminal sequence 2 . Used for short circuit data exchange according
    to IEC 60909. EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    positive_r21: Optional[float] = None
    """"
    Positive sequence series resistance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according
    to IEC 60909. EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    positive_x12: Optional[float] = None
    """"
    Positive sequence series reactance from terminal sequence 1 to terminal sequence 2. Used for short circuit data exchange according
    to IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    positive_x21: Optional[float] = None
    """"
    Positive sequence series reactance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according
    to IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    r: Optional[float] = None
    """"
    Positive sequence series resistance of the reduced branch.
    """

    r21: Optional[float] = None
    """"
    Resistance from terminal sequence 2 to terminal sequence 1 .Used for steady state power flow. This attribute is optional and represent
    unbalanced network such as off-nominal phase shifter. If only EquivalentBranch.r is given, then EquivalentBranch.r21 is assumed equal
    to EquivalentBranch.r. Usage rule : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    x: Optional[float] = None
    """"
    Positive sequence series reactance of the reduced branch.
    """

    x21: Optional[float] = None
    """"
    Reactance from terminal sequence 2 to terminal sequence 1. Used for steady state power flow. This attribute is optional and represents
    an unbalanced network such as off-nominal phase shifter. If only EquivalentBranch.x is given, then EquivalentBranch.x21 is assumed
    equal to EquivalentBranch.x. Usage rule: EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    zero_r12: Optional[float] = None
    """"
    Zero sequence series resistance from terminal sequence 1 to terminal sequence 2. Used for short circuit data exchange according to
    IEC 60909. EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    zero_r21: Optional[float] = None
    """
    Zero sequence series resistance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according to
    IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    zero_x12: Optional[float] = None
    """
    Zero sequence series reactance from terminal sequence 1 to terminal sequence 2. Used for short circuit data exchange according to
    IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """

    zero_x21: Optional[float] = None
    """
    Zero sequence series reactance from terminal sequence 2 to terminal sequence 1. Used for short circuit data exchange according to
    IEC 60909. Usage : EquivalentBranch is a result of network reduction prior to the data exchange.
    """
