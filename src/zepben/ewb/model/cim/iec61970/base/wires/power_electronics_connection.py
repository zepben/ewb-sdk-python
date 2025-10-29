#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerElectronicsConnection"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import RegulatingCondEq
from zepben.ewb.util import ngen, nlen, get_by_mrid, safe_remove, require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import PowerElectronicsUnit
    from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase


@dataslot
@boilermaker
class PowerElectronicsConnection(RegulatingCondEq):
    """
    A connection to the AC network for energy production or consumption that uses power electronics rather than rotating machines.
    """

    max_i_fault: int | None = None
    """Maximum fault current this device will contribute, in per-unit of rated current, before the converter protection will trip or bypass."""

    p: float | None = None
    """Active power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    q: float | None = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""

    max_q: float | None = None
    """Maximum reactive power limit. This is the maximum (nameplate) limit for the unit."""

    min_q: float | None = None
    """Minimum reactive power limit for the unit. This is the minimum (nameplate) limit for the unit."""

    rated_s: int | None = None
    """Nameplate apparent power rating for the unit. The attribute shall have a positive value."""

    rated_u: int | None = None
    """Rated voltage (nameplate data, Ur in IEC 60909-0). It is primarily used for short circuit data exchange according to IEC 60909. 
    The attribute shall be a positive value."""

    inverter_standard: str | None = None
    """The standard this inverter follows, such as AS4777.2:2020"""

    sustain_op_overvolt_limit: int | None = None
    """Indicates the sustained operation overvoltage limit in volts, when the average voltage for a 10-minute period exceeds the V¬nom-max."""

    stop_at_over_freq: float | None = None
    """Over frequency (stop) in Hz. Permitted range is between 51 and 52 (inclusive)"""

    stop_at_under_freq: float | None = None
    """Under frequency (stop) in Hz Permitted range is between 47 and 49 (inclusive)"""

    inv_volt_watt_resp_mode: bool | None = None
    """
    Volt-Watt response mode allows an inverter to reduce is real power output depending on the measured voltage.
    This mode is further described in AS4777.2:2015, section 6.3.2.2. True implies the mode is enabled.
    """

    inv_watt_resp_v1: int | None = ValidatedDescriptor(None)
    """Set point 1 in volts for inverter Volt-Watt response mode. Permitted range is between 200 and 300 (inclusive)."""

    inv_watt_resp_v2: int | None = ValidatedDescriptor(None)
    """Set point 2 in volts for inverter Volt-Watt response mode. Permitted range is between 216 and 230 (inclusive)."""

    inv_watt_resp_v3: int | None = ValidatedDescriptor(None)
    """Set point 3 in volts for inverter Volt-Watt response mode. Permitted range is between 235 and 255 (inclusive)."""

    inv_watt_resp_v4: int | None = ValidatedDescriptor(None)
    """Set point 4 in volts for inverter Volt-Watt response mode. Permitted range is between 244 and 265 (inclusive)."""

    inv_watt_resp_p_at_v1: float | None = ValidatedDescriptor(None)
    """Power output set point 1 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    inv_watt_resp_p_at_v2: float | None = ValidatedDescriptor(None)
    """Power output set point 2 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    inv_watt_resp_p_at_v3: float | None = ValidatedDescriptor(None)
    """Power output set point 3 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 1 (inclusive)."""

    inv_watt_resp_p_at_v4: float | None = ValidatedDescriptor(None)
    """Power output set point 4 as a percentage of rated output for inverter Volt-Watt response mode. Permitted range is between 0 and 0.2 (inclusive)."""

    inv_volt_var_resp_mode: bool | None = None
    """
    Volt-VAr response mode allows an inverter to consume (sink) or produce (source) reactive power depending on the measured voltage.
    This mode is further described in AS4777.2:2015, section 6.3.2.3. True implies the mode is enabled.
    """

    inv_var_resp_v1: int | None = ValidatedDescriptor(None)
    """Set point 1 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    inv_var_resp_v2: int | None = ValidatedDescriptor(None)
    """Set point 2 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    inv_var_resp_v3: int | None = ValidatedDescriptor(None)
    """Set point 3 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    inv_var_resp_v4: int | None = ValidatedDescriptor(None)
    """Set point 4 in volts for inverter Volt-VAr response mode. Permitted range is between 200 and 300 (inclusive)."""

    inv_var_resp_q_at_v1: float | None = ValidatedDescriptor(None)
    """Power output set point 1 as a percentage of rated output for inverter Volt-VAr response mode. Permitted range is between 0 and 0.6 (inclusive)."""

    inv_var_resp_q_at_v2: float | None = ValidatedDescriptor(None)
    """
    Power output set point 2 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
    """

    inv_var_resp_q_at_v3: float | None = ValidatedDescriptor(None)
    """
    Power output set point 3 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -1 and 1 (inclusive) with a negative number referring to a sink.
    """

    inv_var_resp_q_at_v4: float | None = ValidatedDescriptor(None)
    """
    Power output set point 4 as a percentage of rated output for inverter Volt-VAr response mode.
    Permitted range is between -0.6 and 0 (inclusive) with a negative number referring to a sink.
    """

    inv_reactive_power_mode: bool | None = None
    """If true, enables Static Reactive Power mode on the inverter. Note: It must be false if invVoltVarRespMode or InvVoltWattRespMode is true."""

    inv_fix_reactive_power: float | None = None
    """
    Static Reactive Power, specified in a percentage output of the system.
    Permitted range is between -1.0 and 1.0 (inclusive), with a negative sign referring to “sink”.
    """

    power_electronics_units: List[PowerElectronicsUnit] | None = MRIDListAccessor()
    """An AC network connection may have several power electronics units connecting through it."""

    power_electronics_connection_phases: List[PowerElectronicsConnectionPhase] | None = MRIDListAccessor()
    """The individual units models for the power electronics connection."""

    def _retype(self):
        self.power_electronics_units: MRIDListRouter = ...
        self.power_electronics_connection_phases: MRIDListRouter = ...
    
    @validate(inv_watt_resp_v1)
    def _inv_watt_resp_v1_validate(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_watt_resp_v1 [{value}] must be between 200 and 300.")
        return value

    @validate(inv_watt_resp_v2)
    def _inv_watt_resp_v2_validate(self, value):
        require(value is None or 216 <= value <= 230, lambda: f"inv_watt_resp_v2 [{value}] must be between 216 and 230.")
        return value

    @validate(inv_watt_resp_v3)
    def _inv_watt_resp_v3_validate(self, value):
        require(value is None or 235 <= value <= 255, lambda: f"inv_watt_resp_v3 [{value}] must be between 235 and 255.")
        return value

    @validate(inv_watt_resp_v4)
    def _inv_watt_resp_v4_validate(self, value):
        require(value is None or 244 <= value <= 265, lambda: f"inv_watt_resp_v4 [{value}] must be between 244 and 265.")
        return value

    @validate(inv_watt_resp_p_at_v1)
    def _inv_watt_resp_p_at_v1_validate(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v1 [{value}] must be between 0.0 and 1.0.")
        return value

    @validate(inv_watt_resp_p_at_v2)
    def _inv_watt_resp_p_at_v2_validate(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v2 [{value}] must be between 0.0 and 1.0.")
        return value

    @validate(inv_watt_resp_p_at_v3)
    def _inv_watt_resp_p_at_v3_validate(self, value):
        require(value is None or 0.0 <= value <= 1.0, lambda: f"inv_watt_resp_p_at_v3 [{value}] must be between 0.0 and 1.0.")
        return value

    @validate(inv_watt_resp_p_at_v4)
    def _inv_watt_resp_p_at_v4_validate(self, value):
        require(value is None or 0.0 <= value <= 0.2, lambda: f"inv_watt_resp_p_at_v4 [{value}] must be between 0.0 and 0.2.")
        return value

    @validate(inv_var_resp_v1)
    def _inv_var_resp_v1_validate(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v1 [{value}] must be between 200 and 300.")
        return value

    @validate(inv_var_resp_v2)
    def _inv_var_resp_v2_validate(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v2 [{value}] must be between 200 and 300.")
        return value

    @validate(inv_var_resp_v3)
    def _inv_var_resp_v3_validate(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v3 [{value}] must be between 200 and 300.")
        return value

    @validate(inv_var_resp_v4)
    def _inv_var_resp_v4_validate(self, value):
        require(value is None or 200 <= value <= 300, lambda: f"inv_var_resp_v4 [{value}] must be between 200 and 300.")
        return value

    @validate(inv_var_resp_q_at_v1)
    def _inv_var_resp_q_at_v1_validate(self, value):
        require(value is None or 0.0 <= value <= 0.6, lambda: f"inv_var_resp_q_at_v1 [{value}] must be between 0.0 and 0.6.")
        return value

    @validate(inv_var_resp_q_at_v2)
    def _inv_var_resp_q_at_v2_validate(self, value):
        require(value is None or -1.0 <= value <= 1.0, lambda: f"inv_var_resp_q_at_v2 [{value}] must be between -1.0 and 1.0.")
        return value

    @validate(inv_var_resp_q_at_v3)
    def _inv_var_resp_q_at_v3_validate(self, value):
        require(value is None or -1.0 <= value <= 1.0, lambda: f"inv_var_resp_q_at_v3 [{value}] must be between -1.0 and 1.0.")
        return value

    @validate(inv_var_resp_q_at_v4)
    def _inv_var_resp_q_at_v4_validate(self, value):
        require(value is None or -0.6 <= value <= 0.0, lambda: f"inv_var_resp_q_at_v4 [{value}] must be between -0.6 and 0.0.")
        return value

    @property
    def units(self) -> Generator[PowerElectronicsUnit, None, None]:
        """
        The `PowerElectronicsUnit`s for this `PowerElectronicsConnection`.
        """
        return ngen(self.power_electronics_units)

    @property
    def phases(self) -> Generator[PowerElectronicsConnectionPhase, None, None]:
        """
        The `PowerElectronicsConnectionPhase`s for this `PowerElectronicsConnection`.
        """
        return ngen(self.power_electronics_connection_phases)

    @deprecated("BOILERPLATE: Use len(power_electronics_units) instead")
    def num_units(self):
        return len(self.power_electronics_units)

    @deprecated("BOILERPLATE: Use power_electronics_units.get_by_mrid(mrid) instead")
    def get_unit(self, mrid: str) -> PowerElectronicsUnit:
        return self.power_electronics_units.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use power_electronics_units.append(unit) instead")
    def add_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        return self.power_electronics_units.append(unit)

    @deprecated("BOILERPLATE: Use power_electronics_units.remove(unit) instead")
    def remove_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        return self.power_electronics_units.remove(unit)

    @deprecated("BOILERPLATE: Use power_electronics_units.clear() instead")
    def clear_units(self) -> PowerElectronicsConnection:
        return self.power_electronics_units.clear()

    @deprecated("BOILERPLATE: Use len(power_electronics_connection_phases) instead")
    def num_phases(self):
        return len(self.power_electronics_connection_phases)

    @deprecated("BOILERPLATE: Use power_electronics_connection_phases.get_by_mrid(mrid) instead")
    def get_phase(self, mrid: str) -> PowerElectronicsConnectionPhase:
        return self.power_electronics_connection_phases.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use power_electronics_connection_phases.append(phase) instead")
    def add_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        return self.power_electronics_connection_phases.append(phase)

    @deprecated("BOILERPLATE: Use power_electronics_connection_phases.remove(phase) instead")
    def remove_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        return self.power_electronics_connection_phases.remove(phase)

    @deprecated("BOILERPLATE: Use power_electronics_connection_phases.clear() instead")
    def clear_phases(self) -> PowerElectronicsConnection:
        return self.power_electronics_connection_phases.clear()
        return self
