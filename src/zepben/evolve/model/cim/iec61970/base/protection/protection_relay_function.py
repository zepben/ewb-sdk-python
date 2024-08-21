#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, List, Generator, Iterable, Callable

from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.relay_info import RelayInfo
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
from zepben.evolve.model.cim.iec61970.base.protection.relay_setting import RelaySetting
from zepben.evolve.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.evolve.model.cim.iec61970.infiec61970.protection.power_direction_kind import PowerDirectionKind
from zepben.evolve.model.cim.iec61970.infiec61970.protection.protection_kind import ProtectionKind
from zepben.evolve.util import require, nlen, ngen, safe_remove, get_by_mrid
__all__ = ["ProtectionRelayFunction"]


class ProtectionRelayFunction(PowerSystemResource):
    """A function that a relay implements to protect equipment."""

    model: Optional[str] = None
    """The protection equipment type name(manufacturer information)."""

    reclosing: Optional[bool] = None
    """True if the protection equipment is reclosing or False otherwise."""

    relay_delay_time: Optional[float] = None
    """The time delay from detection of abnormal conditions to relay operation in seconds."""

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """The kind of protection being provided by this ProtectionRelayFunction."""

    directable: Optional[bool] = None
    """Whether this ProtectionRelayFunction responds to power flow in a given direction."""

    power_direction: PowerDirectionKind = PowerDirectionKind.UNKNOWN_DIRECTION
    """The flow of the power direction used by this ProtectionRelayFunction."""

    _sensors: Optional[List[Sensor]] = None

    _protected_switches: Optional[List[ProtectedSwitch]] = None

    _schemes: Optional[List[ProtectionRelayScheme]] = None

    _time_limits: Optional[List[float]] = None

    _thresholds: Optional[List[RelaySetting]] = None

    def __init__(self,
                 sensors: Iterable[Sensor] = None,
                 protected_switches: Iterable[ProtectedSwitch] = None,
                 schemes: Iterable[ProtectionRelayScheme] = None,
                 time_limits: Iterable[float] = None,
                 thresholds: Iterable[RelaySetting] = None,
                 relay_info: RelayInfo = None, **kwargs):
        super(ProtectionRelayFunction, self).__init__(**kwargs)

        if sensors is not None:
            for sensor in sensors:
                self.add_sensor(sensor)
        if protected_switches is not None:
            for protected_switch in protected_switches:
                self.add_protected_switch(protected_switch)
        if schemes is not None:
            for scheme in schemes:
                self.add_scheme(scheme)
        if time_limits is not None:
            for time_limit in time_limits:
                self.add_time_limit(time_limit)
        if thresholds is not None:
            for threshold in thresholds:
                self.add_threshold(threshold)
        if relay_info is not None:
            self.relay_info = relay_info

    @property
    def relay_info(self):
        """Datasheet information for this CurrentRelay"""
        return self.asset_info

    @relay_info.setter
    def relay_info(self, relay_info: Optional[RelayInfo]):
        self.asset_info = relay_info

    @property
    def thresholds(self) -> Generator[RelaySetting, None, None]:
        """
        Yields all the thresholds[:class:`RelaySettings<RelaySetting>`] for this :class:`ProtectionRelayFunction`. The order of thresholds corresponds to the order of time limits.

        :return: A generator that iterates over all thresholds[:class:`RelaySettings<RelaySetting>`] for this relay function.
        """
        return ngen(self._thresholds)

    def for_each_threshold(self, action: Callable[[int, RelaySetting], None]):
        """
        Call the `action` on each :class:`RelaySetting` in the `thresholds` collection

        :param action: An action to apply to each :class:`RelaySetting` in the `thresholds` collection, taking the index of the threshold, and the threshold itself.
        """
        for index, point in enumerate(self.thresholds):
            action(index, point)

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
        self._thresholds = list() if self._thresholds is None else self._thresholds
        self._thresholds.insert(sequence_number, threshold)
        return self

    def num_thresholds(self) -> int:
        """
        Get the number of thresholds for this :class:`ProtectionRelayFunction`.

        :return: The number of thresholds for this `ProtectionRelayFunction`.
        """
        return nlen(self._thresholds)

    def get_threshold(self, sequence_number: int) -> RelaySetting:
        """
        Get the threshold[:class:`RelaySetting`] for this :class:`ProtectionRelayFunction` by its `sequence_number`.

        :param sequence_number: The sequence_number of the threshold :class:`RelaySetting` for this :class:`ProtectionRelayFunction`.
        :returns: The threshold[:class:`RelaySetting`]  for this :class:`ProtectionRelayFunction` with sequence number `sequence_number`
        :raises IndexError: if no :class:`RelaySetting` was found with sequence_number `sequence_number`.
        """
        if self._thresholds is not None:
            return self._thresholds[sequence_number]
        else:
            raise IndexError(sequence_number)

    def remove_threshold(self, threshold: RelaySetting) -> ProtectionRelayFunction:
        """
        Removes a threshold[:class:`RelaySetting`] from this :class:`ProtectionRelayFunction`.

        :param threshold: The threshold[:class:`RelaySetting`] to disassociate from this :class:`ProtectionRelayFunction`.
        :returns: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._thresholds = safe_remove(self._thresholds, threshold)
        return self

    def remove_threshold_at(self, sequence_number: int) -> RelaySetting:
        """
        Removes a threshold[:class:`RelaySetting`] from this :class:`ProtectionRelayFunction`.

        :param sequence_number: The sequence_number of the threshold[:class:`RelaySetting`] to disassociate from this :class:`ProtectionRelayFunction`.
        :returns: A reference to removed threshold[:class:`RelaySetting`].
        :raises IndexError: If `sequence_number` is out of range.
        """
        threshold = self.get_threshold(sequence_number)
        self._thresholds = safe_remove(self._thresholds, threshold)
        return threshold

    def clear_thresholds(self) -> ProtectionRelayFunction:
        """
        Removes all thresholds from this :class:`ProtectionRelayFunction`.

        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._thresholds = None
        return self

    @property
    def time_limits(self) -> Generator[float, None, None]:
        """
        Yields all the time limits (in seconds) for this relay function. Order of entries corresponds to the order of entries in thresholds.

        :return: A generator that iterates over all time limits for this relay function.
        """
        return ngen(self._time_limits)

    def for_each_time_limit(self, action: Callable[[int, float], None]):
        """
        Call the `action` on each time limit in the `time_limits` collection

        :param action: An action to apply to each time limit in the `time_limits` collection, taking the index of the limit, and the limit itself.
        """
        for index, limit in enumerate(self.time_limits):
            action(index, limit)

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
        self._time_limits = list() if self._time_limits is None else self._time_limits
        self._time_limits.insert(index, time_limit)
        return self

    def num_time_limits(self) -> int:
        return nlen(self._time_limits)

    def get_time_limit(self, index: int):
        """
        Get the time limit for this :class:`ProtectionRelayFunction` by its `index`.

        :param index: The index of the desired time limit.
        :returns: The time limit with the specified `index` if it exists.
        :raises IndexError: if no time limit was found with provided index.
        """
        if self._time_limits is not None:
            return self._time_limits[index]
        else:
            raise IndexError(index)

    def remove_time_limit(self, time_limit: float) -> ProtectionRelayFunction:
        """
        Remove a time limit from the list.

        :param time_limit: The time limit to remove.
        :returns: A reference to this `ProtectionRelayFunction` to allow fluent use.
        """
        self._time_limits = safe_remove(self._time_limits, time_limit)
        return self

    def remove_time_limit_at(self, index: int) -> float:
        """
        Remove a time limit from the list.

        :param index: The time limit to remove.
        :returns: The time limit that was removed, or `None` if no time limit was present at `index`.
        :raises IndexError: If `sequence_number` is out of range.
        """
        if self._time_limits:
            limit = self._time_limits.pop(index)
            self._time_limits = self._time_limits if self._time_limits else None
            return limit
        raise IndexError(index)

    def clear_time_limits(self) -> ProtectionRelayFunction:
        """
        Removes all time limits from this :class:`ProtectionRelayFunction`.

        :returns: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._time_limits = None
        return self

    @property
    def sensors(self) -> Generator[Sensor, None, None]:
        """
        Yields all the :class:`Sensors<Sensor>` for this relay function.

        :return: A generator that iterates over all :class:`Sensors<Sensor>`  for this relay function.
        """
        return ngen(self._sensors)

    def get_sensor(self, mrid: str) -> Sensor:
        """
        Get a sensor :class:`Sensor` for this :class:`ProtectionRelayFunction` by its mrid.

        :param mrid: The mrid of the desired :class:`Sensor`.
        :returns: The :class:`Sensor` with the specified mrid if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._sensors, mrid)

    def add_sensor(self, sensor: Sensor) -> ProtectionRelayFunction:
        """
        Associate this :class:`ProtectionRelayFunction` with a :class:`Sensor`.

        :param sensor: The :class:`Sensor` to associate with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        if self._validate_reference(sensor, self.get_sensor, "A Sensor"):
            return self
        self._sensors = list() if self._sensors is None else self._sensors
        self._sensors.append(sensor)
        return self

    def num_sensors(self) -> int:
        """
        Get the number of :class:`Sensors<Sensor>` for this :class:`ProtectionRelayFunction`.

        :return: The number of :class:`Sensors<Sensor>` for this :class:`ProtectionRelayFunction`.
        """
        return nlen(self._sensors)

    def remove_sensor(self, sensor: Optional[Sensor]) -> ProtectionRelayFunction:
        """
        Disassociate this :class:`ProtectionRelayFunction` from a :class:`Sensor`.

        :param sensor: The :class:`Sensor` to disassociate from this :class:`ProtectionRelayFunction`.
        :raises ValueError: If sensor was not associated with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._sensors = safe_remove(self._sensors, sensor)
        return self

    def clear_sensors(self) -> ProtectionRelayFunction:
        """
        Disassociate all :class:`Sensors<Sensor>` from this :class:`ProtectionRelayFunction`.

        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._sensors = None
        return self

    @property
    def protected_switches(self) -> Generator[ProtectedSwitch, None, None]:
        """
        Yields the :class:`ProtectedSwitches<ProtectedSwitch>` operated by this :class:`ProtectionRelayFunction`.

        :return: A generator that iterates over all :class:`ProtectedSwitches<ProtectedSwitch>` operated by this :class:`ProtectionRelayFunction`.
        """
        return ngen(self._protected_switches)

    def get_protected_switch(self, mrid: str) -> ProtectedSwitch:
        """
        Get a :class:`ProtectedSwitch` operated by this :class:`ProtectionRelayFunction` by its mrid.

        :param mrid: The mrid of the desired :class:`ProtectedSwitch`.
        :returns: The :class:`ProtectedSwitch` with the specified mrid if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._protected_switches, mrid)

    def add_protected_switch(self, protected_switch: ProtectedSwitch) -> ProtectionRelayFunction:
        """
        Associate this :class:`ProtectionRelayFunction` with a :class:`ProtectedSwitch` it operates.

        :param protected_switch: The :class:`ProtectedSwitch` to associate with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        if self._validate_reference(protected_switch, self.get_protected_switch, "A ProtectedSwitch"):
            return self
        self._protected_switches = list() if self._protected_switches is None else self._protected_switches
        self._protected_switches.append(protected_switch)
        return self

    def num_protected_switches(self) -> int:
        """
        Get the number of :class:`ProtectedSwitches<ProtectedSwitch>` operated by this :class:`ProtectionRelayFunction`.

        :return: The number of :class:`ProtectedSwitches<ProtectedSwitch>` operated by this :class:`ProtectionRelayFunction`.
        """
        return nlen(self._protected_switches)

    def remove_protected_switch(self, protected_switch: Optional[ProtectedSwitch]) -> ProtectionRelayFunction:
        """
        Disassociate this :class:`ProtectionRelayFunction` from a :class:`ProtectedSwitch`.

        :param protected_switch: The :class:`ProtectedSwitch` to disassociate from this :class:`ProtectionRelayFunction`.
        :raises ValueError: If protected_switch was not associated with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._sensors = safe_remove(self._protected_switches, protected_switch)
        return self

    def clear_protected_switches(self) -> ProtectionRelayFunction:
        """
        Disassociate all :class:`ProtectedSwitches<ProtectedSwitch>` from this :class:`ProtectionRelayFunction`.

        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._protected_switches = None
        return self

    @property
    def schemes(self) -> Generator[ProtectionRelayScheme, None, None]:
        """
        Yields the :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` this :class:`ProtectionRelayFunction` operates under.

        :return: A generator that iterates over all :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` this :class:`ProtectionRelayFunction` operates under.
        """
        return ngen(self._schemes)

    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        """
        Get a :class:`ProtectionRelayScheme` this :class:`ProtectionRelayFunction` operates under by its mRID.

        :param mrid: The mRID of the desired :class:`ProtectionRelayScheme`.
        :returns: The :class:`ProtectionRelayScheme` with the specified mrid if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._schemes, mrid)

    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelayFunction:
        """
        Associate this :class:`ProtectionRelayFunction` with a :class:`ProtectionRelayScheme` it operates under.

        :param scheme: The :class:`ProtectionRelayScheme` to associate with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        if self._validate_reference(scheme, self.get_scheme, "A ProtectionRelayScheme"):
            return self
        self._schemes = list() if self._schemes is None else self._schemes
        self._schemes.append(scheme)
        return self

    def num_schemes(self) -> int:
        """
        Get the number of :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` this :class:`ProtectionRelayFunction` operates under.

        :return: The number of:class:`ProtectionRelaySchemes<ProtectionRelayScheme>` operated by this :class:`ProtectionRelayFunction`.
        """
        return nlen(self._schemes)

    def remove_scheme(self, scheme: Optional[ProtectionRelayScheme]) -> ProtectionRelayFunction:
        """
        Disassociate this :class:`ProtectionRelayFunction` from a :class:`ProtectionRelayScheme`.

        :param scheme: The :class:`ProtectionRelayScheme` to disassociate from this :class:`ProtectionRelayFunction`.
        :raises ValueError: If scheme was not associated with this :class:`ProtectionRelayFunction`.
        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._schemes = safe_remove(self._schemes, scheme)
        return self

    def clear_schemes(self) -> ProtectionRelayFunction:
        """
        Disassociate all :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` from this :class:`ProtectionRelayFunction`.

        :return: A reference to this :class:`ProtectionRelayFunction` for fluent use.
        """
        self._schemes = None
        return self
