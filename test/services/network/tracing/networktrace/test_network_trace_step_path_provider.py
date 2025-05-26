#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, Iterable

from pytest_subtests.plugin import subtests

from services.network.test_data.cuts_and_clamps_network import _segment_with_clamp, _segment_with_cut, CutsAndClampsNetwork
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve import NetworkStateOperators, TestNetworkBuilder, NetworkTraceStep, Terminal, NominalPhasePath, Breaker, AcLineSegment, Clamp, Cut, \
    ConductingEquipment
from zepben.evolve.services.network.tracing.networktrace.network_trace_step_path_provider import NetworkTraceStepPathProvider

class PathTerminal(Terminal):
    def __add__(self, other: Terminal) -> NetworkTraceStep.Path:
        """
        allows shorthand notation to create a NetworkTraceStep.Path between 2 terminals. Eg: j0[1]+c1[1]
        """
        return NetworkTraceStep.Path(self, other, None)

    def __sub__(self, other: Terminal) -> NetworkTraceStep.Path:
        """
        allows shorthand notation to create a NetworkTraceStep.Path that traversed an AcLineSegment betweenm 2 terminals. Eg: c1[1]-clamp1[1]
        """
        def traversed_ce(ce):
            if isinstance(ce, AcLineSegment):
                return ce
            elif isinstance(ce, (Clamp, Cut)):
                return ce.ac_line_segment
            else:
                raise TypeError('Did not traverse')
        return NetworkTraceStep.Path(self, other, traversed_ce(self.conducting_equipment))

Terminal.__add__ = PathTerminal.__add__
Terminal.__sub__ = PathTerminal.__sub__

SPK = SinglePhaseKind

