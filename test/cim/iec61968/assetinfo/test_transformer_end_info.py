#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import patch

from hypothesis import given
from hypothesis.strategies import integers, floats

from test.cim.iec61968.assets.test_asset_info import asset_info_kwargs, verify_asset_info_constructor_default, verify_asset_info_constructor_kwargs, \
    verify_asset_info_constructor_args, asset_info_args
from test.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX, sampled_winding_connection_kind, create_transformer_tank_info, \
    create_transformer_star_impedance, create_no_load_test, create_short_circuit_test, create_open_circuit_test
from zepben.evolve import TransformerEndInfo, WindingConnection, TransformerStarImpedance, TransformerTankInfo, ResistanceReactance, NoLoadTest, \
    ShortCircuitTest, OpenCircuitTest

transformer_end_info_kwargs = {
    **asset_info_kwargs,
    "connection_kind": sampled_winding_connection_kind(),
    "emergency_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "end_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "insulation_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_angle_clock": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "short_term_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "transformer_tank_info": create_transformer_tank_info(),
    "transformer_star_impedance": create_transformer_star_impedance(),
    "energised_end_no_load_tests": create_no_load_test(),
    "energised_end_short_circuit_tests": create_short_circuit_test(),
    "grounded_end_short_circuit_tests": create_short_circuit_test(),
    "open_end_open_circuit_tests": create_open_circuit_test(),
    "energised_end_open_circuit_tests": create_open_circuit_test(),
}

transformer_end_info_args = [*asset_info_args, WindingConnection.UNKNOWN_WINDING, 1, 2, 3, 4, 5.0, 6, 7, 8, TransformerTankInfo(), TransformerStarImpedance(),
                             NoLoadTest(), ShortCircuitTest(), ShortCircuitTest(), OpenCircuitTest(), OpenCircuitTest()]


def test_transformer_end_info_constructor_default():
    tei = TransformerEndInfo()

    verify_asset_info_constructor_default(tei)
    assert tei.connection_kind == WindingConnection.UNKNOWN_WINDING
    assert tei.emergency_s == 0
    assert tei.end_number == 0
    assert tei.insulation_u == 0
    assert tei.phase_angle_clock == 0
    assert tei.r == 0.0
    assert tei.rated_s == 0
    assert tei.rated_u == 0
    assert tei.short_term_s == 0
    assert tei.transformer_tank_info is None
    assert tei.transformer_star_impedance is None
    assert tei.energised_end_no_load_tests is None
    assert tei.energised_end_short_circuit_tests is None
    assert tei.grounded_end_short_circuit_tests is None
    assert tei.open_end_open_circuit_tests is None
    assert tei.energised_end_open_circuit_tests is None


@given(**transformer_end_info_kwargs)
def test_transformer_end_info_constructor_kwargs(connection_kind, emergency_s, end_number, insulation_u, phase_angle_clock, r, rated_s, rated_u, short_term_s,
                                                 transformer_tank_info, transformer_star_impedance, energised_end_no_load_tests,
                                                 energised_end_short_circuit_tests, grounded_end_short_circuit_tests, open_end_open_circuit_tests,
                                                 energised_end_open_circuit_tests, **kwargs):
    # noinspection PyArgumentList
    tei = TransformerEndInfo(
        connection_kind=connection_kind,
        emergency_s=emergency_s,
        end_number=end_number,
        insulation_u=insulation_u,
        phase_angle_clock=phase_angle_clock,
        r=r,
        rated_s=rated_s,
        rated_u=rated_u,
        short_term_s=short_term_s,
        transformer_tank_info=transformer_tank_info,
        transformer_star_impedance=transformer_star_impedance,
        energised_end_no_load_tests=energised_end_no_load_tests,
        energised_end_short_circuit_tests=energised_end_short_circuit_tests,
        grounded_end_short_circuit_tests=grounded_end_short_circuit_tests,
        open_end_open_circuit_tests=open_end_open_circuit_tests,
        energised_end_open_circuit_tests=energised_end_open_circuit_tests,
        **kwargs
    )

    verify_asset_info_constructor_kwargs(tei, **kwargs)
    assert tei.connection_kind == connection_kind
    assert tei.emergency_s == emergency_s
    assert tei.end_number == end_number
    assert tei.insulation_u == insulation_u
    assert tei.phase_angle_clock == phase_angle_clock
    assert tei.r == r
    assert tei.rated_s == rated_s
    assert tei.rated_u == rated_u
    assert tei.short_term_s == short_term_s
    assert tei.transformer_tank_info is transformer_tank_info
    assert tei.transformer_star_impedance is transformer_star_impedance
    assert tei.energised_end_no_load_tests is energised_end_no_load_tests
    assert tei.energised_end_short_circuit_tests is energised_end_short_circuit_tests
    assert tei.grounded_end_short_circuit_tests is grounded_end_short_circuit_tests
    assert tei.open_end_open_circuit_tests is open_end_open_circuit_tests
    assert tei.energised_end_open_circuit_tests is energised_end_open_circuit_tests


