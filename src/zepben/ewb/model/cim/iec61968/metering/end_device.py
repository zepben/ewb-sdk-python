#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EndDevice"]

from typing import Optional, List, Generator, TYPE_CHECKING
from abc import ABCMeta
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.assets.asset_container import AssetContainer
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint


@zb_dataclass
class EndDevice(AssetContainer, metaclass=ABCMeta):
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

    customer_mrid: Optional[str] = None
    """The `zepben.ewb.model.cim.iec61968.customers.customer.Customer` owning this `EndDevice`."""

    service_location: Optional[Location] = None
    """Service `zepben.ewb.model.cim.iec61968.common.location.Location` whose service delivery is measured by this `EndDevice`."""

    _usage_points: Optional[List[UsagePoint]] = field(default=None)

    _functions: Optional[List[EndDeviceFunction]] = field(default=None)

    usage_points: MridCollection[UsagePoint] = LazyMridList(
        _usage_points,
        "A UsagePoint",
    )

    functions: MridCollection[EndDeviceFunction] = LazyMridList(
        _functions,
        "An EndDeviceFunction",
    )


    # region deprecated list boilerplate
    # region usage_points boilerplate

    @deprecated("Use len(obj.usage_points) instead.")
    def num_usage_points(self):
        return len(self.usage_points)

    @deprecated("Use obj.usage_points.get_by_mrid(mrid) instead.")
    def get_usage_point(self, mrid: str) -> UsagePoint:
        return self.usage_points.get_by_mrid(mrid)

    @deprecated("Use obj.usage_points.append(up) instead.")
    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        self.usage_points.append(up)
        return self

    @deprecated("Use obj.usage_points.remove(up) instead.")
    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        self.usage_points.remove(up)
        return self

    @deprecated("Use obj.usage_points.clear() instead.")
    def clear_usage_points(self) -> EndDevice:
        self.usage_points.clear()
        return self

    # endregion usage_points boilerplate

    # region functions boilerplate

    @deprecated("Use len(obj.functions) instead.")
    def num_functions(self):
        return len(self.functions)

    @deprecated("Use obj.functions.get_by_mrid(mrid) instead.")
    def get_function(self, mrid: str) -> EndDeviceFunction:
        return self.functions.get_by_mrid(mrid)

    @deprecated("Use obj.functions.append(edf) instead.")
    def add_function(self, edf: 'EndDeviceFunction') -> 'EndDevice':
        self.functions.append(edf)
        return self

    @deprecated("Use obj.functions.remove(edf) instead.")
    def remove_function(self, edf: EndDeviceFunction) -> EndDevice:
        self.functions.remove(edf)
        return self

    @deprecated("Use obj.functions.clear() instead.")
    def clear_functions(self) -> EndDevice:
        self.functions.clear()
        return self

    # endregion functions boilerplate

    # endregion deprecated list boilerplate
