from collections.abc import Callable
from enum import Enum
from typing import List, Iterable

from typing_extensions import override

from autoslot import BackedDescriptor
from autoslot import dataslot


class _Actions(Enum):
    ADD = 'add'
    GET = 'get'
    GET_BY_MRID = 'get_by_mrid'
    REMOVE = 'remove'
    CLEAR = 'clear'
    COUNT = 'num'

_singular_actions = {
    _Actions.ADD,
    _Actions.GET,
    _Actions.GET_BY_MRID,
    _Actions.REMOVE,
}

def boilermaker(cls):
    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        if isinstance(val, ListDescriptor):
            _attr = val.private_name
            inject(cls, val, attr, _attr)

    return cls

def _to_singular(name: str):
    if name.endswith('s'):
        return name[:-1]
    return name

def _get_method_name(attr: str, action: _Actions):
    if action in _singular_actions:
        attr = _to_singular(attr)
    return f'{action.value}_{attr}'

class _BoilerplateInjector:



    def __init__(self, public, private):
        self.public = public
        self.private = private

    _base_class_error = BaseException("Base class methods should not be called! " +
                                     "Use a subclass.")

    def _make_add(self): raise _BoilerplateInjector._base_class_error

    def _make_clear(self): raise _BoilerplateInjector._base_class_error

    def _make_get(self): raise _BoilerplateInjector._base_class_error

    def _make_remove(self): raise _BoilerplateInjector._base_class_error

    def _inject_method(self, cls, action: _Actions, method: Callable):
        name = _get_method_name(self.public, action)
        try:
            getattr(cls, name)
        except AttributeError:
            setattr(cls, name, method)

    def inject_into(self, cls):
        self._inject_method(cls, _Actions.ADD, self._make_add())
        self._inject_method(cls, _Actions.CLEAR, self._make_clear())
        self._inject_method(cls, _Actions.GET, self._make_get())
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

    @override
    def _make_get(self):
        def get(obj, identifier):
            l: List = getattr(obj, self.private) or []
            return l[identifier]
        return get

class MRIDListInjector(ListInjector):
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
            raise KeyError(f'Attempting to access MRID list with identifier ' +
                           f'of type {type(identifier)}.')
        return get

    @override
    def _make_add(self):
        return super()._make_add()
        # def add(obj, item):
        #     ... # TODO: Check mrid
        # return add

    def inject_into(self, cls):
        self._inject_method(cls, _Actions.GET_BY_MRID, self._make_get_by_mrid())


def inject(cls, val, public, private):
    if isinstance(val, MRIDListDescriptor):
        injector = MRIDListInjector(public, private)
    else:
        injector = ListInjector(public, private)
    injector.inject_into(cls)

class Router(Iterable):

    __slots__ = ('_owner', '_attr', '_name')

    def __init__(self, owner: object, attr: str, name: str):
        print('..', attr)
        self._owner = owner
        self._attr = attr
        self._name = name


    def _get(self):
        return getattr(self._owner, self._attr)

    def _get_or_empty(self):
        return getattr(self._owner, self._attr) or []

    def __iter__(self):
        l = self._get_or_empty()
        return iter(l) #TODO: Clean up this hack

    def __repr__(self):
        l = self._get_or_empty()
        return l.__repr__()


    def append(self, item):
        method = _get_method_name(self._name, _Actions.ADD)
        return getattr(self._owner, method)(item)

    def extend(self, iterable: Iterable):
        for e in iterable:
            self.append(e)

    def clear(self):
        method = _get_method_name(self._name, _Actions.CLEAR)
        return getattr(self._owner, method)()

    def remove(self, item):
        method = _get_method_name(self._name, _Actions.REMOVE)
        return getattr(self._owner, method)(item)


    def __getitem__(self, identifier):
        method = _get_method_name(self._name, _Actions.GET)
        return getattr(self._owner, method)(identifier)


class ListDescriptor(BackedDescriptor):
    @override
    def __get__(self, instance, *_):
        return Router(instance, self.private_name, self.public_name)

    @override
    def __set__(self, instance, value, do_validate: bool=True):
        if getattr(instance, self.private_name) is not None:
            raise KeyError('Trying to assign to a list that is already defined!')
        Router(instance, self.private_name, self.public_name).extend(value)

class MRIDListDescriptor(ListDescriptor):
    ...

if __name__ == '__main__':
    @boilermaker
    @dataslot
    class A:
        x: int = 42
        items: List[int] = ListDescriptor()

        # def clear_items(self):
        #     print('SIKE')
        #     self._items = self._items[::-1]

    a = A(items=[2, 3])
    a.add_item(42)
    print(a)
    print(a.items)
    a.clear_items()
    print(a.items)


    a.items.append(42)
    a.items.clear()
    a.items = [24, 25]


    r = Router(a, '_items', 'items')
    def print_router(rtr):
        print('-')
        for i, e in enumerate(r):
            print(f'[{i}] {e} ({r[i]})')

    print(r)
    print_router(r)
    r.append(42)
    print_router(r)
    r.clear()
    print_router(r)

    r.append(6)
    r.remove(6)
    print_router(r)