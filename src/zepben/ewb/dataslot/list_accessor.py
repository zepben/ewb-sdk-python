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
from typing import List, Iterable, Optional, TypeVar, Generator, Type, Dict, Sized

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
    ADD         = partial(lambda item : f'add_{item}')
    CLEAR       = partial(lambda item : f'clear_{item}')
    GET         = partial(lambda item : f'get_{item}')
    GET_BY_MRID = partial(lambda item : f'get_{item}_by_mrid')
    LEN         = partial(lambda item : f'num_{item}')
    REMOVE      = partial(lambda item : f'remove_{item}')

ListActions = _Actions

_plurals = {
    _Actions.CLEAR,
    _Actions.LEN
}


def boilermaker(cls):
    for name, member in cls.__dict__.items():
        if hasattr(member, '__list_action__'):
            action = member.__list_action__
            target = member.__target_list__
            target.methods[action] = member
    for name, member in cls.__dict__.items():
        if isinstance(member, ListAccessor):
            member._attach_router()

    return cls

_action_methods = {
    _Actions.ADD: '_default_add',
    _Actions.CLEAR: '_default_clear',
    _Actions.GET: '_default_get',
    _Actions.LEN: '_default_num',
    _Actions.REMOVE: '_default_remove',
    _Actions.GET_BY_MRID: '_default_get_by_mrid'
}

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

    def _router_method_lookup(self, action: _Actions):
        if action in self.methods:
            return None
        name = _action_methods[action]
        return getattr(self.router_class, name)

    def _attach_router(self):
        router_subname = f"{self.owner.__name__}_{self.public_name}_Router"
        r = self.router_class = type(router_subname, (self.router_class, ), {})

        r.append = self._router_method_lookup(_Actions.ADD) or r.append
        r.clear = self._router_method_lookup(_Actions.CLEAR) or r.clear
        r.remove = self._router_method_lookup(_Actions.REMOVE) or r.remove
        r._len = self._router_method_lookup(_Actions.LEN) or r._len
        r._getitem = self._router_method_lookup(_Actions.GET) or r._getitem


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

    def _attach_router(self):
        super()._attach_router()
        r = self.router_class
        r.get_by_mrid = self._router_method_lookup(_Actions.GET_BY_MRID) or r.get_by_mrid


class MRIDDictAccessor(ListAccessor):
    def __init__(self,
                 default=None,
                 backed_name=None):
        super().__init__(default, backed_name)
        self.router_class = MRIDDictRouter

    def _attach_router(self):
        super()._attach_router()
        r = self.router_class
        r.get_by_mrid = self._router_method_lookup(_Actions.GET_BY_MRID) or r.get_by_mrid



class _Router(Iterable):

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
        self.append = self.append
        self.clear = self.clear
        self.remove = self.remove

    def _method(self, action: _Actions):
        # if action in self._la.methods:
        name = self._la.methods[action].__name__
        return getattr(self._owner, name)
        # name = _action_methods[action]
        # return getattr(self, name)


    def _get(self) -> List | None:
        return getattr(self._owner, self._attr)

    def _get_safe(self) -> List:
        return getattr(self._owner, self._attr) or []


    @property
    def raw(self):
        return self._get_safe()


    def _set(self, val):
        setattr(self._owner, self._attr, val)

    def __iter__(self):
        return iter(self._get_safe())

    def __next__(self):
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

    def _default_add(self, item):
        l: List = self._get()
        if l is None:
            self._set([item])
        else:
            l.append(item)

    def _default_clear(self):
        self._set(None)

    def _default_get(self, identifier):
        l: List = self._get_safe()
        return l[identifier]

    def _default_num(self):
        l: Sized = self._get_safe()
        return len(l)

    def _default_remove(self, item):
        l: List = self._get()
        if not l:
            raise ValueError()
        l.remove(item)
        if not l:
            self._set(None)

    # +-----+ BOILERPLATE CALLERS +-----+
    # Note: The re-assignment speeds the methods up by 10x for subsequent calls;
    #       It is not done in __init__ to avoid defining ones we don't use.
    #       Dunders are aliased because python bypasses instance-wise dunder reassignment.

    def append(self, item):
        self.append = self._method(_Actions.ADD)
        return self.append(item)

    def clear(self):
        self.clear = self._method(_Actions.CLEAR)
        return self.clear()

    def remove(self, item):
        self.remove = self._method(_Actions.REMOVE)
        return self.remove(item)

    def _len(self):
        self._len = self._method(_Actions.LEN)
        return self._len()

    def __len__(self):
        return self._len()

    def num(self):
        return self._len()

    def __hash__(self):
        return 0

    def _getitem(self, item):
        self._getitem = self._method(_Actions.GET)
        return self._getitem(item)

    def __getitem__(self, item):
        return self._getitem(item)

    def get(self, item):
        return self._getitem(item)


