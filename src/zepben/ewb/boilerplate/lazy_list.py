#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from collections.abc import Collection
from dataclasses import field
from typing import TypeVar, Protocol, Any, Iterable, Generic, Iterator, Sequence, overload, Callable

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


class AbstractBackedCollection(Collection[T], Generic[T], ABC):

    @abstractmethod
    def _get_collection(self) -> Collection[T]:
        ...

    @abstractmethod
    def append(self, element: T) -> None:
        ...

    def extend(self, elements: Iterable[T]) -> None:
        for element in elements:
            self.append(element)

    @abstractmethod
    def remove(self, element: T) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    def __len__(self) -> int:
        return len(self._get_collection())

    def __iter__(self) -> Iterator[T]:
        return iter(self._get_collection())

    def __contains__(self, element: object) -> bool:
        return element in self._get_collection()

    def for_each_indexed(self, action: Callable[[int, T], Any]):
        """
        Call the `action` on each item in the list

        :param action: An action to apply to each :class:`RelaySetting` in the `thresholds` collection, taking the index of the threshold, and the threshold itself.
        """
        for index, item in enumerate(self._get_collection()):
            action(index, item)



class AbstractBackedList(
    AbstractBackedCollection[T],
    Sequence[T],
    Generic[T],
    ABC,
):

    @abstractmethod
    def _get_collection(self) -> Sequence[T]:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        return self._get_collection()[index]


class LazyValidatedList(_IterableWrapper, AbstractBackedList[T]):

    def __init__(self,
                 private_field,
                 validate=None,
                 sort_by=None):
        super().__init__(private_field)
        self.validate = validate
        self.sort_by = sort_by

    def _get(self):
        return getattr(self.instance, self.backing_name)

    def _get_collection(self) -> list[T]:
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
        return len(self._get_collection())

    def __iter__(self):
        return iter(self._get_collection())

    def __contains__(self, item):
        return item in (self._get_collection())

    def remove(self, item):
        existing = self._get_collection()
        existing.remove(item)
        if not existing:
            self.clear()

    def clear(self):
        setattr(self.instance, self.backing_name, None)

    def __repr__(self):
        if self.instance is None:
            return self.__class__.__repr__()
        return str(self._get_collection())

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        return (self._get_collection())[item]


class LazyIndexedList(LazyValidatedList[T]):

    def __init__(
        self,
        private_field,
        element_description: str
    ):
        super().__init__(private_field)
        self.element_description = element_description

    def insert(self, index: int, item: T) -> None:
        """
        Insert ``item`` at ``index``.
        """
        size = len(self)

        if not 0 <= index <= size:
            raise ValueError(
                f"Unable to add {self.element_description} to "
                f"{self.instance}. "
                f"Sequence number {index} is invalid. "
                f"Expected a value between 0 and {size}. "
                "Make sure you are adding the items in order and there are "
                "no gaps in the numbering."
            )

        existing = getattr(self.instance, self.backing_name)

        if existing is None:
            existing = [item]
            setattr(self.instance, self.backing_name, existing)
        else:
            existing.insert(index, item)

        if self.sort_by is not None:
            existing.sort(key=self.sort_by)

    def append(self, item: T) -> None:
        self.insert(len(self), item)

    def pop(self, index: int = -1) -> T:
        """
        Remove and return the item at ``index``.

        Uses normal Python list semantics, including support for negative
        indexes and raising ``IndexError`` when the index is invalid.
        """
        existing = getattr(self.instance, self.backing_name)

        if existing is None:
            raise IndexError("pop from empty list")

        item = existing.pop(index)

        if not existing:
            self.clear()

        return item

if __name__ == '__main__':
    @zb_dataclass
    class C(DataclassBase):
        _xs: list[int] | None = field(default=None)
        xs: LazyIndexedList[int] = LazyIndexedList(
            _xs,
            "Thing"
        )

    c = C(xs=[24, 42])
    print(c._xs, c.xs)
    c.xs.clear()
    print(c._xs, c.xs)
    c.xs.append(1)
    c.xs.append(2)
    c.xs.append(3)
    print(c._xs, c.xs)
    c.xs.insert(2, 42)
    print(c._xs, c.xs)
    c.xs.pop(2)
    print(c._xs, c.xs)
