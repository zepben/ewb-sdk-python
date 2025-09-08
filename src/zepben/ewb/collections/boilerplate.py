from collections.abc import Callable
from enum import Enum
from typing import List, Iterable

from typing_extensions import override

from autoslot import BackedDescriptor
from autoslot import dataslot


class _Actions(Enum):
    ADD = 'add'
    GET = 'get'
    REMOVE = 'remove'
    CLEAR = 'clear'
    COUNT = 'num'

_singular_actions = {
    _Actions.ADD,
    _Actions.GET,
    _Actions.REMOVE,
}

def boilermaker(cls):
    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        if isinstance(val, ListDescriptor):
            _attr = val.private_name
            inject(cls, attr, _attr)

    return cls

def _to_singular(name: str):
    if name.endswith('s'):
        return name[:-1]
    return name

def _get_method_name(attr: str, action: _Actions):
    if action in _singular_actions:
        attr = _to_singular(attr)
    return f'{action.value}_{attr}'

class BoilerplateInjector:
    def __init__(self, public, private):
        self.public = public
        self.private = private

    def make_add(self):
        def add(obj, item):
            l = getattr(obj, self.private)
            if l is None:
                setattr(obj, self.private, [item])
            else:
                l.append(item)
        return add

    def make_clear(self):
        def clear(obj):
            setattr(obj, self.private, None)
        return clear

    def inject_into(self, cls):
        self._inject_method(cls, _Actions.ADD, self.make_add())
        self._inject_method(cls, _Actions.CLEAR, self.make_clear())

    def _inject_method(self, cls, action: _Actions, method: Callable):
        name = _get_method_name(self.public, action)
        try:
            getattr(cls, name)
        except AttributeError:
            setattr(cls, name, method)

def inject(cls, public, private):
    injector = BoilerplateInjector(public, private)
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

    def __iter__(self):
        l = self._get()
        if l is None:
            return iter([]) #TODO: Clean up this hack
        return iter(l)

    def append(self, item):
        method = _get_method_name(self._name, _Actions.ADD)
        return getattr(self._owner, method)(item)

    def extend(self, iterable: Iterable):
        for e in iterable:
            self.append(e)

    def clear(self):
        method = _get_method_name(self._name, _Actions.CLEAR)
        return getattr(self._owner, method)()



class ListDescriptor(BackedDescriptor):
    @override
    def __get__(self, instance, *_):
        return Router(instance, self.private_name, self.public_name)

    @override
    def __set__(self, instance, value, do_validate: bool=True):
        Router(instance, self.private_name, self.public_name).extend(value)



if __name__ == '__main__':
    @boilermaker
    @dataslot
    class A:
        x: int = 42
        items: List[int] = ListDescriptor()

        def clear_items(self):
            print('SIKE')
            self._items = self._items[::-1]

    a = A(items=[2, 3])
    a.add_item(42)
    print(a)
    print(a.items)
    a.clear_items()
    print(a.items)


    a.items.append(42)
    a.items = [24, 25]

    r = Router(a, '_items', 'items')
    print(r)
    for x in r:
        print(x)
    r.append(42)
    print('-')
    for x in r:
        print(x)
    r.clear()
    print('-')
    for x in r:
        print(x)