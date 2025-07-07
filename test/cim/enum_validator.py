#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum
from typing import Type, Tuple

# noinspection PyPackageRequirements
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

# noinspection PyProtectedMember
from zepben.evolve.services.common.enum_mapper import EnumMapper


def validate_enum(cim_enum: Type[Enum], pb_enum: EnumTypeWrapper):
    if len(cim_enum) != len(pb_enum.items()):
        print()
        print(f"cim {list(map(lambda it: (it.name, it.value), cim_enum.__members__.values()))}")
        print("   vs")
        print(f"pb {pb_enum.items()}.")
    assert len(cim_enum) == len(pb_enum.items()), f"mismatch in number of entries. cim '{len(cim_enum)}' vs pb '{len(pb_enum.items())}'"

    mapper = EnumMapper(cim_enum, pb_enum)

    for cim in cim_enum:
        # We use the calculated `short_name` for the CIM enum, rather than just the `name`, for cases where we override the name. e.g. UnitSymbol.
        # we use the first value if the enum has multiple (i.e. PhaseCode) as this is the ordinal value.
        pb = pb_enum.DESCRIPTOR.values_by_number[cim.value[0] if isinstance(cim.value, Tuple) else cim.value]

        # noinspection PyUnresolvedReferences
        assert pb.name.upper().replace("_", "").endswith(cim.short_name.upper().replace("_", "")),\
            f"invalid value mapping for {cim.value}: cim '{cim.name}' vs pb '{pb.name}'"

        try:
            as_pb = mapper.to_pb(cim)
        except Exception as ex:
            print(f"Failed to lookup cim {cim.name}")
            raise ex

        try:
            as_cim = mapper.to_cim(pb)
        except Exception as ex:
            print(f"Failed to lookup proto {pb.name}")
            raise ex

        assert as_pb is pb, f"{cim.name}: Expected {pb.name}, found {as_pb}"
        assert as_cim is cim, f"{pb.name}: Expected {cim.name}, found {as_cim.name}"
