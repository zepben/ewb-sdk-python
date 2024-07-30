#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
from typing import List

from zepben.evolve import current_phases, normal_phases


def get_terminal(network, mrid, term_num):
    return network[mrid].terminals[term_num]


def check_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[PhaseDirection]):
    check_expected_phases(t, expected_spks, expected_directions, current_phases)
    check_expected_phases(t, expected_spks, expected_directions, normal_phases)


def check_expected_current_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[PhaseDirection]):
    check_expected_phases(t, expected_spks, expected_directions, current_phases)


def check_expected_normal_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[PhaseDirection]):
    check_expected_phases(t, expected_spks, expected_directions, normal_phases)


def check_expected_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[PhaseDirection],
                          phase_selector):
    assert t is not None
    assert len(expected_spks) == len(expected_directions), "Test requires a direction supplied for each phase only"
    assert len(expected_spks) == t.num_cores, "Test requires the same number of SinglePhaseKinds as terminal's num_cores"
    for spk, d in zip(expected_spks, expected_directions):
        ps = phase_selector(t, spk)
        assert spk == ps.phase(), f"expected: {spk} got: {ps.phase()}"
        assert d == ps.direction(), f"expected: {d} got: {ps.direction()}"
