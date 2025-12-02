#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = [
    'dataslot',
    'private',
    'instantiate',
    'validate',
    'Fget',
    'BackingValue',
    'BackedDescriptor',
    'WeakrefDescriptor',
    'ValidatedDescriptor',
    'NoResetDescriptor',
]


import inspect
import sys
from _weakref import ref
from abc import ABCMeta
from dataclasses import dataclass, field, KW_ONLY
from enum import Enum
from typing import ClassVar, List, Callable, Any, TYPE_CHECKING, overload, Type, TypeVar

from typing_extensions import dataclass_transform



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

    def __call__(self, it):
        return self._get(it)

class Descriptor(metaclass=ABCMeta):
    def __init__(self, default=None):
        self.default = default
        self.typed = None
        self.fget = Fget(self)

    def __set_name__(self, owner, name):
        self.owner = owner
        self.__name__ = self.name = name
        self.fget.__name__ = name

    def __get__(self, instance, *_):
        raise NotImplementedError()

    def __set__(self, instance, value, direct: bool=False):
        raise NotImplementedError()

    def set_default(self, obj):
        self.__set__(obj, self.default, direct=True)

    def set_type(self, typed: type):
        self.typed = typed


Getter = Callable[[Any], Any]
Setter = Callable[[Any, Any], Any]

class _Addressor(Enum):
    Getter = 0
    Setter = 1
    Validator = 2

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
            raise SetOnceError(f"Attribute {self.name} already has a setter.")
        self.setter = setter

    def add_getter(self, getter: Callable=None):
        if self.getter is not None:
            raise SetOnceError(f"Attribute {self.name} already has a getter.")
        self.getter = getter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.getter is None:
            raise AttributeError(f"Descriptor {self.name} of " +
                                 f"{self.owner.__name__} is missing a getter!")
        return self.getter(instance)

    def __set__(self, obj, value, _: bool=False):
        if value is not self:
            if self.setter is None:
                raise AttributeError(f"Descriptor {self.name} of " +
                                     f"{self.owner.__name__} is missing a getter!")
            self.setter(obj, value)

class BackedDescriptor(Descriptor):

    def __init__(self, default=None, backed_name=None, exposed_backing=False):
        super().__init__(default=default)
        self.default = default
        self.private_name = backed_name
        self.exposed_backing=exposed_backing

    def __set_name__(self, owner, name):
        super().__set_name__(owner=owner, name=name)
        if self.private_name is None:
            self.private_name = '_' + name

    def __get__(self, obj, *_):
        if obj is None:
            return self
        value = getattr(obj, self.private_name)
        if value is self:
            self.set_default(obj)
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
            self.set_default(obj)
            value = self.default
        if value is not None:
            return value()
        return value

    def __set__(self, obj, value, direct: bool=False):
        if value:
            value = ref(value)
        setattr(obj, self.private_name, value)


class RangedDescriptor(ValidatedDescriptor):
    def __init__(self,
                 default = None,
                 min=0, max=0,
                 backed_name=None):
        error_msg = lambda val: (
            f"{self.name} [{val}] " +
            f"must be between {min} " +
            f"and {max}.")
        def check(_, val):
            if val is not None and not min <= val <= max:
                raise ValueError(error_msg(val))
            return val
        super().__init__(default=default, validate=check, backed_name=backed_name)

class Alias(BackedDescriptor):
    def __init__(self, default=None, backed_name=None):
        super().__init__(default, backed_name, exposed_backing=True)



def validate(var: object | ValidatedDescriptor):
    def inner(f):
        if not isinstance(var, ValidatedDescriptor):
            raise AttributeError(f"Trying to add a validation method {f} " +
                                 f"to attribute {var} that is not a ValidatedDescriptor!")
        var.validate = f
    return inner

def getter(var: object | CustomDescriptor):
    def inner(f):
        if not isinstance(var, CustomDescriptor):
            raise AttributeError(f"Trying to add a get method {f} " +
                                 f"to attribute {var} that is not a CustomDescriptor!")
        var.add_getter(f)
    return inner

