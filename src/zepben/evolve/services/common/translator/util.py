#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject

__all__ = [
    "mrid_or_empty", "int_or_none", "uint_or_none", "float_or_none", "long_or_none", "str_or_none", "from_nullable_int", "from_nullable_uint",
    "from_nullable_float", "from_nullable_long"
]

#
# NOTE: These values must be comparable using standard equality operators (i.e ==)
#

_UNKNOWN_FLOAT = float("-inf")
_UNKNOWN_INT = -2147483648
_UNKNOWN_UINT = 4294967295
_UNKNOWN_LONG = -9223372036854775808


def mrid_or_empty(io: PBIdentifiedObject) -> str:
    return str(io.mrid) if io else ""


def int_or_none(value: int) -> Optional[int]:
    return value if value != _UNKNOWN_INT else None


def uint_or_none(value: int) -> Optional[int]:
    # The check against negative numbers is to handle issues with Python 3.7, which have been fixed in Python 3.9.
    return value if value != _UNKNOWN_UINT and value >= 0 else None


def float_or_none(value: float) -> Optional[float]:
    return value if value != _UNKNOWN_FLOAT else None


def long_or_none(value: int) -> Optional[int]:
    return value if value != _UNKNOWN_LONG else None


def str_or_none(value: str) -> Optional[str]:
    return value if value else None


def from_nullable_int(value: Optional[int]) -> int:
    return value if value is not None else _UNKNOWN_INT


def from_nullable_uint(value: Optional[int]) -> int:
    return value if value is not None else _UNKNOWN_UINT


def from_nullable_float(value: Optional[float]) -> float:
    return value if value is not None else _UNKNOWN_FLOAT


def from_nullable_long(value: Optional[int]) -> int:
    return value if value is not None else _UNKNOWN_LONG
