#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import Field


class BackedDescriptor:
    """Expose a dataclass field or another descriptor under a public name.

    Reads and writes are delegated to the backing attribute. Descriptor
    chaining supports aliases, while field-backed descriptors support public
    views over private or nullable dataclass storage.
    """

    def __init__(self, private_field):
        if not isinstance(private_field, Field) and not isinstance(private_field, BackedDescriptor):
            raise TypeError(f"private_field parameter of the Descriptor constructor has to be an instance of dataclass Field, instead is {private_field}")
        self.private_field: 'Field | BackedDescriptor' = private_field
        self._backing_name: str | None = None
        self.name = None

    def __set_name__(self, owner, name):
        if name is None:
            return
        self.__name__ = self.name = name
        if not self._backing_name:
            self._backing_name = self.private_field.name

    def __get__(self, instance, _):
        if instance is None:
            return self
        return getattr(instance, self._backing_name)

    def __set__(self, instance, value):
        if self._backing_name is None:
            raise ValueError(f"Descriptor {self} is not yet aware of the supporting field - `__set__` cannot be called")
        return setattr(instance, self._backing_name, value)


Alias = BackedDescriptor
