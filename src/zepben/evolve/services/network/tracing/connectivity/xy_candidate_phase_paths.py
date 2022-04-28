#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from itertools import takewhile
from typing import List, Dict, Tuple, Optional, Counter as CounterType

from dataclassy import dataclass

from zepben.evolve import SinglePhaseKind, PhaseCode

__all__ = ["X_PRIORITY", "Y_PRIORITY", "XyCandidatePhasePaths", "is_before", "is_after"]

X_PRIORITY = [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C]
"""
The pathing priority for nominal phase X
 """

Y_PRIORITY = [SinglePhaseKind.C, SinglePhaseKind.B]
"""
The pathing priority for nominal phase X
 """


def is_before(phase: SinglePhaseKind, before: Optional[SinglePhaseKind]) -> bool:
    if (before is None) or (before == SinglePhaseKind.NONE):
        return True
    elif before == SinglePhaseKind.A:
        return False
    elif before == SinglePhaseKind.B:
        return phase == SinglePhaseKind.A
    elif before == SinglePhaseKind.C:
        return (phase == SinglePhaseKind.A) or (phase == SinglePhaseKind.B)
    else:
        raise ValueError("INTERNAL ERROR: is_before should only ever be checking against valid Y phases. If you get this message you need to ask the dev "
                         "team to go put the planets back into alignment as they stuffed something up!")


def is_after(phase: SinglePhaseKind, after: Optional[SinglePhaseKind]) -> bool:
    if (after is None) or (after == SinglePhaseKind.NONE):
        return True
    elif after == SinglePhaseKind.C:
        return False
    elif after == SinglePhaseKind.B:
        return phase == SinglePhaseKind.C
    elif after == SinglePhaseKind.A:
        return (phase == SinglePhaseKind.C) or (phase == SinglePhaseKind.B)
    else:
        raise ValueError("INTERNAL ERROR: is_after should only ever be checking against valid X phases. If you get this message you need to ask the dev "
                         "team to go put the planets back into alignment as they stuffed something up!")


