#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["VectorGroup"]


class VectorGroup(Enum):
    UNKNOWN = 0
    DD0 = 1
    DZ0 = 2
    DZN0 = 3
    YNY0 = 4
    YNYN0 = 5
    YY0 = 6
    YYN0 = 7
    ZD0 = 8
    ZND0 = 9
    DYN1 = 10
    DZ1 = 11
    DZN1 = 12
    YD1 = 13
    YND1 = 14
    YNZN1 = 15
    YZ1 = 16
    YZN1 = 17
    ZD1 = 18
    ZND1 = 19
    ZNYN1 = 20
    ZY1 = 21
    ZYN1 = 22
    DY5 = 23
    DYN5 = 24
    YD5 = 25
    YND5 = 26
    YNZ5 = 27
    YNZN5 = 28
    YZ5 = 29
    YZN5 = 30
    ZNY5 = 31
    ZNYN5 = 32
    ZY5 = 33
    ZYN5 = 34
    DD6 = 35
    DZ6 = 36
    DZN6 = 37
    YNY6 = 38
    YNYN6 = 39
    YY6 = 40
    YYN6 = 41
    ZD6 = 42
    ZND6 = 43
    DY7 = 44
    DYN7 = 45
    DZ7 = 46
    DZN7 = 47
    YD7 = 48
    YND7 = 49
    YNZN7 = 50
    YZ7 = 51
    YZN7 = 52
    ZD7 = 53
    ZND7 = 54
    ZNYN7 = 55
    ZY7 = 56
    ZYN7 = 57
    DY11 = 58
    DYN11 = 59
    YD11 = 60
    YND11 = 61
    YNZ11 = 62
    YNZN11 = 63
    YZ11 = 64
    YZN11 = 65
    ZNY11 = 66
    ZNYN11 = 67
    ZY11 = 68
    ZYN11 = 69
    DY1 = 70
    Y0 = 71
    YN0 = 72
    D0 = 73
    ZNY1 = 74
    ZNY7 = 75
    DDN0 = 76
    DND0 = 77
    DNYN1 = 78
    DNYN11 = 79
    YNDN1 = 80
    YNDN11 = 81
    TTN11 = 82

    @property
    def short_name(self):
        return str(self)[12:]
