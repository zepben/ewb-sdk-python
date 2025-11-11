#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import inspect
import sys
from _weakref import ref
from abc import ABCMeta
from dataclasses import dataclass, field, KW_ONLY
from enum import Enum
from os import eventfd_write
from typing import ClassVar, List, Callable, Any

from typing_extensions import dataclass_transform

__all__ = [
    'dataslot',
    'private',
    'instantiate',
    'validate',
    'BackingValue',
    'BackedDescriptor',
    'WeakrefDescriptor',
    'ValidatedDescriptor',
    'NoResetDescriptor',
    'TypeRestrictedDescriptor',
]

# from zepben.ewb import require


class SetOnceError(Exception):
    ...


class BackingValue:
    ...

class Fget:
    def __init__(self, descriptor, function=None, name=None):
        self.descriptor = descriptor
        if function:
            self._get = function
        if name:
            self.__name__ = name

    def _get(self, it):
        return getattr(it, self.__name__)
        # return self.descriptor.__get__(it)

    def __call__(self, it):
        return self._get(it)

class Descriptor(metaclass=ABCMeta):
    def __init__(self, default=None):
        self.default = default
        self.typed = None
        self.fget = Fget(self)

    def __set_name__(self, owner, name):
        self.owner = owner
        self.__name__ = self.public_name = name
        self.fget.__name__ = name

    def __get__(self, instance, *_):
        raise NotImplementedError()

    def __set__(self, instance, value, direct: bool=False):
        raise NotImplementedError()

    def _set_default(self, obj):
        self.__set__(obj, self.default, direct=True)

    def set_type(self, typed: type):
        self.typed = typed

    # def fget(self, it):
    #     return self.__get__(it)


Getter = Callable[[Any], Any]
Setter = Callable[[Any, Any], Any]

class _Addressor(Enum):
    Getter     = 0
    Setter     = 1
    Validator  = 2

class CustomDescriptor(Descriptor):
    def __init__(self,
                 default=None,
                 getter: Getter=None,
                 setter: Setter=None):
        super().__init__(default=default)
        self.getter: Getter = getter
        self.setter: Setter = setter


    def add_setter(self, setter: Callable=None):
        if self.setter is not None:
            raise SetOnceError(f"Attribute {self.public_name} already has a setter.")
        self.setter = setter

    def add_getter(self, getter: Callable=None):
        if self.getter is not None:
            raise SetOnceError(f"Attribute {self.public_name} already has a getter.")
        self.getter = getter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.getter is None:
            raise AttributeError(f"Descriptor {self.public_name} of " +
                                 f"{self.owner.__name__} is missing a getter!")
        return self.getter(instance)

    def __set__(self, obj, value, _: bool=False):
        if value is not self:
            if self.setter is None:
                raise AttributeError(f"Descriptor {self.public_name} of " +
                                     f"{self.owner.__name__} is missing a getter!")
            self.setter(obj, value)

class BackedDescriptor(Descriptor):

    def __init__(self, default=None, backed_name=None):
        super().__init__(default=default)
        self.default = default
        self.private_name = backed_name

    def __set_name__(self, owner, name):
        super().__set_name__(owner=owner, name=name)
        if self.private_name is None:
            self.private_name = '_' + name

    def __get__(self, obj, *_):
        if obj is None:
            return self
        value = getattr(obj, self.private_name)
        if value is self:
            self._set_default(obj)
            return self.default
        return value

    def __set__(self, obj, value, direct: bool=False):
        setattr(obj, self.private_name, value)



class ValidatedDescriptor(BackedDescriptor):

    def __init__(self, default = None, validate = None, backed_name=None):
        super().__init__(default=default, backed_name=backed_name)
        self.validate = validate

    def __set__(self, obj, value, direct: bool=False):
        if value is not self and not direct:
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
        if obj is None:
            return self
        value = getattr(obj, self.private_name)
        if value is self:
            self._set_default(obj)
            value = self.default
        if value is not None:
            return value()
        return value

    def __set__(self, obj, value, direct: bool=False):
        if value:
            value = ref(value)
        setattr(obj, self.private_name, value)


