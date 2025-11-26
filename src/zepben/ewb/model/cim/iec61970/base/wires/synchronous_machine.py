#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["SynchronousMachine"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor, custom_add
from zepben.ewb.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine_kind import SynchronousMachineKind

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve


@dataslot
class SynchronousMachine(RotatingMachine):
    """
    An electromechanical device that operates with shaft rotating synchronously with the network. It is a single machine operating either as a generator or
    synchronous condenser or pump.
    """

    curves: List['ReactiveCapabilityCurve'] | None = MRIDListAccessor()

    base_q: float | None = None
    """Default base reactive power value in VAr. This value represents the initial reactive power that can be used by any application function."""

    condenser_p: int | None = None
    """Active power consumed (watts) when in condenser mode operation."""

    earthing: bool | None = None
    """Indicates whether the generator is earthed. Used for short circuit data exchange according to IEC 60909."""

    earthing_star_point_r: float | None = None
    """Generator star point earthing resistance in Ohms (Re). Used for short circuit data exchange according to IEC 60909."""

    earthing_star_point_x: float | None = None
    """Generator star point earthing reactance in Ohms (Xe). Used for short circuit data exchange according to IEC 60909."""

    ikk: float | None = None
    """
    Steady-state short-circuit current (in A for the profile) of generator with compound excitation during 3-phase short circuit.
    - Ikk=0: Generator with no compound excitation.
    - Ikk<>0: Generator with compound excitation.
    Ikk is used to calculate the minimum steady-state short-circuit current for generators with compound excitation. (4.6.1.2 in IEC 60909-0:2001).
    Used only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
    """

    max_q: float | None = None
    """Maximum reactive power limit in VAr. This is the maximum (nameplate) limit for the unit."""

    max_u: int | None = None
    """Maximum voltage limit for the unit in volts."""

    min_q: float | None = None
    """Minimum reactive power limit for the unit in VAr."""

    min_u: int | None = None
    """Minimum voltage limit for the unit in volts."""

    mu: float | None = None
    """
    Factor to calculate the breaking current (Section 4.5.2.1 in IEC 60909-0).
    Used only for single fed short circuit on a generator (Section 4.3.4.2. in IEC 60909-0).
    """

    r: float | None = None
    """
    Equivalent resistance (RG) of generator as a percentage. RG is considered for the calculation of all currents,
    except for the calculation of the peak current ip. Used for short circuit data exchange according to IEC 60909.
    """

    r0: float | None = None
    """Zero sequence resistance of the synchronous machine as a percentage."""

    r2: float | None = None
    """Negative sequence resistance as a percentage."""

    sat_direct_subtrans_x: float | None = None
    """Direct-axis subtransient reactance saturated as a percentage, also known as Xd"sat."""

    sat_direct_sync_x: float | None = None
    """
    Direct-axes saturated synchronous reactance (xdsat); reciprocal of short-circuit ration, as a percentage.
    Used for short circuit data exchange, only for single fed short circuit on a generator. (4.3.4.2. in IEC 60909-0:2001).
    """

    sat_direct_trans_x: float | None = None
    """
    Saturated Direct-axis transient reactance as a percentage.
    The attribute is primarily used for short circuit calculations according to ANSI.
    """

    x0: float | None = None
    """Zero sequence reactance of the synchronous machine as a percentage."""

    x2: float | None = None
    """Negative sequence reactance as a percentage."""

    type: SynchronousMachineKind = SynchronousMachineKind.UNKNOWN
    """Modes that this synchronous machine can operate in."""

    operating_mode: SynchronousMachineKind = SynchronousMachineKind.UNKNOWN
    """Current mode of operation."""

    def _retype(self):
        self.curves: MRIDListRouter['ReactiveCapabilityCurve'] = ...
    
    @deprecated("BOILERPLATE: Use len(curves) instead")
    def num_curves(self):
        return len(self.curves)

    @deprecated("BOILERPLATE: Use curves.get_by_mrid(mrid) instead")
    def get_curve(self, mrid: str) -> 'ReactiveCapabilityCurve':
        return self.curves.get_by_mrid(mrid)

    @custom_add(curves)
    def add_curve(self, curve: 'ReactiveCapabilityCurve') -> 'SynchronousMachine':
        """
        Associate a :class:`ReactiveCapabilityCurve` with this :class:`SynchronousMachine`.

        :param curve: The :class:`ReactiveCapabilityCurve` to associate with this :class:`SynchronousMachine`.
        :returns: A reference to this :class:`SynchronousMachine` to allow fluent use.
        :raises ValueError: If another :class:`ReactiveCapabilityCurve` with the same `mrid` already exists for this :class:`SynchronousMachine`.
        """
        if self._validate_reference(curve, self.get_curve, "A ReactiveCapabilityCurve"):
            return self
        self.curves.append_unchecked(curve)
        return self

    @deprecated("Boilerplate: Use curves.remove(curve) instead")
    def remove_curve(self, curve: 'ReactiveCapabilityCurve') -> 'SynchronousMachine':
        self.curves.remove(curve)
        return self

    @deprecated("BOILERPLATE: Use curves.clear() instead")
    def clear_curves(self) -> 'SynchronousMachine':
        self.curves.clear()
        return self

