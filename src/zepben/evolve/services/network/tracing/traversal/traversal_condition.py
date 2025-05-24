#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import TypeVar, Protocol, runtime_checkable

T = TypeVar('T')

__all__ = ['TraversalCondition']

@runtime_checkable
class TraversalCondition(Protocol[T]):
    """
    Protocol, representing a condition used in a traversal.
    Implementations of this interface can influence the traversal process by determining
    things such as the ability to queue items,stop at specific items, or apply other
    conditional logic during traversal

    T : The type of items being processed
    """
