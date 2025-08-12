#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["VectorGroup"]

from enum import Enum

from zepben.ewb import unique
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
@unique
class VectorGroup(Enum):
    """
    [ZBEX]
    Vector group of the transformer for protective relaying, e.g., Dyn1. For unbalanced transformers, this may not be
    simply determined from the constituent winding connections and phase angle displacements.

    The vectorGroup string consists of the following components in the order listed: high voltage winding connection,
    mid voltage winding connection (for three winding transformers), phase displacement clock number from 0 to 11, low
    voltage winding connection phase displacement clock number from 0 to 11.

    The winding connections are D (delta), Y (wye), YN (wye with neutral), Z (zigzag), ZN (zigzag with neutral),
    A (auto transformer). Upper case means the high voltage, lower case mid or low. The high voltage winding always has
    clock position 0 and is not included in the vector group string.

    Some examples:
                   YNy0 (two winding wye to wye with no phase displacement),
                   YNd11 (two winding wye to delta with 330 degrees phase displacement),
                   YNyn0d5 (three winding transformer wye with neutral high voltage, wye with neutral mid
                            voltage and no phase displacement, delta low voltage with 150 degrees displacement).

    Phase displacement is defined as the angular difference between the phasors representing the voltages between the
    neutral point (real or imaginary) and the corresponding terminals of two windings, a positive sequence voltage system
    being applied to the high-voltage terminals, following each other in alphabetical sequence if they are lettered, or
    in numerical sequence if they are numbered: the phasors are assumed to rotate in a counter-clockwise sense.
    """

    UNKNOWN = 0
    """"[ZBEX] UNKNOWN."""

    DD0 = 1
    """[ZBEX] Dd0."""

    DZ0 = 2
    """[ZBEX] Dz0."""

    DZN0 = 3
    """[ZBEX] Dzn0."""

    YNY0 = 4
    """[ZBEX] YNy0."""

    YNYN0 = 5
    """[ZBEX] YNyn0."""

    YY0 = 6
    """[ZBEX] Yy0."""

    YYN0 = 7
    """[ZBEX] Yyn0."""

    ZD0 = 8
    """[ZBEX] Zd0."""

    ZND0 = 9
    """[ZBEX] ZNd0."""

    DYN1 = 10
    """[ZBEX] Dyn1."""

    DZ1 = 11
    """[ZBEX] Dz1."""

    DZN1 = 12
    """[ZBEX] Dzn1."""

    YD1 = 13
    """[ZBEX] Yd1."""

    YND1 = 14
    """[ZBEX] YNd1."""

    YNZN1 = 15
    """[ZBEX] YNzn1."""

    YZ1 = 16
    """[ZBEX] Yz1."""

    YZN1 = 17
    """[ZBEX] Yzn1."""

    ZD1 = 18
    """[ZBEX] Zd1."""

    ZND1 = 19
    """[ZBEX] ZNd1."""

    ZNYN1 = 20
    """[ZBEX] ZNyn1."""

    ZY1 = 21
    """[ZBEX] Zy1."""

    ZYN1 = 22
    """[ZBEX] Zyn1."""

    DY5 = 23
    """[ZBEX] Dy5."""

    DYN5 = 24
    """[ZBEX] Dyn5."""

    YD5 = 25
    """[ZBEX] Yd5."""

    YND5 = 26
    """[ZBEX] YNd5."""

    YNZ5 = 27
    """[ZBEX] YNz5."""

    YNZN5 = 28
    """[ZBEX] YNzn5."""

    YZ5 = 29
    """[ZBEX] Yz5."""

    YZN5 = 30
    """[ZBEX] Yzn5."""

    ZNY5 = 31
    """[ZBEX] ZNy5."""

    ZNYN5 = 32
    """[ZBEX] ZNyn5."""

    ZY5 = 33
    """[ZBEX] Zy5."""

    ZYN5 = 34
    """[ZBEX] Zyn5."""

    DD6 = 35
    """[ZBEX] Dd6."""

    DZ6 = 36
    """[ZBEX] Dz6."""

    DZN6 = 37
    """[ZBEX] Dzn6."""

    YNY6 = 38
    """[ZBEX] YNy6."""

    YNYN6 = 39
    """[ZBEX] YNyn6."""

    YY6 = 40
    """[ZBEX] Yy6."""

    YYN6 = 41
    """[ZBEX] Yyn6."""

    ZD6 = 42
    """[ZBEX] Zd6."""

    ZND6 = 43
    """[ZBEX] ZNd6."""

    DY7 = 44
    """[ZBEX] Dy7."""

    DYN7 = 45
    """[ZBEX] Dyn7."""

    DZ7 = 46
    """[ZBEX] Dz7."""

    DZN7 = 47
    """[ZBEX] Dzn7."""

    YD7 = 48
    """[ZBEX] Yd7."""

    YND7 = 49
    """[ZBEX] YNd7."""

    YNZN7 = 50
    """[ZBEX] YNzn7."""

    YZ7 = 51
    """[ZBEX] Yz7."""

    YZN7 = 52
    """[ZBEX] Yzn7."""

    ZD7 = 53
    """[ZBEX] Zd7."""

    ZND7 = 54
    """[ZBEX] ZNd7."""

    ZNYN7 = 55
    """[ZBEX] ZNyn7."""

    ZY7 = 56
    """[ZBEX] Zy7."""

    ZYN7 = 57
    """[ZBEX] Zyn7."""

    DY11 = 58
    """[ZBEX] Dy11."""

    DYN11 = 59
    """[ZBEX] Dyn11."""

    YD11 = 60
    """[ZBEX] Yd11."""

    YND11 = 61
    """[ZBEX] YNd11."""

    YNZ11 = 62
    """[ZBEX] YNz11."""

    YNZN11 = 63
    """[ZBEX] YNzn11."""

    YZ11 = 64
    """[ZBEX] Yz11."""

    YZN11 = 65
    """[ZBEX] Yzn11."""

    ZNY11 = 66
    """[ZBEX] ZNy11."""

    ZNYN11 = 67
    """[ZBEX] ZNyn11."""

    ZY11 = 68
    """[ZBEX] Zy11."""

    ZYN11 = 69
    """[ZBEX] Zyn11."""

    DY1 = 70
    """[ZBEX] Dy1."""

    Y0 = 71
    """[ZBEX] Y0."""

    YN0 = 72
    """[ZBEX] YN0."""

    D0 = 73
    """[ZBEX] D0."""

    ZNY1 = 74
    """[ZBEX] ZNy1."""

    ZNY7 = 75
    """[ZBEX] ZNy7."""

    DDN0 = 76
    """[ZBEX] Ddn0."""

    DND0 = 77
    """[ZBEX] DNd0."""

    DNYN1 = 78
    """[ZBEX] DNyn1."""

    DNYN11 = 79
    """[ZBEX] DNyn11."""

    YNDN1 = 80
    """[ZBEX] YNdn1."""

    YNDN11 = 81
    """[ZBEX] YNdn11."""

    TTN11 = 82
    """[ZBEX] Scott-T Transformer."""

    @property
    def short_name(self):
        return str(self)[12:]
