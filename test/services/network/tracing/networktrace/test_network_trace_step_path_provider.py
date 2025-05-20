#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, Tuple, Iterable

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve import NetworkStateOperators, TestNetworkBuilder, NetworkTraceStep, Terminal, NominalPhasePath, Breaker, AcLineSegment, Clamp, Cut, \
    ConductingEquipment
from zepben.evolve.services.network.tracing.networktrace.network_trace_step_path_provider import NetworkTraceStepPathProvider

Path = NetworkTraceStep.Path
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

        current_path = Path(c0[2], j1[1])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(j1[1], j1[2]), Path(j1[1], j1[3])))

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

        current_path = Path(j0[1], j0[2])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(j0[2], c1[1]), Path(j0[2], c2[1])))

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

        current_path = Path(j0[1], j0[2])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(j0[2], c1[1]), ))

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

        current_path = Path(c0[2], tx1[1], None, {NominalPhasePath(SPK.A, SPK.A), NominalPhasePath(SPK.B, SPK.B)})
        next_paths = self.path_provider.next_paths(current_path)

        # Should not contain tx1-t4 because its not in the phase paths
        _verify_paths(next_paths, [
            Path(tx1[1], tx1[2], None, {NominalPhasePath(SPK.A, SPK.A)}),
            Path(tx1[1], tx1[3], None, {NominalPhasePath(SPK.B, SPK.B)})])

    def test_stepping_externally_to_connectivity_node_with_busbars_only_goes_to_busbars(self):
        network = self._busbar_network()

        b0 = network['b0']
        bbs1 = network['bbs1']
        bbs2 = network['bbs2']

        current_path = Path(b0[1], b0[2])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(b0[2], bbs1[1]), Path(b0[2], bbs2[1])))

    def test_steppiong_externally_from_busbars_does_not_step_to_busbars_or_original_from_terminal(self):
        network = self._busbar_network()

        bbs1 = network['bbs1']
        b0= network['b0']
        b3 = network['b3']
        b4 = network['b4']
        b5 = network['b5']
        b6 = network['b6']

        current_path = Path(b0[2], bbs1[1])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(bbs1[1], b3[1]), Path(bbs1[1], b4[1]), Path(bbs1[1], b5[1]), Path(bbs1[1], b6[1])))

    def test_traversing_segment_with_clamps_from_t1_includes_all_clamp_steps(self):
        network = self._acls_with_clamps_network()

        breaker = network['b0']
        segment: AcLineSegment = network['c1']
        clamp1 = network['c1-clamp1']
        clamp2 = network['c1-clamp2']

        current_path = Path(breaker[2], segment[1])
        next_paths = self.path_provider.next_paths(current_path)

        _verify_paths(next_paths, (Path(segment[1], clamp1[1]), Path(segment[1], clamp2[1]), Path(segment[1], segment[2])))

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

    def _acls_with_clamps_network(self):
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

    def _acls_with_clamps_and_cuts_network(self):
        #
        #          2                     2
        #          c3          2         c7          2
        #          1           c5        1           c9
        #          1 clamp1    1         1 clamp3    1
        #          |           |         |           |
        # 1 b0 21--*--*1 cut1 2*--*--c1--*--*1 cut2 2*--*--21 b2 2
        #             |           |         |           |
        #             1           1 clamp2  1           1 clamp4
        #             c4          1         c8          1
        #             2           c6        2           c10
        #                         2                     2
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_breaker()  # b2
                   .to_acls()  # c3
                   .to_acls()  # c4
                   .to_acls()  # c5
                   .to_acls()  # c6
                   .to_acls()  # c7
                   .to_acls()  # c8
                   .to_acls()  # c9
                   .to_acls()  # c10
                   ).network

        segment: AcLineSegment = network['c1']

        clamp1 = _segment_with_clamp(network, segment, 1.0)
        cut1 = _segment_with_cut(network, segment, 2.0)
        clamp2 = _segment_with_clamp(network, segment, 3.0)
        clamp3 = _segment_with_clamp(network, segment, 4.0)
        cut2 = _segment_with_cut(network, segment, 5.0)
        clamp4 = _segment_with_clamp(network, segment, 6.0)

        network.connect(clamp1[1], network.get('c3', ConductingEquipment)[1])
        network.connect(cut1[1], network.get('c4', ConductingEquipment)[1])
        network.connect(cut1[2], network.get('c5', ConductingEquipment)[1])
        network.connect(clamp2[1], network.get('c6', ConductingEquipment)[1])
        network.connect(clamp3[1], network.get('c7', ConductingEquipment)[1])
        network.connect(cut2[1], network.get('c8', ConductingEquipment)[1])
        network.connect(cut2[2], network.get('c9', ConductingEquipment)[1])
        network.connect(clamp4[1], network.get('c10', ConductingEquipment)[1])

        return network

def _segment_with_clamp(network: NetworkService, segment: AcLineSegment, length_from_terminal1: float) -> Clamp:
    clamp = Clamp(mrid=f'clamp{segment.num_clamps() + 1}')
    clamp.add_terminal(Terminal(mrid=f'{clamp.mrid}-t1'))
    clamp.length_from_terminal_1 = length_from_terminal1

    segment.add_clamp(clamp)
    network.add(clamp)
    return clamp

def _segment_with_cut(network: NetworkService, segment: AcLineSegment, length_from_terminal1: float) -> Cut:
    cut = Cut(mrid=f'cut{segment.num_cuts() + 1}', length_from_terminal_1=length_from_terminal1)
    cut.add_terminal(Terminal(mrid=f'{cut.mrid}-t1'))
    cut.add_terminal(Terminal(mrid=f'{cut.mrid}-t2'))

    segment.add_cut(cut)
    network.add(cut)
    return cut


def _verify_paths(in_paths: Generator[NetworkTraceStep.Path, None, None], in_expected: Iterable[Path], check_length=True):
    paths = sorted(list(in_paths), key=lambda p: (p.from_terminal, p.to_terminal))
    expected = sorted(in_expected, key=lambda p: (p.from_terminal, p.to_terminal))
    assert paths == expected
