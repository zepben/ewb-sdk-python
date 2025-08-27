#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Meter"]

from typing import Optional

from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice


class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point. Used for measuring consumption and detection of events.
    """

    @property
    def company_meter_id(self) -> Optional[str]:
        """ Returns this `Meter`s ID. Currently stored in `IdentifiedObject.name` """
        return self.name

    @company_meter_id.setter
    def company_meter_id(self, meter_id: Optional[str]):
        """
        `meter_id` The ID to set for this Meter. Will use `IdentifiedObject.name` as a backing field.
        """
        self.name = meter_id
