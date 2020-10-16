


#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.exceptions import CoreException
__all__ = ["SUPPORTED_CORES", "validate_core", "from_count", "CorePath"]
SUPPORTED_CORES = 4


def validate_core(core: int):
    if core < 0 or core > SUPPORTED_CORES:
        raise CoreException(f"Invalid number of cores, was {core} but must be between 0 and {SUPPORTED_CORES}")
    return core


def from_count(num_cores: int):
    validate_core(num_cores)
    return range(0, num_cores)


class CorePath(object):
    def __init__(self, from_core: int, to_core: int):
        self.from_core = validate_core(from_core)
        self.to_core = validate_core(to_core)

    def __eq__(self, other):
        if self is other:
            return True
        return self.from_core == other.from_core and self.to_core == other.to_core

    def __ne__(self, other):
        if self is other:
            return False
        return self.from_core != other.from_core or self.to_core != other.to_core

    def __hash__(self):
        return hash((self.from_core, self.to_core))

    def __lt__(self, other):
        if self.from_core < other.from_core and self.to_core < other.to_core:
            return True
        else:
            return False