class TypeRestrictedDescriptor(BackedDescriptor):

    def __set__(self, obj, value, direct: bool=False):
        if value is not self and self.typed:
            if not isinstance(value, self.typed):
                raise TypeError(f'Trying to pass type {type(value)} ' +
                                f'to descriptor {self.public_name} ' +
                                f'which only accepts type {self.typed}')
        super().__set__(obj, value, direct)

class RangedDescriptor(ValidatedDescriptor):
    def __init__(self,
                 default = None,
                 min=0, max=0,
                 backed_name=None):
        error_msg = lambda val: (
            f"{self.public_name} [{val}] " +
            f"must be between {min} " +
            f"and {max}.")
        def check(_, val):
            if val is not None and not min <= val <= max:
                raise ValueError(error_msg(val))
            return val
        super().__init__(default=default, validate=check, backed_name=backed_name)

class Alias(BackedDescriptor):
    ...




def _addressor(var: object | ValidatedDescriptor, _type: _Addressor):
    def dec(f):
        f.__addressor_target__ = var
        f.__addressor_type__ = _type
        return f
    return dec

def validate(var: object | ValidatedDescriptor):
    return _addressor(var, _Addressor.Validator)
def getter(var: object | CustomDescriptor):
    return _addressor(var, _Addressor.Getter)
def setter(var: object | CustomDescriptor):
    return _addressor(var, _Addressor.Setter)


DEBUG_LOG = False
BAN_KWARGS = True


def _spew(cls):
    print(cls.__name__, '::')
    # for k, v in cls.__dict__.items():
    #     print(f'\t{k}: {v}')


def _get_descriptors(cls: type, _type: type):
    """
    Find class variables of cls that inherit BackedDescriptor.
    """
    dict_ = cls.__dict__
    return [dict_[attr] for attr in dict_
            if isinstance(dict_[attr], _type)]


def _get_descriptors_inherited(cls: type, _type: type):
    """
    Find all class variables of cls and its superclasses
    that are descriptors.
    """
    descriptors = _get_descriptors(cls, _type)
    for base in cls.__bases__:
        descriptors += _get_descriptors_inherited(base, _type)
    return set(descriptors)

def attr_or_placeholder(attr: str):
    if not attr.startswith('_init_placeholder_for_'):
        return attr
    return attr[len('_init_placeholder_for_'):-1]

def amend_init(obj: type, cls: type):
    """
    Intercept dataclass init and initialise descriptors separately.
    Call the original init to allow the dataclass to handle fields.
    """
    init_signature = inspect.signature(obj.__init__)

    # Make dictionaries for easy access
    descriptors = _get_descriptors_inherited(cls, Descriptor)
    public_names = {d.public_name: d for d in descriptors}
    private_names = {d.private_name: d for d in descriptors if hasattr(d, 'private_name')}
    del descriptors  # Free memory

    def add_kv(attr, val, dc_kwargs, descriptor_values):
        attr = attr_or_placeholder(attr)
        if attr in private_names:
            desc = private_names[attr]
            name = desc.public_name
            descriptor_values[name] = val
        elif attr in public_names:
            descriptor_values[attr] = val
        else:
            dc_kwargs[attr] = val

    if hasattr(cls, 'mrid') and BAN_KWARGS:
        def __init__(self, mrid=None, *args, **kwargs):
            dc_kwargs = {}
            descriptor_values = {}
            it = iter(init_signature.parameters)
            it.__next__()
            if args:
                raise ValueError('Objects derived from IdentifiedObject take at most 1 positional' +
                                 'argument - mrid; Use kwargs for object instantiation!')
            if mrid is not None and isinstance(mrid, str):
                dc_kwargs['mrid'] = mrid
            for attr, val in kwargs.items():
                add_kv(attr, val, dc_kwargs, descriptor_values)

            self.__dataclass_init__(**dc_kwargs)
            for k, v in descriptor_values.items():
                setattr(self, k, v)
    else:
        def __init__(self, *args, **kwargs):
            dc_kwargs = {}
            descriptor_values = {}
            it = iter(init_signature.parameters)
            it.__next__()
            for val in args:
                attr = it.__next__()
                add_kv(attr, val, dc_kwargs, descriptor_values)
            for attr, val in kwargs.items():
                add_kv(attr, val, dc_kwargs, descriptor_values)

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
        an = cls.__annotations__[_attr]
        if an == ClassVar or an.__origin__ == ClassVar:
            val = cls.__dict__.get(_attr)
            if isinstance(val, BackingValue):
                return
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

