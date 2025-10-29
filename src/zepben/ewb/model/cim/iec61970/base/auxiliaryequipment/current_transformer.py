#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["CurrentTransformer"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated

from zepben.ewb.dataslot.dataslot import Alias
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo


@dataslot
class CurrentTransformer(Sensor):
    """
    Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or monitored.
    Typically used as current transducer for the purpose of metering or protection.
    A typical secondary current rating would be 5A.
    """

    core_burden: int | None = None
    """Power burden of the CT core in watts."""

    current_transformer_info: Optional['CurrentTransformerInfo'] = Alias(backed_name='asset_info')
