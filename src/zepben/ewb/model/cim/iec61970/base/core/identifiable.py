#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Identifiable"]

from abc import ABCMeta, abstractmethod

from zepben.ewb.dataclassy import dataclass

@dataclass(slots=True)
class Identifiable(metaclass=ABCMeta):
    """
    An interface that marks an object as identifiable.
    :argument mrid: The identifier for this object.
    """
    mrid: str

    def __init__(self, **kwargs):
        if kwargs:
            raise TypeError("unexpected keyword arguments in Identified constructor: {}".format(kwargs))

    @abstractmethod
    def __str__(self) -> str:
        """
        Printable version of the object including its name, mrid, and optionally, type
        """
