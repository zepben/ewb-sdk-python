#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["RemoteControl"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.scada.remote_point import RemotePoint

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.meas.control import Control


@dataslot
class RemoteControl(RemotePoint):
    """
    Remote controls are outputs that are sent by the remote unit to actuators in the process.
    """

    control: Optional['Control'] = None
    """The `zepben.ewb.model.cim.iec61970.base.meas.control.Control` for the `RemoteControl` point."""
