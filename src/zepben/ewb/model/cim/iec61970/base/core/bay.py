#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Bay"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import ngen, get_by_mrid, safe_remove, nlen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.breaker_configuration import BreakerConfiguration
    from zepben.ewb.model.cim.iec61970.base.core.busbar_configuration import BusbarConfiguration
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.voltage_level import VoltageLevel
    from zepben.ewb.model.cim.iec61970.infiec61970.feeder.circuit import Circuit


class Bay(EquipmentContainer):
    """
    A collection of power system resources within a given substation.
    A bay typically represents a physical grouping related to modularization of equipment.
    """

    substation: Optional[Substation] = None
    """The Substation containing the bay."""

    voltage_level: Optional[VoltageLevel] = None
    """The VoltageLevel containing the bay."""

    circuit: Optional[Circuit] = None
    """The Circuit that ends at this bay."""

    bay_energy_meas_flag: Optional[bool] = None
    """Indicates the presence/absence of energy measurements."""

    bay_power_meas_flag: Optional[bool] = None
    """Indicates the presence/absence of active/reactive power measurements."""

    breaker_configuration: Optional[BreakerConfiguration] = None
    """The breaker configuration of the bay."""

    bus_bar_configuration: Optional[BusbarConfiguration] = None
    """The busbar configuration of the bay."""

    def __init__(self, substation: Substation = None, voltage_level: VoltageLevel = None,
                 circuit: Circuit = None, bay_energy_meas_flag: bool = None,
                 bay_power_meas_flag: bool = None,
                 breaker_configuration: BreakerConfiguration = None,
                 bus_bar_configuration: BusbarConfiguration = None, **kwargs):
        super(Bay, self).__init__(**kwargs)
        if substation is not None:
            self.substation = substation
        if voltage_level is not None:
            self.voltage_level = voltage_level
        if circuit is not None:
            self.circuit = circuit
        if bay_energy_meas_flag is not None:
            self.bay_energy_meas_flag = bay_energy_meas_flag
        if bay_power_meas_flag is not None:
            self.bay_power_meas_flag = bay_power_meas_flag
        if breaker_configuration is not None:
            self.breaker_configuration = breaker_configuration
        if bus_bar_configuration is not None:
            self.bus_bar_configuration = bus_bar_configuration

    def set_substation(self, substation: Substation) -> Bay:
        """
        Associate this Bay with a Substation.

        `substation` The Substation to associate with this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.substation = substation
        return self

    def remove_substation(self) -> Bay:
        """
        Disassociate the Substation from this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.substation = None
        return self

    def set_voltage_level(self, voltage_level: VoltageLevel) -> Bay:
        """
        Associate this Bay with a VoltageLevel.

        `voltage_level` The VoltageLevel to associate with this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.voltage_level = voltage_level
        return self

    def remove_voltage_level(self) -> Bay:
        """
        Disassociate the VoltageLevel from this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.voltage_level = None
        return self

    def set_circuit(self, circuit: Circuit) -> Bay:
        """
        Associate this Bay with a Circuit.

        `circuit` The Circuit to associate with this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.circuit = circuit
        return self

    def remove_circuit(self) -> Bay:
        """
        Disassociate the Circuit from this Bay.
        Returns A reference to this Bay to allow fluent use.
        """
        self.circuit = None
        return self

    def set_bay_energy_meas_flag(self, bay_energy_meas_flag: bool) -> Bay:
        """
        Set the energy measurement flag.

        `bay_energy_meas_flag` The flag value.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bay_energy_meas_flag = bay_energy_meas_flag
        return self

    def clear_bay_energy_meas_flag(self) -> Bay:
        """
        Clear the energy measurement flag.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bay_energy_meas_flag = None
        return self

    def set_bay_power_meas_flag(self, bay_power_meas_flag: bool) -> Bay:
        """
        Set the power measurement flag.

        `bay_power_meas_flag` The flag value.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bay_power_meas_flag = bay_power_meas_flag
        return self

    def clear_bay_power_meas_flag(self) -> Bay:
        """
        Clear the power measurement flag.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bay_power_meas_flag = None
        return self

    def set_breaker_configuration(self, breaker_configuration: BreakerConfiguration) -> Bay:
        """
        Set the breaker configuration.

        `breaker_configuration` The breaker configuration.
        Returns A reference to this Bay to allow fluent use.
        """
        self.breaker_configuration = breaker_configuration
        return self

    def clear_breaker_configuration(self) -> Bay:
        """
        Clear the breaker configuration.
        Returns A reference to this Bay to allow fluent use.
        """
        self.breaker_configuration = None
        return self

    def set_bus_bar_configuration(self, bus_bar_configuration: BusbarConfiguration) -> Bay:
        """
        Set the busbar configuration.

        `bus_bar_configuration` The busbar configuration.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bus_bar_configuration = bus_bar_configuration
        return self

    def clear_bus_bar_configuration(self) -> Bay:
        """
        Clear the busbar configuration.
        Returns A reference to this Bay to allow fluent use.
        """
        self.bus_bar_configuration = None
        return self
