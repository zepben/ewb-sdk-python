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


class BackedDescriptor:
    """
    A simple descriptor that references a dataclass field as a backing value.
    This allows it to have internal side effects and stateful implementation.
    Used for name shadowing and lazy fields (fields that can be None on instance level)
    """

    def __init__(self, private_field):
        if not isinstance(private_field, Field) and not isinstance(private_field, BackedDescriptor):
            raise TypeError(f"private_field parameter of the Descriptor constructor has to be an instance of dataclass Field, instead is {private_field}")
        self.private_field: Field | 'BackedDescriptor' = private_field
        self.backing_name: str | None = None
        self.name = None

    def __set_name__(self, owner, name):
        if name is None:
            return
        self.__name__ = self.name = name
        if not self.backing_name:
            self.backing_name = self.private_field.name

    def __get__(self, instance, _):
        return getattr(instance, self.backing_name)

    def __set__(self, instance, value):
        return setattr(instance, self.backing_name, value)

Alias = BackedDescriptor

# Alias for dataclass with params. Makes it easier to edit params for all of CIM at once.
# zb_dataclass = dataclass(init=False, eq=False, slots=True, repr=False)
