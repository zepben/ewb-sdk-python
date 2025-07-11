#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["EndDevice"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.model.cim.iec61968.assets.asset_container import AssetContainer
from zepben.ewb.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction
    from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint


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

    customer_mrid: Optional[str] = None
    """The `zepben.ewb.model.cim.iec61968.customers.customer.Customer` owning this `EndDevice`."""

    service_location: Optional[Location] = None
    """Service `zepben.ewb.model.cim.iec61968.common.location.Location` whose service delivery is measured by this `EndDevice`."""

    _usage_points: Optional[List[UsagePoint]] = None

    _functions: Optional[List[EndDeviceFunction]] = None

    def __init__(self, usage_points: List[UsagePoint] = None, functions: List[EndDeviceFunction] = None, **kwargs):
        super(EndDevice, self).__init__(**kwargs)
        if usage_points:
            for up in usage_points:
                self.add_usage_point(up)
        if functions:
            for edf in functions:
                self.add_function(edf)

    def num_usage_points(self):
        """
        Returns The number of `UsagePoint`s associated with this `EndDevice`
        """
        return nlen(self._usage_points)

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        The `UsagePoint`s associated with this `EndDevice`
        """
        return ngen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `UsagePoint` for this `EndDevice` identified by `mrid`

        `mrid` the mRID of the required `UsagePoint`
        Returns The `UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Associate `up` to this `EndDevice`.

        `up` the `UsagePoint` to associate with this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if another `UsagePoint` with the same `mrid` already exists for this `EndDevice`.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Disassociate `up` from this `EndDevice`

        `up` the `UsagePoint` to disassociate from this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `EndDevice`.
        """
        self._usage_points = safe_remove(self._usage_points, up)
        return self

    def clear_usage_points(self) -> EndDevice:
        """
        Clear all usage_points.
        Returns A reference to this `EndDevice` to allow fluent use.
        """
        self._usage_points = None
        return self

    def num_functions(self):
        """
        Returns The number of `EndDeviceFunction`s associated with this `EndDevice`
        """
        return nlen(self._functions)

    @property
    def functions(self) -> Generator[EndDeviceFunction, None, None]:
        """
        The `EndDeviceFunction`s associated with this `EndDevice`
        """
        return ngen(self._functions)

    def get_function(self, mrid: str) -> EndDeviceFunction:
        """
        Get the `EndDeviceFunction` for this `EndDevice` identified by `mrid`

        `mrid` the mRID of the required `EndDeviceFunction`
        Returns The `EndDeviceFunction` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._functions, mrid)

    def add_function(self, edf: EndDeviceFunction) -> EndDevice:
        """
        Associate `edf` to this `EndDevice`.

        `edf` the `EndDeviceFunction` to associate with this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if another `EndDeviceFunction` with the same `mrid` already exists for this `EndDevice`.
        """
        if self._validate_reference(edf, self.get_function, "An EndDeviceFunction"):
            return self
        self._functions = list() if self._functions is None else self._functions
        self._functions.append(edf)
        return self

    def remove_function(self, edf: EndDeviceFunction) -> EndDevice:
        """
        Disassociate `edf` from this `EndDevice`

        `up` the `EndDeviceFunction` to disassociate from this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `EndDevice`.
        """
        self._functions = safe_remove(self._functions, edf)
        return self

    def clear_functions(self) -> EndDevice:
        """
        Clear all end_device_functions.
        Returns A reference to this `EndDevice` to allow fluent use.
        """
        self._functions = None
        return self
