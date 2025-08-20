#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import typing

from zepben.ewb import IdentifiedObject
from zepben.ewb.collections.zepben_list import ZepbenList

T_MRID = typing.TypeVar('T_MRID', bound=IdentifiedObject)

class MRIDList(ZepbenList[T_MRID]):

    def get_by_mrid(self, mrid: str):
        try:
            return next(item for item in self if item.mrid == mrid)
        except StopIteration:
            raise KeyError(mrid)

    def has_mrid(self, mrid: str):
        return any(item.mrid == mrid for item in self)

    def __contains__(self, item):
        if isinstance(item, str):
            return self.has_mrid(item)
        return super().__contains__(item)

    def add(self, item: T_MRID):
        if self.has_mrid(item.mrid):
            return #TODO: Figure out errors
        super().add(item)


