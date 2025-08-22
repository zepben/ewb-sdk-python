#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import typing

from zepben.ewb import IdentifiedObject
from zepben.ewb.collections.zepben_list import ZepbenList


T_MRID = typing.TypeVar('T_MRID', bound=IdentifiedObject)

class MRIDList(ZepbenList[T_MRID]):
    def get_by_mrid(self, mrid: str, safe: bool=False):
        try:
            return next(item for item in self if item.mrid == mrid)
        except StopIteration:
            if safe:
                return None
            raise KeyError(mrid)

    def has_mrid(self, mrid: str):
        return any(item.mrid == mrid for item in self)

    def __contains__(self, identifier: str | T_MRID):
        if isinstance(identifier, str):
            return self.has_mrid(identifier)
        return super().__contains__(identifier)

    def add(self, item: T_MRID, safe: bool=False):
        if (other := self.get_by_mrid(item.mrid)) is not None:
            if not safe:
                if item is not other:
                    self.error_duplicate(item)
            return

        super().add(item)

    def error_duplicate(self, item: IdentifiedObject):
        raise ValueError(f"{item.__class__.__name__} with mRID {item.mrid} already exists.")




