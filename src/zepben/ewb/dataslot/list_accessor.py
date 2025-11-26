#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""

This file is a work-in-progress monolith that is used to develop
features related to boilerplate injection. The code will be typed,
cleaned up, and split up once the first version is finalised.

Do not rely on features from this file.

"""
from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from functools import partial, cache
from typing import List, Iterable, Optional, TypeVar, Generator, Type, Dict, Sized, Generic, Iterator, ClassVar

from typing_extensions import override

from zepben.ewb.dataslot.dataslot import BackedDescriptor, Fget

__all__ = [
    'boilermaker',
    'ListActions',

    'ListAccessor',
    'MRIDListAccessor',
    'MRIDDictAccessor',

    'ListRouter',
    'MRIDDictRouter',
    'MRIDListRouter',

    'override_boilerplate',
    'custom_add',
    'custom_clear',
    'custom_get',
    'custom_get_by_mrid',
    'custom_len',
    'custom_remove',
]


T = TypeVar('T')
S = TypeVar('S')

class _Actions(Enum):
    ADD = partial(lambda item : f'add_{item}')
    CLEAR = partial(lambda item : f'clear_{item}')
    REMOVE = partial(lambda item : f'remove_{item}')

ListActions = None


def boilermaker(cls):
    ...
    return cls

_action_methods = {
    _Actions.ADD: '_default_add',
    _Actions.CLEAR: '_default_clear',
    _Actions.REMOVE: '_default_remove',
}


class _Fwd:
    def __init__(self, callable):
        self._callable = callable
    def __call__(self, *args, **kwargs):
        self._callable(*args, **kwargs)

class ListInterface:
    def __init__(self, _owner=None):
        self.__owner__ = _owner

    def append_unchecked(self, __object):
        raise NotImplementedError()
    def remove_unchecked(self, __object):
        raise NotImplementedError()
    def clear_unchecked(self):
        raise NotImplementedError()

    _custom_append: ClassVar[Callable | None] = None
    _custom_clear: ClassVar[Callable | None] = None
    _custom_remove: ClassVar[Callable | None] = None

    def _append_caller(self, __object):
        self._custom_append(self.__owner__, __object)
    def _clear_caller(self):
        self._custom_clear(self.__owner__)
    def _remove_caller(self, __object):
        self._custom_remove(self.__owner__, __object)

# This is needed to make the type checker chill out
# ListAccessor __get__ return is picked up as default type otherwise
class _ListAccessorBase(BackedDescriptor):
    def __init__(self,
                 default=None,
                 backed_name=None):
        super().__init__(default, backed_name)
        self.methods = {}


class ListAccessor(_ListAccessorBase):
    def __init__(self,
                 default=None,
                 backed_name=None):
        super().__init__(default, backed_name)
        self.router_class = ListRouter
        self.custom_append = None
        self.custom_clear = None
        self.custom_remove = None

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self._subclass_router()

    def _subclass_router(self):
        router_subname = (self.owner.__name__ + "_"
                          + self.public_name + "_"
                          + self.router_class.__name__)
        r = self.router_class = type(router_subname, (self.router_class,), {})
        if self.custom_append is not None:
            r._custom_append = self.custom_append
            r.append = r._append_forwarding
        elif self.custom_clear is not None:
            r._custom_clear = self.custom_clear
            r.clear = r._clear_forwarding
        elif self.custom_remove is not None:
            r._custom_remove = self.custom_remove
            r.remove = r._remove_forwarding

    def attach_router_member(self, member: Callable, action: _Actions):
        if action == _Actions.ADD:
            self.custom_append = member
        elif action == _Actions.CLEAR:
            self.custom_clear = member
        elif action == _Actions.REMOVE:
            self.custom_remove = member

    def _rawdog(self, instance):
        return self.router_class(instance, self, self.private_name, self.public_name)

    @cache
    def _get_cached(self, instance, _id):
        return self._rawdog(instance)

    def get_method(self, action: _Actions):
        return self.methods[action]

    @override
    def __get__(self, instance, default=None):
        try:
            return self._get_cached(instance, id(instance))
        except TypeError:
            return self._rawdog(instance)

    @override
    def __set__(self, instance, value, do_validate: bool=True):
        if value is ...:
            return
        if getattr(instance, self.private_name) is not None:
            raise KeyError('Trying to assign to a list that is already defined!')
        if value:
            self._rawdog(instance).extend(value)
class MRIDListAccessor(ListAccessor):
    def __init__(self,
                 default=None,
                 backed_name=None):
        super().__init__(default, backed_name)
        self.router_class = MRIDListRouter


class MRIDDictAccessor(ListAccessor):
    def __init__(self,
                 default=None,
                 backed_name=None):
        super().__init__(default, backed_name)
        self.router_class = MRIDDictRouter



class _Router(Generic[T]):

    def __init__(self,
                 owner: object,
                 accessor: _ListAccessorBase,
                 attr: str,
                 name: str):
        self._owner: object = owner
        self._la: _ListAccessorBase = accessor
        self._attr: str = attr
        self._name: str = name
        self.__name__ = name

        self.fget = Fget(descriptor=accessor, name=name)

        # Type checker fix - public methods only
        if True: return
        self.append: Callable[[T], None] = self.append
        self.clear: Callable[None, None] = self.clear
        self.remove: Callable[[T], None] = self.remove

    def _get(self) -> List | None:
        return getattr(self._owner, self._attr)

    def _get_safe(self) -> List:
        return getattr(self._owner, self._attr) or []

    @property
    def raw(self):
        return self._get_safe()


    def _set(self, val):
        setattr(self._owner, self._attr, val)

    def __iter__(self) -> Iterator[T]:
        return iter(self._get_safe())

    def __next__(self) -> T:
        return next(iter(self._get_safe()))

    def __repr__(self):
        l = self._get_safe()
        return l.__repr__()

    def extend(self, iterable: Iterable):
        for e in iterable:
            self.append(e)
        if len(self) == 0:
            self._set(None)


    def append_unchecked(self, item):
        raise NotImplementedError()

    # +-----+ BOILERPLATE DEFAULTS +-----+

    def append(self, item):
        l: List = self._get()
        if l is None:
            self._set([item])
        else:
            l.append(item)

    def clear(self):
        self._set(None)

    def remove(self, item):
        l: List = self._get()
        if not l:
            raise ValueError()
        l.remove(item)
        if not l:
            self._set(None)

    # +-----+ BOILERPLATE CALLERS +-----+
    # Note: The re-assignment speeds the methods up by 10x for subsequent calls;
    #       It is not done in __init__ to avoid defining ones we don't use.

    _custom_append: ClassVar[Callable] = None
    _custom_clear: ClassVar[Callable] = None
    _custom_remove: ClassVar[Callable] = None

    def _append_forwarding(self, item: T):
        self.append = getattr(self._owner, self._custom_append.__name__)
        self.append(item)

    def _clear_forwarding(self):
        self.clear = getattr(self._owner, self._custom_clear.__name__)
        self.clear()

    def _remove_forwarding(self, item: T):
        self.remove = getattr(self._owner, self._custom_remove.__name__)
        self.remove(item)

    def __len__(self):
        return len(self._get_safe())

    def __hash__(self):
        return 0

    def __getitem__(self, item) -> T:
        return self._get_safe()[item]


class ListRouter(_Router[T]):

    @override
    def _get(self) -> Optional[List]:
        return getattr(self._owner, self._attr)

    @override
    def _get_safe(self) -> List:
        if self._owner is None:
            return []
        return getattr(self._owner, self._attr) or []

    def sort(self, *,
             key: Callable=None,
             reverse: bool=False):
        self._get_safe().sort(key=key, reverse=reverse)

    def of_type(self, t: Type[S]) -> Generator[S, None, None]:
        yield (item for item in self._get_safe() if isinstance(item, t))

    def num_of_type(self, t: Type) -> int:
        return sum(1 for item in self._get_safe() if isinstance(item, t))

    def set_raw(self, val):
        self._set(list(val))

    def append_unchecked(self, item):
        l: List = self._get()
        if l is None:
            self._set([item])
        else:
            l.append(item)

    def insert_raw(self, index, item):
        l = self._get()
        if l is None :
            if index == 0:
                self._set([item])
                return
            else:
                l = []
        l.insert(index, item)

    def pop(self, index):
        return self._get_safe().pop(index)

    def fget(self, it) -> List:
        import warnings
        warnings.warn("Lists are no longer properties! Do not use fget()")
        return getattr(it, self._attr) or []


def _error_duplicate(obj, item):
    raise ValueError(f"A {item.__class__.__name__} " +
                     f"with mRID {item.mrid} already exists " +
                     f"in {obj}.")
# E       ValueError: AssetOrganisationRole with mRID 1 already exists in this Asset.
# An? (current )?{other1.__class__.__name__} with mRID {other1.mrid} already exists in {re.escape(str(it))}

class MRIDListRouter(ListRouter[T]):

    # +-----+ BOILERPLATE DEFAULTS +-----+

    @override
    def append(self, item):
        l: List = self._get()
        if not l:
            self._set([item])
            return

        other = next((io for io in l if io.mrid == item.mrid), None)
        if other is None:
            l.append(item)
        elif other is not item:
            _error_duplicate(self._owner, item)

    def get_by_mrid(self, mrid):
        l = self._get_safe()
        try:
            return next(io for io in l if io.mrid == mrid)
        except StopIteration:
            raise KeyError(mrid)

    @override
    def __getitem__(self, identifier):
        if isinstance(identifier, str):
            return self.get_by_mrid(identifier)
        elif isinstance(identifier, int):
            return self._get_safe()[identifier]
        raise TypeError(f'Attempting to access MRID list with identifier ' +
                        f'of type {type(identifier)}.')



class MRIDDictRouter(_Router[T]):

    @override
    def _get(self) -> Optional[Dict]:
        return getattr(self._owner, self._attr)

    @override
    def _get_safe(self) -> Dict:
        if self._owner is None:
            return {}
        return getattr(self._owner, self._attr) or {}

    @override
    def __iter__(self) -> Iterator[T]:
        return iter(self._get_safe().values())

    @override
    def append_unchecked(self, item):
        d: Dict = self._get()
        if d is None:
            self._set({item.mrid: item})
        else:
            d[item.mrid] = item

    # +-----+ BOILERPLATE DEFAULTS +-----+

    # +-----+ BOILERPLATE DEFAULTS +-----+
    @override
    def append(self, item):
        l: Dict = self._get()
        mrid = item.mrid
        if not l:
            self._set({mrid: item})
            return

        other = l.get(mrid, None)
        if other is None:
            l[mrid] = item
        elif other is not item:
            _error_duplicate(self._owner, item)

    @override
    def __getitem__(self, identifier):
        if isinstance(identifier, int):
            val = next((v for i, v in enumerate(self._get_safe().values()) if i == identifier), None)
            if val is None:
                raise IndexError("List index out of range")
            return val
        l: Dict = self._get_safe()
        return l[identifier]

    @override
    def remove(self, item):
        l: Dict = self._get()
        if not l:
            raise ValueError()
        del l[item.mrid]
        if not l:
            self._set(None)

    def get_by_mrid(self, mrid):
        l: Dict = self._get_safe()
        return l[mrid]

    # +-----+ BOILERPLATE CALLERS +-----+

    def fget(self, it) -> List:
        import warnings
        warnings.warn("Lists are no longer properties! Do not use fget()")
        return list((getattr(it, self._attr) or {}).values())


def override_boilerplate(l: ListAccessor, action: _Actions):
    def inner(f):
        l.attach_router_member(f, action)
        return f
    return inner


def custom_add(l: Iterable):
    return override_boilerplate(l, _Actions.ADD)
def custom_clear(l: Iterable):
    return override_boilerplate(l, _Actions.CLEAR)
def custom_remove(l: Iterable):
    return override_boilerplate(l, _Actions.REMOVE)

custom_get = None
custom_get_by_mrid = None
custom_len = None