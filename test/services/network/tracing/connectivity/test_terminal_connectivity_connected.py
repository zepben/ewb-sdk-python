#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter
from typing import List, Tuple

from zepben.evolve import NetworkService, PhaseCode, SinglePhaseKind as Phase, Terminal, ConnectivityNode, AcLineSegment, NominalPhasePath, \
    TerminalConnectivityConnected


class TestTerminalConnectivityConnected:
    _network_service = NetworkService()
    _connectivity = TerminalConnectivityConnected()

    def test_straight_connections(self):
        t1, t2 = self._create_connected_terminals(PhaseCode.ABCN, PhaseCode.ABCN)
        self._validate_connection(t1, Phase.A, Phase.B, Phase.C, Phase.N)
        self._validate_connection(t2, Phase.A, Phase.B, Phase.C, Phase.N)

        t1, t2 = self._create_connected_terminals(PhaseCode.ABCN, PhaseCode.AN)
        self._validate_connection(t1, Phase.A, Phase.NONE, Phase.NONE, Phase.N)
        self._validate_connection(t2, Phase.A, Phase.N)

        t1, t2 = self._create_connected_terminals(PhaseCode.ABN, PhaseCode.BCN)
        self._validate_connection(t1, Phase.NONE, Phase.B, Phase.N)
        self._validate_connection(t2, Phase.B, Phase.NONE, Phase.N)

        t1, t2 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.YN)
        self._validate_connection(t1, Phase.NONE, Phase.Y, Phase.N)
        self._validate_connection(t2, Phase.Y, Phase.N)

    def test_xyn_connectivity(self):
        t1, t2 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.AN)
        self._validate_connection(t1, Phase.A, Phase.NONE, Phase.N)
        self._validate_connection(t2, Phase.X, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.BCN)

        self._validate_connection(t1, Phase.NONE, Phase.NONE, Phase.N)
        self._validate_connection(t2, Phase.NONE, Phase.N)

        t1, t2 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.BN)
        self._validate_connection(t1, Phase.B, Phase.NONE, Phase.N)
        self._validate_connection(t2, Phase.X, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.ABN)

        self._validate_connection(t1, Phase.NONE, Phase.B, Phase.N)
        self._validate_connection(t2, Phase.Y, Phase.N)

        t1, t2 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.CN)
        self._validate_connection(t1, Phase.C, Phase.NONE, Phase.N)
        self._validate_connection(t2, Phase.X, Phase.N)

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.BCN, PhaseCode.ABCN)
        self._validate_connection_multi(t1, [(t2, [Phase.B, Phase.C, Phase.N]), (t3, [Phase.B, Phase.C, Phase.N])])
        self._validate_connection_multi(t2, [(t1, [Phase.X, Phase.Y, Phase.N]), (t3, [Phase.B, Phase.C, Phase.N])])
        self._validate_connection_multi(t3, [(t1, [Phase.NONE, Phase.X, Phase.Y, Phase.N]), (t2, [Phase.NONE, Phase.B, Phase.C, Phase.N])])

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.YN, PhaseCode.ABCN)
        self._validate_connection_multi(t1, [(t2, [Phase.NONE, Phase.Y, Phase.N]), (t3, [Phase.A, Phase.C, Phase.N])])
        self._validate_connection_multi(t2, [(t1, [Phase.Y, Phase.N]), (t3, [Phase.C, Phase.N])])
        self._validate_connection_multi(t3, [(t1, [Phase.X, Phase.NONE, Phase.Y, Phase.N]), (t2, [Phase.NONE, Phase.NONE, Phase.Y, Phase.N])])

    def test_xn_connectivity(self):
        t1, t2 = self._create_connected_terminals(PhaseCode.XN, PhaseCode.ABCN)
        self._validate_connection(t1, Phase.A, Phase.N)
        self._validate_connection(t2, Phase.X, Phase.NONE, Phase.NONE, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.AN)

        self._validate_connection(t1, Phase.A, Phase.N)
        self._validate_connection(t2, Phase.X, Phase.NONE, Phase.NONE, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.BN)

        self._validate_connection(t1, Phase.B, Phase.N)
        self._validate_connection(t2, Phase.NONE, Phase.X, Phase.NONE, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.CN)

        self._validate_connection(t1, Phase.C, Phase.N)
        self._validate_connection(t2, Phase.NONE, Phase.NONE, Phase.X, Phase.N)

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XN, PhaseCode.BN, PhaseCode.ABCN)
        self._validate_connection_multi(t1, [(t2, [Phase.B, Phase.N]), (t3, [Phase.B, Phase.N])])
        self._validate_connection_multi(t2, [(t1, [Phase.X, Phase.N]), (t3, [Phase.B, Phase.N])])
        self._validate_connection_multi(t3, [(t1, [Phase.NONE, Phase.X, Phase.NONE, Phase.N]), (t2, [Phase.NONE, Phase.B, Phase.NONE, Phase.N])])

    def test_yn_connectivity(self):
        t1, t2 = self._create_connected_terminals(PhaseCode.YN, PhaseCode.ABCN)
        self._validate_connection(t1, Phase.C, Phase.N)
        self._validate_connection(t2, Phase.NONE, Phase.NONE, Phase.Y, Phase.N)

        self._replace_normal_phases(t1, PhaseCode.BN)

        self._validate_connection(t1, Phase.B, Phase.N)
        self._validate_connection(t2, Phase.NONE, Phase.Y, Phase.NONE, Phase.N)

        # Y can be forced onto phase A with traced phases (will not happen in practice).
        self._replace_normal_phases(t1, PhaseCode.AN)

        self._validate_connection(t1, Phase.A, Phase.N)
        self._validate_connection(t2, Phase.Y, Phase.NONE, Phase.NONE, Phase.N)

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.YN, PhaseCode.AN, PhaseCode.ABCN)
        self._validate_connection_multi(t1, [(t2, [Phase.NONE, Phase.N]), (t3, [Phase.C, Phase.N])])
        self._validate_connection_multi(t2, [(t1, [Phase.NONE, Phase.N]), (t3, [Phase.A, Phase.N])])
        self._validate_connection_multi(t3, [(t1, [Phase.NONE, Phase.NONE, Phase.Y, Phase.N]), (t2, [Phase.A, Phase.NONE, Phase.NONE, Phase.N])])

    def test_single_phase_xy_priority_connectivity(self):
        t1, t2, t3 = self._create_connected_terminals(PhaseCode.X, PhaseCode.Y, PhaseCode.A)
        self._validate_connection_multi(t1, [(t3, [Phase.A])])
        self._validate_connection(t2)
        self._validate_connection_multi(t3, [(t1, [Phase.X])])

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.X, PhaseCode.Y, PhaseCode.B)
        self._validate_connection_multi(t1, [(t3, [Phase.B])])
        self._validate_connection(t2)
        self._validate_connection_multi(t3, [(t1, [Phase.X])])

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.X, PhaseCode.Y, PhaseCode.C)
        self._validate_connection_multi(t1, [(t3, [Phase.C])])
        self._validate_connection(t2)
        self._validate_connection_multi(t3, [(t1, [Phase.X])])

    def test_straight_xyn_chain_connectivity(self):
        (t11, t12), (t21, t22) = self._create_xy_chained_terminals([PhaseCode.ABN], [PhaseCode.ABCN])

        self._validate_connection(t11, Phase.A, Phase.B, Phase.N)
        self._validate_connection(t12, Phase.X, Phase.Y, Phase.N)

        self._validate_connection(t21, Phase.A, Phase.B, Phase.N)
        self._validate_connection(t22, Phase.X, Phase.Y, Phase.NONE, Phase.N)

        (t11, t12), (t21, t22) = self._create_xy_chained_terminals([PhaseCode.ACN], [PhaseCode.ABCN])

        self._validate_connection(t11, Phase.A, Phase.C, Phase.N)
        self._validate_connection(t12, Phase.X, Phase.Y, Phase.N)

        self._validate_connection(t21, Phase.A, Phase.C, Phase.N)
        self._validate_connection(t22, Phase.X, Phase.NONE, Phase.Y, Phase.N)

        (t11, t12), (t21, t22) = self._create_xy_chained_terminals([PhaseCode.BCN], [PhaseCode.ABCN])

        self._validate_connection(t11, Phase.B, Phase.C, Phase.N)
        self._validate_connection(t12, Phase.X, Phase.Y, Phase.N)

        self._validate_connection(t21, Phase.B, Phase.C, Phase.N)
        self._validate_connection(t22, Phase.NONE, Phase.X, Phase.Y, Phase.N)

        (t11, t12), (t21, t22, t23) = self._create_xy_chained_terminals([PhaseCode.BCN], [PhaseCode.ABCN, PhaseCode.ABN])

        self._validate_connection(t11, Phase.B, Phase.C, Phase.N)
        self._validate_connection(t12, Phase.X, Phase.Y, Phase.N)

        self._validate_connection_multi(t21, [(t22, [Phase.B, Phase.C, Phase.N]), (t23, [Phase.B, Phase.NONE, Phase.N])])
        self._validate_connection_multi(t22, [(t21, [Phase.NONE, Phase.X, Phase.Y, Phase.N]), (t23, [Phase.A, Phase.B, Phase.NONE, Phase.N])])
        self._validate_connection_multi(t23, [(t21, [Phase.NONE, Phase.X, Phase.N]), (t22, [Phase.A, Phase.B, Phase.N])])

    def test_xy_to_split_connectivity(self):
        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XY, PhaseCode.A, PhaseCode.B)
        self._validate_connection_multi(t1, [(t2, [Phase.A, Phase.NONE]), (t3, [Phase.NONE, Phase.B])])
        self._validate_connection_multi(t2, [(t1, [Phase.X])])
        self._validate_connection_multi(t3, [(t1, [Phase.Y])])

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XY, PhaseCode.A, PhaseCode.C)
        self._validate_connection_multi(t1, [(t2, [Phase.A, Phase.NONE]), (t3, [Phase.NONE, Phase.C])])
        self._validate_connection_multi(t2, [(t1, [Phase.X])])
        self._validate_connection_multi(t3, [(t1, [Phase.Y])])

        t1, t2, t3 = self._create_connected_terminals(PhaseCode.XY, PhaseCode.B, PhaseCode.C)
        self._validate_connection_multi(t1, [(t2, [Phase.B, Phase.NONE]), (t3, [Phase.NONE, Phase.C])])
        self._validate_connection_multi(t2, [(t1, [Phase.X])])
        self._validate_connection_multi(t3, [(t1, [Phase.Y])])

    def test_secondary_phases_are_not_connected(self):
        t1, t2 = self._create_connected_terminals(PhaseCode.s1, PhaseCode.s2)
        self._validate_connection(t1)
        self._validate_connection(t2)

    def _create_connected_terminals(self, *phase_codes: PhaseCode) -> List[Terminal]:
        cn = self._get_next_connectivity_node()

        def create_terminal(phase_code: PhaseCode) -> Terminal:
            terminal = Terminal(phases=phase_code)
            self._network_service.connect_by_mrid(terminal, cn.mrid)
            return terminal

        return list(map(create_terminal, phase_codes))

    def _create_xy_chained_terminals(self, phase_codes1: List[PhaseCode], phase_codes2: List[PhaseCode]) -> List[List[Terminal]]:
        terminals1 = self._create_connected_terminals(PhaseCode.XYN, *phase_codes1)
        terminals2 = self._create_connected_terminals(PhaseCode.XYN, *phase_codes2)

        mid_point_terminals = self._create_connected_terminals(PhaseCode.XYN, PhaseCode.XYN)

        acls1 = AcLineSegment(mrid="acls1")
        acls1.add_terminal(terminals1[0])
        acls1.add_terminal(mid_point_terminals[0])

        acls2 = AcLineSegment(mrid="acls2")
        acls2.add_terminal(mid_point_terminals[1])
        acls2.add_terminal(terminals2[0])

        return [terminals1, terminals2]

    def _validate_connection(self, t: Terminal, *expected_phases: Phase):
        # noinspection PyArgumentList
        expected = [NominalPhasePath(t.phases.single_phases[index], phases) for index, phases in enumerate(expected_phases) if phases != Phase.NONE]

        if expected:
            assert Counter(self._connectivity.connected_terminals(t)[0].nominal_phase_paths) == Counter(expected)
        else:
            assert not self._connectivity.connected_terminals(t)

    def _validate_connection_multi(self, t: Terminal, expected_phases: List[Tuple[Terminal, List[Phase]]]):
        connected = {it.to_terminal: it for it in self._connectivity.connected_terminals(t)}

        assert len(connected) == len(expected_phases)
        for to_terminal, phases in expected_phases:
            # noinspection PyArgumentList
            assert Counter(connected[to_terminal].nominal_phase_paths) == Counter(
                [NominalPhasePath(t.phases.single_phases[index], phase) for index, phase in enumerate(phases) if phase != Phase.NONE]
            )

    @staticmethod
    def _replace_normal_phases(terminal: Terminal, normal_phases: PhaseCode):
        for index, phase in enumerate(terminal.phases.single_phases):
            terminal.traced_phases.set_normal(phase, Phase.NONE)
            terminal.traced_phases.set_normal(phase, normal_phases.single_phases[index])

    def _get_next_connectivity_node(self) -> ConnectivityNode:
        return self._network_service.add_connectivity_node(f"cn{self._network_service.len_of(ConnectivityNode)}")
