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
from dataclasses import field, dataclass
from enum import Enum
from functools import partial, cache
from typing import List, Iterable, Optional, TypeVar, Generator, Type, Dict, Sized, Collection

from typing_extensions import override

from autoslot import BackedDescriptor

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



@dataclass
class NamingOptions:
    attr_alias: str | None = None
    singular: bool = False
    method_aliases: dict[_Actions, str] = field(default_factory=dict)

def _hash_on_mrid(cls):
    # TODO
    def __hash__(self):
        return self.mrid.__hash__()

    # if not hasattr(cls, '__hash__'):
    if hasattr(cls, 'mrid'):
        cls.__hash__ = __hash__
            # setattr(cls, '__hash__', mrid_hash)


def boilermaker(cls):
    for name, member in cls.__dict__.items():
        if hasattr(member, '__list_action__'):
            action = member.__list_action__
            target = member.__target_list__
            target.methods[action] = member

    # for attr, _type in cls.__annotations__.items():
    #     val = cls.__dict__.get(attr, None)
    #     if val is None: continue
    #     if isinstance(val, ListAccessor):
    #         _attr = val.private_name
    #         inject(cls, val, attr, _attr, val.options)

    # _hash_on_mrid(cls)

    return cls

# def _to_singular(name: str):
#     if name.endswith('s'):
#         return name[:-1]
#     return name
#
# def _get_method_name(attr: str, action: _Actions, options: NamingOptions=None):
#
#     options = options if options else NamingOptions()
#
#     if options.attr_alias is not None:
#         attr = options.attr_alias
#
#     name = options.method_aliases.get(action)
#     if name:
#         return name
#     if action not in _plurals or options.singular:
#         attr = _to_singular(attr)
#     return action.value(attr)
#
#


