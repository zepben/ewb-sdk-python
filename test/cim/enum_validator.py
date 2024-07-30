#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum
from typing import Type, Tuple

# noinspection PyPackageRequirements
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper


def validate_enum(cim_enum: Type[Enum], pb_enum: EnumTypeWrapper):
    if len(cim_enum) != len(pb_enum.items()):
        print()
        print(f"cim {list(map(lambda it: (it.name, it.value), cim_enum.__members__.values()))}")
        print("   vs")
        print(f"pb {pb_enum.items()}.")
    assert len(cim_enum) == len(pb_enum.items()), f"mismatch in number of entries. cim '{len(cim_enum)}' vs pb '{len(pb_enum.items())}'"

    for cim in cim_enum:
        if isinstance(cim.value, Tuple):
            assert pb_enum.Value(cim.short_name) == cim.value[0], f"invalid name mapping for cim '{cim.value[0]}' vs pb '{pb_enum.Value(cim.short_name)}'"
            assert pb_enum.Name(cim.value[0]) == cim.short_name, f"invalid value mapping for cim '{cim.short_name}' vs pb '{pb_enum.Name(cim.value[0])}'"
        else:
            assert pb_enum.Value(cim.short_name) == cim.value, f"invalid name mapping for cim '{cim.value}' vs pb '{pb_enum.Value(cim.short_name)}'"
            assert pb_enum.Name(cim.value) == cim.short_name, f"invalid value mapping for cim '{cim.short_name}' vs pb '{pb_enum.Name(cim.value)}'"
