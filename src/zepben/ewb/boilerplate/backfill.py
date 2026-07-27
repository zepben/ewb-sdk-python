#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import Field
from types import MemberDescriptorType
from typing import Any, Callable, TypeVar, Protocol

from zepben.ewb import BackedDescriptor


class HasMrid(Protocol):
    mrid: str


S = TypeVar("S", bound=HasMrid)


class Backfill:
    def __init__(self, backfill_prop: property):
        self.backfill_prop = backfill_prop

    def apply(self, element: S, owner: Any):
        name = self.backfill_prop.fget.__name__

        if hasattr(self.backfill_prop, "__target"):
            backing_name = self.backfill_prop.__target.__name__
        else:
            backing_name = name

        if getattr(element, backing_name) is None:
            setattr(element, backing_name, owner)

        ref = getattr(element, backing_name)
        if ref is not owner:
            raise ValueError(f"{element} `{name}` property references {ref}, expected {owner}.")


def internal(target: Any):
    if not any(isinstance(target, cls) for cls in (Field, MemberDescriptorType, BackedDescriptor, property)):
        raise TypeError(f"target parameter of the target decorator has to be an instance of dataclass Field, instead is {target}")

    def dec(func: Callable):
        setattr(func, "__target", target)
        return func
    return dec
