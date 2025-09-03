#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABCMeta
from dataclasses import dataclass
from typing import ClassVar, List
from typing_extensions import dataclass_transform


class BackedDescriptor(metaclass=ABCMeta):
    def __init__(self, default=None):
        self.default = default

class ValidatedDescriptor(BackedDescriptor):

    def __init__(self, default=None, validate = None):
        super().__init__(default=default)
        self.validate = validate

    def __set_name__(self, owner, name):
        print(f'set name {owner} {name}')
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, *_):
        value = getattr(obj, self.private_name)
        print(f'Accessing {self.private_name} giving {value}')
        if value is self:
            self.__set_default(obj)
            return self.default
        return value

    def __set__(self, obj, value, do_validate: bool=True):
        if value is not self and do_validate:
            if self.validate:
                value = self.validate(obj, value)
        print(f'Updating {self.private_name} to {value}')
        setattr(obj, self.private_name, value)

    def __set_default(self, obj):
        self.__set__(obj, self.default, do_validate=False)



class NoResetDescriptor(ValidatedDescriptor):
    def __init__(self, default=None):
        super().__init__(default=default)
        self.validate = self.__one_set_validate

    def __one_set_validate(self, obj, value):
        old = getattr(obj, self.private_name)
        print(old, obj, value)
        if old is None or old is value:
            return value
        raise ValueError(f'{self.private_name} for {obj.__class__.__name__}' +
                         f' has already been set to {old},' +
                         f' cannot reset this field to {value}')



DEBUG_LOG = True

def _spew(cls):
    print(cls.__name__, '::')
    for k, v in cls.__dict__.items():
        print(f'\t{k}: {v}')

@dataclass_transform(
    kw_only_default=False,
    eq_default=True,
    order_default=False,
)
def autoslot_dataclass(cls=None, *_, slots=True, **kwargs):
    def decorator(cls):
        new_annotations = cls.__annotations__.copy()
        if DEBUG_LOG: _spew(cls)

        for attr, _type in cls.__annotations__.items():
            val = cls.__dict__.get(attr, None)
            if isinstance(val, BackedDescriptor):
                _attr = f'_{attr}'
                new_annotations[ attr] = ClassVar[_type]
                new_annotations[_attr] = _type
                setattr(cls, _attr, val.default)
        cls.__annotations__ = new_annotations

        if DEBUG_LOG: _spew(cls)

        return dataclass(slots=slots, **kwargs)(cls)

    if cls is None:
        return decorator
    return decorator(cls)






if __name__ == '__main__':

    @autoslot_dataclass(slots=False)
    class A:
        l: List[int]

        y: str = NoResetDescriptor()

        x: int = 42


    @autoslot_dataclass
    class B(A):
        l2: List[int] = None


    l = [42, 24, 4]
    a = B(l)

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
