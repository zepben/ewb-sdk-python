#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
from _weakref import ref
from abc import ABCMeta
from dataclasses import dataclass, InitVar
from typing import ClassVar, List

from typing_extensions import dataclass_transform


class BackedDescriptor(metaclass=ABCMeta):

    def __init__(self, default=None, backed_name=None):
        self.default = default
        self.private_name = backed_name
        self.typed = None


    def __set_name__(self, owner, name):
        self.public_name = name
        if self.private_name is None:
            self.private_name = '_' + name

    def __get__(self, obj, *_):
        value = getattr(obj, self.private_name)
        if value is self:
            self._set_default(obj)
            return self.default
        return value

    def __set__(self, obj, value, do_validate: bool=True):
        setattr(obj, self.private_name, value)

    def _set_default(self, obj):
        self.__set__(obj, self.default, do_validate=False)

    def set_type(self, typed: type):
        self.typed = typed



class ValidatedDescriptor(BackedDescriptor):

    def __init__(self, default = None, validate = None, backed_name=None):
        super().__init__(default=default, backed_name=backed_name)
        self.validate = validate

    def __set__(self, obj, value, do_validate: bool=True):
        if value is not self and do_validate:
            if self.validate:
                value = self.validate(obj, value)
        setattr(obj, self.private_name, value)



class NoResetDescriptor(ValidatedDescriptor):

    def __init__(self, default=None, backed_name=None):
        super().__init__(default=default, backed_name=backed_name)
        self.validate = self.__one_set_validate

    def __one_set_validate(self, obj, value):
        old = getattr(obj, self.private_name)
        if old is None or old is value:
            return value
        raise ValueError(f'{self.private_name} for {obj.__class__.__name__}' +
                         f' has already been set to {old},' +
                         f' cannot reset this field to {value}')



class WeakrefDescriptor(BackedDescriptor):

    def __init__(self, default=None):
        super().__init__(default=default)

    def __get__(self, obj, *_):
        value = getattr(obj, self.private_name)
        if value is self:
            self._set_default(obj)
            value = self.default
        if value is not None:
            value = value()
        return value

    def __set__(self, obj, value, do_validate: bool=True):
        if value:
            value = ref(value)
        setattr(obj, self.private_name, value)



class TypeRestrictedDescriptor(BackedDescriptor):

    def __set__(self, obj, value, do_validate: bool=True):
        if value is not self and self.typed:
            if not isinstance(value, self.typed):
                raise TypeError(f'Trying to pass type {type(value)} ' +
                                f'to descriptor {self.public_name} ' +
                                f'which only accepts type {self.typed}')
        super().__set__(obj, value, do_validate)


DEBUG_LOG = True

def _spew(cls):
    print(cls.__name__, '::')
    # for k, v in cls.__dict__.items():
    #     print(f'\t{k}: {v}')

def generate_slots(annotations):
    slots = []
    for attr, _type in annotations.items():
        if _type is ClassVar or _type is InitVar or isinstance(_type, BackedDescriptor):
            continue
        slots.append(attr)
    return tuple(slots)


def _autoslot(cls, slots=True, **kwargs):
    print(cls, slots, kwargs)
    new_annotations = cls.__annotations__.copy()
    if DEBUG_LOG: _spew(cls)

    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        if isinstance(val, BackedDescriptor):
            _attr = f'_{attr}'
            new_annotations[attr] = ClassVar[_type]
            new_annotations[_attr] = _type
            setattr(cls, _attr, val.default)
            val.set_type(_type)

    cls.__annotations__ = new_annotations

    if DEBUG_LOG: _spew(cls)

    # cls.__slots__ = generate_slots(new_annotations)

    return dataclass(slots=False, **kwargs)(cls)



@dataclass_transform(
    kw_only_default=False,
    eq_default=True,
    order_default=False,
)
def autoslot_dataclass(cls_outer = None, *, slots=True, **kwargs):
    def dec(cls):
        return _autoslot(cls, slots=slots, **kwargs)

    if cls_outer:
        return dec(cls_outer)
    return dec






if __name__ == '__main__':

    @autoslot_dataclass
    class A:
        l: List[int]

        y: str = NoResetDescriptor()

        x: int = 42



    @dataclass
    class C:
        l1 : List[int] = None

    @autoslot_dataclass
    class B(A):
        l2: List[int] = None

        c: C = WeakrefDescriptor()


    @autoslot_dataclass
    class T(A):
        t: int = TypeRestrictedDescriptor(backed_name='x')


    t = T([])
    t.t = 24
    print(t.x)

    l = [42, 24, 4]
    a = B(l)

    print(A.__slots__)
    print(a.__slots__)
    print(a.__dict__)

    c = C()

    print(sys.getrefcount(a.c))

    a.c = c
    print('ref', a.c)

    print(sys.getrefcount(a.c))

    del c

    print(sys.getrefcount(a.c))


    print(a.l)


    print(a.y)


    a.y = 'cool'
    print(a)

    a.y = 'cool'
    print(1)

    a.l = []
    a.x = 24
    print(a)

    a.y = 'cool2'
    print(2)
    t.t = C()
