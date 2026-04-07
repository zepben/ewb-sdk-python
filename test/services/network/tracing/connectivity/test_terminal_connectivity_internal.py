#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Type, Callable, TypeVar

from zepben.ewb import TerminalConnectivityInternal, PhaseCode, PowerTransformer, Terminal, generate_id, require, ConnectivityResult, ConductingEquipment, \
    LinearShuntCompensator, AcLineSegment

TConductingEquipment = TypeVar("TConductingEquipment", bound=ConductingEquipment)


class TestTerminalConnectivityInternal:
    _connectivity = TerminalConnectivityInternal()

    def test_paths_through_hv3_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, returns=PhaseCode.ABC),
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABCN, returns=PhaseCode.ABCN),
            ExpectedPaths(from_phases=PhaseCode.ABCN, to_phases=PhaseCode.ABC, returns=PhaseCode.ABC),
        )

    def test_paths_through_hv1_hv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.AC, returns=PhaseCode.AC),

            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
        )

    def test_paths_through_hv1_lv2_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.BCN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.ACN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.ABN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.ACN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.ABN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.BCN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),
        )

    def test_paths_through_hv1_lv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.AN, returns=PhaseCode.AN),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.BN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.CN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.AN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.BN, returns=PhaseCode.BN),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.CN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.AN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.BN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.CN, returns=PhaseCode.CN),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.AN, returns=PhaseCode.AN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.BN, returns=PhaseCode.BN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.CN, returns=PhaseCode.CN),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.XN, returns=PhaseCode.XN),
        )

    def test_paths_through_lv2_lv2_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),

            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),
        )

    def test_paths_through_lv2_hv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
        )

    def test_paths_through_lv1_hv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
        )

    def test_paths_through_hv1_swer_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AB, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BC, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.AC, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.XY, to_phases=PhaseCode.X, returns=PhaseCode.X),
        )

    def test_paths_through_swer_hv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.AC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.AB, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.BC, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.XY, returns=PhaseCode.XY),

            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.BC, returns=PhaseCode.BC),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.AC, returns=PhaseCode.AC),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.XY, returns=PhaseCode.XY),
        )

    def test_paths_through_swer_lv1_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.AN, returns=PhaseCode.AN),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.BN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.CN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.AN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.BN, returns=PhaseCode.BN),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.CN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.AN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.BN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.CN, returns=PhaseCode.CN),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.XN, returns=PhaseCode.XN),

            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.AN, returns=PhaseCode.AN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.BN, returns=PhaseCode.BN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.CN, returns=PhaseCode.CN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.XN, returns=PhaseCode.XN),
        )

    def test_paths_through_lv1_swer_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.AN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.CN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.XN, to_phases=PhaseCode.X, returns=PhaseCode.X),
        )

    def test_paths_through_swer_lv2_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.BCN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.ACN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.A, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.ABN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.ACN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.B, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.ABN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.BCN, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),
            ExpectedPaths(from_phases=PhaseCode.C, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),

            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.ABN, returns=PhaseCode.ABN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.BCN, returns=PhaseCode.BCN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.ACN, returns=PhaseCode.ACN),
            ExpectedPaths(from_phases=PhaseCode.X, to_phases=PhaseCode.XYN, returns=PhaseCode.XYN),
        )

    def test_paths_through_lv2_swer_tx(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.X, returns=PhaseCode.X),
        )

    def test_paths_through_lv2_swer_tx2(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ABN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.C, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.BCN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.A, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.B, returns=PhaseCode.NONE),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.ACN, to_phases=PhaseCode.X, returns=PhaseCode.X),

            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.A, returns=PhaseCode.A),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.B, returns=PhaseCode.B),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.C, returns=PhaseCode.C),
            ExpectedPaths(from_phases=PhaseCode.XYN, to_phases=PhaseCode.X, returns=PhaseCode.X),
        )

    def test_can_filter_transformer_paths(self):
        self._validate_paths_through(
            PowerTransformer,
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, using=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.ABCN, to_phases=PhaseCode.ABC, using=PhaseCode.AC, returns=PhaseCode.AC),

            # Neutral is picked up as it is added by the transformer, so not filtered out by the included phases.
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABCN, using=PhaseCode.BC, returns=PhaseCode.BCN),
        )

    def test_check_shunt_compensator_paths(self):
        def set_grounding_terminal(lsc: LinearShuntCompensator):
            lsc.grounding_terminal = next((it for it in lsc.terminals if it.phases == PhaseCode.N), None)

        self._validate_paths_through(
            LinearShuntCompensator,
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, returns=PhaseCode.ABC),
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.N, returns=PhaseCode.N),
            ExpectedPaths(from_phases=PhaseCode.N, to_phases=PhaseCode.ABC, returns=PhaseCode.ABC),

            #
            # NOTE: When moving to/from the grounding terminal, all phases are added by the shunt compensator, so
            #       will not be impacted by the included phases.
            #
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, using=PhaseCode.AB, returns=PhaseCode.AB),
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.N, using=PhaseCode.AB, returns=PhaseCode.N),
            ExpectedPaths(from_phases=PhaseCode.N, to_phases=PhaseCode.ABC, using=PhaseCode.N, returns=PhaseCode.ABC),

            additional_setup=set_grounding_terminal,
        )

    def test_check_straight_paths(self):
        self._validate_paths_through(
            AcLineSegment,
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, returns=PhaseCode.ABC),
            ExpectedPaths(from_phases=PhaseCode.ABC, to_phases=PhaseCode.ABC, using=PhaseCode.AB, returns=PhaseCode.AB),
        )

    def _validate_paths_through(
        self,
        builder: Type[TConductingEquipment],
        *paths: 'ExpectedPaths',
        additional_setup: Optional[Callable[[TConductingEquipment], None]] = None,
    ):
        ce = builder(mrid=generate_id())
        terminal = Terminal(mrid=generate_id())
        other_terminal = Terminal(mrid=generate_id())

        ce.add_terminal(terminal)
        ce.add_terminal(other_terminal)

        for from_phases, to_phases, expected, included in paths:
            terminal.phases = from_phases
            other_terminal.phases = to_phases

            if additional_setup:
                additional_setup(ce)

            actual_phases = {it.to_phase for it in self._find_paths_between(terminal, other_terminal, included).nominal_phase_paths}
            expected_phases = set(expected.single_phases) if expected != PhaseCode.NONE else set()

            assert actual_phases == expected_phases, f"{builder.__name__} from_phases {from_phases} to {to_phases} using {included} should return {expected}"

    def _find_paths_between(self, terminal: Terminal, other_terminal: Terminal, included: PhaseCode) -> ConnectivityResult:
        return self._connectivity.between(terminal, other_terminal, set(included.single_phases))


class ExpectedPaths:

    def __init__(
        self,
        from_phases: PhaseCode,
        to_phases: PhaseCode,
        using: Optional[PhaseCode] = None,
        returns: Optional[PhaseCode] = None,
    ):
        self.from_phases = from_phases
        self.to_phases = to_phases
        self.expected = returns if returns is not None else to_phases
        self.included = using if using is not None else from_phases

        require(
            set(self.included.single_phases).issubset(set(self.from_phases.single_phases)),
            lambda: "`included` must only contain phases in `from`",
        )

    def __getitem__(self, item):
        return (self.from_phases, self.to_phases, self.expected, self.included)[item]
