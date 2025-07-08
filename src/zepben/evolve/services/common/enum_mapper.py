#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [""]

import os.path
from enum import Enum
from typing import Type, TypeVar, Generic

from google.protobuf.descriptor import EnumValueDescriptor
# noinspection PyPackageRequirements
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

TCimEnum = TypeVar("TCimEnum", bound=Enum)
TProtoEnum = TypeVar("TProtoEnum")


# NOTE: EnumMapper has been deliberately left out of the package exports as it is not public API.
class EnumMapper(Generic[TCimEnum, TProtoEnum]):
    """
    A class for mapping between CIM and protobuf variants of the same Enum.

    NOTE: There is no need to do the reverse map back to CIM as the python version uses ints that can just be used to construct the enum directly.
    """

    def __init__(self, cim_enum: Type[TCimEnum], pb_enum: EnumTypeWrapper):
        pb_common_key = self._common_prefix(pb_enum)

        cim_by_key = {self._extract_key_from_cim(it): it for it in cim_enum}
        pb_by_key = {self._extract_key_from_pb(it, pb_common_key): it for it in pb_enum.DESCRIPTOR.values}

        self._cim_to_proto = {cim: pb_by_key[key] for key, cim in cim_by_key.items()}

    def to_pb(self, cim: TCimEnum) -> TProtoEnum:
        """Convert the CIM enum value to the equivalent protobuf variant."""
        return self._cim_to_proto[cim].number

    @staticmethod
    def _extract_key(name: str) -> str:
        return name.upper().replace("_", "")

    def _extract_key_from_cim(self, enum: Enum) -> str:
        # We use the calculated `short_name` for the CIM enum, rather than just the `name`, for cases where we override the name. e.g. UnitSymbol.
        # noinspection PyUnresolvedReferences
        return self._extract_key(enum.short_name)

    def _extract_key_from_pb(self, enum: EnumValueDescriptor, pb_common_key: str) -> str:
        return self._extract_key(enum.name.removeprefix(pb_common_key))

    @staticmethod
    def _common_prefix(pb_enum: EnumTypeWrapper) -> str:
        """Find the common starting for the protobuf enum."""
        return os.path.commonprefix([it for it in pb_enum.keys()])
