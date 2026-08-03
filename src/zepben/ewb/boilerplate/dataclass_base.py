#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass, fields, MISSING


def _is_set(obj: object, name: str) -> bool:
    try:
        object.__getattribute__(obj, name)
    except AttributeError:
        return False
    return True

@dataclass(slots=True)
class DataclassBase:
    """
    Instantiate the default fields and interpret the kwargs like ``@dataclass`` does

    This class serves as a base class for mostly init-less dataclasses used in CIM,
    allowing custom inits to not break the entire inheritance tree.
    It fills fields with default values, and treats kwargs the same way @dataclass does.

    For more motivation, refer to `MANIFESTO.md`
    """
    def __init__(self, **kwargs) -> None:
        # Assign all of the kwargs manually.
        # str-based setattr triggers descriptors, allowing us to intercept __set__.
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        # Manually assign defaults in dataclass fields
        for f in fields(type(self)):
            # We cannot just check kwargs because fields could be set in subclass __init__'s
            if _is_set(self, f.name):
                continue

            # Set field defaults
            if f.default is not MISSING:
                setattr(self, f.name, f.default)
            elif f.default_factory is not MISSING:
                setattr(self, f.name, f.default_factory())

            # Ignore custom descriptors
            elif hasattr(f, '__get__'):
                continue

            # Mimic default Python missing arg error
            else:
                raise TypeError(
                    f"Missing required field {f.name!r} "
                    f"for {type(self).__name__}"
                )

        # Currently post init implementation requires a lot of extra logic,
        # which would mess with readability. If you require it - add it.
        if callable(getattr(self, "__post_init__", None)):
            raise NotImplementedError("Current dataclass base does not support __post_init__ calls for redundancy reasons.")


# Alias for dataclass with params. Makes it easier to edit params for all of CIM at once.
zb_dataclass = dataclass(init=False, eq=False, slots=True, repr=False)
"""
Shorthand alias for ``@dataclass(init=False,eq=False,slots=True,repr=False)``
Allows us to modify dataclass parameters for all of CIM from a single reference point
"""

