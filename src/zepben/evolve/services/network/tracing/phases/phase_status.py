#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from zepben.evolve.model.cim.iec61970.base.core.phase_code import phase_code_from_single_phases, PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

if TYPE_CHECKING:
    from zepben.evolve import Terminal, UnsupportedOperationException


class PhaseStatus:

    terminal: Terminal

    def __init__(self, terminal: Terminal):
        self._terminal = terminal

        self._phase_status_internal = SinglePhaseKind.NONE

    def __getitem__(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        Get the traced phase for the specified `nominal_phase`.

        `nominal_phase` The nominal phase you are interested in querying.

        Returns the traced phase.
        """
        return self.get(nominal_phase)

    def __setitem__(self, nominal_phase: SinglePhaseKind, traced_phase: SinglePhaseKind) -> bool:
        """
        Set the traced phase for the specified `nominal_phase`.

        `nominal_phase` The nominal phase you are interested in updating.

        `traced_phase` The phase you wish to set for this `nominal_phase`. Specify `SinglePhaseKind.NONE` to clear the phase.

        Returns True if the phase is updated, otherwise False.
        """
        return self._terminal.normal_phases.set(nominal_phase, traced_phase)

    def get(self, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self._phase_status_internal

    def set(self, nominal_phase: SinglePhaseKind, single_phase_kind: SinglePhaseKind) -> bool:
        if nominal_phase == single_phase_kind:
            return False
        elif SinglePhaseKind.NONE in (nominal_phase, single_phase_kind):
            # TODO: Add phase to internal
            return True
        else:
            raise UnsupportedOperationException(f'Crossing phases [({nominal_phase}) ({single_phase_kind})')


    def as_phase_code(self) -> Optional[PhaseCode]:
        """
        Get the traced phase for each nominal phase as a `PhaseCode`.

        Returns The `PhaseCode` if the combination of phases makes sense, otherwise `None`.
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

