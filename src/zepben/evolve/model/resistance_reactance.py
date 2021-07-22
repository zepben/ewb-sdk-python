#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, Callable, TYPE_CHECKING

from dataclassy import dataclass

if TYPE_CHECKING:
    pass

__all__ = ["ResistanceReactance"]


@dataclass(slots=True)
class ResistanceReactance(object):
    r: Optional[float] = None
    x: Optional[float] = None
    r0: Optional[float] = None
    x0: Optional[float] = None

    def is_complete(self) -> bool:
        return self.r is not None and self.x is not None and self.r0 is not None and self.x0 is not None

    def is_empty(self) -> bool:
        return self.r is None and self.x is None and self.r0 is None and self.x0 is None

    def merge_if_incomplete(self, to_merge: Callable[[], Optional[ResistanceReactance]]) -> ResistanceReactance:
        if self.is_complete():
            return self
        else:
            rr = to_merge()
            if rr is not None:
                return ResistanceReactance(self.r if self.r is not None else rr.r,
                                           self.x if self.x is not None else rr.x,
                                           self.r0 if self.r0 is not None else rr.r0,
                                           self.x0 if self.x0 is not None else rr.x0)
            else:
                return self
