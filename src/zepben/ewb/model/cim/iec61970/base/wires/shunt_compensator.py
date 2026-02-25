#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ShuntCompensator"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.ewb.model.cim.iec61970.base.wires.regulating_cond_eq import RegulatingCondEq

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.shunt_compensator_info import ShuntCompensatorInfo
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


class ShuntCompensator(RegulatingCondEq):
    """
    A shunt capacitor or reactor or switchable bank of shunt capacitors or reactors. A section of a shunt compensator
    is an individual capacitor or reactor.  A negative value for reactivePerSection indicates that the compensator is
    a reactor. ShuntCompensator is a single terminal device.  Ground is implied.

    :var grounded: Used for Yn and Zn connections. True if the neutral is solidly grounded. nom_u : The voltage at which the nominal reactive power may be
        calculated. This should normally be within 10% of the voltage at which the capacitor is connected to the network.
    :var nom_u: The voltage at which the nominal reactive power may be calculated. This should normally be within 10% of the voltage at which the capacitor is
        connected to the network.
    :var phase_connection: The type of phase connection, such as wye or delta.
    :var grounding_terminal: [ZBEX] The terminal connecting to grounded network.
    :var sections: Shunt compensator sections in use. Starting value for steady state solution. Non integer values are allowed to support continuous variables.
        The reasons for continuous value are to support study cases where no discrete shunt compensator's has yet been designed, a solutions where a narrow
        voltage band force the sections to oscillate or accommodate for a continuous solution as input.
        For `LinearShuntCompensator` the value shall be between zero and `ShuntCompensator.maximumSections`. At value zero the shunt compensator conductance and
        admittance is zero. Linear interpolation of conductance and admittance between the previous and next integer section is applied in case of non-integer
        values.
        For `NonlinearShuntCompensator`s shall only be set to one of the NonlinearShuntCompensatorPoint.sectionNumber. There is no interpolation between
        NonlinearShuntCompensatorPoint-s.
    """
    grounded: Optional[bool] = None

    nom_u: Optional[int] = None

    phase_connection: PhaseShuntConnectionKind = PhaseShuntConnectionKind.UNKNOWN

    grounding_terminal: 'Terminal | None' = None

    sections: Optional[float] = None

    @property
    def shunt_compensator_info(self) -> Optional['ShuntCompensatorInfo']:
        """The `ShuntCompensatorInfo` for this `ShuntCompensator`"""
        return self.asset_info

    @shunt_compensator_info.setter
    def shunt_compensator_info(self, sci: Optional['ShuntCompensatorInfo']):
        """
        Set the `ShuntCompensatorInfo` for this `ShuntCompensator`
        `sci` The `ShuntCompensatorInfo` for this `ShuntCompensator`
        """
        self.asset_info = sci
