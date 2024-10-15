#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import PowerElectronicsUnit

from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.util import ngen, nlen, get_by_mrid, safe_remove, require

__all__ = ["PowerElectronicsConnection", "PowerElectronicsConnectionPhase"]


class PowerElectronicsConnectionPhase(PowerSystemResource):
    """A single phase of a power electronics connection."""

    power_electronics_connection: Optional[PowerElectronicsConnection] = None
    """The power electronics connection to which the phase belongs."""

    p: Optional[float] = None
    """Active power injection. Load sign convention is used, i.e. positive sign means flow into the equipment from the network."""

    phase: SinglePhaseKind = SinglePhaseKind.X
    """
    Phase of this energy producer component. If the energy producer is wye connected, the connection is from the indicated phase to the central
    ground or neutral point. If the energy producer is delta connected, the phase indicates an energy producer connected from the indicated phase to the next
    logical non-neutral phase.
    """

    q: Optional[float] = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow into the equipment from the network."""


class PowerElectronicsConnection(RegulatingCondEq):
    """
    A connection to the AC network for energy production or consumption that uses power electronics rather than rotating machines.
    """

    max_i_fault: Optional[int] = None
    """Maximum fault current this device will contribute, in per-unit of rated current, before the converter protection will trip or bypass."""

    p: Optional[float] = None
    """Active power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    q: Optional[float] = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    max_q: Optional[float] = None
    """Maximum reactive power limit. This is the maximum (nameplate) limit for the unit."""

    min_q: Optional[float] = None
    """Minimum reactive power limit for the unit. This is the minimum (nameplate) limit for the unit."""

    rated_s: Optional[int] = None
    """Nameplate apparent power rating for the unit. The attribute shall have a positive value."""

    rated_u: Optional[int] = None
    """Rated voltage (nameplate data, Ur in IEC 60909-0). It is primarily used for short circuit data exchange according to IEC 60909. 
    The attribute shall be a positive value."""

    inverter_standard: Optional[str] = None
    """The standard this inverter follows, such as AS4777.2:2020"""

    sustain_op_overvolt_limit: Optional[int] = None
    """Indicates the sustained operation overvoltage limit in volts, when the average voltage for a 10-minute period exceeds the V¬nom-max."""

    stop_at_over_freq: Optional[float] = None
    """Over frequency (stop) in Hz. Permitted range is between 51 and 52 (inclusive)"""

    stop_at_under_freq: Optional[float] = None
    """Under frequency (stop) in Hz Permitted range is between 47 and 49 (inclusive)"""

    inv_volt_watt_resp_mode: Optional[bool] = None
    """
    Volt-Watt response mode allows an inverter to reduce is real power output depending on the measured voltage.
    This mode is further described in AS4777.2:2015, section 6.3.2.2. True implies the mode is enabled.
    """

    _inv_watt_resp_v1: Optional[int] = None
    """Set point 1 in volts for inverter Volt-Watt response mode. Permitted range is between 200 and 300 (inclusive)."""

    _inv_watt_resp_v2: Optional[int] = None
    """Set point 2 in volts for inverter Volt-Watt response mode. Permitted range is between 216 and 230 (inclusive)."""

    _inv_watt_resp_v3: Optional[int] = None
    """Set point 3 in volts for inverter Volt-Watt response mode. Permitted range is between 235 and 255 (inclusive)."""

    _inv_watt_resp_v4: Optional[int] = None
    """Set point 4 in volts for inverter Volt-Watt response mode. Permitted range is between 244 and 265 (inclusive)."""

    _inv_watt_resp_p_at_v1: Optional[float] = None
    """Power output set point 1 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    _inv_watt_resp_p_at_v2: Optional[float] = None
    """Power output set point 2 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    _inv_watt_resp_p_at_v3: Optional[float] = None
    """Power output set point 3 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    _inv_watt_resp_p_at_v4: Optional[float] = None
    """Power output set point 4 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 0.2 (inclusive)."""

    inv_volt_var_resp_mode: Optional[bool] = None
    """
    Volt-VAr response mode allows an inverter to consume (sink) or produce (source) reactive power depending on the measured voltage.
    This mode is further described in AS4777.2:2015, section 6.3.2.3. True implies the mode is enabled.
    """

    _inv_var_resp_v1: Optional[int] = None
    """Set point 1 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    _inv_var_resp_v2: Optional[int] = None
    """Set point 2 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    _inv_var_resp_v3: Optional[int] = None
    """Set point 3 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    _inv_var_resp_v4: Optional[int] = None
    """Set point 4 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    _inv_var_resp_q_at_v1: Optional[float] = None
    """Power output set point 1 as a percentage of rated output for inverter Volt-VAr response mode. Permitted range is between 0 and 0.6 (inclusive)."""

    _inv_var_resp_q_at_v2: Optional[float] = None
    """
    Power output set point 2 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
    """

    _inv_var_resp_q_at_v3: Optional[float] = None
    """
    Power output set point 3 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
    """

    _inv_var_resp_q_at_v4: Optional[float] = None
    """
    Power output set point 4 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -0.6 and 0 (inclusive) with a negative number referring to a sink.
    """

    inv_reactive_power_mode: Optional[bool] = None
    """If true, enables Static Reactive Power mode on the inverter. Note: It must be false if invVoltVarRespMode or InvVoltWattRespMode is true."""

    inv_fix_reactive_power: Optional[float] = None
    """
    Static Reactive Power, specified in a percentage output of the system.
    Permitted range is between -1.0 and 1.0 (inclusive), with a negative sign referring to “sink”.
    """

    _power_electronics_units: Optional[List[PowerElectronicsUnit]] = None
    """An AC network connection may have several power electronics units connecting through it."""

    _power_electronics_connection_phases: Optional[List[PowerElectronicsConnectionPhase]] = None
    """The individual units models for the power electronics connection."""

    def __init__(self, power_electronics_units: List[PowerElectronicsUnit] = None,
                 power_electronics_connection_phases: List[PowerElectronicsConnectionPhase] = None,
                 inv_watt_resp_v1=None,
                 inv_watt_resp_v2=None,
                 inv_watt_resp_v3=None,
                 inv_watt_resp_v4=None,
                 inv_watt_resp_p_at_v1=None,
                 inv_watt_resp_p_at_v2=None,
                 inv_watt_resp_p_at_v3=None,
                 inv_watt_resp_p_at_v4=None,
                 inv_var_resp_v1=None,
                 inv_var_resp_v2=None,
                 inv_var_resp_v3=None,
                 inv_var_resp_v4=None,
                 inv_var_resp_q_at_v1=None,
                 inv_var_resp_q_at_v2=None,
                 inv_var_resp_q_at_v3=None,
                 inv_var_resp_q_at_v4=None,
                 **kwargs):
        super(PowerElectronicsConnection, self).__init__(**kwargs)
        if power_electronics_units:
            for unit in power_electronics_units:
                self.add_unit(unit)

        if power_electronics_connection_phases:
            for phase in power_electronics_connection_phases:
                self.add_phase(phase)

        if inv_watt_resp_v1 is not None:
            self.inv_watt_resp_v1 = inv_watt_resp_v1

        if inv_watt_resp_v2 is not None:
            self.inv_watt_resp_v2 = inv_watt_resp_v2

        if inv_watt_resp_v3 is not None:
            self.inv_watt_resp_v3 = inv_watt_resp_v3

        if inv_watt_resp_v4 is not None:
            self.inv_watt_resp_v4 = inv_watt_resp_v4

        if inv_watt_resp_p_at_v1 is not None:
            self.inv_watt_resp_p_at_v1 = inv_watt_resp_p_at_v1

        if inv_watt_resp_p_at_v2 is not None:
            self.inv_watt_resp_p_at_v2 = inv_watt_resp_p_at_v2

        if inv_watt_resp_p_at_v3 is not None:
            self.inv_watt_resp_p_at_v3 = inv_watt_resp_p_at_v3

        if inv_watt_resp_p_at_v4 is not None:
            self.inv_watt_resp_p_at_v4 = inv_watt_resp_p_at_v4

        if inv_var_resp_v1 is not None:
            self.inv_var_resp_v1 = inv_var_resp_v1

        if inv_var_resp_v2 is not None:
            self.inv_var_resp_v2 = inv_var_resp_v2

        if inv_var_resp_v3 is not None:
            self.inv_var_resp_v3 = inv_var_resp_v3

        if inv_var_resp_v4 is not None:
            self.inv_var_resp_v4 = inv_var_resp_v4

        if inv_var_resp_q_at_v1 is not None:
            self.inv_var_resp_q_at_v1 = inv_var_resp_q_at_v1

        if inv_var_resp_q_at_v2 is not None:
            self.inv_var_resp_q_at_v2 = inv_var_resp_q_at_v2

        if inv_var_resp_q_at_v3 is not None:
            self.inv_var_resp_q_at_v3 = inv_var_resp_q_at_v3

        if inv_var_resp_q_at_v4 is not None:
            self.inv_var_resp_q_at_v4 = inv_var_resp_q_at_v4

    @property
    def inv_watt_resp_v1(self):
        """
        Set point 1 in volts for inverter Volt-Watt response mode. Permitted range is between 200 and 300 (inclusive).
        """
        return self._inv_watt_resp_v1

    @inv_watt_resp_v1.setter
    def inv_watt_resp_v1(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_watt_resp_v1 [{value}] must be between 200 and 300.")
        self._inv_watt_resp_v1 = value

    @property
    def inv_watt_resp_v2(self):
        """
        Set point 2 in volts for inverter Volt-Watt response mode. Permitted range is between 216 and 230 (inclusive).
        """
        return self._inv_watt_resp_v2

    @inv_watt_resp_v2.setter
    def inv_watt_resp_v2(self, value):
        require(value is None or 216 <= value <= 230, lambda: f"inv_watt_resp_v2 [{value}] must be between 216 and 230.")
        self._inv_watt_resp_v2 = value

    @property
    def inv_watt_resp_v3(self):
        """
        Set point 3 in volts for inverter Volt-Watt response mode. Permitted range is between 235 and 255 (inclusive).
        """
        return self._inv_watt_resp_v3

    @inv_watt_resp_v3.setter
    def inv_watt_resp_v3(self, value):
        require(value is None or 235 <= value <= 255, lambda: f"inv_watt_resp_v3 [{value}] must be between 235 and 255.")
        self._inv_watt_resp_v3 = value

    @property
    def inv_watt_resp_v4(self):
        """
        Set point 4 in volts for inverter Volt-Watt response mode. Permitted range is between 244 and 265 (inclusive).
        """
        return self._inv_watt_resp_v4

    @inv_watt_resp_v4.setter
    def inv_watt_resp_v4(self, value):
        require(value is None or 244 <= value <= 265, lambda: f"inv_watt_resp_v4 [{value}] must be between 244 and 265.")
        self._inv_watt_resp_v4 = value

    @property
    def inv_watt_resp_p_at_v1(self):
        """
        Power output set point 1 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive).
        """
        return self._inv_watt_resp_p_at_v1

    @inv_watt_resp_p_at_v1.setter
    def inv_watt_resp_p_at_v1(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v1 [{value}] must be between 0.0 and 1.0.")
        self._inv_watt_resp_p_at_v1 = value

    @property
    def inv_watt_resp_p_at_v2(self):
        """
        Power output set point 2 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive).
        """
        return self._inv_watt_resp_p_at_v2

    @inv_watt_resp_p_at_v2.setter
    def inv_watt_resp_p_at_v2(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v2 [{value}] must be between 0.0 and 1.0.")
        self._inv_watt_resp_p_at_v2 = value

    @property
    def inv_watt_resp_p_at_v3(self):
        """
        Power output set point 3 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive).
        """
        return self._inv_watt_resp_p_at_v3

    @inv_watt_resp_p_at_v3.setter
    def inv_watt_resp_p_at_v3(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v3 [{value}] must be between 0.0 and 1.0.")
        self._inv_watt_resp_p_at_v3 = value

    @property
    def inv_watt_resp_p_at_v4(self):
        """
        Power output set point 4 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 0.2 (inclusive).
        """
        return self._inv_watt_resp_p_at_v4

    @inv_watt_resp_p_at_v4.setter
    def inv_watt_resp_p_at_v4(self, value):
        require(value is None or 0.0 <= value <= 0.2, lambda: f"inv_watt_resp_p_at_v4 [{value}] must be between 0.0 and 0.2.")
        self._inv_watt_resp_p_at_v4 = value

    @property
    def inv_var_resp_v1(self):
        """
        Set point 1 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive).
        """
        return self._inv_var_resp_v1

    @inv_var_resp_v1.setter
    def inv_var_resp_v1(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v1 [{value}] must be between 200 and 300.")
        self._inv_var_resp_v1 = value

    @property
    def inv_var_resp_v2(self):
        """
        Set point 2 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive).
        """
        return self._inv_var_resp_v2

    @inv_var_resp_v2.setter
    def inv_var_resp_v2(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v2 [{value}] must be between 200 and 300.")
        self._inv_var_resp_v2 = value

    @property
    def inv_var_resp_v3(self):
        """
        Set point 3 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive).
        """
        return self._inv_var_resp_v3

    @inv_var_resp_v3.setter
    def inv_var_resp_v3(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v3 [{value}] must be between 200 and 300.")
        self._inv_var_resp_v3 = value

    @property
    def inv_var_resp_v4(self):
        """
        Set point 4 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive).
        """
        return self._inv_var_resp_v4

    @inv_var_resp_v4.setter
    def inv_var_resp_v4(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v4 [{value}] must be between 200 and 300.")
        self._inv_var_resp_v4 = value

    @property
    def inv_var_resp_q_at_v1(self):
        """
        Power output set point 1 as a percentage of rated output for inverter Volt-VAr response mode. Permitted range is between 0 and 0.6 (inclusive).
        """
        return self._inv_var_resp_q_at_v1

    @inv_var_resp_q_at_v1.setter
    def inv_var_resp_q_at_v1(self, value):
        require(value is None or 0.0 <= value <= 0.6, lambda: f"inv_var_resp_q_at_v1 [{value}] must be between 0.0 and 0.6.")
        self._inv_var_resp_q_at_v1 = value

    @property
    def inv_var_resp_q_at_v2(self):
        """
        Power output set point 2 as a percentage of rated output for inverter Volt-VAr response mode. \
        Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
        """
        return self._inv_var_resp_q_at_v2

    @inv_var_resp_q_at_v2.setter
    def inv_var_resp_q_at_v2(self, value):
        require(value is None or -1.0 <= value <= 1.0, lambda: f"inv_var_resp_q_at_v2 [{value}] must be between -1.0 and 1.0.")
        self._inv_var_resp_q_at_v2 = value

    @property
    def inv_var_resp_q_at_v3(self):
        """
        Power output set point 3 as a percentage of rated output for inverter Volt-VAr response mode. \
        Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
        """
        return self._inv_var_resp_q_at_v3

    @inv_var_resp_q_at_v3.setter
    def inv_var_resp_q_at_v3(self, value):
        require(value is None or -1.0 <= value <= 1.0, lambda: f"inv_var_resp_q_at_v3 [{value}] must be between -1.0 and 1.0.")
        self._inv_var_resp_q_at_v3 = value

    @property
    def inv_var_resp_q_at_v4(self):
        """
        Power output set point 4 as a percentage of rated output for inverter Volt-VAr response mode. \
        Permitted range is between -0.6 and 0 (inclusive) with a negative number referring to a sink.
        """
        return self._inv_var_resp_q_at_v4

    @inv_var_resp_q_at_v4.setter
    def inv_var_resp_q_at_v4(self, value):
        require(value is None or -0.6 <= value <= 0.0, lambda: f"inv_var_resp_q_at_v4 [{value}] must be between -0.6 and 0.0.")
        self._inv_var_resp_q_at_v4 = value

    @property
    def units(self) -> Generator[PowerElectronicsUnit, None, None]:
        """
        The `PowerElectronicsUnit`s for this `PowerElectronicsConnection`.
        """
        return ngen(self._power_electronics_units)

    @property
    def phases(self) -> Generator[PowerElectronicsConnectionPhase, None, None]:
        """
        The `PowerElectronicsConnectionPhase`s for this `PowerElectronicsConnection`.
        """
        return ngen(self._power_electronics_connection_phases)

    def num_units(self):
        """Return the number of `PowerElectronicsUnit`s associated with this `PowerElectronicsConnection`"""
        return nlen(self._power_electronics_units)

    def get_unit(self, mrid: str) -> PowerElectronicsUnit:
        """
        Get the `PowerElectronicsUnit` for this
        `PowerElectronicsConnection` identified by `mrid`

        `mrid` the mRID of the required `PowerElectronicsUnit`
        Returns The `PowerElectronicsUnit` with the specified `mrid`
        if it exists

        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_electronics_units, mrid)

    def add_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        """
        Associate an `PowerElectronicsUnit` with this
        `PowerElectronicsConnection`

        `unit` the `PowerElectronicsUnit` to associate with this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if another `PowerElectronicsUnit` with the same `mrid` already exists for this `PowerElectronicsConnection`.
        """
        if self._validate_reference(unit, self.get_unit, "A PowerElectronicsUnit"):
            return self
        self._power_electronics_units = list() if self._power_electronics_units is None else self._power_electronics_units
        self._power_electronics_units.append(unit)
        return self

    def remove_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        """
        Disassociate `unit` from this `PowerElectronicsConnection`

        `unit` the `PowerElectronicsUnit` to disassociate from this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if `unit` was not associated with this `PowerElectronicsConnection`.
        """
        self._power_electronics_units = safe_remove(self._power_electronics_units, unit)
        return self

    def clear_units(self) -> PowerElectronicsConnection:
        """
        Clear all units.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        """
        self._power_electronics_units = None
        return self

    def num_phases(self):
        """Return the number of `PowerElectronicsConnectionPhase`s associated with this `PowerElectronicsConnection`"""
        return nlen(self._power_electronics_connection_phases)

    def get_phase(self, mrid: str) -> PowerElectronicsConnectionPhase:
        """
        Get the `PowerElectronicsConnectionPhase` for this `PowerElectronicsConnection` identified by `mrid`

        `mrid` the mRID of the required `PowerElectronicsConnectionPhase`
        Returns The `PowerElectronicsConnectionPhase` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._power_electronics_connection_phases, mrid)

    def add_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        """
        Associate a `PowerElectronicsConnectionPhase` with this `PowerElectronicsConnection`

        `phase` the `PowerElectronicsConnectionPhase` to associate with this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if another `PowerElectronicsConnectionPhase` with the same `mrid` already exists for this `PowerElectronicsConnection`.
        """
        if self._validate_reference(phase, self.get_phase, "A PowerElectronicsConnectionPhase"):
            return self
        self._power_electronics_connection_phases = list() if self._power_electronics_connection_phases is None else self._power_electronics_connection_phases
        self._power_electronics_connection_phases.append(phase)
        return self

    def remove_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        """
        Disassociate `phase` from this `PowerElectronicsConnection`

        `phase` the `PowerElectronicsConnectionPhase` to disassociate from this `PowerElectronicsConnection`.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
        Raises `ValueError` if `phase` was not associated with this `PowerElectronicsConnection`.
        """
        self._power_electronics_connection_phases = safe_remove(self._power_electronics_connection_phases, phase)
        return self

    def clear_phases(self) -> PowerElectronicsConnection:
        """
        Clear all phases.
        Returns A reference to this `PowerElectronicsConnection` to allow fluent use.
       """
        self._power_electronics_connection_phases = None
        return self
