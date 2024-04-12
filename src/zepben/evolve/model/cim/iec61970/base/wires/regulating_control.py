#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, List, Generator, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import RegulatingCondEq

from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.regulating_control_mode_kind import RegulatingControlModeKind


from zepben.evolve.util import nlen, get_by_mrid, safe_remove, ngen

__all__ = ["RegulatingControl"]


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

    discrete: Optional[bool] = None
    """The regulation is performed in a discrete mode. This applies to equipment with discrete controls, e.g. tap changers and shunt compensators."""

    mode: [RegulatingControlModeKind] = RegulatingControlModeKind.UNKNOWN_CONTROL_MODE
    """
    The regulating control mode presently available. This specification allows for determining the kind of regulation without need for obtaining the 
    units from a schedule.
    """

    monitored_phase: [PhaseCode] = PhaseCode.NONE
    """Phase voltage controlling this regulator, measured at regulator location."""

    target_deadband: Optional[float] = None
    """
    This is a deadband used with discrete control to avoid excessive update of controls like tap changers and shunt compensator banks while regulating. 
    The units are the base units appropriate for the mode. The attribute shall be a positive value or zero. If RegulatingControl.discrete is set to "false",
    the RegulatingControl.target_deadband is to be ignored. Note that for instance, if the targetValue is 100 kV and the targetDeadband is 2 kV the range is 
    from 99 to 101 kV.
    """

    target_value: Optional[float] = None
    """
    The target value specified for case input. This value can be used for the target value without the use of schedules. The value has the units appropriate 
    to the mode attribute.
    """

    enabled: Optional[bool] = None
    """The flag tells if regulation is enabled."""

    max_allowed_target_value: Optional[float] = None
    """Maximum allowed target value (RegulatingControl.targetValue)."""

    min_allowed_target_value: Optional[float] = None
    """Minimum allowed target value (RegulatingControl.targetValue)."""

    rated_current: Optional[float] = None
    """The rated current of associated CT in amps for this RegulatingControl. Forms the base used to convert Line Drop Compensation settings from ohms to 
    voltage."""

    terminal: Optional[Terminal] = None
    """
    The terminal associated with this regulating control. The terminal is associated instead of a node, since the terminal could connect into either a 
    topological node or a connectivity node. Sometimes it is useful to model regulation at a terminal of a bus bar object.
    """

    _regulating_cond_eq: Optional[List[RegulatingCondEq]] = None
    """The [RegulatingCondEq] that are controlled by this regulating control scheme."""

    def __init__(self, regulating_conducting_equipment: Optional[Iterable[RegulatingCondEq]] = None, **kwargs):
        super(PowerSystemResource, self).__init__(**kwargs)
        if regulating_conducting_equipment is not None:
            for eq in regulating_conducting_equipment:
                self.add_regulating_cond_eq(eq)

    @property
    def regulating_conducting_equipment(self) -> Generator[RegulatingCondEq, None, None]:
        """
        Yields all the :class:`RegulatingCondEq` that are controlled by this :class:`RegulatingControl`.

        :return: A generator that iterates over all RegulatingCondEq controlled by this RegulatingControl.
        """
        return ngen(self._regulating_cond_eq)

    def num_regulating_cond_eq(self) -> int:
        """
        Get the number of :class:`RegulatingCondEq` that are controlled by this :class:`RegulatingControl`.

        :return: The number of RegulatingCondEq that are controlled by this RegulatingControl.
        """
        return nlen(self._regulating_cond_eq)

    def get_regulating_cond_eq(self, mrid: str) -> RegulatingCondEq:
        """
        Get a :class:`RegulatingCondEq` controlled by this :class:`RegulatingControl`.

        :param mrid: The mRID of the desired RegulatingCondEq
        :return: The RegulatingCondEq with the specified mRID if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._regulating_cond_eq, mrid)

    def add_regulating_cond_eq(self, regulating_cond_eq: RegulatingCondEq) -> RegulatingControl:
        """
        Associate this :class:`RegulatingControl` with a :class:`RegulatingCondEq` it is controlling.

        :param regulating_cond_eq: The RegulatingCondEq to associate with this RegulatingControl.
        :return: A reference to this RegulatingControl for fluent use.
        """
        if self._validate_reference(regulating_cond_eq, self.get_regulating_cond_eq, "A RegulatingCondEq"):
            return self

        self._regulating_cond_eq = list() if self._regulating_cond_eq is None else self._regulating_cond_eq
        self._regulating_cond_eq.append(regulating_cond_eq)
        return self

    def remove_regulating_cond_eq(self, regulating_cond_eq: Optional[RegulatingCondEq]) -> RegulatingControl:
        """
        Disassociate this :class:`RegulatingControl` from a :class:`RegulatingCondEq`.

        :param regulating_cond_eq: The RegulatingCondEq to disassociate from this RegulatingControl.
        :return: A reference to this RegulatingControl for fluent use.
        """
        self._regulating_cond_eq = safe_remove(self._regulating_cond_eq, regulating_cond_eq)
        return self

    def clear_regulating_cond_eq(self) -> RegulatingControl:
        """
        Disassociate all :class:`RegulatingCondEq` from this :class:`RegulatingControl`.
        :return: A reference to this RegulatingControl for fluent use.
        """
        self._regulating_cond_eq = None
        return self