def _attach_accessors(cls):
    for name, member in cls.__dict__.items():
        if hasattr(member, '__addressor_target__'):
            target = member.__addressor_target__
            _type = member.__addressor_type__
            if _type == _Addressor.Validator:
                if not isinstance(target, ValidatedDescriptor):
                    raise AttributeError(f"Trying to add a validation method {member} " +
                                         f"to attribute {target} that is not an instance of ValidatedDescriptor!")
                target.validate = member
            elif _type in [_Addressor.Getter, _Addressor.Setter]:
                if isinstance(target, CustomDescriptor):
                    if _type == _Addressor.Getter:
                        target.add_getter(member)
                    if _type == _Addressor.Setter:
                        target.add_setter(member)
                else:
                    raise AttributeError(f"Trying to add a get/set method {member} " +
                                     f"to attribute {target} that is not an instance of CustomDescriptor!")

def _autoslot(cls, slots=True, weakref=False, inherit_hash=True, **kwargs):
    """
    Wrangle object creation to enable descriptor use
    in dataclasses with slots.

    This creates annotations and defaults for the internal variables,
    and re-types descriptors as ClassVar to force the dataclass
    creator to skip them.
    """
    new_annotations = cls.__annotations__.copy()
    if DEBUG_LOG: _spew(cls)

    no_kwargs = BAN_KWARGS and hasattr(cls, 'mrid')

    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        del new_annotations[attr]
        if isinstance(val, Descriptor):
            _attr = None
            if isinstance(val, BackedDescriptor):
                _attr = val.private_name
                if not isinstance(val, Alias):
                    new_annotations[_attr] = _type
            elif isinstance(val, CustomDescriptor):
                if not no_kwargs:
                    _attr = f'_init_placeholder_for_{attr}_'
                    new_annotations[_attr] = bool
                else:
                    new_annotations[attr] = ClassVar[_type]
                    continue
            if _attr and not isinstance(val, Alias):
                _validate_backed_name(cls, attr, _attr)

            val.set_type(_type)
            new_annotations[attr] = ClassVar[_type]
            if _attr and not isinstance(val, Alias):
                setattr(cls, _attr, val.default)

        else:
            new_annotations[attr] = _type

    _attach_accessors(cls)


    cls.__annotations__ = new_annotations

    if inherit_hash:
        kwargs['eq'] = False
        # kwargs['eq'] = True
        # kwargs['unsafe_hash'] = True

    if DEBUG_LOG: _spew(cls)

    obj = dataclass(slots=slots, **kwargs)(cls)
    if weakref and slots:
        cls.__slots__ = (*obj.__slots__, '__weakref__')
        obj = dataclass(slots=False, **kwargs)(cls)

    amend_init(obj, cls)
    del cls
    return obj


def private(default: Any, /, *, init: bool = False) -> Any:
    """A shorthand for a non-init dataclass field with a default value."""
    return field(default=default, init=init)  # or whatever sentinel your runtime uses

def instantiate(default_factory: Callable[[], Any], **kwargs):
    """A shorthand for a non-init dataclass field with a default factory."""
    return field(default_factory=default_factory, **kwargs)

@dataclass_transform(
    field_specifiers=(field,private,)
)
def dataslot(cls_outer=None, *, slots=True, weakref=False, inherit_hash=True, **kwargs):
    def dec(cls):
        new = _autoslot(cls, slots=slots, weakref=weakref, inherit_hash=inherit_hash, **kwargs)
        del cls
        import gc
        gc.collect()
        return new

    if cls_outer:
        return dec(cls_outer)
    return dec

