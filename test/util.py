"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from __future__ import annotations
from zepben.cimbend import Terminal, Direction
from zepben.protobuf.cim.iec61970 import SinglePhaseKind
from typing import List


def get_terminal(network, mrid, term_num):
    return network[mrid].terminals[term_num]


def check_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[Direction]):
    check_expected_phases(t, expected_spks, expected_directions, t.current_phases)
    check_expected_phases(t, expected_spks, expected_directions, t.normal_phases)


def check_expected_current_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[Direction]):
    check_expected_phases(t, expected_spks, expected_directions, t.current_phases)


def check_expected_normal_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[Direction]):
    check_expected_phases(t, expected_spks, expected_directions, t.normal_phases)


def check_expected_phases(t: Terminal, expected_spks: List[SinglePhaseKind], expected_directions: List[Direction],
                          phase_selector):
    assert t is not None
    assert len(expected_spks) == len(expected_directions), "Test requires a direction supplied for each phase only"
    assert len(expected_spks) == t.num_cores, "Test requires the same number of SinglePhaseKinds as terminal's num_cores"
    for (i, spk), d in zip(enumerate(expected_spks), expected_directions):
        ps = phase_selector(i)
        assert spk == ps.phase(), f"expected: {spk} got: {ps.phase()}"
        assert d == ps.direction(), f"expected: {d} got: {ps.direction()}"
