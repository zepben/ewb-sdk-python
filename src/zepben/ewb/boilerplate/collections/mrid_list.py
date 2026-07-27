#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod, ABC
from dataclasses import dataclass, field, Field
from types import MemberDescriptorType
from typing import Any, TypeVar, Protocol, Callable, Sequence

import pytest
from typing_extensions import Self

from zepben.ewb import BackedDescriptor
from zepben.ewb.boilerplate.collections.lazy_list import LazyValidatedList
from zepben.ewb.boilerplate.collections.wrapper import _IterableWrapper
from zepben.ewb.boilerplate.collections.base import AbstractBackedCollection, AbstractBackedList


class HasMrid(Protocol):
    mrid: str

T = TypeVar("T")
S = TypeVar("S", bound=HasMrid)

class MridCollection(AbstractBackedCollection[S], ABC):
    instance: Any
    element_description: str

    @abstractmethod
    def _safe_get_by_mrid(self, mrid: str) -> S | None: ...

    def get_by_mrid(self, mrid: str) -> S:
        res = self._safe_get_by_mrid(mrid)
        if res is None:
            raise KeyError
        return res

    def _can_add_by_mrid(self, element: S) -> bool:
        existing = self._safe_get_by_mrid(element.mrid)

        if existing is None:
            return True

        if existing is not element:
            raise ValueError(
                f"{self.element_description} with mRID {element.mrid} "
                f"already exists in {self.instance}."
            )

        return False


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

class LazyMridList(LazyValidatedList, MridCollection[S]):
    def __init__(self,
                 private_field,
                 element_description: str,
                 backfill: Backfill = None,
                 validate=None,
                 sort_by=None):
        super().__init__(private_field, validate, sort_by)
        self.element_description = element_description
        self.backfill = backfill

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        existing = self._get()
        if existing is None:
            return None
        found = next((element for element in existing if element.mrid == mrid), None)
        return found

    def append(self, item: T):
        if not self._can_add_by_mrid(item):
            return

        if self.backfill is not None:
            self.backfill.apply(item, self.instance)

        super().append(item)


class MridList(_IterableWrapper, AbstractBackedList[S], MridCollection[S]):
    def __init__(self,
                 private_field,
                 element_description: str,
                 validate=None,
                 sort_by=None):
        super().__init__(private_field)
        self.element_description = element_description
        self.validate = validate
        self.sort_by = sort_by
        self.backing_list = None

    def __get__(self, instance, owner=None) -> Self:
        obj = super().__get__(instance, owner)
        if obj is not self:
            # noinspection PyUnresolvedReferences
            obj.__post_init__()
        return obj

    def __post_init__(self):
        self.backing_list = getattr(self.instance, self.backing_name)

    def _get_collection(self) -> Sequence[T]:
        return self.backing_list

    def _safe_get_by_mrid(self, mrid: str) -> S | None:
        found = next((element for element in self.backing_list if element.mrid == mrid), None)
        return found

    def append(self, item: S):
        if not self._can_add_by_mrid(item):
            return

        if self.validate is not None:
            self.validate(self.instance, item)

        self.backing_list.append(item)

        if self.sort_by is not None:
            self.backing_list.sort(key=self.sort_by)

    def __len__(self):
        return len(self.backing_list)

    def __iter__(self):
        return iter(self.backing_list)

    def __contains__(self, item):
        return item in self.backing_list

    def remove(self, item):
        self.backing_list.remove(item)

    def clear(self):
        self.backing_list.clear()

    def __repr__(self):
        return str(self.backing_list)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        return self.backing_list[item]






if __name__ == '__main__':
    @dataclass(slots=True)
    class Ido:
        mrid: str
        n: int = 42

    @dataclass(slots=True)
    class A:
        # _x: list[Ido] = field(default_factory=list)
        _x: list[Ido] = field(default=None)
        # x: MridCollection[Ido] = MridList(
        x: MridCollection[Ido] = LazyMridList(
            _x,
            "A Thingo",
            validate=(lambda self, it: self.validate_x(it)),
            sort_by=(lambda it: it.n),
        )

        def validate_x(self, item):
            print(f"validating {item}")

        def __hash__(self):
            return object.__hash__(self)

    o1 = Ido("1")
    o2 = Ido("2", 24)
    oX = Ido("2", 32)

    a = A()
    print(a, a.x)
    a.x.append(o1)
    print(a, a.x)
    a.x.append(o2)
    print(a, a.x)
    for t in a.x:
        print(t)
    a.x.remove(o1)
    print(a, a.x)
    a.x.remove(o2)
    print(a, a.x)

    a.x.append(o2)
    print(a, a.x)
    with pytest.raises(ValueError):
        a.x.append(oX)
    print(a, a.x)
