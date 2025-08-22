#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import typing
from typing import List, Optional, Iterable

T = typing.TypeVar('T')

class ZepbenList(typing.Iterator[T]):
    """
    Generic list class
    """
    def __init__(self, data: Optional[Iterable[T]] = None):
        self._data: Optional[List[T]] = None
        if data is not None:
            self.update(data)

    def __iter__(self):
        yield from self._data or []

    def __next__(self):
        ...

    def __len__(self):
        return 0 if self._data is None else len(self._data)

    def num(self):
        """
        Get the number of items in this Zepben List
        Equivalent to `len(zblist_object)`
        """
        return len(self)

    def add(self, item: T):
        """
        Add an item to this Zepben List
        """
        if self._data is None:
            self._data = []
        self._data.append(item)

    def update(self, items: Iterable[T]):
        for item in items:
            self.add(item)

    def remove(self, item: T):
        """
        Remove an item from this Zepben List by item value
        """
        if item in self:
            self._data.remove(item)


    def clear(self):
        """
        Clear the contents of this Zepben List
        """
        del self._data

    def __contains__(self, item: T):
        if self._data is None:
            return False
        return item in self._data

    def __getitem__(self, idx: int):
        return self._data[idx]

    def has(self, item: T):
        """
        Check if an item is inside this Zepben List.
        Equivalent to `some_item in zblist_object`
        """
        return item in self

    def of_type(self, _type: typing.Type):
        yield from (item for item in self if isinstance(item, type))

    def num_of_type(self, _type: typing.Type):
        return sum(1 for item in self if isinstance(item, type))

    def print_contents(self):
        """
        Print all items in this Zepben List
        """
        print(self._data)

    def __repr__(self):
        return f'{self.__class__.__name__} [{self._data}]'




if __name__ == '__main__':
    # z  = ZbList()
    z : ZepbenList[int] = ZepbenList()

    for v in z:
        print(v)

    z.add(42)
    # z.add('24')
    for v in z: print(v)

    z.clear()

    print('z')
    for v in z: print(v)

    z.print_contents()

    z.add(3)
    for v in z: print(v)
    print(z.has(4))
    print(z.has(3))

    print(len(z))

