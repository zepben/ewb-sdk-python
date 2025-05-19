#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, Tuple, Iterable

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve import NetworkStateOperators, TestNetworkBuilder, NetworkTraceStep, Terminal, NominalPhasePath, Breaker
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


def _verify_paths(in_paths: Generator[NetworkTraceStep.Path, None, None], in_expected: Iterable[Path], check_length=True):
    paths = list(in_paths)
    expected = list(in_expected)
    for path in expected:
        assert path in paths
    if check_length:
        assert len(paths) == len(expected)
