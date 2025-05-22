#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import abc
from typing import TypeVar, Generic

T = TypeVar('T')

__all__ = ['TraversalCondition']


class TraversalCondition(Generic[T], metaclass=abc.ABCMeta):
    """
    Protocol, representing a condition used in a traversal.
    Implementations of this interface can influence the traversal process by determining
    things such as the ability to queue items,stop at specific items, or apply other
    conditional logic during traversal

    New subclasses of this class should be made via:
    
    >>>@TraversalCondition.register
    >>>class SomeCondition(Generic[T]):
    >>>    pass

    and not direct subclassing as it will enforce overriding of `__init__`

    T : The type of items being processed
    """
    @abc.abstractmethod
    def __init__(self):
        """This method is only defined to deny the ability to create this class without subclassing"""