def setter(var: object | CustomDescriptor):
    def inner(f):
        if not isinstance(var, CustomDescriptor):
            raise AttributeError(f"Trying to add a set method {f} " +
                                 f"to attribute {var} that is not a CustomDescriptor!")
        var.add_setter(f)
    return inner



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

def _amend_init(obj: type, cls: type):
    """
    Intercept dataclass init and initialise descriptors separately.
    Call the original init to allow the dataclass to handle fields.
    """

    # Retrieve the dataclass init signature to ensure arg ordering is maintained
    init_signature = inspect.signature(obj.__init__)

    # Make dictionaries for easy access (associated with type, not instances)
    descriptors = _get_descriptors_inherited(cls, Descriptor)
    # Indexed by descriptor names (for kwargs)
    names = {d.name: d for d in descriptors}
    # Indexed by private names (dataclass args will be generated with private field names)
    private_names = {d.private_name: d for d in descriptors if hasattr(d, 'private_name')}
    # Free memory
    del descriptors


    def __init__(self, *args, **kwargs):
        dc_kwargs = {}  # kwargs for dataclass - normal fields
        descriptor_values = {}  # Descriptor args - ignored by the dataclass init

        # Iterate through the generated args first
        it = iter(init_signature.parameters.values())
        it.__next__()   # Skip self
        for i, val in enumerate(args):
            # Retrieve generated init arg
            param = it.__next__()
            name = param.name if not param.name in private_names else private_names[param.name].name
            if param.kind == inspect.Parameter.KEYWORD_ONLY:
                raise TypeError(f"Parameter {name} of {cls.__name__} is keyword-only!")
            if isinstance(val, CustomDescriptor):
                raise TypeError(f"CustomDecsriptors cannot be instantiated with positional args! ({name} of {cls.__name__})")
            # Put the parameter into kwargs (processed later)
            kwargs[name] = val

        # Go through all passed kwargs, including calues extracted from args above
        for attr, val in kwargs.items():
            if attr in names:   # value belongs to a descriptor
                descriptor_values[attr] = val
            else:   # Normal dc field
                dc_kwargs[attr] = val

        # Call the dataclass init with just the normal fields
        self.__dataclass_init_for_dataslot(**dc_kwargs)
        # Manually call the setter for all the found descriptor values
        for k, v in descriptor_values.items():
            d = names[k]
            d.__set__(self, v)

    # Save the dataclass init under a different name
    obj.__dataclass_init_for_dataslot = obj.__init__
    # Insert the newly generated init to be called on creation
    obj.__init__ = __init__

def _validate_backed_name(cls: type, attr, _attr):
    """
    Check that the name about to be used to back a descriptor
    is not already in use.
    """
    if not hasattr(cls, '__annotations__'):
        return
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
        _validate_backed_name(base, attr, _attr)
        # if not hasattr(base, '__annotations__'):
        #     continue
        # if _attr in base.__annotations__:
        #     raise AttributeError(f'Cannot create a descriptor {attr} ' +
        #                          f'backed by field {_attr} ' +
        #                          f'because the field already exists in superclass {base.__name__}')


