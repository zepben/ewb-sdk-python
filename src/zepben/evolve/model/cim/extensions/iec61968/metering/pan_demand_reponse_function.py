#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List, Union

from zepben.evolve.model.cim.extensions.zbex import zbex
from zepben.evolve.model.cim.iec61968.metering.controlled_appliance import ControlledAppliance, Appliance
from zepben.evolve.model.cim.iec61968.metering.metering import EndDeviceFunction, EndDeviceFunctionKind

if TYPE_CHECKING:
    pass

from zepben.evolve.util import require

__all__ = ["PanDemandResponseFunction"]


@zbex
class PanDemandResponseFunction(EndDeviceFunction):
    """
    [ZBEX] PAN function that an end device supports, distinguished by 'kind'.
    """

    kind: EndDeviceFunctionKind = EndDeviceFunctionKind.UNKNOWN
    """[ZBEX] `zepben.evolve.model.cim.iec61968.metering.metering.EndDeviceFunctionKind` of this `PanDemandResponseFunction`"""

    _appliance_bitmask: Optional[int] = None

    def __init__(self, appliances: Union[int, ControlledAppliance] = None, **kwargs):
        super(PanDemandResponseFunction, self).__init__(**kwargs)
        if appliances is not None:
            self.appliance = appliances

    @property
    def appliance(self) -> Optional[ControlledAppliance]:
        """
        [ZBEX]
        The `ControlledAppliance`s being controlled by this `PanDemandResponseFunction`.
        """
        if self._appliance_bitmask is None:
            return None
        else:
            return ControlledAppliance(self._appliance_bitmask)

    @appliance.setter
    def appliance(self, appliance: Optional[Union[int, ControlledAppliance]]):
        if isinstance(appliance, int):
            self._appliance_bitmask = appliance
        elif isinstance(appliance, ControlledAppliance):
            if appliance:
                self._appliance_bitmask = appliance.bitmask
        else:
            if appliance:
                raise ValueError(f"Unsupported type for appliance: {appliance}. Must be either an int or ControlledAppliance")
            else:
                self._appliance_bitmask = None

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

    def add_appliances(self, appliances: List[Appliance]):
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

    def remove_appliances(self, appliances: List[Appliance]):
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
