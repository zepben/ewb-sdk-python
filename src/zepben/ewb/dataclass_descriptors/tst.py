#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import copy
import time
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import Any
from typing_extensions import Self, deprecated
from zepben.ewb import remove_descriptor_annotations, BackedDescriptor, resolve_default


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

    def __get__(self, instance, _=None) -> Self:
        """
        This creates a copy of self, pointing it to the specific instance that the wrapper is attached to.
        From there on, the wrapper functions as a lazy list.
        """
        obj = type(self)(*self._init_args, **self._init_kwargs)
        obj.instance = instance
        obj.backing_name = self.private_field.name
        return obj

class _WrapperFgetFix(_Wrapper):
    """
    This class exists to fix the tests that rely on the old lists being @property.
    TODO: Remove in a separate PR fixing tests
    """
    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)

        def fget(instance):
            return self.__get__(instance)

        fget.__name__ = name
        fget.__qualname__ = f"{owner.__qualname__}.{name}"

        self.fget = fget

    @deprecated("Lists are no longer a property")
    def fget(self, instance):
        # TODO: Remove test hack in separate PR
        raise NotImplementedError()

class _IterableWrapper(_WrapperFgetFix, ABC):
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

    @abstractmethod
    def extend(self, items): ...

    @abstractmethod
    def clear(self): ...


class ListWrapper(_IterableWrapper):

    def clear(self):
        self._set(None)

    def extend(self, items):
        for item in items:
            self.append(item)

    def __init__(
        self,
        private_field: Any,
        validate = None,
        sort_by = None
    ):
        super().__init__(private_field)
        self.validate = validate
        self.sort_by = sort_by

    def _get(self):
        if self.instance is None:
            return self
        return getattr(self.instance, self.backing_name)

    def _set(self, value):
        if self.instance is None:
            return
        setattr(self.instance, self.backing_name, value)

    def __str__(self):
        return str(self._get())

    def append(self, item):
        l = self._get()
        if l is None:
            self._set([item])
        else:
            l.append(item)




@dataclass
class C:
    _x: list[int] | None = field(default=None)
    x: ListWrapper = ListWrapper(_x, sort_by=lambda it: -it)

    @property
    def thing(self):
        return 42

if __name__ == '__main__':
    c = C([1, 2, 3])
    print(c)
    print(c.x)
    print(c.x.sort_by)
    c.x.clear()
    c.x.append(42)
    print(c)
    print(c.x)

    c.thing = 24

    # class C:
    #     def __init__(self, x, f1, f2):
    #         self.x = x
    #         self.y = x + x
    #         self.f1 = f1
    #         self.f2 = f2
    #
    # N = 1_000_000
    # t = time.time()
    # for _ in range(N):
    #     tmp = C("blahblahblah", lambda : 42, lambda : 24)
    # print(time.time() - t)
    #
    # c = C("blahblahblah", lambda : 42, lambda : 24)
    # t = time.time()
    # for _ in range(N):
    #     tmp = copy.copy(c)
    # print(time.time() - t)
    ...