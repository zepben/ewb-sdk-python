#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import abstractmethod

__all__ = ["Tracker"]

from typing import TypeVar, Generic
from dataclassy import dataclass

T = TypeVar("T")


@dataclass(slots=True)
class Tracker(Generic[T]):
    """
    An interface used by `Traversal`'s to 'track' items that have been visited.

    A `Traversal` will utilise `has_visited`, `visit`, and `clear`.
    """

    @abstractmethod
    def has_visited(self, item: T) -> bool:
        """
        Check if the tracker has already seen an item.
        `item` The item to check if it has been visited.
        Returns true if the item has been visited, otherwise false.
        """
        raise NotImplementedError()

    @abstractmethod
    def visit(self, item: T) -> bool:
        """
        Visit an item. Item will not be visited if it has previously been visited.
        `item` The item to visit.
        Returns True if visit succeeds. False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        """
        Clear the tracker, removing all visited items.
        """
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> Tracker[T]:
        """
        Create a copy of this tracker. `has_visited` should report the same for the copied tracker for each item,
        but visiting an item on one of either the copy or original should not make the other report it as visited.
        Returns the copied tracker.
        """
        raise NotImplementedError()
