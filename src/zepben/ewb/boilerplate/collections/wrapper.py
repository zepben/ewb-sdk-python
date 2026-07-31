#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import ABC
from dataclasses import Field
from typing import Any, TypeVar

from typing_extensions import Self, deprecated

from zepben.ewb import BackedDescriptor, resolve_default
from zepben.ewb.boilerplate.collections.abstract_backed_collection import AbstractBackedCollection


class _Wrapper(BackedDescriptor):
    """
    Descriptor base for collection views backed by another dataclass field.

    Access through an instance creates a short-lived wrapper bound to that
    instance and its backing field. For example::

        class Container:
            _items = field(default=None)
            items = LazyList(_items)

        container = Container()

        # Calls Container.items.__get__(container, Container), returning a
        # wrapper whose _instance is container and _backing_name is "_items".
        bound_items = container.items
        bound_items.append("value")

        assert container._items == ["value"]

    Access through the class returns the original shared descriptor::

        assert isinstance(Container.items, LazyList)
    """

    _instance: Any
    _backing_name: Any

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """
        This __new__ stores the init arguments, and otherwise acts as default.
        We need this to efficiently and truly re-create the wrapper and bind it to an instance upon a get call.
        """
        obj = super().__new__(cls)
        obj._init_args = args
        obj._init_kwargs = kwargs.copy()
        return obj

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._instance = None
        self._backing_name = None

    def __get__(self, instance, _=None) -> Self:
        """
        This creates a copy of self, pointing it to the specific instance that the wrapper is attached to.
        From there on, the wrapper functions as a lazy list.
        """
        if instance is None:
            return self
        obj = type(self)(*self._init_args, **self._init_kwargs)
        obj._instance = instance
        obj._backing_name = self.private_field.name
        return obj


class _WrapperFgetFix(_Wrapper):
    """
    This class exists to fix the tests that rely on the old lists being @property.
    It implements a minimalistic callable fget with a name.
    TODO: Remove in a separate PR fixing tests
    """
    def __init__(self, *args, **kwargs) -> None:
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

T = TypeVar("T")

class _IterableWrapper(_WrapperFgetFix, AbstractBackedCollection[T], ABC):
    """
    This class allows us to assign lists at init time to avoid special-case handling.
    """
    def __set__(self, instance, value) -> None:
        if instance is None:
            return
        if not hasattr(instance, self._backing_name) and isinstance(self.private_field, Field):
            resolve_default(instance, self.private_field)
        elif getattr(instance, self._backing_name):
            raise ValueError(f"Cannot assign list {self.__name__} for {instance}: currently non-empty")
        if value is not None:
            self.__get__(instance).extend(value)
        else:
            self.__get__(instance).clear()
