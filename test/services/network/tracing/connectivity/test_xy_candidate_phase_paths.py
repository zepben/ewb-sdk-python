#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from collections import Counter

import pytest

from zepben.evolve import XyCandidatePhasePaths, SinglePhaseKind as Phase, PhaseCode


class TestXyCandidatePhasePaths:
    """
    Test suite for `XyCandidatePhasePaths`
    """

    def test_uses_known_over_candidates(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.X, Phase.A)
        candidates.add_known(Phase.Y, Phase.B)

        candidates.add_candidates(Phase.X, [Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.B)

    def test_handles_duplicate_known(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.X, Phase.B)
        candidates.add_known(Phase.Y, Phase.B)

        self._validate_paths(candidates, Phase.B, Phase.NONE)

    def test_uses_candidates_if_unknown(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.X, Phase.A)
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.B)

        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.X, Phase.B)
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A])
        candidates.add_known(Phase.Y, Phase.B)

        self._validate_paths(candidates, Phase.A, Phase.B)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A])
        candidates.add_known(Phase.Y, Phase.A)

        self._validate_paths(candidates, Phase.NONE, Phase.A)

    def test_candidates_use_most_common(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.A, Phase.A, Phase.B, Phase.B, Phase.C])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.C)

    def test_candidates_use_priority_with_duplicate_most_common(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.NONE)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.NONE, Phase.C)

    def test_handles_no_candidates(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        self._validate_paths(candidates, Phase.NONE, Phase.NONE)

        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.X, Phase.B)

        self._validate_paths(candidates, Phase.B, Phase.NONE)

        candidates = XyCandidatePhasePaths()
        candidates.add_known(Phase.Y, Phase.B)

        self._validate_paths(candidates, Phase.NONE, Phase.B)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.B])

        self._validate_paths(candidates, Phase.B, Phase.NONE)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.Y, [Phase.B])

        self._validate_paths(candidates, Phase.NONE, Phase.B)

    def test_uses_most_common_candidate(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.A, Phase.B, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.B)

    def test_duplicate_candidate_occurrences_between_xy_resolved_by_priority(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.A, Phase.B, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.B)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B, Phase.B, Phase.C, Phase.C])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.C, Phase.C])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.A, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.C, Phase.C])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.C, Phase.C])

        self._validate_paths(candidates, Phase.C, Phase.NONE)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.B, Phase.B, Phase.C])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B, Phase.C])

        self._validate_paths(candidates, Phase.B, Phase.C)

    def test_only_candidates_take_priority_over_occurrences(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        candidates.add_candidates(Phase.X, [Phase.A, Phase.B, Phase.B, Phase.B])
        candidates.add_candidates(Phase.Y, [Phase.B, Phase.B])

        self._validate_paths(candidates, Phase.A, Phase.B)

    def test_only_tracks_xy(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        for phase in Phase:
            if phase in PhaseCode.XY:
                candidates.add_known(phase, Phase.B)
                candidates.add_candidates(phase, [Phase.B])
            else:
                with pytest.raises(ValueError, match=re.escape(f"Unable to track phase {phase}, expected X or Y.")):
                    candidates.add_known(phase, Phase.B)

                with pytest.raises(ValueError, match=re.escape(f"Unable to track phase {phase}, expected X or Y.")):
                    candidates.add_candidates(phase, [Phase.B])

    def test_validates_candidate_phases(self):
        """
        """
        candidates = XyCandidatePhasePaths()
        for phase in Phase:
            if phase == Phase.A:
                candidates.add_candidates(Phase.X, [phase])

                with pytest.raises(ValueError, match=re.escape(f"Unable to use phase {phase} as a candidate, expected B or C.")):
                    candidates.add_candidates(Phase.Y, [phase])
            elif phase in PhaseCode.BC:
                candidates.add_candidates(Phase.X, [phase])
                candidates.add_candidates(Phase.Y, [phase])
            else:
                with pytest.raises(ValueError, match=re.escape(f"Unable to use phase {phase} as a candidate, expected A, B or C.")):
                    candidates.add_candidates(Phase.X, [phase])

                with pytest.raises(ValueError, match=re.escape(f"Unable to use phase {phase} as a candidate, expected B or C.")):
                    candidates.add_candidates(Phase.Y, [phase])

    @staticmethod
    def _validate_paths(candidates: XyCandidatePhasePaths, expected_x: Phase, expected_y: Phase):
        assert Counter(candidates.calculate_paths()) == Counter({Phase.X: expected_x, Phase.Y: expected_y})
