#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelayFunction"]

from typing import Optional, List, Generator, Iterable, Callable, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated

from zepben.ewb.dataslot.dataslot import Alias
from zepben.ewb.model.cim.extensions.iec61970.base.protection.power_direction_kind import PowerDirectionKind
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import ProtectionKind
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.util import require, nlen, ngen, safe_remove, get_by_mrid

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61968.assetinfo.relay_info import RelayInfo
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.relay_setting import RelaySetting
    from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
    from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch


@zbex
@dataslot
class ProtectionRelayFunction(PowerSystemResource):
    """
    [ZBEX]
    A function that a relay implements to protect equipment.
    """

    model: str | None = None
    """[ZBEX] The protection equipment type name(manufacturer information)."""

    reclosing: bool | None = None
    """[ZBEX] True if the protection equipment is reclosing or False otherwise."""

    relay_delay_time: float | None = None
    """[ZBEX] The time delay from detection of abnormal conditions to relay operation in seconds."""

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """[ZBEX] The kind of protection being provided by this ProtectionRelayFunction."""

    directable: bool | None = None
    """[ZBEX] Whether this ProtectionRelayFunction responds to power flow in a given direction."""

    power_direction: PowerDirectionKind = PowerDirectionKind.UNKNOWN
    """[ZBEX] The flow of the power direction used by this ProtectionRelayFunction."""

    sensors: List[Sensor] | None = MRIDListAccessor()

    protected_switches: List[ProtectedSwitch] | None = MRIDListAccessor()

    schemes: List[ProtectionRelayScheme] | None = MRIDListAccessor()

    time_limits: List[float] | None = ListAccessor()

    thresholds: List[RelaySetting] | None = ListAccessor()

    relay_info: RelayInfo | None = Alias(backed_name="asset_info")

    def _retype(self):
        self.sensors: MRIDListRouter[Sensor] = ...
        self.protected_switches: MRIDListRouter[ProtectedSwitch] = ...
        self.schemes: MRIDListRouter[ProtectionRelayScheme] = ...
        self.time_limits: ListRouter[float] = ...
        self.thresholds: ListRouter[RelaySetting] = ...

    def for_each_threshold(self, action: Callable[[int, RelaySetting], None]):
        """
        Call the `action` on each :class:`RelaySetting` in the `thresholds` collection

        :param action: An action to apply to each :class:`RelaySetting` in the `thresholds` collection, taking the index of the threshold, and the threshold itself.
        """
        for index, point in enumerate(self.thresholds):
            action(index, point)

    @custom_add(thresholds)
    def add_threshold(self, threshold: RelaySetting, sequence_number: int = None) -> ProtectionRelayFunction:
        """
        Add a threshold[:class:`RelaySetting`] to this :class:`ProtectionRelayFunction`'s list of thresholds.

        :param threshold: The threshold[:class:`RelaySetting`] to add to this :class:`ProtectionRelayFunction`.
        :param sequence_number: The sequence number of the `threshold` being added.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        if sequence_number is None:
            sequence_number = self.num_thresholds()
        require(0 <= sequence_number <= self.num_thresholds(),
                lambda: f"Unable to add RelaySetting to {str(self)}. Sequence number {sequence_number} "
                        f"is invalid. Expected a value between 0 and {self.num_thresholds()}. Make sure you are "
                        f"adding the items in order and there are no gaps in the numbering.")
        self.thresholds.insert_raw(sequence_number, threshold)
        return self

    @deprecated("BOILERPLATE: Use len(thresholds) instead")
    def num_thresholds(self) -> int:
        return len(self.thresholds)

    @deprecated("BOILERPLATE: Use self.thresholds[sequence_number] instead")
    def get_threshold(self, sequence_number: int) -> RelaySetting:
        """
        Get the threshold[:class:`RelaySetting`] for this :class:`ProtectionRelayFunction` by its `sequence_number`.

        :param sequence_number: The sequence_number of the threshold :class:`RelaySetting` for this :class:`ProtectionRelayFunction`.
        :returns: The threshold[:class:`RelaySetting`]  for this :class:`ProtectionRelayFunction` with sequence number `sequence_number`
        :raises IndexError: if no :class:`RelaySetting` was found with sequence_number `sequence_number`.
        """
        return self.thresholds[sequence_number]

    @deprecated("BOILERPLATE: Use thresholds.remove(threshold) instead")
    def remove_threshold(self, threshold: RelaySetting) -> ProtectionRelayFunction:
        """
        Removes a threshold[:class:`RelaySetting`] from this :class:`ProtectionRelayFunction`.

        :param threshold: The threshold[:class:`RelaySetting`] to disassociate from this :class:`ProtectionRelayFunction`.
        :returns: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self.thresholds.remove(threshold)
        return self

    def remove_threshold_at(self, sequence_number: int) -> RelaySetting:
        """
        Removes a threshold[:class:`RelaySetting`] from this :class:`ProtectionRelayFunction`.

        :param sequence_number: The sequence_number of the threshold[:class:`RelaySetting`] to disassociate from this :class:`ProtectionRelayFunction`.
        :returns: A reference to removed threshold[:class:`RelaySetting`].
        :raises IndexError: If `sequence_number` is out of range.
        """
        threshold = self.get_threshold(sequence_number)
        self.thresholds.remove(threshold)
        return threshold

    @deprecated("BOILERPLATE: Use thresholds.clear() instead")
    def clear_thresholds(self) -> ProtectionRelayFunction:
        return self.thresholds.clear()

    def for_each_time_limit(self, action: Callable[[int, float], None]):
        """
        Call the `action` on each time limit in the `time_limits` collection

        :param action: An action to apply to each time limit in the `time_limits` collection, taking the index of the limit, and the limit itself.
        """
        for index, limit in enumerate(self.time_limits):
            action(index, limit)

    @custom_add(time_limits)
    def add_time_limit(self, time_limit: float, index: int = None) -> ProtectionRelayFunction:
        """
        Add a time limit.

        :param time_limit: The time limit in seconds to add to this :class:`ProtectionRelayFunction`.
        :param index: The index into the list to add the time limit at. Defaults to the end of the list.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        if index is None:
            index = self.num_time_limits()
        require(0 <= index <= self.num_time_limits(),
                lambda: f"Unable to add float to {str(self)}. Sequence number {index} "
                        f"is invalid. Expected a value between 0 and {self.num_time_limits()}. Make sure you are "
                        f"adding the items in order and there are no gaps in the numbering.")
        self.time_limits.insert_raw(index, time_limit)
        return self

    @deprecated("BOILERPLATE: Use len(time_limits) instead")
    def num_time_limits(self) -> int:
        return len(self.time_limits)

    @deprecated("BOILERPLATE: Use self.time_limits[index] instead")
    def get_time_limit(self, index: int):
        """
        Get the time limit for this :class:`ProtectionRelayFunction` by its `index`.

        :param index: The index of the desired time limit.
        :returns: The time limit with the specified `index` if it exists.
        :raises IndexError: if no time limit was found with provided index.
        """
        return self.time_limits[index]

    @deprecated("BOILERPLATE: Use time_limits.remove() instead")
    def remove_time_limit(self, time_limit: float) -> ProtectionRelayFunction:
        """
        Remove a time limit from the list.

        :param time_limit: The time limit to remove.
        :returns: A reference to this `ProtectionRelayFunction` to allow fluent use.
        """
        self.time_limits.remove(time_limit)
        return self

    def remove_time_limit_at(self, index: int) -> float:
        """
        Remove a time limit from the list.

        :param index: The time limit to remove.
        :returns: The time limit that was removed, or `None` if no time limit was present at `index`.
        :raises IndexError: If `sequence_number` is out of range.
        """
        if self.time_limits:
            limit = self.time_limits.pop(index)
            return limit
        raise IndexError(index)

    @deprecated("BOILERPLATE: Use time_limits.clear() instead")
    def clear_time_limits(self) -> ProtectionRelayFunction:
        return self.time_limits.clear()

    @deprecated("BOILERPLATE: Use sensors.get_by_mrid(mrid) instead")
    def get_sensor(self, mrid: str) -> Sensor:
        return self.sensors.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use sensors.append(sensor) instead")
    def add_sensor(self, sensor: Sensor) -> ProtectionRelayFunction:
        self.sensors.append(sensor)
        return self

    @deprecated("BOILERPLATE: Use len(sensors) instead")
    def num_sensors(self) -> int:
        return len(self.sensors)

    @deprecated("Boilerplate: Use sensors.remove(sensor) instead")
    def remove_sensor(self, sensor: Sensor | None) -> ProtectionRelayFunction:
        self.sensors.remove(sensor)
        return self

    @deprecated("BOILERPLATE: Use sensors.clear() instead")
    def clear_sensors(self) -> ProtectionRelayFunction:
        return self.sensors.clear()

    @deprecated("BOILERPLATE: Use protected_switches.get_by_mrid(mrid) instead")
    def get_protected_switch(self, mrid: str) -> ProtectedSwitch:
        return self.protected_switches.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use protected_switches.append(protected_switch) instead")
    def add_protected_switch(self, protected_switch: ProtectedSwitch) -> ProtectionRelayFunction:
        self.protected_switches.append(protected_switch)
        return self

    @deprecated("BOILERPLATE: Use len(protected_switches) instead")
    def num_protected_switches(self) -> int:
        return len(self.protected_switches)

    @deprecated("Boilerplate: Use protected_switches.remove(protected_switch) instead")
    def remove_protected_switch(self, protected_switch: ProtectedSwitch | None) -> ProtectionRelayFunction:
        self.protected_switches.remove(protected_switch)
        return self

    @deprecated("BOILERPLATE: Use protected_switches.clear() instead")
    def clear_protected_switches(self) -> ProtectionRelayFunction:
        return self.protected_switches.clear()

    @deprecated("BOILERPLATE: Use schemes.get_by_mrid(mrid) instead")
    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        return self.schemes.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use schemes.append(scheme) instead")
    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelayFunction:
        self.schemes.append(scheme)
        return self

    @deprecated("BOILERPLATE: Use len(schemes) instead")
    def num_schemes(self) -> int:
        return len(self.schemes)

    @deprecated("Boilerplate: Use schemes.remove(scheme) instead")
    def remove_scheme(self, scheme: ProtectionRelayScheme | None) -> ProtectionRelayFunction:
        self.schemes.remove(scheme)
        return self

    @deprecated("BOILERPLATE: Use schemes.clear() instead")
    def clear_schemes(self) -> ProtectionRelayFunction:
        self.schemes.clear()
        return self

