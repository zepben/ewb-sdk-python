#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from collections.abc import Collection
from dataclasses import field
from typing import TypeVar, Protocol, Any, Iterable

from typing_extensions import deprecated, Self

from zepben.ewb import BackedDescriptor, remove_descriptor_annotations, resolve_default, DataclassBase, zb_dataclass


# from descriptor_fix import BackedDescriptor, remove_descriptor_annotations


class HasMrid(Protocol):
    mrid: str

T = TypeVar("T")
S = TypeVar("S", bound=HasMrid)

class MutableCollection(Collection[T], Protocol[T]):
    def append(self, item: T) -> None: ...

    def remove(self, item: T) -> None: ...

    def clear(self) -> None: ...

    def extend(self, items: Collection[T]) -> None:
        for item in items:
            self.append(item)

    def __next__(self):
        # TODO: Remove test hack in separate PR
        return next(iter(self))

    def __eq__(self, other):
        return isinstance(other, Iterable) and all(a == b for a, b in zip(self, other))


class IndexedMutableCollection(MutableCollection, ABC):
    def __getitem__(self, idx: int) -> T: ...



class _Wrapper(BackedDescriptor):

    instance: Any
    backing_name: Any

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """
        This __new__ stores the init arguments, and otherwise acts as default.
        We need this to efficiently and truly re-create the wrapper and bind it to an instance upon a get call.
        """
        obj = super().__new__(cls)
        obj._init_args = args
        obj._init_kwargs = kwargs.copy()
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = None
        self.backing_name = None

    def __get__(self, instance, _=None) -> Self:
        """
        This creates a copy of self, pointing it to the specific instance that the wrapper is attached to.
        From there on, the wrapper functions as a lazy list.
        """
        if instance is None:
            return self
        obj = type(self)(*self._init_args, **self._init_kwargs)
        obj.instance = instance
        obj.backing_name = self.private_field.name
        return obj

class _WrapperFgetFix(_Wrapper):
    """
    This class exists to fix the tests that rely on the old lists being @property.
    TODO: Remove in a separate PR fixing tests
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        def fget(instance):
            return self.__get__(instance)
        self.fget = fget

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self.fget.__name__ = name
        self.fget.__qualname__ = f"{owner.__qualname__}.{name}"

    @deprecated("Lists are no longer a property")
    def fget(self, instance): ...

class _IterableWrapper(_WrapperFgetFix, IndexedMutableCollection, ABC):
    """
    This class allows us to assign lists at init time to avoid special-case handling.
    """
    def __set__(self, instance, value):
        if instance is None:
            return
        if not hasattr(instance, self.backing_name):
            resolve_default(instance, self.private_field)
        elif getattr(instance, self.backing_name):
            raise ValueError(f"Cannot assign list {self.__name__} for {instance}: currently non-empty")
        if value is not None:
            self.__get__(instance).extend(value)
        else:
            self.__get__(instance).clear()

class LazyValidatedList(_IterableWrapper, IndexedMutableCollection[T]):
    def __init__(self,
                 private_field,
                 validate=None,
                 sort_by=None):
        super().__init__(private_field)
        self.validate = validate
        self.sort_by = sort_by

    def _get(self):
        return getattr(self.instance, self.backing_name)

    def _get_or_empty(self) -> list[T]:
        return getattr(self.instance, self.backing_name) or []

    # clearIfEmpty is inlined for performance

    def append(self, item):
        if self.validate is not None:
            self.validate(self.instance, item)

        existing = getattr(self.instance, self.backing_name)
        if existing is None:
            existing = [item]
            setattr(self.instance, self.backing_name, existing)
        else:
            existing.append(item)

        if self.sort_by is not None:
            existing.sort(key=self.sort_by)

    def __len__(self):
        return len(self._get_or_empty())

    def __iter__(self):
        return iter(self._get_or_empty())

    def __contains__(self, item):
        return item in (self._get_or_empty())

    def remove(self, item):
        existing = self._get_or_empty()
        existing.remove(item)
        if not existing:
            self.clear()

    def clear(self):
        setattr(self.instance, self.backing_name, None)

    def __repr__(self):
        if self.instance is None:
            return self.__class__.__repr__()
        return str(self._get_or_empty())

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        return (self._get_or_empty())[item]


if __name__ == '__main__':
    @zb_dataclass
    class C(DataclassBase):
        _xs: list[int] | None = field(default=None)
        xs: IndexedMutableCollection[int] = LazyValidatedList(
            _xs,
            validate=lambda self, it: print("validate", it),
            sort_by=lambda it: -it
        )

    c = C(xs=[24, 42])
    print(c._xs)
    c.xs.clear()
    print(c._xs)
    c.xs.append(1)
    c.xs.append(2)
    c.xs.append(3)
    print(c._xs)
