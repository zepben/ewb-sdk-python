#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["VoltageLevel"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import ngen, get_by_mrid, safe_remove, nlen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.bay import Bay
    from zepben.ewb.model.cim.iec61970.base.core.base_voltage import BaseVoltage
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation


class VoltageLevel(EquipmentContainer):
    """
    A collection of equipment at one common system voltage forming a switchgear.
    The equipment typically consists of breakers, busbars, instrumentation,
    control, regulation and protection devices as well as assemblies of all these.
    """

    substation: Optional[Substation] = None
    """The Substation of the voltage level."""

    base_voltage: Optional[BaseVoltage] = None
    """The base voltage used for all equipment within the voltage level."""

    high_voltage_limit: Optional[str] = None
    """The bus bar's high voltage limit. Applies to all equipment and nodes
    contained in a given VoltageLevel. Operational VoltageLimit prevails if present."""

    low_voltage_limit: Optional[str] = None
    """The bus bar's low voltage limit. Applies to all equipment and nodes
    contained in a given VoltageLevel. Operational VoltageLimit prevails if present."""

    _bays: Optional[List[Bay]] = None

    def __init__(self, substation: Substation = None, base_voltage: BaseVoltage = None,
                 high_voltage_limit: str = None, low_voltage_limit: str = None,
                 bays: List[Bay] = None, **kwargs):
        super(VoltageLevel, self).__init__(**kwargs)
        if substation is not None:
            self.substation = substation
        if base_voltage is not None:
            self.base_voltage = base_voltage
        if high_voltage_limit is not None:
            self.high_voltage_limit = high_voltage_limit
        if low_voltage_limit is not None:
            self.low_voltage_limit = low_voltage_limit
        if bays:
            for bay in bays:
                self.add_bay(bay)

    @property
    def bays(self) -> Generator[Bay, None, None]:
        """The Bays within this voltage level."""
        return ngen(self._bays)

    def num_bays(self):
        """Return the number of Bays associated with this VoltageLevel."""
        return nlen(self._bays)

    def get_bay(self, mrid: str) -> Bay:
        """
        Get the Bay for this VoltageLevel identified by mrid.

        `mrid` The mrid of the required Bay.
        Returns The Bay with the specified mrid if it exists.
        Raises KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._bays, mrid)

    def add_bay(self, bay: Bay) -> VoltageLevel:
        """
        Associate a Bay with this VoltageLevel.

        `bay` The Bay to associate with this VoltageLevel.
        Returns A reference to this VoltageLevel to allow fluent use.
        Raises ValueError if another Bay with the same mrid already exists.
        """
        if self._validate_reference(bay, self.get_bay, "A Bay"):
            return self
        self._bays = list() if self._bays is None else self._bays
        self._bays.append(bay)
        return self

    def remove_bay(self, bay: Bay) -> VoltageLevel:
        """
        Disassociate bay from this VoltageLevel.

        `bay` The Bay to disassociate from this VoltageLevel.
        Returns A reference to this VoltageLevel to allow fluent use.
        """
        self._bays = safe_remove(self._bays, bay)
        return self

    def clear_bays(self) -> VoltageLevel:
        """Clear all current Bays."""
        self._bays = None
        return self

    def set_substation(self, substation: Substation) -> VoltageLevel:
        """Associate this VoltageLevel with a Substation."""
        self.substation = substation
        return self

    def remove_substation(self) -> VoltageLevel:
        """Disassociate the Substation from this VoltageLevel."""
        self.substation = None
        return self

    def set_base_voltage(self, base_voltage: BaseVoltage) -> VoltageLevel:
        """Associate this VoltageLevel with a BaseVoltage."""
        self.base_voltage = base_voltage
        return self

    def remove_base_voltage(self) -> VoltageLevel:
        """Disassociate the BaseVoltage from this VoltageLevel."""
        self.base_voltage = None
        return self

    def set_high_voltage_limit(self, high_voltage_limit: str) -> VoltageLevel:
        """Set the high voltage limit."""
        self.high_voltage_limit = high_voltage_limit
        return self

    def clear_high_voltage_limit(self) -> VoltageLevel:
        """Clear the high voltage limit."""
        self.high_voltage_limit = None
        return self

    def set_low_voltage_limit(self, low_voltage_limit: str) -> VoltageLevel:
        """Set the low voltage limit."""
        self.low_voltage_limit = low_voltage_limit
        return self

    def clear_low_voltage_limit(self) -> VoltageLevel:
        """Clear the low voltage limit."""
        self.low_voltage_limit = None
        return self
