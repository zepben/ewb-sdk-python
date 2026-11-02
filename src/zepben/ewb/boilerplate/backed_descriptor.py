#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import Field
from typing import TypeVar

T = TypeVar("T", bound=type)



class BackedDescriptor:
    """
    A simple descriptor that references a dataclass field as a backing value.
    This allows it to have internal side effects and stateful implementation.
    Used for name shadowing and lazy fields (fields that can be None on instance level)
    """

    def __init__(self, private_field):
        if not isinstance(private_field, Field):
            raise TypeError("private_field parameter of the Descriptor constructor has to be an instance of dataclass Field.")
        self.private_field: Field = private_field
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, _):
        return getattr(instance, self.private_field.name)

    def __set__(self, instance, value):
        return setattr(instance, self.private_field.name, value)



def remove_descriptor_annotations(cls: T) -> T:
    """
    Remove annotations for class attributes that are data descriptors.

    This is intended for descriptor attributes that should remain class-level
    descriptors (classes defining ``__get__``/``__set__`` methods, controlling attribute access),
    rather than becoming dataclass fields/slots. Dataclasses decide
    which fields to create from ``__annotations__``. By removing annotations for
    descriptor-backed attributes before ``@dataclass`` runs, those attributes are
    left alone and can continue to behave as descriptors.

    Use this decorator below ``@dataclass`` so that it is called first. Python
    applies decorators from the bottom up::

        @dataclass
        @remove_descriptor_annotations
        class MyClass:
            _x: int = field(default=0)

            x: int = MyDescriptor("_x")

    In the example above, ``x`` is annotated, but its class value is a descriptor.
    Without ``remove_descriptor_annotations``, ``@dataclass`` would treat ``x`` as
    a dataclass field and may try to include it in generated fields, slots, init,
    repr, etc. With this decorator, the annotation for ``x`` is removed before
    dataclass processing, while normal fields such as ``_x`` are left intact.

    Dataclass ``Field`` instances are themselves descriptors and are thus skipped.
    In the example above, the slot for ``_x`` is still created.

    Before decoration::

        MyClass.__annotations__ == {
            "_x": int,
            "x": int,
        }

    After ``remove_descriptor_annotations`` runs::

        MyClass.__annotations__ == {
            "_x": int,
        }

    The class is then passed to ``@dataclass`` with only real dataclass fields
    remaining in ``__annotations__``.
    """
    # Get editable annotations
    original_annotations = dict(getattr(cls, "__annotations__", {}))
    tweaked_annotations = dict(original_annotations)

    # Get the current values of class fields. Before @dataclass is run, we see Descriptor instances here
    cls_dict = vars(cls)

    for name in list(tweaked_annotations):
        try:
            value = cls_dict[name]
            # Skip dataclass fields - they need annotations
            if isinstance(value, Field):
                continue
            # Any descriptor needs to implement get or set - most likely both.
            if hasattr(value, "__get__") or hasattr(value, "__set__"):
                tweaked_annotations.pop(name)
        # Values without defaults will error out - definitely not descriptors
        except KeyError:
            pass

    # Update annotations on the class
    cls.__annotations__ = tweaked_annotations

    return cls