class ListRouter(_Router):

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

class MRIDListRouter(ListRouter):

    def __init__(self,
                 owner: object,
                 accessor: ListAccessor,
                 attr: str,
                 name: str):
        super().__init__(owner, accessor, attr, name)


        # Type checker fix - public methods only
        self.get_by_mrid = self.get_by_mrid

    # +-----+ BOILERPLATE DEFAULTS +-----+

    @override
    def _default_add(self, item):
        l: List = self._get()
        if not l:
            self._set([item])
            return

        other = next((io for io in l if io.mrid == item.mrid), None)
        if other is None:
            l.append(item)
        elif other is not item:
            _error_duplicate(self._owner, item)

    def _default_get_by_mrid(self, mrid):
        l = self._get_safe()
        try:
            return next(io for io in l if io.mrid == mrid)
        except StopIteration:
            raise KeyError(mrid)

    @override
    def _default_get(self, identifier):
        if isinstance(identifier, str):
            return self.get_by_mrid(identifier)
        elif isinstance(identifier, int):
            return self._get_safe()[identifier]
        raise TypeError(f'Attempting to access MRID list with identifier ' +
                        f'of type {type(identifier)}.')

    # +-----+ BOILERPLATE CALLERS +-----+

    def get_by_mrid(self, mrid: str):
        self.get_by_mrid = self._method(_Actions.GET_BY_MRID)
        return self.get_by_mrid(mrid)



class MRIDDictRouter(_Router):

    def __init__(self,
                 owner: object,
                 accessor: ListAccessor,
                 attr: str,
                 name: str):
        super().__init__(owner, accessor, attr, name)

        # Type checker fix - public methods only
        self.get_by_mrid = self.get_by_mrid

    @override
    def _get(self) -> Optional[Dict]:
        return getattr(self._owner, self._attr)

    @override
    def _get_safe(self) -> Dict:
        if self._owner is None:
            return {}
        return getattr(self._owner, self._attr) or {}

    @override
    def __iter__(self):
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
    def _default_add(self, item):
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
    def _default_clear(self):
        self._set(None)

    @override
    def _default_get(self, identifier):
        l: Dict = self._get_safe()
        return l[identifier]

    @override
    def _default_remove(self, item):
        l: Dict = self._get()
        if not l:
            raise ValueError()
        del l[item.mrid]
        if not l:
            self._set(None)

    def _default_get_by_mrid(self, mrid):
        l: Dict = self._get_safe()
        return l[mrid]

    # +-----+ BOILERPLATE CALLERS +-----+

    def get_by_mrid(self, mrid):
        self.get_by_mrid = self._method(_Actions.GET_BY_MRID)
        return self.get_by_mrid(mrid)

    def fget(self, it) -> List:
        import warnings
        warnings.warn("Lists are no longer properties! Do not use fget()")
        return list((getattr(it, self._attr) or {}).values())


def override_boilerplate(l: Iterable, action: _Actions):
    def inner(f):
        f.__list_action__ = action
        f.__target_list__ = l
        return f
    return inner


def custom_add(l: Iterable):
    return override_boilerplate(l, _Actions.ADD)
def custom_clear(l: Iterable):
    return override_boilerplate(l, _Actions.CLEAR)
def custom_get(l: Iterable):
    return override_boilerplate(l, _Actions.GET)
def custom_get_by_mrid(l: Iterable):
    return override_boilerplate(l, _Actions.GET_BY_MRID)
def custom_len(l: Iterable):
    return override_boilerplate(l, _Actions.LEN)
def custom_remove(l: Iterable):
    return override_boilerplate(l, _Actions.REMOVE)

