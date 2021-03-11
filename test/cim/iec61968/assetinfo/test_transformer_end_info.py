#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats
from unittest.mock import MagicMock, patch

from test.cim.constructor_validation import ai_kwargs, ai_args, verify_asset_info_constructor, verify_ai_args
from test.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX, windingconnectionkind
from zepben.evolve import TransformerEndInfo, WindingConnection, TransformerStarImpedance, TransformerTankInfo, ResistanceReactance

tei_kwargs = {
    "connection_kind": windingconnectionkind(),
    "emergency_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "end_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "insulation_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_angle_clock": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "short_term_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "transformer_star_impedance": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    **ai_kwargs,
}
tei_args = (*ai_args, WindingConnection.UNKNOWN_WINDING, 1, 2, 3, 4, 5.0, 6, 7, 8, TransformerTankInfo("tti1"), TransformerStarImpedance("tei1"))


@given(**tei_kwargs)
def test_tei_constructor_kwargs(transformer_star_impedance, **kwargs):
    tei = TransformerEndInfo(transformer_star_impedance=transformer_star_impedance)
    assert tei.transformer_star_impedance == transformer_star_impedance
    verify_asset_info_constructor(clazz=TransformerEndInfo, **kwargs)


def test_tei_constructor_args():
    tei = TransformerEndInfo(*tei_args)
    assert tei.connection_kind == WindingConnection.UNKNOWN_WINDING
    assert tei.emergency_s == 1
    assert tei.end_number == 2
    assert tei.insulation_u == 3
    assert tei.phase_angle_clock == 4
    assert tei.r == 5.0
    assert tei.rated_s == 6
    assert tei.rated_u == 7
    assert tei.short_term_s == 8
    assert tei.transformer_tank_info == tei_args[-2]
    assert tei.transformer_star_impedance == tei_args[-1]
    verify_ai_args(tei)


def test_populates_resistance_reactance_off_end_star_impedance_if_available():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        info = TransformerEndInfo(transformer_star_impedance=TransformerStarImpedance(r=1.1, r0=1.2, x=1.3, x0=1.4))
        validate_resistance_reactance(info.resistance_reactance(), 1.1, 1.2, 1.3, 1.4)
        method.assert_not_called()


def test_populates_resistance_reactance_off_end_info_tests_if_available():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        method.return_value = ResistanceReactance(2.1, 2.2, 2.3, 2.4)
        info = TransformerEndInfo()
        validate_resistance_reactance(info.resistance_reactance(), 2.1, 2.2, 2.3, 2.4)
        method.assert_called_once()


def test_merges_resistance_reactance_if_required():
    with patch.object(TransformerEndInfo, "calculate_resistance_reactance_from_tests") as method:
        method.return_value = ResistanceReactance(None, 2.2, None, None)
        info = TransformerEndInfo(transformer_star_impedance=TransformerStarImpedance(r=1.1, r0=None, x=None, x0=None))
        validate_resistance_reactance(info.resistance_reactance(), 1.1, 2.2, None, None)
        method.assert_called_once()


def test_calculates_resistance_reactance_off_end_info_tests_if_available():
    info = TransformerEndInfo()
    assert info.calculate_resistance_reactance_from_tests() is None


def validate_resistance_reactance(rr: ResistanceReactance, r, r0, x, x0):
    assert rr.r == r
    assert rr.r0 == r0
    assert rr.x == x
    assert rr.x0 == x0
