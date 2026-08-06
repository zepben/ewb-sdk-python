#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC, abstractmethod
from typing import Any, Callable, Collection, Generic, Iterable, Iterator, TypeVar


T = TypeVar("T")


class AbstractBackedCollection(Collection[T], Generic[T], ABC):
    """A mutable collection whose contents are stored elsewhere.

    Implementations provide the current contents through
    :meth:`_get_collection`. Element validation and the append lifecycle are
    centralised here, with hooks for raw storage and removal cleanup.

    :meth:`_post_remove` is invoked after individual removal. :meth:`clear`
    clears the backing storage directly, avoiding repeated removal bookkeeping
    when bulk cleanup is unnecessary.
    """

    _instance: Any
    validate: Callable[[Any, T], object] | None = None

    @abstractmethod
    def _get_collection(self) -> Collection[T]:
        """Return the current backing collection."""
        ...

    def _append_raw(self, item: T, /) -> None:
        """Append ``item`` to storage without validation or other hooks."""
        self._get_collection().append(item)  # type: ignore[attr-defined]

    def _post_remove(self, item: T, /) -> None:
        """Perform cleanup after ``item`` is removed."""

    def _clear_raw(self, collection: Collection[T], /) -> None:
        """Clear ``collection`` without per-item cleanup."""
        collection.clear()  # type: ignore[attr-defined]

    def _clear_and_copy(self, collection: Collection[T], /) -> Collection[T]:
        """Clear ``collection`` and return its former elements."""
        former_items = list(collection)
        self._clear_raw(collection)
        return former_items

    def append(self, item: T, /) -> None:
        """Append ``item`` after validation.

        This performs validation and storage, but no mRID check, backfill, or
        sorting.
        """
        if self.validate is not None:
            self.validate(self._instance, item)
        self._append_raw(item)

    def extend(self, items: Iterable[T] | None, /) -> None:
        """Append each item to the collection."""
        for element in items or []:
            self.append(element)

    def remove(self, item: T, /) -> None:
        """Remove ``item`` and perform per-item cleanup."""
        self._get_collection().remove(item)  # type: ignore[attr-defined]
        self._post_remove(item)

    def clear(self) -> None:
        """Clear the backing collection."""
        self._clear_raw(self._get_collection())

    def __len__(self) -> int:
        return len(self._get_collection())

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the backing collection."""
        return iter(self._get_collection())

    def __contains__(self, item: object) -> bool:
        """Return whether the backing collection contains ``item``."""
        return item in self._get_collection()

    def for_each_indexed(self, action: Callable[[int, T], object]) -> None:
        """Call the `action` on each item in the list."""
        for index, item in enumerate(self._get_collection()):
            action(index, item)