def _autoslot(cls, slots=True, weakref=False, **kwargs):
    """
    This method changes runtime annotations to trick dataclasses into
    generating the correct slots signature, while maintaining correct
    type hinting in the editor.

    The specific steps are:
    1. Change descriptors to ClassVar (removes them from slots)
    2. Add descriptor private fields to annotations (adds them to slots without showing in init)
    3. Set defaults for private fields to those specified in the decorators

    It re-builds all annotations to maintain parameter order consistent with type hints.
    """
    new_annotations = {}

    for attr, _type in cls.__annotations__.items():
        val = cls.__dict__.get(attr, None)
        if isinstance(val, Descriptor):
            # Step 1: force dataclass to ignore descriptors
            new_annotations[attr] = ClassVar[_type]
            val.set_type(_type)     # Communicate type to the descriptor

            # Step 2: if descriptor has a private field, add it to the class definition
            if isinstance(val, BackedDescriptor):
                _attr = val.private_name
                if not val.exposed_backing:
                    new_annotations[_attr] = _type
                    _validate_backed_name(cls, attr, _attr)     # Check that there is no name conflict
                    # Step 3: set the default for the private field
                    setattr(cls, _attr, val.default)
        # If the member is not a descriptor, copy it over with no changes
        else:
            new_annotations[attr] = _type

    # Update the annotations on the original class
    cls.__annotations__ = new_annotations

    # Manually invoke the dataclass decorator
    new_cls = dataclass(slots=slots, **kwargs)(cls)

    # We can't partially define slots, so to add weakref, we use those generated by the dataclass
    # and inject the weakref, then re-generate the class.
    # Note: Dubious.
    # TODO: Remove this once 3.10 is deprecated. 3.11 onwards has weakref as one of the dataclass params.
    if weakref and slots:
        cls.__slots__ = (*new_cls.__slots__, '__weakref__')
        new_cls = dataclass(slots=False, **kwargs)(cls)

    # Fix the init to comprehend descriptors correctly
    _amend_init(new_cls, cls)
    # Remove the old class because it is unused
    del cls

    return new_cls

def private(default: Any, /, *, init: bool = False) -> Any:
    """A shorthand for a non-init dataclass field with a default value."""
    return field(default=default, init=init)  # or whatever sentinel your runtime uses

def instantiate(default_factory: Callable[[], Any] | type, **kwargs):
    """A shorthand for a non-init dataclass field with a default factory."""
    return field(default_factory=default_factory, **kwargs)

@dataclass_transform(
    field_specifiers=(field,private,),
    eq_default=False,
    kw_only_default=True
)
def _dataslot(cls_outer=None, /, *, slots=True, weakref=False, **kwargs):
    # TODO: Add kwargs mimicking dataclass
    kwargs.setdefault('kw_only', True)
    kwargs.setdefault('eq', False)
    def dec(cls):
        new = _autoslot(cls, slots=slots, weakref=weakref, **kwargs)
        return new

    if cls_outer:
        return dec(cls_outer)
    return dec



T = TypeVar("T")

if TYPE_CHECKING:

    # Python < 3.11 overload (no weakref_slot)
    if sys.version_info < (3, 11):

        @overload
        def dataslot(
            *,
            init: bool = True, repr: bool = True, eq: bool = False, order: bool = False, unsafe_hash: bool = False,
            frozen: bool = False, match_args: bool = True, kw_only: bool = True, slots: bool = True,
        ) -> Callable[[Type[T]], Type[T]]:
            ...


        @overload
        def dataslot(
            _cls: Type[T], /, *,
            init: bool = True, repr: bool = True, eq: bool = False, order: bool = False, unsafe_hash: bool = False,
            frozen: bool = False, match_args: bool = True, kw_only: bool = True, slots: bool = True,
        ) -> Type[T]:
            ...

    # Python >= 3.11 overload (adds weakref_slot)
    else:

        @overload
        def dataslot(
            *,
            init: bool = True, repr: bool = True, eq: bool = False, order: bool = False, unsafe_hash: bool = False,
            frozen: bool = False, match_args: bool = True, kw_only: bool = True, slots: bool = True,
            weakref_slot: bool = False,
        ) -> Callable[[Type[T]], Type[T]]:
            ...

        @overload
        def dataslot(
            _cls: Type[T], /, *,
            init: bool = True, repr: bool = True, eq: bool = False, order: bool = False, unsafe_hash: bool = False,
            frozen: bool = False, match_args: bool = True, kw_only: bool = True, slots: bool = True,
            weakref_slot: bool = False,
        ) -> Type[T]:
            ...
else:
    def dataslot(*args, **kwargs):
        return _dataslot(*args, **kwargs)

if __name__ == '__main__':

    @dataslot(kw_only=False)
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

