#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC
from typing import Any
from typing_extensions import Self, deprecated

from zepben.ewb import BackedDescriptor, resolve_default
from zepben.ewb.boilerplate.collections.base import AbstractBackedList


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


class _IterableWrapper(_WrapperFgetFix, AbstractBackedList, ABC):
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
