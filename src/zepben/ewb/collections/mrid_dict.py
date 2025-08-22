#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Dict, Iterable

from zepben.ewb.collections.mrid_list import MRIDList, T_MRID


class MRIDDict(MRIDList):
    """
    Generic list class
    """

    def __init__(self, data: Optional[Iterable[T_MRID]] = None):
        super().__init__()
        self._data: Optional[Dict[str, T_MRID]] = None
        if data is not None:
            self.update(data)

    def __iter__(self):
        values = [] if self._data is None else self._data.values()
        yield from values

    def __next__(self):
        ...

    def add(self, item: T_MRID, safe: bool=False):
        """
        Add an item to this Zepben List
        """
        if self._data is None:
            self._data = dict()

        if not safe:
            if item.mrid in self._data:
                if self.get_by_mrid(item.mrid) is not object:
                    self.error_duplicate(item)

        self._data[item.mrid] = item

    def remove(self, item: T_MRID):
        """
        Remove an item from this Zepben List by item value
        """
        if item in self:
            local = self._data[item.mrid]
            if local is item:
                del self._data[item.mrid]


    def clear(self):
        """
        Clear the contents of this Zepben List
        """
        self._data = None

    def has_mrid(self, mrid: str):
        if self._data is None:
            return False
        return mrid in self._data

    def __contains__(self, identifier: str | T_MRID):
        if self._data is None:
            return False
        if isinstance(identifier, str):
            return self.has_mrid(identifier)
        return identifier in self._data.values()
