#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["validate_property_accessor"]


def validate_property_accessor(t, info, prop):
    obj = t()
    assert getattr(obj, prop.fget.__name__) is None

    iobj = info()
    setattr(obj, prop.fset.__name__, iobj)
    assert getattr(obj, prop.fget.__name__) is iobj

    setattr(obj, prop.fset.__name__, None)
    assert getattr(obj, prop.fget.__name__) is None
