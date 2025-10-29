#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TransformerEnd"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.base_voltage import BaseVoltage
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
    from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import RatioTapChanger
    from zepben.ewb.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance


@dataslot
class TransformerEnd(IdentifiedObject):
    """
    A conducting connection point of a power transformer. It corresponds to a physical transformer winding terminal.
    In earlier CIM versions, the TransformerWinding class served a similar purpose, but this class is more flexible
    because it associates to terminal but is not a specialization of ConductingEquipment.
    """
    grounded: bool | None = None
    """(for Yn and Zn connections) True if the neutral is solidly grounded."""

    r_ground: float | None = None
    """(for Yn and Zn connections) Resistance part of neutral impedance where 'grounded' is true"""

    x_ground: float | None = None
    """(for Yn and Zn connections) Reactive part of neutral impedance where 'grounded' is true"""

    ratio_tap_changer: Optional['RatioTapChanger'] = None
    """Ratio tap changer associated with this transformer end."""

    terminal: Optional['Terminal'] = ValidatedDescriptor(None)
    """The terminal of the transformer that this end is associated with"""

    base_voltage: Optional['BaseVoltage'] = None
    """Base voltage of the transformer end.  This is essential for PU calculation."""

    end_number: int = 0
    """Number for this transformer end, corresponding to the end’s order in the power transformer vector group or phase angle clock number. 
    Highest voltage winding should be 1. Each end within a power transformer should have a unique subsequent end number. 
    Note the transformer end number need not match the terminal sequence number."""

    star_impedance: Optional['TransformerStarImpedance'] = None
    """(accurate for 2- or 3-winding transformers only) Pi-model impedances of this transformer end. By convention, for a two winding transformer, the full
     values of the transformer should be entered on the high voltage end (endNumber=1)."""

    @validate(terminal)
    def _terminal_validate(self, value: Optional['Terminal']):
        if value is not None:
            from zepben.ewb.model.cim.iec61970.base.wires.power_transformer import PowerTransformer
            require(value.conducting_equipment is None or isinstance(value.conducting_equipment, PowerTransformer),
                    lambda: f"Cannot assign {self.__class__.__name__}[{self.mrid}] to {value.__class__.__name__}[{value.mrid}], which is connected to a " +
                            f"{value.conducting_equipment.__class__.__name__}[{value.conducting_equipment.mrid}] rather than a PowerTransformer.")
            return value
