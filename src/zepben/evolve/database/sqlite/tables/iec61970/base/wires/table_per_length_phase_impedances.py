#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.database.sqlite.tables.iec61970.base.wires.table_per_length_impedances import TablePerLengthImpedances

__all__ = ["TablePerLengthPhaseImpedances"]


class TablePerLengthPhaseImpedances(TablePerLengthImpedances):

    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "per_length_phase_impedances"