if __name__ == '__main__':

    @dataslot
    class A:
        l: List[int]

        _: KW_ONLY = ...

        _l2: ClassVar[int] = None

        y: str = NoResetDescriptor()

        z: int | None = ValidatedDescriptor()

        x: int = 42

        @validate(z)
        def _z_validator(self, val):
            if val != 42 and val != 24:
                raise ValueError(f"BOOOOOP {self.z}")
            return val

    @dataslot
    class Tst:
        a: int = 42
        _l: List[int] = private(None)
        b: int = CustomDescriptor(3)
        l2: List[int] = instantiate(list)

        @getter(b)
        def get_b(self):
            if not self._l: return None
            return self._l[0]

        @setter(b)
        def set_b(self, value):
            if not self._l:
                self._l = [value]
            else:
                self._l[0] = value

    @dataslot
    class Tst2:
        a: int = 42
        _l: List[int] = private(None)

    a1 = A([2, 3], 'aabc', 42, 33)
    print(a1)

    tst = Tst(24,7)
    print(tst.l2)
    print(sys.getsizeof(tst))
    tst2 = Tst2(24)
    print(sys.getsizeof(tst2))

    print(tst.b)
    print(tst._l)
    tst.b = 6
    print(tst.b)
    print(tst._l)
    print(tst.__slots__)


    @dataclass
    class C:
        l1 : List[int] = None

    @dataslot
    class B(A):
        l2: List[int] = None

        c: C = WeakrefDescriptor()

        d: int = Alias(default=32, backed_name='x')

        r: int = RangedDescriptor(min=24, max=42)


    @dataslot
    class T(A):
        _z: ClassVar = BackingValue()
        t: int = TypeRestrictedDescriptor(backed_name='_z')

    @dataslot
    class I1(A):
        pass


    @dataslot
    class I2(I1):
        pass

    t = I2([], y='boop')
    print(t)


    @dataslot(weakref=True)
    class CN:
        mrid: str = None
        x: int = 42

    @dataslot
    class WR:
        cn: CN | None = WeakrefDescriptor()
        y: int = 24

        # @setter(cn)
        # def _set_cn(self, val):
        #     return ref(val)
        #
        # @getter(cn)
        # def _get_cn(self):
        #     # try:
        #     return self._cn()
            # except:
            #     return None

    t = WR()
    print('WR', t.cn)
    a  = CN('abc')
    t.cn = a
    print('WR', t.cn)
    print(a)

    t2 = WR()
    t2.cn = CN('abc')
    print('WEAKREF DEL:', t2.cn)

    t = T([])
    t.t = 24
    print(t.x)
    print(t.t)
    # print(t._z)

    a = A([1, 2], y='abc')

    l = [42, 24, 4]
    a = B(l=[1], y='abc', x=24)

    b = B(l=[2], y='de')
    print('!!!', a.y, a.x, b.y, b.x)
    print(b.d)

    b.r = 30
    try:
        b.r = 50
    except ValueError as e:
        print(e)
    print(b.r)

    a.z = 24
    try:
        a.z = 43
    except ValueError as e:
        print(e)


    c = C()

    print(sys.getrefcount(a.c))

    a.c = c
    print('ref', a.c)

    print(sys.getrefcount(a.c))

    del c

    print(sys.getrefcount(a.c))


    print(a.l)


    print(a.y)


    try:
        a.y = 'cool'
    except ValueError as e:
        print(e)
    print(a)


    a.l = []
    a.x = 24
    print(a)

    try:
        a.y = 'cool'
    except ValueError as e:
        print(e)

    @dataslot
    class H1:
        mrid: str | None = None
        def __hash__(self):
            print('HASH', self.mrid, self.mrid.__hash__())
            return self.mrid.__hash__()

    @dataslot
    class H2(H1):
        x: int = 42

    s = 'abc'

    h1 = H1(s)
    print(h1.__hash__())

    h2 = H2(s)
    print(h2)
    print(h2.__hash__())

    @dataslot
    class ABM:
        _mask: int = private(None)
        a: List[bool] = CustomDescriptor()
        a_s: List[bool] = Alias(backed_name='a')

        @getter(a)
        def _g(self):
            return [42] if self._mask else [24]

        @setter(a)
        def _s(self, val):
            self._mask = 1 if val else 0

    abm = ABM(a_s=[])
    print(abm.a)
    abm.a = [True]
    print(abm.a)