# class _BoilerplateInjector:
#
#     def __init__(self, accessor, public, private, options):
#         self.accessor = accessor
#         self.public = public
#         self.private = private
#         self.options = options
#
#     _base_class_error = BaseException("Base class methods should not be called! " +
#                                       "Use a subclass.")
#
#     def _make_add(self): raise _BoilerplateInjector._base_class_error
#
#     def _make_clear(self): raise _BoilerplateInjector._base_class_error
#
#     def _make_get(self): raise _BoilerplateInjector._base_class_error
#
#     def _make_num(self): raise _BoilerplateInjector._base_class_error
#
#     def _make_remove(self): raise _BoilerplateInjector._base_class_error
#
#     def _inject_method(self, cls, action: _Actions, method: Callable):
#         name = _get_method_name(self.public, action, self.options)
#
#         # If user has defined a custom method, skip injection
#         user_method = self.accessor.methods.get(action, None)
#         if user_method is not None:
#             return
#
#         # If there exists a non-deprecated method, raise a name conflict
#         existing_method = getattr(cls, name, None)
#         if existing_method is not None:
#             if not hasattr(existing_method, '__deprecated__'):
#                 raise AttributeError(f"Class {cls.__name__} has a custom method " +
#                                      f"{name} that is not marked as boilerplate override, " +
#                                      f'causing a name conflict. Rename the method or mark it as ' +
#                                      f'@override_boilerplate({self.public}, {action}).')
#
#         # Assign method to the class; Inform the accessor.
#         setattr(cls, name, method)
#         method.__name__ = name
#         self.accessor.methods[action] = method
#
#     def inject_into(self, cls):
#         self._inject_method(cls, _Actions.ADD,    self._make_add())
#         self._inject_method(cls, _Actions.CLEAR,  self._make_clear())
#         self._inject_method(cls, _Actions.GET,    self._make_get())
#         self._inject_method(cls, _Actions.LEN,    self._make_num())
#         self._inject_method(cls, _Actions.REMOVE, self._make_remove())
#
#
# class ListInjector(_BoilerplateInjector):
#
#     @override
#     def _make_add(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def add(obj, item):
#             l: List = getattr(obj, self.private)
#             if l is None:
#                 setattr(obj, self.private, [item])
#             else:
#                 l.append(item)
#             return obj
#         # +-----+ END +-----+
#         return add
#
#     @override
#     def _make_clear(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def clear(obj):
#             setattr(obj, self.private, None)
#             return obj
#         # +-----+ END +-----+
#         return clear
#
#     @override
#     def _make_get(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def get(obj, identifier):
#             l: List = getattr(obj, self.private) or []
#             return l[identifier]
#         # +-----+ END +-----+
#         return get
#
#
#     @override
#     def _make_num(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def num(obj):
#             l: Sized = getattr(obj, self.private) or []
#             return len(l)
#         # +-----+ END +-----+
#         return num
#
#     @override
#     def _make_remove(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def remove(obj, item):
#             l: List = getattr(obj, self.private)
#             if not l:
#                 raise ValueError()
#             l.remove(item)
#             if not l:
#                 setattr(obj, self.private, None)
#             return obj
#         # +-----+ END +-----+
#         return remove
#
#
# class MRIDListInjector(ListInjector):
#
#     @staticmethod
#     def error_duplicate(obj, item):
#         raise ValueError(f"{item.__class__.__name__} " +
#                          f"with mRID {item.mrid} already exists " +
#                          f"in this {obj.__class__.__name__}.")
#
#     @override
#     def _make_add(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def add(obj, item):
#             l: List = getattr(obj, self.private)
#             if not l:
#                 setattr(obj, self.private, [item])
#                 return obj
#
#             other = next((io for io in l if io.mrid == item.mrid), None)
#             if other is None:
#                 l.append(item)
#             elif other is not item:
#                 MRIDListInjector.error_duplicate(obj, item)
#             return obj
#         # +-----+ END +-----+
#         return add
#
#     def _make_get_by_mrid(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def get_by_mrid(obj, mrid):
#             l = getattr(obj, self.private)
#             if not l:
#                 raise KeyError(mrid)
#             try:
#                 return next(io for io in l if io.mrid == mrid)
#             except StopIteration:
#                 raise KeyError(mrid)
#         # +-----+ END +-----+
#         return get_by_mrid
#
#     @override
#     def _make_get(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def get(obj, identifier):
#             if isinstance(identifier, str):
#                 return obj.get_by_mrid(obj, identifier)
#             elif isinstance(identifier, int):
#                 l: List = getattr(obj, self.private) or []
#                 return l[identifier]
#             raise TypeError(f'Attempting to access MRID list with identifier ' +
#                            f'of type {type(identifier)}.')
#         # +-----+ END +-----+
#         return get
#
#     @override
#     def inject_into(self, cls):
#         super().inject_into(cls)
#         self._inject_method(cls, _Actions.GET_BY_MRID, self._make_get_by_mrid())
#
# class MRIDDictInjector(MRIDListInjector):
#
#     @override
#     def _make_add(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def add(obj, item):
#             mrid = item.mrid
#             d: Dict = getattr(obj, self.private)
#             if not d:
#                 setattr(obj, self.private, {mrid: item})
#                 return obj
#
#             other = d.get(mrid, None)
#             if other is None:
#                 d[mrid] = item
#             elif other is not item:
#                 MRIDListInjector.error_duplicate(obj, item)
#             return obj
#         # +-----+ END +-----+
#         return add
#
#     @override
#     def _make_get(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def get(obj, identifier):
#             l: Dict = getattr(obj, self.private) or {}
#             return l[identifier]
#         # +-----+ END +-----+
#         return get
#
#     @override
#     def _make_get_by_mrid(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def get_by_mrid(obj, mrid):
#             d: Dict = getattr(obj, self.private)
#             if not d:
#                 raise KeyError(mrid)
#             return d[mrid]
#         # +-----+ END +-----+
#         return get_by_mrid
#
#     @override
#     def _make_remove(self):
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         def remove(obj, item):
#             d: Dict = getattr(obj, self.private)
#             if not d:
#                 raise KeyError() # Different to MRIDList
#             del d[item.mrid]
#             if not d:
#                 setattr(obj, self.private, None)
#             return obj
#         # +-----+ BOILERPLATE TEMPLATE +-----+
#         return remove
#
#
# def inject(cls, val, public, private, options=None):
#     if isinstance(val, MRIDListAccessor):
#         injector_class = MRIDListInjector
#     elif isinstance(val, MRIDDictAccessor):
#         injector_class = MRIDDictInjector
#     else:
#         injector_class = ListInjector
#     injector = injector_class(val, public, private, options)
#     injector.inject_into(cls)

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
                 backed_name=None,
                 naming_options=None):
        super().__init__(default, backed_name)
        self.options = naming_options
        # self.methods = {}
        self.router_class = ListRouter

    def _rawdog(self, instance):
        return self.router_class(instance, self, self.private_name, self.public_name, self.options)

    @cache
    def _get_cached(self, instance):
        return self._rawdog(instance)

    def get_method(self, action: _Actions):
        return self.methods[action]

    @override
    def __get__(self, instance, default=None):
        try:
            return self._get_cached(instance)
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
                 backed_name=None,
                 naming_options=None):
        super().__init__(default, backed_name, naming_options)
        self.router_class = MRIDListRouter

