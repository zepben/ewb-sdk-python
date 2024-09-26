#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, List, Generator

from zepben.evolve.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve
from zepben.evolve.model.cim.iec61970.base.wires.rotating_machine import RotatingMachine
from zepben.evolve.model.cim.iec61970.base.wires.synchronous_machine_kind import SynchronousMachineKind
from zepben.evolve.util import ngen, nlen, get_by_mrid, safe_remove


class SynchronousMachine(RotatingMachine):
    """
    An electromechanical device that operates with shaft rotating synchronously with the network. It is a single machine operating either as a generator or
    synchronous condenser or pump.
    """

    _reactive_capability_curves: Optional[List[ReactiveCapabilityCurve]] = None

    base_q: Optional[float] = None
    """Default base reactive power value in VAr. This value represents the initial reactive power that can be used by any application function."""

    condenser_p: Optional[int] = None
    """Active power consumed (watts) when in condenser mode operation."""

    earthing: bool = False
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

    def __init__(self, curves: List[ReactiveCapabilityCurve] = None, **kwargs):
        """
        `reactive_capability_curves` A list of `ReactiveCapabilityCurve`s to associate with this `SynchronousMachine`.
        """
        super(SynchronousMachine, self).__init__(**kwargs)
        if curves:
            for rcc in curves:
                self.add_curve(rcc)

    @property
    def curves(self) -> Generator[ReactiveCapabilityCurve, None, None]:
        """
        The available reactive capability curves for this synchronous machine. The first shall be the default for this :class:`SynchronousMachine`.
        """
        return ngen(self._reactive_capability_curves)

    def num_curves(self):
        """Return the number of :class:`ReactiveCapabilityCurve`s associated with this :class:`SynchronousMachine`."""
        return nlen(self._reactive_capability_curves)

    def get_curve(self, mrid: str) -> ReactiveCapabilityCurve:
        """
        Get the :class:`ReactiveCapabilityCurve` for this :class:`SynchronousMachine` identified by `mrid`

        :param mrid: The mRID of the required :class:`ReactiveCapabilityCurve`.
        :returns: The :class:`ReactiveCapabilityCurve` with the specified `mrid` if it exists.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._reactive_capability_curves, mrid)

    def add_curve(self, curve: ReactiveCapabilityCurve) -> "SynchronousMachine":
        """
        Associate a :class:`ReactiveCapabilityCurve` with this :class:`SynchronousMachine`.

        :param curve: The :class:`ReactiveCapabilityCurve` to associate with this :class:`SynchronousMachine`.
        :returns: A reference to this :class:`SynchronousMachine` to allow fluent use.
        :raises ValueError: If another :class:`ReactiveCapabilityCurve` with the same `mrid` already exists for this :class:`SynchronousMachine`.
        """
        if self._validate_reference(curve, self.get_curve, "A ReactiveCapabilityCurve"):
            return self
        self._reactive_capability_curves = self._reactive_capability_curves or []
        self._reactive_capability_curves.append(curve)
        return self

    def remove_curve(self, curve: ReactiveCapabilityCurve) -> "SynchronousMachine":
        """
        Disassociate a :class:`ReactiveCapabilityCurve` from this :class:`SynchronousMachine`.

        :param curve: The :class:`ReactiveCapabilityCurve` to disassociate from this :class:`SynchronousMachine`.
        :returns: A reference to this :class:`SynchronousMachine` to allow fluent use.
        :raises ValueError: If `curve` was not associated with this :class:`SynchronousMachine`.
        """
        self._reactive_capability_curves = safe_remove(self._reactive_capability_curves, curve)
        return self

    def clear_curves(self) -> "SynchronousMachine":
        """
        Clear all :class:`ReactiveCapabilityCurve` associated with this :class:`SynchronousMachine`.
        :returns: A reference to this :class:`SynchronousMachine` to allow fluent use.
        """
        self._reactive_capability_curves = None
        return self
