#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, fields, MISSING, Field
from typing import TypeVar, cast

from typing_extensions import dataclass_transform


T = TypeVar("T")


def _is_set(obj: object, name: str) -> bool:
    try:
        object.__getattribute__(obj, name)
    except AttributeError:
        return False
    return True

def remove_descriptor_annotations(cls: type[T]) -> T:
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

@dataclass_transform(eq_default=False, order_default=False)
def zb_dataclass(cls: type[T]) -> type[T]:
    """
    Shorthand alias for ``@dataclass(init=False, eq=False, slots=True, repr=False)``
    Allows us to modify dataclass parameters for all of CIM from a single reference point
    """
    cls = remove_descriptor_annotations(cls)
    # The cast is purely for type checkers to be aware of the true class of cls
    return cast(
        type[T],
        dataclass(
            init=False,
            eq=False,
            slots=True,
            repr=False,
        )(cls),
    )

def resolve_default(instance, field: Field):
    # Set field defaults
    if field.default is not MISSING:
        setattr(instance, field.name, field.default)
    elif field.default_factory is not MISSING:
        setattr(instance, field.name, field.default_factory())

    # Note: custom descriptors are not included in `fields(cls)`, so we don't need to handle them here

    # Mimic default Python missing arg error
    else:
        raise TypeError(
            f"Missing required field {field.name!r} "
            f"for {type(instance).__name__}"
        )


@zb_dataclass
class DataclassBase:
    """
    Instantiate the default fields and interpret the kwargs like ``@dataclass`` does

    This class serves as a base class for mostly init-less dataclasses used in CIM,
    allowing custom inits to not break the entire inheritance tree.
    It fills fields with default values, and treats kwargs the same way @dataclass does.

    For more motivation, refer to `MANIFESTO.md`
    """
    def __init__(self, **kwargs) -> None:
        # Currently post init implementation requires a lot of extra logic,
        # which would mess with readability. If you require it - add it.
        if callable(getattr(self, "__post_init__", None)):
            raise NotImplementedError("Current dataclass base does not support __post_init__ calls for redundancy reasons.")

        # Manually assign defaults in dataclass fields
        for f in fields(type(self)):
            # We cannot just check kwargs because fields could be set in subclass __init__'s
            if _is_set(self, f.name) or f.name in kwargs:
                continue

            resolve_default(self, f)

        # Assign all of the kwargs manually.
        # str-based setattr triggers descriptors, allowing us to intercept __set__.
        for attr, value in kwargs.items():
            setattr(self, attr, value)
