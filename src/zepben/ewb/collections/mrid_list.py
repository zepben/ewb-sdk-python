#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Iterable

from zepben.ewb import IdentifiedObject
from zepben.ewb.collections.zepben_list import ZepbenList


class MRIDList(ZepbenList[IdentifiedObject]):

    def get_by_mrid(self, mrid: str):
        try:
            return next(item for item in self._data if item.mrid == mrid)
        except StopIteration:
            raise KeyError(mrid)

    def has_mrid(self, mrid: str):
        return any(item.mrid == mrid for item in self._data)


    def __contains__(self, item):
        if isinstance(item, str):
            return self.has_mrid(item)
        return super().__contains__(item)

    def add(self, item):
        if item.mrid in self:
            return #TODO: Figure out errors
        super().add(item)