@dataclass(slots=True)
class XyCandidatePhasePaths:
    """
    Used to track the candidate and know paths for XY phase connectivity.
    """

    _known_tracking: Dict[SinglePhaseKind, SinglePhaseKind] = {}
    """
    Map of nominal phase to known phase.
    """

    _candidate_tracking: Dict[SinglePhaseKind, List[SinglePhaseKind]] = {}
    """
    Map of nominal phase to list of candidate phases.
    """

    def add_known(self, xy_phase: SinglePhaseKind, known_phase: SinglePhaseKind):
        """
        Add a `known_phase` for the specified `xy_phase`. If there is already a `known_phase` the new value will be ignored.

        `xy_phase` The phase that is being tracked.

        `known_phase` The phase that should be allocated to the tracked phase.

        Raises `NominalPhaseException` if the `xy_phase` is invalid.
        """
        _validate_for_tracking(xy_phase)
        if xy_phase not in self._known_tracking:
            self._known_tracking[xy_phase] = known_phase

    def add_candidates(self, xy_phase: SinglePhaseKind, candidate_phases: List[SinglePhaseKind]):
        """
        Add `candidate_phases` for the specified `xy_phase`. If the same candidate has been found from more than
        one path it should be added multiple times

        `xy_phase` The phase that is being tracked.

        `candidate_phases` The phases that could be allocated to the tracked phase.

        Raises `NominalPhaseException` if the `xy_phase` is invalid.

        Raises `PhaseException` if the `candidate_phases` is invalid.
         """
        _validate_for_tracking(xy_phase)
        if xy_phase not in self._candidate_tracking:
            self._candidate_tracking[xy_phase] = []

        self._candidate_tracking[xy_phase].extend([it for it in candidate_phases if _is_valid_candidate(it, xy_phase)])

    def calculate_paths(self) -> Dict[SinglePhaseKind, SinglePhaseKind]:
        """
        Calculate the paths for the tracked phases taking into account the following:
        1. Known phases take preference.
        2. X is always a "lower" phase than Y.
        3. If multiple candidates are valid then the one with the most occurrences will be chosen.
        4. If multiple candidates are valid and are equally common, the phases will be chosen with the following priority maintaining the above rules:
           X: A, B then C
           Y: C then B
        """
        paths = {}

        known_x = self._known_tracking.get(SinglePhaseKind.X)
        if known_x is not None:
            paths[SinglePhaseKind.X] = known_x

        known_y = self._known_tracking.get(SinglePhaseKind.Y)
        if (known_y is not None) and (known_x != known_y):
            paths[SinglePhaseKind.Y] = known_y
        else:
            known_y = None

        if (known_x is not None) and (known_y is not None):
            return paths

        candidate_phase_counts = {xy: Counter(candidates) for xy, candidates in self._candidate_tracking.items()}
        if known_x is not None:
            candidates = candidate_phase_counts.get(SinglePhaseKind.Y)
            if candidates:
                paths[SinglePhaseKind.Y] = self._find_candidate(candidates, priority=Y_PRIORITY, after=known_x)
            else:
                paths[SinglePhaseKind.Y] = SinglePhaseKind.NONE
        elif known_y is not None:
            candidates = candidate_phase_counts.get(SinglePhaseKind.X)
            if candidates:
                paths[SinglePhaseKind.X] = self._find_candidate(candidates, priority=X_PRIORITY, before=known_y)
            else:
                paths[SinglePhaseKind.X] = SinglePhaseKind.NONE
        else:
            x_candidate, y_candidate = self._process_candidates(candidate_phase_counts)
            paths[SinglePhaseKind.X] = x_candidate
            paths[SinglePhaseKind.Y] = y_candidate

        return paths

    def _process_candidates(self, candidate_phase_counts: Dict[SinglePhaseKind, CounterType[SinglePhaseKind]]) -> Tuple[SinglePhaseKind, SinglePhaseKind]:
        candidate_x_counts = candidate_phase_counts.get(SinglePhaseKind.X, Counter())
        candidate_y_counts = candidate_phase_counts.get(SinglePhaseKind.Y, Counter())

        if not candidate_x_counts:
            return SinglePhaseKind.NONE, self._find_candidate(candidate_y_counts, priority=Y_PRIORITY)
        elif len(candidate_x_counts) == 1:
            x_candidate = list(candidate_x_counts.keys())[0]
            return x_candidate, self._find_candidate(candidate_y_counts, priority=Y_PRIORITY, after=x_candidate)
        elif not candidate_y_counts:
            return self._find_candidate(candidate_x_counts, priority=X_PRIORITY), SinglePhaseKind.NONE
        elif len(candidate_y_counts) == 1:
            y_candidate = list(candidate_y_counts.keys())[0]
            return self._find_candidate(candidate_x_counts, priority=X_PRIORITY, before=y_candidate), y_candidate
        else:
            x_candidate = self._find_candidate(candidate_x_counts, priority=X_PRIORITY)
            y_candidate = self._find_candidate(candidate_y_counts, priority=Y_PRIORITY)

            if is_before(x_candidate, y_candidate):
                return x_candidate, y_candidate
            elif candidate_x_counts[x_candidate] > candidate_y_counts[y_candidate]:
                return x_candidate, self._find_candidate(candidate_y_counts, priority=Y_PRIORITY, after=x_candidate)
            elif candidate_y_counts[y_candidate] > candidate_x_counts[x_candidate]:
                return self._find_candidate(candidate_x_counts, priority=X_PRIORITY, before=y_candidate), y_candidate
            else:
                x_candidate2 = self._find_candidate(candidate_x_counts, priority=X_PRIORITY, before=y_candidate)
                y_candidate2 = self._find_candidate(candidate_y_counts, priority=Y_PRIORITY, after=x_candidate)

                if x_candidate2 == SinglePhaseKind.NONE:
                    return x_candidate, y_candidate2
                elif y_candidate2 == SinglePhaseKind.NONE:
                    return x_candidate2, y_candidate
                elif candidate_x_counts[x_candidate2] > candidate_y_counts[y_candidate2]:
                    return x_candidate2, y_candidate
                elif candidate_y_counts[y_candidate2] > candidate_x_counts[x_candidate2]:
                    return x_candidate, y_candidate2
                else:
                    return x_candidate, y_candidate2

    @staticmethod
    def _find_candidate(
        candidate_counts: CounterType[SinglePhaseKind],
        priority: List[SinglePhaseKind],
        before: Optional[SinglePhaseKind] = None,
        after: Optional[SinglePhaseKind] = None
    ) -> SinglePhaseKind:
        valid_candidates = [(phase, count) for (phase, count) in candidate_counts.most_common() if is_before(phase, before) and is_after(phase, after)]
        if not valid_candidates:
            return SinglePhaseKind.NONE
        elif len(valid_candidates) == 1:
            return valid_candidates[0][0]

        candidates = list(takewhile(lambda cand: cand[1] == valid_candidates[0][1], valid_candidates))
        if len(candidates) == 1:
            return candidates[0][0]

        for phase in priority:
            for candidate, _ in candidates:
                if candidate == phase:
                    return candidate

        raise ValueError("INTERNAL ERROR: If you get here it means you did not limit the candidates to only valid phases, go fix that!")


def _validate_for_tracking(phase: SinglePhaseKind):
    if phase not in PhaseCode.XY:
        raise ValueError(f"Unable to track phase {phase}, expected X or Y.")


def _is_valid_candidate(phase: SinglePhaseKind, xy_phase: SinglePhaseKind) -> bool:
    if xy_phase == SinglePhaseKind.X:
        return _is_valid_candidate_x(phase)
    else:
        return _is_valid_candidate_y(phase)


def _is_valid_candidate_x(phase: SinglePhaseKind) -> bool:
    if phase in PhaseCode.ABC:
        return True
    else:
        raise ValueError(f"Unable to use phase {phase} as a candidate, expected A, B or C.")


def _is_valid_candidate_y(phase: SinglePhaseKind) -> bool:
    if phase in PhaseCode.BC:
        return True
    else:
        raise ValueError(f"Unable to use phase {phase} as a candidate, expected B or C.")
