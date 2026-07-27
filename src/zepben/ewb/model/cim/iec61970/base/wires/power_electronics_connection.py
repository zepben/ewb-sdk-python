#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PowerElectronicsConnection"]

from dataclasses import field
from typing import Optional, List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb import Alias
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, LazyMridList
from zepben.ewb.boilerplate.backfill import Backfill
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase
from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import RegulatingCondEq
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.generation.production.power_electronics_unit import PowerElectronicsUnit


@zb_dataclass
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

    _power_electronics_units: Optional[List[PowerElectronicsUnit]] = field(default=None)
    """An AC network connection may have several power electronics units connecting through it."""

    _power_electronics_connection_phases: Optional[List[PowerElectronicsConnectionPhase]] = field(default=None)
    """The individual units models for the power electronics connection."""


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

    units: MridCollection[PowerElectronicsUnit] = LazyMridList(
        _power_electronics_units,
        "A PowerElectronicsUnit",
    )
    power_electronics_units = Alias(units)

    phases: MridCollection[PowerElectronicsConnectionPhase] = LazyMridList(
        _power_electronics_connection_phases,
        "A PowerElectronicsConnectionPhase",
        backfill=Backfill(PowerElectronicsConnectionPhase.power_electronics_connection)
    )
    power_electronics_connection_phases = Alias(phases)




    # region deprecated list boilerplate
    # region units boilerplate

    @deprecated("Use len(obj.units) instead.")
    def num_units(self):
        return len(self.units)

    @deprecated("Use obj.units.get_by_mrid(mrid) instead.")
    def get_unit(self, mrid: str) -> PowerElectronicsUnit:
        return self.units.get_by_mrid(mrid)

    @deprecated("Use obj.units.append(unit) instead.")
    def add_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        self.units.append(unit)
        return self

    @deprecated("Use obj.units.remove(unit) instead.")
    def remove_unit(self, unit: PowerElectronicsUnit) -> PowerElectronicsConnection:
        self.units.remove(unit)
        return self

    @deprecated("Use obj.units.clear() instead.")
    def clear_units(self) -> PowerElectronicsConnection:
        self.units.clear()
        return self

    # endregion units boilerplate

    # region phases boilerplate

    @deprecated("Use len(obj.phases) instead.")
    def num_phases(self):
        return len(self.phases)

    @deprecated("Use obj.phases.get_by_mrid(mrid) instead.")
    def get_phase(self, mrid: str) -> PowerElectronicsConnectionPhase:
        return self.phases.get_by_mrid(mrid)

    @deprecated("Use obj.phases.append(phase) instead.")
    def add_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        self.phases.append(phase)
        return self

    @deprecated("Use obj.phases.remove(phase) instead.")
    def remove_phase(self, phase: PowerElectronicsConnectionPhase) -> PowerElectronicsConnection:
        self.phases.remove(phase)
        return self

    @deprecated("Use obj.phases.clear() instead.")
    def clear_phases(self) -> PowerElectronicsConnection:
        self.phases.clear()
        return self

    # endregion phases boilerplate

    # endregion deprecated list boilerplate
