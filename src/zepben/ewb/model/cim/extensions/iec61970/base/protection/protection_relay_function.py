#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelayFunction"]

import sys
import warnings
from typing import Optional, List, Generator, Iterable, Callable, TYPE_CHECKING, Any
from abc import ABCMeta

from zepben.ewb.dataclass_descriptors.lazy_list import LazyIndexedList
if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated
from dataclasses import field

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.extensions.iec61970.base.protection.power_direction_kind import PowerDirectionKind
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import ProtectionKind
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.util import require, nlen, ngen, safe_remove, get_by_mrid
from zepben.ewb import remove_descriptor_annotations
from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61968.assetinfo.relay_info import RelayInfo
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.relay_setting import RelaySetting
    from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
    from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch


@zb_dataclass
@zbex
class ProtectionRelayFunction(PowerSystemResource, metaclass=ABCMeta):
    """
    [ZBEX]
    A function that a relay implements to protect equipment.
    """

    asset_info: Optional[RelayInfo] = None

    model: Optional[str] = None
    """[ZBEX] The protection equipment type name(manufacturer information)."""

    reclosing: Optional[bool] = None
    """[ZBEX] True if the protection equipment is reclosing or False otherwise."""

    relay_delay_time: Optional[float] = None
    """[ZBEX] The time delay from detection of abnormal conditions to relay operation in seconds."""

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """[ZBEX] The kind of protection being provided by this ProtectionRelayFunction."""

    directable: Optional[bool] = None
    """[ZBEX] Whether this ProtectionRelayFunction responds to power flow in a given direction."""

    power_direction: PowerDirectionKind = PowerDirectionKind.UNKNOWN
    """[ZBEX] The flow of the power direction used by this ProtectionRelayFunction."""

    _sensors: Optional[List[Sensor]] = field(default=None)

    _protected_switches: Optional[List[ProtectedSwitch]] = field(default=None)

    _schemes: Optional[List[ProtectionRelayScheme]] = field(default=None)

    _time_limits: Optional[List[float]] = field(default=None)

    _thresholds: Optional[List[RelaySetting]] = field(default=None)


    @property
    @deprecated("use asset_info instead.")
    def relay_info(self):
        """Datasheet information for this CurrentRelay"""
        return self.asset_info

    @relay_info.setter
    @deprecated("use asset_info instead.")
    def relay_info(self, relay_info: Optional[RelayInfo]):
        self.asset_info = relay_info

    time_limits: LazyIndexedList[float] = LazyIndexedList(
        _time_limits,
        "float"
    )

    thresholds: LazyIndexedList[RelaySetting] = LazyIndexedList(
        _thresholds,
        "RelaySetting"
    )

    sensors: MridCollection[Sensor] = LazyMridList(
        _sensors,
        "A Sensor",
    )

    protected_switches: MridCollection[ProtectedSwitch] = LazyMridList(
        _protected_switches,
        "A ProtectedSwitch",
    )

    schemes: MridCollection[ProtectionRelayScheme] = LazyMridList(
        _schemes,
        "A ProtectionRelayScheme",
    )


    # region deprecated list boilerplate

    # region thresholds boilerplate

    @deprecated("Use thresholds.for_each_indexed(action)")
    def for_each_threshold(self, action: Callable[[int, RelaySetting], Any]):
        self.thresholds.for_each_indexed(action)

    @deprecated("Use thresholds.append(threshold)")
    def add_threshold(
        self,
        threshold: RelaySetting,
        sequence_number: int = None,
    ) -> ProtectionRelayFunction:
        if sequence_number is None: sequence_number = len(self.thresholds)
        self.thresholds.insert(sequence_number, threshold)
        return self

    @deprecated("Use len(thresholds) instead.")
    def num_thresholds(self) -> int:
        return len(self.thresholds)

    @deprecated("Use thresholds[sequence_number] instead.")
    def get_threshold(self, sequence_number: int) -> RelaySetting:
        return self.thresholds[sequence_number]

    @deprecated("Use thresholds.remove(threshold) instead.")
    def remove_threshold(
        self,
        threshold: RelaySetting,
    ) -> ProtectionRelayFunction:
        self.thresholds.remove(threshold)
        return self

    @deprecated("Use thresholds.pop(sequence_number) instead.")
    def remove_threshold_at(
        self,
        sequence_number: int,
    ) -> RelaySetting:
        return self.thresholds.pop(sequence_number)

    @deprecated("Use thresholds.clear() instead.")
    def clear_thresholds(self) -> ProtectionRelayFunction:
        self.thresholds.clear()
        return self

    # endregion

    # region time_limits boilerplate
    @deprecated("Use time_limits.for_each_indexed(action)")
    def for_each_time_limit(self, action: Callable[[int, float], Any]):
        self.time_limits.for_each_indexed(action)

    @deprecated(
        "Use time_limits.append(time_limit)")
    def add_time_limit(
        self,
        time_limit: float,
        index: int = None,
    ) -> ProtectionRelayFunction:
        if index is None: index = len(self.time_limits)
        self.time_limits.insert(index, time_limit)
        return self

    @deprecated("Use len(time_limits) instead.")
    def num_time_limits(self) -> int:
        return len(self.time_limits)

    @deprecated("Use time_limits[index] instead.")
    def get_time_limit(self, index: int) -> float:
        return self.time_limits[index]

    @deprecated("Use time_limits.remove(time_limit) instead.")
    def remove_time_limit(
        self,
        time_limit: float,
    ) -> ProtectionRelayFunction:
        self.time_limits.remove(time_limit)
        return self

    @deprecated("Use time_limits.pop(index) instead.")
    def remove_time_limit_at(self, index: int) -> float:
        return self.time_limits.pop(index)

    @deprecated("Use time_limits.clear() instead.")
    def clear_time_limits(self) -> ProtectionRelayFunction:
        self.time_limits.clear()
        return self

    # endregion

    # region sensors boilerplate

    @deprecated("Use len(obj.sensors) instead.")
    def num_sensors(self) -> int:
        return len(self.sensors)

    @deprecated("Use obj.sensors.get_by_mrid(mrid) instead.")
    def get_sensor(self, mrid: str) -> Sensor:
        return self.sensors.get_by_mrid(mrid)

    @deprecated("Use obj.sensors.append(sensor) instead.")
    def add_sensor(self, sensor: Sensor) -> ProtectionRelayFunction:
        self.sensors.append(sensor)
        return self

    @deprecated("Use obj.sensors.remove(sensor) instead.")
    def remove_sensor(self, sensor: Optional[Sensor]) -> ProtectionRelayFunction:
        self.sensors.remove(sensor)
        return self

    @deprecated("Use obj.sensors.clear() instead.")
    def clear_sensors(self) -> ProtectionRelayFunction:
        self.sensors.clear()
        return self

    # endregion sensors boilerplate

    # region protected_switches boilerplate

    @deprecated("Use len(obj.protected_switches) instead.")
    def num_protected_switches(self) -> int:
        return len(self.protected_switches)

    @deprecated("Use obj.protected_switches.get_by_mrid(mrid) instead.")
    def get_protected_switch(self, mrid: str) -> ProtectedSwitch:
        return self.protected_switches.get_by_mrid(mrid)

    @deprecated("Use obj.protected_switches.append(protected_switch) instead.")
    def add_protected_switch(self, protected_switch: ProtectedSwitch) -> ProtectionRelayFunction:
        self.protected_switches.append(protected_switch)
        return self

    @deprecated("Use obj.protected_switches.remove(protected_switch) instead.")
    def remove_protected_switch(self, protected_switch: Optional[ProtectedSwitch]) -> ProtectionRelayFunction:
        self.protected_switches.remove(protected_switch)
        return self

    @deprecated("Use obj.protected_switches.clear() instead.")
    def clear_protected_switches(self) -> ProtectionRelayFunction:
        self.protected_switches.clear()
        return self

    # endregion protected_switches boilerplate

    # region schemes boilerplate

    @deprecated("Use len(obj.schemes) instead.")
    def num_schemes(self) -> int:
        return len(self.schemes)

    @deprecated("Use obj.schemes.get_by_mrid(mrid) instead.")
    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        return self.schemes.get_by_mrid(mrid)

    @deprecated("Use obj.schemes.append(scheme) instead.")
    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelayFunction:
        self.schemes.append(scheme)
        return self

    @deprecated("Use obj.schemes.remove(scheme) instead.")
    def remove_scheme(self, scheme: Optional[ProtectionRelayScheme]) -> ProtectionRelayFunction:
        self.schemes.remove(scheme)
        return self

    @deprecated("Use obj.schemes.clear() instead.")
    def clear_schemes(self) -> ProtectionRelayFunction:
        self.schemes.clear()
        return self

    # endregion schemes boilerplate

    # endregion deprecated list boilerplate
