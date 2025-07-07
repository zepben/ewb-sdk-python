#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [""]

import os.path
from enum import Enum
from typing import Type

# noinspection PyPackageRequirements
from google.protobuf.descriptor import EnumDescriptor
# noinspection PyPackageRequirements
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper


# NOTE: EnumMapper has been deliberately left out of the package exports as it is not public API.
class EnumMapper:
    """
    A class for mapping between CIM and protobuf variants of the same Enum.
    """

    def __init__(self, cim_enum: Type[Enum], pb_enum: EnumTypeWrapper):
        pb_common_key = self._common_prefix(pb_enum)

        cim_by_key = {self._extract_key_from_cim(it): it for it in cim_enum}
        pb_by_key = {self._extract_key_from_pb(it, pb_common_key): it for it in pb_enum.DESCRIPTOR.values}

        # todo requireNotNull(pb_by_key[key]) { "$cim: CIM key '$key' wasn't found in the protobuf enum mappings $pb_by_key" }
        self._cim_to_proto = {cim: pb_by_key[key] for key, cim in cim_by_key.items()}

        # todo requireNotNull(cim_by_key[key]) { "$pb: Protobuf key '$key' wasn't found in the CIM enum mappings $cim_by_key" }
        self._proto_to_cim = {pb: cim_by_key[key] for key, pb in pb_by_key.items()}

    def to_pb(self, cim: Enum) -> EnumDescriptor:
        """Convert the CIM enum value to the equivalent protobuf variant."""
        return self._cim_to_proto[cim]

    def to_cim(self, pb: EnumDescriptor) -> Enum:
        """Convert the protobuf enum value to the equivalent CIM variant."""
        return self._proto_to_cim[pb]

    @staticmethod
    def _extract_key(name: str) -> str:
        return name.upper().replace("_", "")

    def _extract_key_from_cim(self, enum: Enum) -> str:
        # We use the calculated `short_name` for the CIM enum, rather than just the `name`, for cases where we override the name. e.g. UnitSymbol.
        # noinspection PyUnresolvedReferences
        return self._extract_key(enum.short_name)

    def _extract_key_from_pb(self, enum: Enum, pb_common_key: str) -> str:
        return self._extract_key(enum.name.removeprefix(pb_common_key))

    @staticmethod
    def _common_prefix(pb_enum: EnumTypeWrapper) -> str:
        """Find the common starting for the protobuf enum."""
        return os.path.commonprefix([it for it in pb_enum.keys()])
