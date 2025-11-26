#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EndDevice"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assets.asset_container import AssetContainer
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint


@dataslot
class EndDevice(AssetContainer):
    """
    Asset container that performs one or more end device functions. One type of end device is a meter which can perform
    metering, load management, connect/disconnect, accounting functions, etc. Some end devices, such as ones monitoring
    and controlling air conditioners, refrigerators, pool pumps may be connected to a meter. All end devices may have
    communication capability defined by the associated communication function(s).

    An end device may be owned by a consumer, a service provider, utility or otherwise.

    There may be a related end device function that identifies a sensor or control point within a metering application
    or communications systems (e.g., water, gas, electricity).

    Some devices may use an optical port that conforms to the ANSI C12.18 standard for communications.
    """

    customer_mrid: str | None = None
    """The `zepben.ewb.model.cim.iec61968.customers.customer.Customer` owning this `EndDevice`."""

    service_location: Location | None = None
    """Service `zepben.ewb.model.cim.iec61968.common.location.Location` whose service delivery is measured by this `EndDevice`."""

    usage_points: List[UsagePoint] | None = MRIDListAccessor()

    functions: List[EndDeviceFunction] | None = MRIDListAccessor()

    def _retype(self):
        self.usage_points: MRIDListRouter[UsagePoint] = ...
        self.functions: MRIDListRouter[EndDeviceFunction] = ...
    
    @deprecated("BOILERPLATE: Use len(usage_points) instead")
    def num_usage_points(self):
        return len(self.usage_points)

    @deprecated("BOILERPLATE: Use usage_points.get_by_mrid(mrid) instead")
    def get_usage_point(self, mrid: str) -> UsagePoint:
        return self.usage_points.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use usage_points.append(up) instead")
    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        self.usage_points.append(up)
        return self

    @deprecated("Boilerplate: Use usage_points.remove(up) instead")
    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        self.usage_points.remove(up)
        return self

    @deprecated("BOILERPLATE: Use usage_points.clear() instead")
    def clear_usage_points(self) -> EndDevice:
        return self.usage_points.clear()

    @deprecated("BOILERPLATE: Use len(functions) instead")
    def num_functions(self):
        return len(self.functions)

    @deprecated("BOILERPLATE: Use functions.get_by_mrid(mrid) instead")
    def get_function(self, mrid: str) -> EndDeviceFunction:
        return self.functions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use functions.append(edf) instead")
    def add_function(self, edf: EndDeviceFunction) -> EndDevice:
        self.functions.append(edf)
        return self

    @deprecated("Boilerplate: Use functions.remove(edf) instead")
    def remove_function(self, edf: EndDeviceFunction) -> EndDevice:
        self.functions.remove(edf)
        return self

    @deprecated("BOILERPLATE: Use functions.clear() instead")
    def clear_functions(self) -> EndDevice:
        self.functions.clear()
        return self

