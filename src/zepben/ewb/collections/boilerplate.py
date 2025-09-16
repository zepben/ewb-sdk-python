from collections.abc import Callable
from dataclasses import field, dataclass
from enum import Enum
from functools import partial
from typing import List, Iterable, Optional

from typing_extensions import override

from autoslot import BackedDescriptor


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
    singular: bool = False
    aliases: dict[_Actions, str] = field(default_factory=dict)


def boilermaker(cls):
    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        if isinstance(val, ListAccessor):
            _attr = val.private_name
            inject(cls, val, attr, _attr, val.options)

    return cls

def _to_singular(name: str):
    if name.endswith('s'):
        return name[:-1]
    return name

def _get_method_name(attr: str, action: _Actions, options: NamingOptions=None):
    options = options if options else NamingOptions()
    name = options.aliases.get(action)
    if name:
        return name
    if action not in _plurals or options.singular:
        attr = _to_singular(attr)
    return action.value(attr)




class _BoilerplateInjector:

    def __init__(self, public, private, options):
        self.public = public
        self.private = private
        self.options = options

    _base_class_error = BaseException("Base class methods should not be called! " +
                                      "Use a subclass.")

    def _make_add(self): raise _BoilerplateInjector._base_class_error

    def _make_clear(self): raise _BoilerplateInjector._base_class_error

    def _make_get(self): raise _BoilerplateInjector._base_class_error

    def _make_num(self): raise _BoilerplateInjector._base_class_error

    def _make_remove(self): raise _BoilerplateInjector._base_class_error

    def _inject_method(self, cls, action: _Actions, method: Callable):
        name = _get_method_name(self.public, action, self.options)
        try:
            existing_method = getattr(cls, name)
            write_method = hasattr(existing_method, '__deprecated__')
        except AttributeError:
            write_method = True
        if write_method:
            setattr(cls, name, method)

    def inject_into(self, cls):
        self._inject_method(cls, _Actions.ADD,    self._make_add())
        self._inject_method(cls, _Actions.CLEAR,  self._make_clear())
        self._inject_method(cls, _Actions.GET,    self._make_get())
        self._inject_method(cls, _Actions.LEN,    self._make_num())
        self._inject_method(cls, _Actions.REMOVE, self._make_remove())




class ListInjector(_BoilerplateInjector):

    @override
    def _make_add(self):
        def add(obj, item):
            l: List = getattr(obj, self.private)
            if l is None:
                setattr(obj, self.private, [item])
            else:
                l.append(item)
            return obj
        return add

    @override
    def _make_clear(self):
        def clear(obj):
            setattr(obj, self.private, None)
            return obj
        return clear

    @override
    def _make_get(self):
        def get(obj, identifier):
            l: List = getattr(obj, self.private) or []
            return l[identifier]
        return get


    @override
    def _make_num(self):
        def num(obj):
            l: List = getattr(obj, self.private) or []
            return len(l)
        return num

    @override
    def _make_remove(self):
        def remove(obj, item):
            l: List = getattr(obj, self.private)
            if not l:
                raise ValueError()
            l.remove(item)
            l = l if l else None
            setattr(obj, self.private, l)
            return obj
        return remove


class MRIDListInjector(ListInjector):

    @override
    def _make_add(self):
        def add(obj, item):
            l: List = getattr(obj, self.private)
            if not l:
                setattr(obj, self.private, [item])
                return obj

            other = next((io for io in l if io.mrid == item.mrid), None)
            if other is None:
                l.append(item)
            elif other is not item:
                raise ValueError(f"{item.__class__.__name__} with mRID {item.mrid} already exists in this {obj.__class__.__name__}.")
            return obj


        return add

    def _make_get_by_mrid(self):
        def get_by_mrid(obj, mrid):
            l = getattr(obj, self.private)
            if not l:
                raise KeyError(mrid)
            try:
                return next(io for io in l if io.mrid == mrid)
            except StopIteration:
                raise KeyError(mrid)
        return get_by_mrid

    @override
    def _make_get(self):
        def get(obj, identifier):
            if isinstance(identifier, str):
                return obj.get_by_mrid(obj, identifier)
            elif isinstance(identifier, int):
                l: List = getattr(obj, self.private) or []
                return l[identifier]
            raise TypeError(f'Attempting to access MRID list with identifier ' +
                           f'of type {type(identifier)}.')
        return get

    @override
    def inject_into(self, cls):
        super().inject_into(cls)
        self._inject_method(cls, _Actions.GET_BY_MRID, self._make_get_by_mrid())


def inject(cls, val, public, private, options=None):
    if isinstance(val, MRIDListAccessor):
        injector = MRIDListInjector(public, private, options)
    else:
        injector = ListInjector(public, private, options)
    injector.inject_into(cls)

class Router(Iterable):

    # Apparently slots increase creation time
    # __slots__ = ('_owner', '_attr', '_name')

    def __init__(self, owner: object, attr: str, name: str, options: NamingOptions=None):
        self._owner = owner
        self._attr = attr
        self._name = name

        self._options = options if options else NamingOptions()

        # Type checker fix - public methods only
        self.append = self.append
        self.clear  = self.clear
        self.remove = self.remove

    def _method(self, action: _Actions):
        method = _get_method_name(self._name, action, self._options)
        return getattr(self._owner, method)

    def _get(self) -> Optional[List]:
        return getattr(self._owner, self._attr)

    def _get_safe(self) -> List:
        return getattr(self._owner, self._attr) or []

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

    # --------{] boilerplate callers [}--------
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

    def _getitem(self, item):
        self._getitem = self._method(_Actions.GET)
        return self._getitem(item)

    def __getitem__(self, item):
        return self._getitem(item)

    # TODO: Make this immutable only or add verification
    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            l = self._get_safe()
            try:
                return object.__getattribute__(l, item)
            except AttributeError:
                raise AttributeError(f"'{l.__class__.__name__}' " +
                                     f"has no attribute '{item}'")

class ListAccessor(BackedDescriptor):
    def __init__(self,
                 default=None,
                 backed_name=None,
                 naming_options=None):
        super().__init__(default, backed_name)
        self.options = naming_options

    @override
    def __get__(self, instance, *_):
        return Router(instance, self.private_name, self.public_name, self.options)

    @override
    def __set__(self, instance, value, do_validate: bool=True):
        if getattr(instance, self.private_name) is not None:
            raise KeyError('Trying to assign to a list that is already defined!')
        if value:
            Router(instance, self.private_name, self.public_name, self.options).extend(value)

class MRIDListAccessor(ListAccessor):
    ...
