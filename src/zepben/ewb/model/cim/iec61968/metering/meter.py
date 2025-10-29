#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Meter"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.metering.end_device import EndDevice


@dataslot
class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point. Used for measuring consumption and detection of events.
    """

    @property
    def company_meter_id(self) -> str | None:
        """ Returns this `Meter`s ID. Currently stored in `IdentifiedObject.name` """
        return self.name

    @company_meter_id.setter
    def company_meter_id(self, meter_id: str | None):
        """
        `meter_id` The ID to set for this Meter. Will use `IdentifiedObject.name` as a backing field.
        """
        self.name = meter_id
