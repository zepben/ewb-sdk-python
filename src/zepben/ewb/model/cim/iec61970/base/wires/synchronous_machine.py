#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["SynchronousMachine"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine_kind import SynchronousMachineKind
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import MridCollection, LazyMridList

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve


@zb_dataclass
class SynchronousMachine(RotatingMachine):
    """
    An electromechanical device that operates with shaft rotating synchronously with the network. It is a single machine operating either as a generator or
    synchronous condenser or pump.
    """

    _reactive_capability_curves: Optional[List['ReactiveCapabilityCurve']] = field(default=None)

    base_q: Optional[float] = None
    """Default base reactive power value in VAr. This value represents the initial reactive power that can be used by any application function."""

    condenser_p: Optional[int] = None
    """Active power consumed (watts) when in condenser mode operation."""

    earthing: Optional[bool] = None
    """Indicates whether the generator is earthed. Used for short circuit data exchange according to IEC 60909."""

    earthing_star_point_r: Optional[float] = None
    """Generator star point earthing resistance in Ohms (Re). Used for short circuit data exchange according to IEC 60909."""

    earthing_star_point_x: Optional[float] = None
    """Generator star point earthing reactance in Ohms (Xe). Used for short circuit data exchange according to IEC 60909."""

    ikk: Optional[float] = None
    """
    Steady-state short-circuit current (in A for the profile) of generator with compound excitation during 3-phase short circuit.
    - Ikk=0: Generator with no compound excitation.
    - Ikk<>0: Generator with compound excitation.
    Ikk is used to calculate the minimum steady-state short-circuit current for generators with compound excitation. (4.6.1.2 in IEC 60909-0:2001).
    Used only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
    """

    max_q: Optional[float] = None
    """Maximum reactive power limit in VAr. This is the maximum (nameplate) limit for the unit."""

    max_u: Optional[int] = None
    """Maximum voltage limit for the unit in volts."""

    min_q: Optional[float] = None
    """Minimum reactive power limit for the unit in VAr."""

    min_u: Optional[int] = None
    """Minimum voltage limit for the unit in volts."""

    mu: Optional[float] = None
    """
    Factor to calculate the breaking current (Section 4.5.2.1 in IEC 60909-0).
    Used only for single fed short circuit on a generator (Section 4.3.4.2. in IEC 60909-0).
    """

    r: Optional[float] = None
    """
    Equivalent resistance (RG) of generator as a percentage. RG is considered for the calculation of all currents,
    except for the calculation of the peak current ip. Used for short circuit data exchange according to IEC 60909.
    """

    r0: Optional[float] = None
    """Zero sequence resistance of the synchronous machine as a percentage."""

    r2: Optional[float] = None
    """Negative sequence resistance as a percentage."""

    sat_direct_subtrans_x: Optional[float] = None
    """Direct-axis subtransient reactance saturated as a percentage, also known as Xd"sat."""

    sat_direct_sync_x: Optional[float] = None
    """
    Direct-axes saturated synchronous reactance (xdsat); reciprocal of short-circuit ration, as a percentage.
    Used for short circuit data exchange, only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
    """

    sat_direct_trans_x: Optional[float] = None
    """
    Saturated Direct-axis transient reactance as a percentage.
    The attribute is primarily used for short circuit calculations according to ANSI.
    """

    x0: Optional[float] = None
    """Zero sequence reactance of the synchronous machine as a percentage."""

    x2: Optional[float] = None
    """Negative sequence reactance as a percentage."""

    type: SynchronousMachineKind = SynchronousMachineKind.UNKNOWN
    """Modes that this synchronous machine can operate in."""

    operating_mode: SynchronousMachineKind = SynchronousMachineKind.UNKNOWN
    """Current mode of operation."""

    curves: MridCollection['ReactiveCapabilityCurve'] = LazyMridList(
        _reactive_capability_curves,
        "A ReactiveCapabilityCurve",
    )






    # region deprecated list boilerplate
    # region curves boilerplate

    @deprecated("Use len(obj.curves) instead.")
    def num_curves(self):
        return len(self.curves)

    @deprecated("Use obj.curves.get_by_mrid(mrid) instead.")
    def get_curve(self, mrid: str) -> 'ReactiveCapabilityCurve':
        return self.curves.get_by_mrid(mrid)

    @deprecated("Use obj.curves.append(curve) instead.")
    def add_curve(self, curve: 'ReactiveCapabilityCurve') -> 'SynchronousMachine':
        self.curves.append(curve)
        return self

    @deprecated("Use obj.curves.remove(curve) instead.")
    def remove_curve(self, curve: 'ReactiveCapabilityCurve') -> 'SynchronousMachine':
        self.curves.remove(curve)
        return self

    @deprecated("Use obj.curves.clear() instead.")
    def clear_curves(self) -> 'SynchronousMachine':
        self.curves.clear()
        return self

    # endregion curves boilerplate

    # endregion deprecated list boilerplate
