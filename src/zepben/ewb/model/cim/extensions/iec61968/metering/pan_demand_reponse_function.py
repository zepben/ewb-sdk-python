#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PanDemandResponseFunction"]

from typing import Optional, List, Union

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61968.metering.controlled_appliance import ControlledAppliance, Appliance
from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction
from zepben.ewb.model.cim.iec61968.metering.end_device_function_kind import EndDeviceFunctionKind
from zepben.ewb.util import require


@zbex
@dataslot
class PanDemandResponseFunction(EndDeviceFunction):
    """
    [ZBEX] PAN function that an end device supports, distinguished by 'kind'.
    """

    kind: EndDeviceFunctionKind = EndDeviceFunctionKind.UNKNOWN
    """[ZBEX] `zepben.ewb.model.cim.iec61968.metering.metering.EndDeviceFunctionKind` of this `PanDemandResponseFunction`"""

    appliance: int | None = ValidatedDescriptor(None)

    @validate(appliance)
    def _appliance_validate(self, appliance: Union[int, ControlledAppliance] | None):
        if isinstance(appliance, int):
            return appliance
        elif isinstance(appliance, ControlledAppliance):
            if appliance:
                return appliance.bitmask
        else:
            if appliance:
                raise ValueError(f"Unsupported type for appliance: {appliance}. Must be either an int or ControlledAppliance")
            else:
                return None

    def add_appliance(self, appliance: Appliance) -> bool:
        """
        Add an appliance to the appliances being controlled.
        :param appliance: The appliance to add.
        :return: True if the controlled appliances were updated.
        """
        previous = self._appliance_bitmask
        bm = self._appliance_bitmask if self._appliance_bitmask else 0
        self._appliance_bitmask = bm | appliance.bitmask
        return self._appliance_bitmask != previous

    def add_appliances(self, appliances: List[Appliance]) -> bool:
        """
        Add appliances to the appliances being controlled.
        :param appliances: The appliances to add.
        :return: True if the controlled appliances were updated.
        """
        require(len(appliances) > 0, lambda: "You must provide at least one appliance to add")
        previous = self._appliance_bitmask

        def f(bitmask: int, nxt: Appliance) -> int:
            return bitmask | nxt.bitmask

        acc = self._appliance_bitmask if self._appliance_bitmask is not None else 0
        _ = [acc := f(acc, app) for app in appliances]
        self._appliance_bitmask = acc
        return self._appliance_bitmask != previous

    def remove_appliance(self, appliance: Appliance) -> bool:
        """
        Remove an appliance from the appliances being controlled.
        :param appliance: The appliance to remove.
        :return: True if the controlled appliances were updated.
        """
        previous = self._appliance_bitmask
        bm = self._appliance_bitmask if self._appliance_bitmask else 0
        self._appliance_bitmask = bm & ~appliance.bitmask
        return self._appliance_bitmask != previous

    def remove_appliances(self, appliances: List[Appliance]) -> bool:
        """
        Remove appliances from the appliances being controlled.
        :param appliances: Additional appliances to remove.
        :return: True if the controlled appliances were updated.
        """
        require(len(appliances) > 0, lambda: "You must provide at least one appliance to remove")
        previous = self._appliance_bitmask

        def f(bitmask: int, nxt: Appliance) -> int:
            return bitmask | nxt.bitmask

        acc = 0
        current = self._appliance_bitmask if self._appliance_bitmask is not None else 0
        _ = [acc := f(acc, app) for app in appliances]
        self._appliance_bitmask = current & ~acc
        return self._appliance_bitmask != previous
