#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import sys
from typing import Iterable

from zepben.ewb import Terminal, ConductingEquipment, require
from zepben.ewb.collections.mrid_list import MRIDList


class TerminalList(MRIDList[Terminal]):
    def __init__(self,
                 terminals: Iterable[Terminal],
                 conducting_equipment: ConductingEquipment = None,
                 max_terminals = int(sys.maxsize)):
        self.conducting_equipment: ConductingEquipment = conducting_equipment
        self.max_terminals = max_terminals
        super().__init__(terminals)

    def get_by_sn(self, sn: int):
        try:
            return next(term for term in self if term.sequence_number == sn)
        except StopIteration:
            raise IndexError(f"No Terminal with sequence_number {sn} was found in ConductingEquipment {str(self.conducting_equipment)}")

    def get(self, identifier: int | str):
        if isinstance(identifier, str):
            return self.get_by_mrid(identifier)
        elif isinstance(identifier, int):
            return self.get_by_sn(identifier)
        raise TypeError(f'`identifier` parameter not a recognised type: {type(identifier)}')

    def add(self, terminal: Terminal):
        require(len(self) < self.max_terminals,
                lambda: f"Unable to add {terminal} to {str(self.conducting_equipment)}" +
                        f". This conducting equipment already has the maximum number of terminals " +
                        f"({self.max_terminals}).")

        super().add(terminal)

        # TODO: Check if this thing is only supposed to run at init
        if self.conducting_equipment is not None:
            if terminal.conducting_equipment is None:
                terminal.conducting_equipment = self.conducting_equipment

        if terminal.sequence_number == 0:
            terminal.sequence_number = len(self) + 1

        self._data.sort(key=lambda t: t.sequence_number)




