#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import TablePowerElectronicsUnit

__all__ = ["TableEvChargingUnits"]


class TableEvChargingUnits(TablePowerElectronicsUnit):

    def name(self) -> str:
        return "ev_charging_units"
