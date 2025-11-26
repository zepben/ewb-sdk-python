#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RegulatingControl"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control_mode_kind import RegulatingControlModeKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import RegulatingCondEq


@dataslot
class RegulatingControl(PowerSystemResource):
    """
    Specifies a set of equipment that works together to control a power system quantity such as voltage or flow. Remote bus voltage control is possible by
    specifying the controlled terminal located at some place remote from the controlling equipment. The specified terminal shall be associated with the
    connectivity node of the controlled point. The most specific subtype of RegulatingControl shall be used in case such equipment participate in the
    control, e.g. TapChangerControl for tap changers.

    For flow control, load sign convention is used, i.e. positive sign means flow out from a TopologicalNode (bus) into the conducting equipment.

    The attribute minAllowedTargetValue and maxAllowedTargetValue are required in the following cases: For a power generating module operated in power factor
    control mode to specify maximum and minimum power factor values; Whenever it is necessary to have an off center target voltage for the tap changer
    regulator. For instance, due to long cables to off shore wind farms and the  need to have a simpler setup at the off shore transformer platform,
    the voltage is controlled from the land at the connection point for the off shore wind farm.

    Since there usually is a voltage rise along the cable, there is typically an overvoltage of up 3-4 kV compared to the on shore station. Thus in normal
    operation the tap changer on the on shore station is operated with a target set point, which is in the lower parts of the dead band.

    The attributes minAllowedTargetValue and maxAllowedTargetValue are not related to the attribute targetDeadband and thus they are not treated as an
    alternative of the targetDeadband. They are needed due to limitations in the local substation controller.

    The attribute targetDeadband is used to prevent the power flow from move the tap position in circles (hunting) that is to be used regardless of the
    attributes minAllowedTargetValue and maxAllowedTargetValue.
    """

    discrete: bool | None = None
    """The regulation is performed in a discrete mode. This applies to equipment with discrete controls, e.g. tap changers and shunt compensators."""

    mode: [RegulatingControlModeKind] = RegulatingControlModeKind.UNKNOWN
    """
    The regulating control mode presently available. This specification allows for determining the kind of regulation without need for obtaining the 
    units from a schedule.
    """

    monitored_phase: [PhaseCode] = PhaseCode.NONE
    """Phase voltage controlling this regulator, measured at regulator location."""

    target_deadband: float | None = None
    """
    This is a deadband used with discrete control to avoid excessive update of controls like tap changers and shunt compensator banks while regulating. 
    The units are the base units appropriate for the mode. The attribute shall be a positive value or zero. If RegulatingControl.discrete is set to "false",
    the RegulatingControl.target_deadband is to be ignored. Note that for instance, if the targetValue is 100 kV and the targetDeadband is 2 kV the range is 
    from 99 to 101 kV.
    """

    target_value: float | None = None
    """
    The target value specified for case input. This value can be used for the target value without the use of schedules. The value has the units appropriate 
    to the mode attribute.
    """

    enabled: bool | None = None
    """The flag tells if regulation is enabled."""

    max_allowed_target_value: float | None = None
    """Maximum allowed target value (RegulatingControl.targetValue)."""

    min_allowed_target_value: float | None = None
    """Minimum allowed target value (RegulatingControl.targetValue)."""

    rated_current: float | None = None
    """The rated current of associated CT in amps for this RegulatingControl. Forms the base used to convert Line Drop Compensation settings from ohms to 
    voltage."""

    terminal: Terminal | None = None
    """
    The terminal associated with this regulating control. The terminal is associated instead of a node, since the terminal could connect into either a 
    topological node or a connectivity node. Sometimes it is useful to model regulation at a terminal of a bus bar object.
    """

    ct_primary: float | None = None
    """
    [ZBEX]
    Current rating of the CT, expressed in terms of the current (in Amperes) that flows in the Primary where the 'Primary' is the conductor
    being monitored. It ensures proper operation of the regulating equipment by providing the necessary current references for control actions. An important side
    effect of this current value is that it also defines the current value at which the full LDC R and X voltages are applied by the controller, where enabled.
    """

    min_target_deadband: float | None = None
    """
    [ZBEX]
    This is the minimum allowable range for discrete control in regulating devices, used to prevent frequent control actions and
    promote operational stability. This attribute sets a baseline range within which no adjustments are made, applicable across various devices like voltage
    regulators, shunt compensators, or battery units.
    """

    regulating_conducting_equipment: List[RegulatingCondEq] | None = MRIDListAccessor()
    """The [RegulatingCondEq] that are controlled by this regulating control scheme."""

    def _retype(self):
        self.regulating_conducting_equipment: MRIDListRouter[RegulatingCondEq] = ...

    @deprecated("BOILERPLATE: Use len(regulating_cond_eq) instead")
    def num_regulating_cond_eq(self) -> int:
        return len(self.regulating_conducting_equipment)

    @deprecated("BOILERPLATE: Use regulating_cond_eq.get_by_mrid(mrid) instead")
    def get_regulating_cond_eq(self, mrid: str) -> RegulatingCondEq:
        return self.regulating_conducting_equipment.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use regulating_cond_eq.append(regulating_cond_eq) instead")
    def add_regulating_cond_eq(self, regulating_cond_eq: RegulatingCondEq) -> RegulatingControl:
        self.regulating_conducting_equipment.append(regulating_cond_eq)
        return self

    @deprecated("Boilerplate: Use regulating_cond_eq.remove(regulating_cond_eq) instead")
    def remove_regulating_cond_eq(self, regulating_cond_eq: RegulatingCondEq | None) -> RegulatingControl:
        self.regulating_conducting_equipment.remove(regulating_cond_eq)
        return self

    @deprecated("BOILERPLATE: Use regulating_cond_eq.clear() instead")
    def clear_regulating_cond_eq(self) -> RegulatingControl:
        self.regulating_conducting_equipment.clear()
        return self

