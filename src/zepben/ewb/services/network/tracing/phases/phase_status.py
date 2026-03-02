#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PhaseStatus"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from zepben.ewb.model.cim.iec61970.base.core.phase_code import phase_code_from_single_phases, PhaseCode
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.exceptions import PhaseException
from zepben.ewb.services.network.tracing.phases.traced_phases_bit_manipulation import TracedPhasesBitManipulation

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


def _validate_spk(spk: SinglePhaseKind):
    if spk in (SinglePhaseKind.NONE, SinglePhaseKind.INVALID):
        raise ValueError(f"INTERNAL ERROR: Phase {spk.name} is invalid")
    return spk


SinglePhaseKind.validate = _validate_spk

@dataclass(slots=True)
class PhaseStatus:
    """
    Class that holds the traced phase statuses for a nominal phase on a [Terminal].

    :var _phase_status_internal:
    """
    terminal: Terminal

    _phase_status_internal: int = 0
    """
    The underlying implementation value tracking the phase status for nominal phases of a terminal.
    It is exposed internally for data serialisation and debugging within official EWB libraries and utilities.
    
    This property should be considered internal and not for public use as the underlying
    data structure to store the status could change at any time (and thus be a breaking change).
    Use directly at your own risk.
    
    See ``TracedPhasesBitManipulation`` for details on bit representation for phase_status_internal and how we track phases status.
    """

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        Get the traced phase for the specified ``nominal_phase``.

        :param nominal_phase: The nominal phase you are interested in querying.

        :returns: the traced phase.
        """
        return TracedPhasesBitManipulation.get(self._phase_status_internal, nominal_phase.validate())

    def __setitem__(self, nominal_phase: SinglePhaseKind, single_phase_kind: SinglePhaseKind) -> bool:
        """
        Set the traced phase for the specified ``nominal_phase``.

        :param nominal_phase: The nominal phase you are interested in updating.
        :param single_phase_kind: The phase you wish to set for this ``single_phase_kind``. Specify ``SinglePhaseKind.NONE`` to clear the phase.

        :returns: ``True`` if the phase is updated, otherwise False.
        """
        it = self[nominal_phase]
        if it == single_phase_kind:
            return False

        elif it == SinglePhaseKind.NONE or single_phase_kind == SinglePhaseKind.NONE:
            self._phase_status_internal = TracedPhasesBitManipulation.set(
                self._phase_status_internal,
                nominal_phase,
                single_phase_kind
            )
            return True
        else:
            raise PhaseException("Crossing Phases")

    def as_phase_code(self) -> Optional[PhaseCode]:
        """
        Get the traced phase for each nominal phase as a ``PhaseCode``.

        :returns: The ``PhaseCode`` if the combination of phases makes sense, otherwise ``None``.
        """
        if self.terminal.phases == PhaseCode.NONE:
            return PhaseCode.NONE

        traced_phases = [self[it] for it in self.terminal.phases]
        phases = set(traced_phases)

        if phases == {SinglePhaseKind.NONE}:
            return PhaseCode.NONE
        elif SinglePhaseKind.NONE in phases:
            return None
        elif len(phases) == len(traced_phases):
            return phase_code_from_single_phases(phases)
        else:
            return None
