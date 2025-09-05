#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import inspect
import sys
from _weakref import ref
from abc import ABCMeta
from dataclasses import dataclass
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


class _WeakRefLink:
    __slots__ = '__weakref__', '_obj'

    def __init__(self, obj: object):
        self._obj = obj

    def unwrap(self):
        return self._obj


class WeakrefDescriptor(BackedDescriptor):

    def __init__(self, default=None):
        super().__init__(default=default)

    def __get__(self, obj, *_):
        value = getattr(obj, self.private_name)
        if value is self:
            self._set_default(obj)
            value = self.default
        if value is not None:
            if value() is None:
                return None
            value = value().unwrap()
        return value

    def __set__(self, obj, value, do_validate: bool=True):
        if value:
            wrapper = _WeakRefLink(value)
            value = ref(wrapper)
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


def _get_descriptors(cls: type):
    """
    Find class variables of cls that inherit BackedDescriptor.
    """
    dict_ = cls.__dict__
    return [dict_[attr] for attr in dict_
            if isinstance(dict_[attr], BackedDescriptor)]


def _get_descriptors_inherited(cls: type):
    """
    Find all class variables of cls and its superclasses
    that are descriptors.
    """
    descriptors = _get_descriptors(cls)
    for base in cls.__bases__:
        descriptors += _get_descriptors(base)
    return set(descriptors)


def amend_init(obj: type, cls: type):
    """
    Intercept dataclass init and initialise descriptors separately.
    Call the original init to allow the dataclass to handle fields.
    """
    init_signature = inspect.signature(obj.__init__)
    dc_kwargs = {}
    descriptor_values = {}

    # Make dictionaries for easy access
    descriptors = _get_descriptors_inherited(cls)
    public_names = {d.public_name: d for d in descriptors}
    private_names = {d.private_name: d for d in descriptors}
    del descriptors  # Free memory

    def add_kv(attr, val):
        if attr in private_names:
            desc = private_names[attr]
            name = desc.public_name
            descriptor_values[name] = val
        elif attr in public_names:
            descriptor_values[attr] = val
        else:
            dc_kwargs[attr] = val

    def __init__(self, *args, **kwargs):
        it = iter(init_signature.parameters)
        it.__next__()
        for val in args:
            attr = it.__next__()
            add_kv(attr, val)
        for attr, val in kwargs.items():
            add_kv(attr, val)

        print('= ', dc_kwargs, descriptor_values)

        self.__dataclass_init__(**dc_kwargs)
        for k, v in descriptor_values.items():
            setattr(self, k, v)

    obj.__dataclass_init__ = obj.__init__
    obj.__init__ = __init__


def _validate_backed_name(cls: type, attr, _attr):
    """
    Check that the name about to be used to back a descriptor
    is not already in use.
    """
    if _attr in cls.__annotations__:
        raise AttributeError(f'Cannot create a descriptor {attr} ' +
                             f'backed by field {_attr} ' +
                             f'because the field already exists in class {cls.__name__}')
    for base in cls.__bases__:
        if not hasattr(base, '__annotations__'):
            continue
        if _attr in base.__annotations__:
            raise AttributeError(f'Cannot create a descriptor {attr} ' +
                                 f'backed by field {_attr} ' +
                                 f'because the field already exists in superclass {base.__name__}')


def _autoslot(cls, slots=True, **kwargs):
    """
    Wrangle object creation to enable descriptor use
    in dataclasses with slots.

    This creates annotations and defaults for the internal variables,
    and re-types descriptors as ClassVar to force the dataclass
    creator to skip them.
    """
    print(cls, slots, kwargs)
    new_annotations = cls.__annotations__.copy()
    if DEBUG_LOG: _spew(cls)

    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        del new_annotations[attr]
        if isinstance(val, BackedDescriptor):
            _attr = val.private_name
            _validate_backed_name(cls, attr, _attr)

            new_annotations[attr] = ClassVar[_type]
            new_annotations[_attr] = _type
            setattr(cls, _attr, val.default)
            val.set_type(_type)
        else:
            new_annotations[attr] = _type

    cls.__annotations__ = new_annotations

    if DEBUG_LOG: _spew(cls)

    obj = dataclass(slots=slots, **kwargs)(cls)
    amend_init(obj, cls)
    return obj


@dataclass_transform(
    kw_only_default=False,
    eq_default=True,
    order_default=False,
)
def autoslot_dataclass(cls_outer=None, *, slots=True, **kwargs):
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
        t: int = TypeRestrictedDescriptor(backed_name='z')


    t = T([])
    t.t = 24
    print(t.x)

    l = [42, 24, 4]
    a = B([1], 'abc', 24)

    b = B([2], 'de', 25)
    print('!!!', a.y, a.x, b.y, b.x)



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
