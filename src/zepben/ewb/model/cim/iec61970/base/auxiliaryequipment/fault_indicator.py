#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["FaultIndicator"]

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment


@dataslot
class FaultIndicator(AuxiliaryEquipment):
    """
    A FaultIndicator is typically only an indicator (which may or may not be remotely monitored), and not a piece of
    equipment that actually initiates a protection event. It is used for FLISR (Fault Location, Isolation and
    Restoration) purposes, assisting with the dispatch of crews to "most likely" part of the network (i.e. assists
    with determining circuit section where the fault most likely happened).
    """
    pass