def test_transformer_end_info_constructor_args():
    # noinspection PyArgumentList
    tei = TransformerEndInfo(*transformer_end_info_args)

    verify_asset_info_constructor_args(tei)
    assert tei.connection_kind is transformer_end_info_args[-16]
    assert tei.emergency_s == transformer_end_info_args[-15]
    assert tei.end_number == transformer_end_info_args[-14]
    assert tei.insulation_u == transformer_end_info_args[-13]
    assert tei.phase_angle_clock == transformer_end_info_args[-12]
    assert tei.r == transformer_end_info_args[-11]
    assert tei.rated_s == transformer_end_info_args[-10]
    assert tei.rated_u == transformer_end_info_args[-9]
    assert tei.short_term_s == transformer_end_info_args[-8]
    assert tei.transformer_tank_info is transformer_end_info_args[-7]
    assert tei.transformer_star_impedance is transformer_end_info_args[-6]
    assert tei.energised_end_no_load_tests is transformer_end_info_args[-5]
    assert tei.energised_end_short_circuit_tests is transformer_end_info_args[-4]
    assert tei.grounded_end_short_circuit_tests is transformer_end_info_args[-3]
    assert tei.open_end_open_circuit_tests is transformer_end_info_args[-2]
    assert tei.energised_end_open_circuit_tests is transformer_end_info_args[-1]


def test_populates_resistance_reactance_off_end_star_impedance_if_available():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        # noinspection PyArgumentList
        info = TransformerEndInfo(transformer_star_impedance=TransformerStarImpedance(r=1.1, r0=1.2, x=1.3, x0=1.4))
        validate_resistance_reactance(info.resistance_reactance(), 1.1, 1.2, 1.3, 1.4)
        method.assert_not_called()


def test_populates_resistance_reactance_off_end_info_tests_if_available():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        # noinspection PyArgumentList
        method.return_value = ResistanceReactance(2.1, 2.2, 2.3, 2.4)
        info = TransformerEndInfo()
        validate_resistance_reactance(info.resistance_reactance(), 2.1, 2.2, 2.3, 2.4)
        method.assert_called_once()


def test_merges_resistance_reactance_if_required():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        # noinspection PyArgumentList
        method.return_value = ResistanceReactance(None, 2.2, None, None)
        # noinspection PyArgumentList
        info = TransformerEndInfo(transformer_star_impedance=TransformerStarImpedance(r=1.1, r0=None, x=None, x0=None))
        validate_resistance_reactance(info.resistance_reactance(), 1.1, 2.2, None, None)
        method.assert_called_once()


def test_calculates_resistance_reactance_off_end_info_tests_if_available():
    info = TransformerEndInfo()
    assert info.calculate_resistance_reactance_from_tests() is None
    info.rated_u = 400000
    info.rated_s = 1630000000
    short_circuit_test = ShortCircuitTest()
    info.energised_end_short_circuit_tests = short_circuit_test
    assert info.calculate_resistance_reactance_from_tests() is None
    grounded_short_circuit_test = ShortCircuitTest()
    info.grounded_end_short_circuit_tests = grounded_short_circuit_test
    assert info.calculate_resistance_reactance_from_tests() is None
    short_circuit_test.loss = 2020180
    short_circuit_test.voltage = 11.85
    info.calculate_resistance_reactance_from_tests()
    validate_resistance_reactance(info.resistance_reactance(), r=0.12, x=11.63, r0=None, x0=None)
    short_circuit_test = ShortCircuitTest()
    short_circuit_test.voltage_ohmic_part = 0.124
    short_circuit_test.voltage = 11.85
    info.energised_end_short_circuit_tests = short_circuit_test
    validate_resistance_reactance(info.resistance_reactance(), r=0.12, x=11.63, r0=None, x0=None)


def validate_resistance_reactance(rr: ResistanceReactance, r, r0, x, x0):
    assert rr.r == r
    assert rr.r0 == r0
    assert rr.x == x
    assert rr.x0 == x0
