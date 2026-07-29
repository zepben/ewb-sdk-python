#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.ewb import Terminal
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList


class TerminalsList(LazyMridList[Terminal]):

    def get_by_sequence_number(self, sequence_number: int) -> Terminal:
        term = next((it for it in self if it.sequence_number == sequence_number), None)
        if term is None:
            raise IndexError(f"No Terminal with sequence_number {sequence_number} was found in ConductingEquipment {str(self._instance)}")
        return term