class MRIDDictAccessor(ListAccessor):
    def __init__(self,
                 default=None,
                 backed_name=None,
                 naming_options=None):
        super().__init__(default, backed_name, naming_options)
        self.router_class = MRIDDictRouter




class _Router(Iterable):

    def __init__(self,
                 owner: object,
                 accessor: _ListAccessorBase,
                 attr: str,
                 name: str,
                 options: NamingOptions = None):
        self._owner: object = owner
        self._la: _ListAccessorBase = accessor
        self._attr: str = attr
        self._name: str = name

        self._options = options if options else NamingOptions()

        # Type checker fix - public methods only
        if True: return
        self.append = self.append
        self.clear = self.clear
        self.remove = self.remove

    def _method(self, action: _Actions):
        if action in self._la.methods:
            name = self._la.methods[action].__name__
            return getattr(self._owner, name)
        name = _action_methods[action]
        return getattr(self, name)

        # method = _get_method_name(self._name, action, self._options)
        # return getattr(self._owner, method)

    def _get(self) -> Optional[Collection]:
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
        return self._owner

    def _default_clear(self):
        self._set(None)
        return self._owner

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
        return self._owner

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

    def append_unchecked(self, item):
        l: List = self._get()
        if l is None:
            self._set([item])
        else:
            l.append(item)

def _error_duplicate(obj, item):
    raise ValueError(f"{item.__class__.__name__} " +
                     f"with mRID {item.mrid} already exists " +
                     f"in this {obj.__class__.__name__}.")

class MRIDListRouter(ListRouter):

    def __init__(self,
                 owner: object,
                 accessor: ListAccessor,
                 attr: str,
                 name: str,
                 options: NamingOptions = None):
        super().__init__(owner, accessor, attr, name, options)


        # Type checker fix - public methods only
        self.get_by_mrid = self.get_by_mrid

    # +-----+ BOILERPLATE DEFAULTS +-----+

    @override
    def _default_add(self, item):
        l: List = self._get()
        if not l:
            self._set([item])
            return self._owner

        other = next((io for io in l if io.mrid == item.mrid), None)
        if other is None:
            l.append(item)
        elif other is not item:
            _error_duplicate(self._owner, item)
        return self._owner

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

    action_methods = super

    def __init__(self,
                 owner: object,
                 accessor: ListAccessor,
                 attr: str,
                 name: str,
                 options: NamingOptions = None):
        super().__init__(owner, accessor, attr, name, options)

        # Type checker fix - public methods only
        self.get_by_mrid = self.get_by_mrid

    @override
    def _get(self) -> Optional[Dict]:
        return getattr(self._owner, self._attr)

    @override
    def _get_safe(self) -> Dict:
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
            return self._owner

        other = l.get(mrid, None)
        if other is None:
            l[mrid] = item
        elif other is not item:
            _error_duplicate(self._owner, item)
        return self._owner

    @override
    def _default_clear(self):
        self._set(None)
        return self._owner

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
        return self._owner

    def _default_get_by_mrid(self, mrid):
        l: Dict = self._get_safe()
        return l[mrid]

    # +-----+ BOILERPLATE CALLERS +-----+

    def get_by_mrid(self, mrid):
        self.get_by_mrid = self._method(_Actions.GET_BY_MRID)
        return self.get_by_mrid(mrid)



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
