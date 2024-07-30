#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter

from zepben.evolve import TerminalConnectivityInternal, PhaseCode, PowerTransformer, Terminal


class TestTerminalConnectivityInternal:
    _connectivity = TerminalConnectivityInternal()

    def test_paths_through_hv3_tx(self):
        self._validate_tx_paths(PhaseCode.ABC, PhaseCode.ABC)
        self._validate_tx_paths(PhaseCode.ABC, PhaseCode.ABCN)
        self._validate_tx_paths(PhaseCode.ABCN, PhaseCode.ABC)

    def test_paths_through_hv1_hv1_tx(self):
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.AC)

        self._validate_tx_paths(PhaseCode.AB, PhaseCode.XY)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.XY)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.XY, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.XY)

    def test_paths_through_hv1_lv2_tx(self):
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.BCN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.ACN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.BC, PhaseCode.ABN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.ACN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.AC, PhaseCode.ABN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.BCN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.ACN)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.XY, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.ACN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.XYN)

    def test_paths_through_hv1_lv1_tx(self):
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.AN)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.BN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.CN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.BC, PhaseCode.AN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.BN)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.CN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.AC, PhaseCode.AN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.BN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.CN)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.XY, PhaseCode.AN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.BN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.CN)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.XN)

    def test_paths_through_lv2_lv2_tx(self):
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.ACN)

        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.XYN)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.XYN)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.ACN)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.XYN)

    def test_paths_through_lv2_hv1_tx(self):
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.XY)

    def test_paths_through_lv1_hv1_tx(self):
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.BN, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.CN, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.XN, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.XY)

    def test_paths_through_hv1_swer_tx(self):
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AB, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.BC, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BC, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.AC, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.AC, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.XY, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.XY, PhaseCode.X)

    def test_paths_through_swer_hv1_tx(self):
        self._validate_tx_paths(PhaseCode.A, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.B, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.AC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.C, PhaseCode.AB, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.BC, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.XY)

        self._validate_tx_paths(PhaseCode.X, PhaseCode.AB)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.BC)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.AC)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.XY)

    def test_paths_through_swer_lv1_tx(self):
        self._validate_tx_paths(PhaseCode.A, PhaseCode.AN)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.BN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.CN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.B, PhaseCode.AN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.BN)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.CN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.C, PhaseCode.AN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.BN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.CN)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.XN)

        self._validate_tx_paths(PhaseCode.X, PhaseCode.AN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.BN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.CN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.XN)

    def test_paths_through_lv1_swer_tx(self):
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.AN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.BN, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.CN, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.CN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.XN, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.XN, PhaseCode.X)

    def test_paths_through_swer_lv2_tx(self):
        self._validate_tx_paths(PhaseCode.A, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.BCN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.ACN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.A, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.B, PhaseCode.ABN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.ACN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.B, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.C, PhaseCode.ABN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.BCN, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.ACN)
        self._validate_tx_paths(PhaseCode.C, PhaseCode.XYN)

        self._validate_tx_paths(PhaseCode.X, PhaseCode.ABN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.BCN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.ACN)
        self._validate_tx_paths(PhaseCode.X, PhaseCode.XYN)

    def test_paths_through_lv2_swer_tx(self):
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ABN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.C, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.BCN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.A, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.B, PhaseCode.NONE)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.ACN, PhaseCode.X)

        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.A)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.B)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.C)
        self._validate_tx_paths(PhaseCode.XYN, PhaseCode.X)

    def _validate_tx_paths(self, primary: PhaseCode, secondary: PhaseCode, traced: PhaseCode = None):
        traced = traced or secondary
        primary_terminal = Terminal(phases=primary)
        secondary_terminal = Terminal(phases=secondary)
        PowerTransformer(terminals=[primary_terminal, secondary_terminal])

        if traced != PhaseCode.NONE:
            assert Counter([it.to_phase for it in self._connectivity.between(primary_terminal, secondary_terminal).nominal_phase_paths]) == \
                   Counter(traced.single_phases)
        else:
            assert not self._connectivity.between(primary_terminal, secondary_terminal).nominal_phase_paths
