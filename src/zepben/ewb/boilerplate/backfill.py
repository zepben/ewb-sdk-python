#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import Field
from types import MemberDescriptorType
from typing import Any, Callable, TypeVar

from zepben.ewb import BackedDescriptor
from zepben.ewb.boilerplate.collections.mrid_collection import S


F = TypeVar("F", bound=Callable[..., Any])


class Backfill:
    def __init__(self, backfill_prop: property) -> None:
        if backfill_prop.fget is None:
            raise TypeError(f"Cannot backfill a property without a getter: {backfill_prop!r}")

        self.backfill_prop = backfill_prop

    def apply(self, element: S, owner: Any) -> None:
        name = self.backfill_prop.fget.__name__

        target = getattr(self.backfill_prop.fget, "_internal_target", None)
        backing_name = name if target is None else (
            getattr(target, "name", None)
            or getattr(target, "__name__", None)
            or getattr(getattr(target, "fget", None), "__name__", None)
        )

        if backing_name is None:
            raise TypeError(f"Cannot determine backing name for {target!r}")

        if getattr(element, backing_name) is None:
            setattr(element, backing_name, owner)

        ref = getattr(element, backing_name)
        if ref is not owner:
            raise ValueError(f"{element} `{name}` property references {ref}, expected {owner}.")


def internal(target: Any) -> Callable[[F], F]:
    if not any(isinstance(target, cls) for cls in (Field, MemberDescriptorType, BackedDescriptor, property)):
        raise TypeError(f"target parameter of the target decorator has to be an instance of property or dataclass Field, instead is {target}")

    if isinstance(target, property) and target.fget is None:
        raise TypeError(f"Cannot backfill a property without a getter: {target}")

    def dec(func: Callable):
        setattr(func, "_internal_target", target)
        return func
    return dec