class TestNetworkTraceStepPathProvider:
    path_provider = NetworkTraceStepPathProvider(NetworkStateOperators.NORMAL)

    def test_current_external_path_steps_internally(self):
        #
        #            2
        # 1--c0--2 1 j1
        #            3
        #
        network = (TestNetworkBuilder()
                   .from_acls()  # c0
                   .to_junction(num_terminals=3)  # j1
                   ).network

        c0 = network['c0']
        j1 = network['j1']

        current_path = c0[2] + j1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (j1[1] + j1[2], j1[1] + j1[3]))

    def test_current_internal_path_steps_externally(self):
        #
        # 1 j0 21--c1--2
        #      1
        #      c2
        #      2
        #
        network = (TestNetworkBuilder()
                   .from_junction()  # j0
                   .to_acls()  # c1
                   .from_acls()  # c2
                   .connect('j0', 'c2', 2, 1)
                   ).network

        j0 = network['j0']
        c1 = network['c1']
        c2 = network['c2']

        current_path = j0[1] + j0[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (j0[2] + c1[1], j0[2] + c2[1]))

    def test_only_steps_to_in_service_equipment(self):
        #
        # 1 j0 21--c1--2
        #      1
        #      c2 (not in service)
        #      2
        #
        network = (TestNetworkBuilder()
                   .from_junction()  # j0
                   .to_acls()  # c1
                   .from_acls()  # c2
                   .connect('j0', 'c2', 2, 1)
                   ).network

        network['c2'].normally_in_service = False

        j0 = network['j0']
        c1 = network['c1']

        current_path = j0[1] + j0[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (j0[2] + c1[1], ) )

    def test_only_includes_followed_phases(self):
        #
        #            2 (A)
        # 1--c0--21 tx1 3 (B)
        #            4 (C)
        #
        network = (TestNetworkBuilder()
                   .from_acls()  # c0
                   .to_power_transformer([PhaseCode.ABC, PhaseCode.A, PhaseCode.B, PhaseCode.C])
                   ).network

        c0 = network['c0']
        tx1 = network['tx1']

        current_path = NetworkTraceStep.Path(c0[2], tx1[1], None, {NominalPhasePath(SPK.A, SPK.A), NominalPhasePath(SPK.B, SPK.B)})
        next_paths = self.path_provider.next_paths(current_path)

        # Should not contain tx1-t4 because its not in the phase paths
        _verify_paths(next_paths, [
            NetworkTraceStep.Path(tx1[1], tx1[2], None, {NominalPhasePath(SPK.A, SPK.A)}),
            NetworkTraceStep.Path(tx1[1], tx1[3], None, {NominalPhasePath(SPK.B, SPK.B)})])

    def test_stepping_externally_to_connectivity_node_with_busbars_only_goes_to_busbars(self):
        network = self._busbar_network()

        b0 = network['b0']
        bbs1 = network['bbs1']
        bbs2 = network['bbs2']

        current_path = b0[1] + b0[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (b0[2] + bbs1[1], b0[2] + bbs2[1]))

    def test_steppiong_externally_from_busbars_does_not_step_to_busbars_or_original_from_terminal(self):
        network = self._busbar_network()

        bbs1 = network['bbs1']
        b0= network['b0']
        b3 = network['b3']
        b4 = network['b4']
        b5 = network['b5']
        b6 = network['b6']

        current_path = b0[2] + bbs1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (bbs1[1] + b3[1], bbs1[1] + b4[1], bbs1[1] + b5[1], bbs1[1] + b6[1]))

    def test_traversing_segment_with_clamps_from_t1_includes_all_clamp_steps(self):
        network = self._acls_with_clamps_network()

        breaker = network['b0']
        segment: AcLineSegment = network['c1']
        clamp1 = network['clamp1']
        clamp2 = network['clamp2']

        current_path = breaker[2] + segment[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (segment[1] - clamp1[1], segment[1] - clamp2[1], segment[1] - segment[2]))

    def test_traversing_segment_with_clamps_from_t2_includes_all_clamp_steps(self):
        network = self._acls_with_clamps_network()

        breaker = network['b2']
        segment: AcLineSegment = network['c1']
        clamp1 = network['clamp1']
        clamp2 = network['clamp2']

        current_path = breaker[1] + segment[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (segment[2] - clamp2[1], segment[2] - clamp1[1], segment[2] - segment[1]))

    def test_non_traverse_step_to_segment_t1_traverses_towards_t2_stopping_at_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        b0 = network['b0']
        segment = network['c1']
        clamp1 = network['clamp1']
        cut1 = network['cut1']

        current_path = b0[2] + segment[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (segment[1] - clamp1[1], segment[1] - cut1[1]))

    def test_non_traverse_step_to_segment_t2_traverses_towards_t1_stopping_at_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        b2 = network['b2']
        segment = network['c1']
        clamp4 = network['clamp4']
        cut2 = network['cut2']

        current_path = b2[1] + segment[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (segment[2] - clamp4[1], segment[2] - cut2[2]))

    def test_traverse_step_to_cut_t1_steps_externally_and_across_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        cut1 = network['cut1']
        c4 = network['c4']

        current_path = segment[1] - cut1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut1[1] + cut1[2], cut1[1] + c4[1]))

    def test_traverse_step_to_cut_t2_steps_externally_and_across_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        cut2 = network['cut2']
        c9 = network['c9']

        current_path = segment[2] - cut2[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut2[2] + cut2[1], cut2[2] + c9[1]))

    def test_non_traverse_step_to_cut_t1_traverses_segment_towards_t1_and_internally_through_cut_to_t2(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        clamp1 = network['clamp1']
        cut1 = network['cut1']
        c4 = network['c4']

        current_path = c4[1] + cut1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut1[1] - clamp1[1], cut1[1] - segment[1], cut1[1] + cut1[2]))

    def test_non_traverse_step_to_cut_t2_traverses_segment_towards_t2_and_internally_through_cut_to_t1(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        clamp4 = network['clamp4']
        cut2 = network['cut2']
        c9 = network['c9']

        current_path = c9[1] + cut2[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut2[2] - clamp4[1], cut2[2] - segment[2], cut2[2] + cut2[1]))

    def test_non_traverse_step_to_clamp_traverses_segment_in_both_directions(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        clamp1 = network['clamp1']
        cut1 = network['cut1']
        c3 = network['c3']

        current_path = c3[1] + clamp1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (clamp1[1] - segment[1], clamp1[1] - cut1[1]))

    def test_traverse_step_to_clamp_traces_externally_and_does_not_traverse_back_along_segment(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        segment = network['c1']
        clamp1 = network['clamp1']
        c3 = network['c3']

        current_path = segment[1] - clamp1[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (clamp1[1] + c3[1], ))

    def test_non_traverse_step_to_clamp_between_cuts_traverses_segment_both_ways_stopping_at_cuts(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c6 = network['c6']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        cut1 = network['cut1']
        cut2 = network['cut2']

        current_path = c6[1] + clamp2[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (clamp2[1] - cut1[2], clamp2[1] - clamp3[1], clamp2[1] - cut2[1]))

    def test_non_traverse_external_step_to_cut_t2_between_cuts_traverses_segment_towards_t2_stopping_at_next_cut_and_steps_internally_to_cut_t1(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c5 = network['c5']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        cut1 = network['cut1']
        cut2 = network['cut2']

        current_path = c5[1] + cut1[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut1[2] - clamp2[1], cut1[2] - clamp3[1], cut1[2] - cut2[1], cut1[2] + cut1[1]))

    def test_non_traverse_external_step_to_cut_t1_between_cuts_traverses_segment_towards_t1_stopping_at_next_cut_and_steps_internally_to_cut_t2(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c8 = network['c8']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        cut1 = network['cut1']
        cut2 = network['cut2']

        current_path = c8[1] + cut2[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut2[1] - clamp3[1], cut2[1] - clamp2[1], cut2[1] - cut1[2], cut2[1] + cut2[2]))

    def test_internal_step_to_cut_t2_between_cuts_steps_externally_and_traverses_segment_towards_t2_stopping_at_the_next_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c5 = network['c5']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        cut1 = network['cut1']
        cut2 = network['cut2']

        current_path = cut1[1] + cut1[2]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut1[2] - clamp2[1], cut1[2] - clamp3[1], cut1[2] - cut2[1], cut1[2] + c5[1]))

    def test_internal_step_to_cut_t1_between_cuts_steps_externally_and_traverses_segment_towards_t1_stopping_at_the_next_cut(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c8 = network['c8']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        cut1 = network['cut1']
        cut2 = network['cut2']

        current_path = cut2[2] + cut2[1]
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (cut2[1] - clamp2[1], cut2[1] - clamp3[1], cut2[1] - cut1[2], cut2[1] + c8[1]))

    def test_starting_on_clamp_terminal_flagged_as_traversed_segment_only_steps_externally(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c3 = network['c3']
        clamp1 = network['clamp1']

        next_paths = self.path_provider.next_paths(clamp1[1] - clamp1[1])
        _verify_paths(next_paths, (clamp1[1] + c3[1], ))

    def test_starting_on_clamp_terminal_that_flagged_as_not_traversed_segment_steps_externally_and_traverses(self):
        network = CutsAndClampsNetwork.multi_cut_and_clamp_network().network

        c3 = network['c3']
        clamp1 = network['clamp1']
        cut1 = network['cut1']
        c1 = network['c1']

        next_paths = self.path_provider.next_paths(clamp1[1] + clamp1[1])
        _verify_paths(next_paths, (clamp1[1] + c3[1], clamp1[1] - c1[1], clamp1[1] - cut1[1]))

    def test_traverse_with_cut_with_unknown_length_from_t1_does_not_return_clamp_with_known_length_from_t1(self, subtests):
        #
        # (Cut with null length is treated as 0.0
        # 1 b0 21*1 cut1 2*-c1-*-21 b2 2
        #                      1
        #                      clamp1
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   ).network

        c1 = network['c1']
        b0 = network['b0']
        b2 = network['b2']

        clamp = _segment_with_clamp(network, c1, 1.0)
        cut = _segment_with_cut(network, c1, None)

        with subtests.test('Traverse from T1 towards T2'):
            current_path = b0[2] + c1[1]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[1] - cut[1], ))

        with subtests.test('Traverse from T2 towards T1'):
            current_path = b2[1] + c1[2]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[2] - clamp[1], c1[2] - cut[2]))

    def test_multiple_cuts_at_same_positions_step_to_all_cuts_at_that_position(self, subtests):
        #
        #            *1 cut2 2*
        # 1 b0 21-c1-*1 cut1 2*-c1-*-21 b2 2
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   ).network

        c1 = network['c1']
        b0 = network['b0']
        b2 = network['b2']

        cut1 = _segment_with_cut(network, c1, 1.0)
        cut2 = _segment_with_cut(network, c1, 1.0)

        with subtests.test('Traverse from T1 towards T2 should have both cuts t1'):
            current_path = b0[2] + c1[1]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[1] - cut1[1], c1[1] - cut2[1]))

        with subtests.test('Traverse from T2 towards T1 should have both cuts t2'):
            current_path = b2[1] + c1[2]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[2] - cut1[2], c1[2] - cut2[2]))

        with subtests.test('Internal step on cut1 t1 to t2 has cut2.t2 and traverses towards segment T2'):
            current_path = cut1[1] + cut1[2]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (cut1[2] - c1[2], cut1[2] - cut2[2]))

        with subtests.test('Internal step on cut1 t2 to t1 traverses towards segment T2'):
            current_path = cut1[2] + cut1[1]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (cut1[1] - c1[1], cut1[1] - cut2[1]))

    def test_cut_and_clamp_without_length_only_returns_clamp_on_T1_side_of_cut(self, subtests):
        #
        # 1 b0 21*1 cut1 2*-c1-*-21 b2 2
        #        1
        #        clamp1
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   ).network

        c1 = network['c1']
        b0 = network['b0']
        b2 = network['b2']

        clamp = _segment_with_clamp(network, c1, None)
        cut = _segment_with_cut(network, c1, None)

        with subtests.test('Traverse from T1 towards T2'):
            current_path = b0[2] + c1[1]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[1] - cut[1], c1[1] - clamp[1]))

        with subtests.test('Traverse from T2 towards T1'):
            current_path = b2[1] + c1[2]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (c1[2] - cut[2], ))

        with subtests.test('Internally stepped on cut T1 to T2, traverse towards c1.t2'):
            current_path = cut[1] + cut[2]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (cut[2] - c1[2], ))

        with subtests.test('Internally stepped on cut T2 to T2, traverse towards c1.t1'):
            current_path =cut[2] + cut[1]
            next_paths = self.path_provider.next_paths(current_path)
            _verify_paths(next_paths, (cut[1] - c1[1], cut[1] - clamp[1]))

    def test_multiple_clamps_at_same_position_does_not_return_the_other_clamps_more_then_once(self):
        # (Cut with None length is treated as 0.0
        #        clamp2
        #        1
        # 1 b0 21*1 cut1 2*-c1-*-21 b2 2
        #        1
        #        clamp1
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   ).network

        c1 = network['c1']

        clamp1 = _segment_with_clamp(network, c1, None)
        clamp2 = _segment_with_clamp(network, c1, None)
        cut = _segment_with_cut(network, c1, None)

        next_paths = self.path_provider.next_paths(clamp1[1] + clamp1[1])
        _verify_paths(next_paths, (clamp1[1] - c1[1], clamp1[1] - clamp2[1], clamp1[1] - cut[1]))

    def test_unrealistic_cuts_and_clamps_network_doesnt_break_the_pathing_algorith(self, subtests):
        network = self._acls_with_clamps_and_cuts_at_same_position_network()

        b0 = network['b0']
        b2 = network['b2']
        c1 = network['c1']
        clamp1 = network['clamp1']
        clamp2 = network['clamp2']
        clamp3 = network['clamp3']
        clamp4 = network['clamp4']
        clamp5 = network['clamp5']
        clamp6 = network['clamp6']
        cut1 = network['cut1']
        cut2 = network['cut2']
        cut3 = network['cut3']
        cut4 = network['cut4']
        cut5 = network['cut5']
        cut6 = network['cut6']
        cClamp1 = network['c-clamp1']
        cCut1t1 = network['c-cut1t1']
        cCut1t2 = network['c-cut1t2']
        cClamp3 = network['c-clamp3']
        cCut3t1 = network['c-cut3t1']
        cCut3t2 = network['c-cut3t2']
        cClamp5 = network['c-clamp5']
        cCut5t1 = network['c-cut5t1']
        cCut5t2 = network['c-cut5t2']
        
        with subtests.test("traverse from c1.t1 should get clamps at start and stop at both cuts at start"):
            next_paths = self.path_provider.next_paths(b0[2] + c1[1])
            _verify_paths(next_paths, (c1[1] - clamp1[1], c1[1] - clamp2[1], c1[1] - cut1[1], c1[1] - cut2[1]))

        with subtests.test('traverse from clamp1.t1 should traverse to other clamp at start, stop at both cuts at start and c1.t1'):
            next_paths = self.path_provider.next_paths(cClamp1[1] + clamp1[1])
            _verify_paths(next_paths, (clamp1[1] - clamp2[1], clamp1[1] - c1[1], clamp1[1] - cut1[1], clamp1[1] - cut2[1]))

        with subtests.test("traverse from cut1.t1 (external) should traverse to cut2.t1, clamps at start, c1.t1 and internally step to cut1.t2"):
            next_paths = self.path_provider.next_paths(cCut1t1[1] + cut1[1])
            _verify_paths(next_paths, (cut1[1] - cut2[1], cut1[1] - clamp1[1], cut1[1] - clamp2[1], cut1[1] - c1[1], cut1[1] + cut1[2]))

        with subtests.test("traverse from cut1.t1 (internal) should traverse to cut2.t1, clamps at start, c1.t1 and step to cCut1"):
            next_paths = self.path_provider.next_paths(cut1[2] + cut1[1])
            _verify_paths(next_paths, (cut1[1] - cut2[1], cut1[1] - clamp1[1], cut1[1] - clamp2[1], cut1[1] - c1[1], cut1[1] + cCut1t1[1]))

        with subtests.test("traverse from cut1.t2 (external) should traverse to cut2.t2, middle cuts, middle clamps, internally step to c1.t1"):
            next_paths = self.path_provider.next_paths(cCut1t2[1] + cut1[2])
            _verify_paths(next_paths, (cut1[2] - cut2[2], cut1[2] - clamp3[1], cut1[2] - clamp4[1], cut1[2] - cut3[1], cut1[2] - cut4[1], cut1[2] + cut1[1]))

        with subtests.test("traverse from cut1.t2 (internal) should traverse to cut2.t2, middle cuts, middle clamps and externally to cCut1t2"):
            next_paths = self.path_provider.next_paths(cut1[1] + cut1[2])
            _verify_paths(next_paths, (cut1[2] - cut2[2], cut1[2] - clamp3[1], cut1[2] - clamp4[1], cut1[2] - cut3[1], cut1[2] - cut4[1], cut1[2] + cCut1t2[1]))

        with subtests.test("traverse from middle clamp (clamp3) should traverse to cuts at start, middle cuts, and other middle clamp"):
            next_paths = self.path_provider.next_paths(cClamp3[1] + clamp3[1])
            _verify_paths(next_paths, (clamp3[1] - cut1[2], clamp3[1] - cut2[2], clamp3[1] - cut3[1], clamp3[1] - cut4[1], clamp3[1] - clamp4[1]))

        with subtests.test("traverse from cut3.t1 (external) should traverse to cut4.t1, start cuts, middle clamps, and internally step to cut3.t2"):
            next_paths = self.path_provider.next_paths(cCut3t1[1] + cut3[1])
            _verify_paths(next_paths, (cut3[1] - cut4[1], cut3[1] - cut1[2], cut3[1] - cut2[2], cut3[1] - clamp3[1], cut3[1] - clamp4[1], cut3[1] + cut3[2]))

        with subtests.test("traverse from cut3.t1 (internal) should traverse to cut2.t1, clamps at start, middle clamp and step to cCut3t1"):
            next_paths = self.path_provider.next_paths(cut3[2] + cut3[1])
            _verify_paths(next_paths, (cut3[1] - cut4[1], cut3[1] - cut1[2], cut3[1] - cut2[2], cut3[1] - clamp3[1], cut3[1] - clamp4[1], cut3[1] + cCut3t1[1]))

        with subtests.test("traverse from cut3.t2 (external) should traverse to cut4.t2, end cuts, end clamps and internally step to cut3.t1"):
            next_paths = self.path_provider.next_paths(cCut3t2[1] + cut3[2])
            _verify_paths(next_paths, (cut3[2] - cut4[2], cut3[2] - cut5[1], cut3[2] - cut6[1], cut3[2] - clamp5[1], cut3[2] - clamp6[1], cut3[2] + cut3[1]))

        with subtests.test("traverse from cut3.t2 (internal) should traverse to cut4.t2, end cuts, end clamps and externally to cut3t2"):
            next_paths = self.path_provider.next_paths(cut3[1] + cut3[2])
            _verify_paths(next_paths, (cut3[2] - cut4[2], cut3[2] - cut5[1], cut3[2] - cut6[1], cut3[2] - clamp5[1], cut3[2] - clamp6[1], cut3[2] + cCut3t2[1]))

        with subtests.test("traverse from end clamp (clamp5) should traverse to middle cuts, end cuts and other end clamp"):
            next_paths = self.path_provider.next_paths(cClamp5[1] + clamp5[1])
            _verify_paths(next_paths, (clamp5[1] - cut3[2], clamp5[1] - cut4[2], clamp5[1] - cut5[1], clamp5[1] - cut6[1], clamp5[1] - clamp6[1]))

        with subtests.test("traverse from cut5.t1 (external) should traverse to cut6.t1, middle cuts, end clamps, and internally step to cut5.t2"):
            next_paths = self.path_provider.next_paths(cCut5t1[1] + cut5[1])
            _verify_paths(next_paths, (cut5[1] - cut6[1], cut5[1] - cut3[2], cut5[1] - cut4[2], cut5[1] - clamp5[1], cut5[1] - clamp6[1], cut5[1] + cut5[2]))

        with subtests.test("traverse from cut5.t1 (internal) should traverse to cut6.t1, middle cuts, end clamps, and step to cCut5t1"):
            next_paths = self.path_provider.next_paths(cut5[2] + cut5[1])
            _verify_paths(next_paths, (cut5[1] - cut6[1], cut5[1] - cut3[2], cut5[1] - cut4[2], cut5[1] - clamp5[1], cut5[1] - clamp6[1], cut5[1] + cCut5t1[1]))

        with subtests.test("traverse from cut5.t1 (external) should traverse to cut6.t2, c1.t2, and internally step out to cut5.t1"):
            next_paths = self.path_provider.next_paths(cCut5t2[2] + cut5[2])
            _verify_paths(next_paths, (cut5[2] - cut6[2], cut5[2] - c1[2], cut5[2] + cut5[1]))

        with subtests.test("traverse from cut5.t2 (internal) should traverse to cut6.t2, c1.t2, end step externally to cCut5t2"):
            next_paths = self.path_provider.next_paths(cut5[1] + cut5[2])
            _verify_paths(next_paths, (cut5[2] - cut6[2], cut5[2] - c1[2], cut5[2] + cCut5t2[1]))

        with subtests.test("traverse from c1.t2 should get cuts at end"):
            next_paths = self.path_provider.next_paths(b2[1] + c1[2])
            _verify_paths(next_paths, (c1[2] - cut5[2], c1[2] - cut6[2]))


    def _busbar_network(self) -> NetworkService:
        #        1
        #        b0
        # bbs1 1-2-1 bbs2
        # -----|   |-----
        # 1    1   1    1
        # b3   b4  b5   b6
        # 2    2   2    2
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_busbar_section()  # bbs1
                   .branch_from('b0', 2)
                   .to_busbar_section()  # bbs2
                   .branch_from('bbs1', 1)
                   .to_breaker()  # b3
                   .branch_from('bbs1', 1)
                   .to_breaker()  # b4
                   .branch_from('bbs2', 1)
                   .to_breaker()  # b5
                   .branch_from('bbs2', 1)
                   .to_breaker()  # b6
                   ).network

        bbs1 = network['bbs1']
        bbs2 = network['bbs2']
        b0: Breaker = network['b0']
        b3 = network['b3']
        b4 = network['b4']
        b5 = network['b5']
        b6 = network['b6']

        b0_terms = list(b0[2].connectivity_node.terminals)
        for term in (b0[2], bbs1[1], bbs2[1], b3[1], b4[1], b5[1], b6[1]):
            assert term in b0_terms

        return network

    def _acls_with_clamps_network(self) -> NetworkService:
        #
        #            clamp1
        #            1
        # 1 b0 21 ---*---c1---*---21 b2 2
        #                     1
        #                     clamp2
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   ).network
        segment: AcLineSegment = network['c1']

        _segment_with_clamp(network, segment, 1.0)
        _segment_with_clamp(network, segment, 2.0)

        return network

    def _acls_with_clamps_and_cuts_at_same_position_network(self) -> NetworkService:
        # Drawing this is very messy, so it will be described in writing:
        # The network has 2 Breakers (b0, b2) with an AcLineSegment (c1) between them ( 1 b0 21--c1--21 b2 1 )
        # There is then 2 Clamps and 2 Cuts at the following position on c1
        # * At the start (0.0) (clamp1, clamp2, cut1, cut2)
        # * In the middle (length 1.0) (clamp3, clamp4, cut3, cut4)
        # * At the end (length 2.0) (clamp5, clamp6, cut5, cut6)
        # On each clamp terminal there is a separate AcLineSegment connected to it. (ids of c-clampX)
        # On each cut terminal (both 1 and 2) there is a separate AcLineSegment connected to it. (ids of c-cutXtN)
        
        def acls_length(acls: AcLineSegment) -> None:
            acls.length = 2.0

        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls(action=acls_length)  # c1
                   .to_breaker()  # b2
                   .from_acls(mrid='c-clamp1')
                   .from_acls(mrid='c-clamp2')
                   .from_acls(mrid='c-cut1t1')
                   .from_acls(mrid='c-cut1t2')
                   .from_acls(mrid='c-cut2t1')
                   .from_acls(mrid='c-cut2t2')
                   .from_acls(mrid='c-clamp3')
                   .from_acls(mrid='c-clamp4')
                   .from_acls(mrid='c-cut3t1')
                   .from_acls(mrid='c-cut3t2')
                   .from_acls(mrid='c-cut4t1')
                   .from_acls(mrid='c-cut4t2')
                   .from_acls(mrid='c-clamp5')
                   .from_acls(mrid='c-clamp6')
                   .from_acls(mrid='c-cut5t1')
                   .from_acls(mrid='c-cut5t2')
                   .from_acls(mrid='c-cut6t1')
                   .from_acls(mrid='c-cut6t2')
                   ).network

        segment = network['c1']
        assert segment.length is not None

        clamp1 = _segment_with_clamp(network, segment, 0.0)
        clamp2 = _segment_with_clamp(network, segment, None)
        cut1 = _segment_with_cut(network, segment, 0.0)
        cut2 = _segment_with_cut(network, segment, None)
        clamp3 = _segment_with_clamp(network, segment, 1.0)
        clamp4 = _segment_with_clamp(network, segment, 1.0)
        cut3 = _segment_with_cut(network, segment, 1.0)
        cut4 = _segment_with_cut(network, segment, 1.0)
        clamp5 = _segment_with_clamp(network, segment, segment.length)
        clamp6 = _segment_with_clamp(network, segment, segment.length)
        cut5 = _segment_with_cut(network, segment, segment.length)
        cut6 = _segment_with_cut(network, segment, segment.length)

        network.connect(clamp1[1], network.get('c-clamp1', ConductingEquipment)[1])
        network.connect(clamp2[1], network.get('c-clamp2', ConductingEquipment)[1])
        network.connect(cut1[1], network.get('c-cut1t1', ConductingEquipment)[1])
        network.connect(cut1[2], network.get('c-cut1t2', ConductingEquipment)[1])
        network.connect(cut2[1], network.get('c-cut2t1', ConductingEquipment)[1])
        network.connect(cut2[2], network.get('c-cut2t2', ConductingEquipment)[1])
        network.connect(clamp3[1], network.get('c-clamp3', ConductingEquipment)[1])
        network.connect(clamp4[1], network.get('c-clamp4', ConductingEquipment)[1])
        network.connect(cut3[1], network.get('c-cut3t1', ConductingEquipment)[1])
        network.connect(cut3[2], network.get('c-cut3t2', ConductingEquipment)[1])
        network.connect(cut4[1], network.get('c-cut4t1', ConductingEquipment)[1])
        network.connect(cut4[2], network.get('c-cut4t2', ConductingEquipment)[1])
        network.connect(clamp5[1], network.get('c-clamp5', ConductingEquipment)[1])
        network.connect(clamp6[1], network.get('c-clamp6', ConductingEquipment)[1])
        network.connect(cut5[1], network.get('c-cut5t1', ConductingEquipment)[1])
        network.connect(cut5[2], network.get('c-cut5t2', ConductingEquipment)[1])
        network.connect(cut6[1], network.get('c-cut6t1', ConductingEquipment)[1])
        network.connect(cut6[2], network.get('c-cut6t2', ConductingEquipment)[1])

        return network


def _verify_paths(in_paths: Generator[NetworkTraceStep.Path, None, None], in_expected: Iterable[NetworkTraceStep.Path], check_length=True):
    paths = list(in_paths)
    expected = list(in_expected)
    for path in paths:
        if path in expected:
            continue
        assert paths == expected  # doesn't represent the actual comparison, but dumps both sides of it.