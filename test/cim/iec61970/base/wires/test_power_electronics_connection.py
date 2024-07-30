#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import integers, builds, lists, floats, text, booleans

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.wires.test_regulating_cond_eq import verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args, regulating_cond_eq_kwargs, regulating_cond_eq_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX, ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import PowerElectronicsUnit, PowerElectronicsConnectionPhase, BatteryUnit, PowerElectronicsConnection

power_electronics_connection_kwargs = {
    **regulating_cond_eq_kwargs,
    "max_i_fault": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "max_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "min_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "inverter_standard": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "sustain_op_overvolt_limit": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "stop_at_over_freq": floats(min_value=51.0, max_value=52.0),
    "stop_at_under_freq": floats(min_value=47.0, max_value=49.0),
    "inv_volt_watt_resp_mode": booleans(),
    "inv_watt_resp_v1": integers(min_value=200, max_value=300),
    "inv_watt_resp_v2": integers(min_value=216, max_value=230),
    "inv_watt_resp_v3": integers(min_value=235, max_value=255),
    "inv_watt_resp_v4": integers(min_value=244, max_value=265),
    "inv_watt_resp_p_at_v1": floats(min_value=0.0, max_value=1.0),
    "inv_watt_resp_p_at_v2": floats(min_value=0.0, max_value=1.0),
    "inv_watt_resp_p_at_v3": floats(min_value=0.0, max_value=1.0),
    "inv_watt_resp_p_at_v4": floats(min_value=0.0, max_value=0.2),
    "inv_volt_var_resp_mode": booleans(),
    "inv_var_resp_v1": integers(min_value=200, max_value=300),
    "inv_var_resp_v2": integers(min_value=200, max_value=300),
    "inv_var_resp_v3": integers(min_value=200, max_value=300),
    "inv_var_resp_v4": integers(min_value=200, max_value=300),
    "inv_var_resp_q_at_v1": floats(min_value=0.0, max_value=0.6),
    "inv_var_resp_q_at_v2": floats(min_value=-1.0, max_value=1.0),
    "inv_var_resp_q_at_v3": floats(min_value=-1.0, max_value=1.0),
    "inv_var_resp_q_at_v4": floats(min_value=-0.6, max_value=0.0),
    "inv_reactive_power_mode": booleans(),
    "inv_fix_reactive_power": floats(min_value=-1.0, max_value=1.0),
    "power_electronics_units": lists(builds(BatteryUnit), max_size=2),
    "power_electronics_connection_phases": lists(builds(PowerElectronicsConnectionPhase), max_size=2)
}

power_electronics_connection_args = [*regulating_cond_eq_args, 1, 2.2, 3.3, 4.4, 5.5, 6, 7, "1", 208, 51.9, 47.10, False,
                                     211, 228, 248, 258, 0.15, 0.16, 0.17, 0.18, True, 219, 220, 221, 222, 0.23, 0.24, 0.25, 0.26, False,
                                     0.27, [BatteryUnit(), BatteryUnit()], [PowerElectronicsConnectionPhase(), PowerElectronicsConnectionPhase()]]


def test_power_electronics_connection_constructor_default():
    pec = PowerElectronicsConnection()

    verify_regulating_cond_eq_constructor_default(pec)
    assert pec.max_i_fault is None
    assert pec.p is None
    assert pec.q is None
    assert pec.max_q is None
    assert pec.min_q is None
    assert pec.rated_s is None
    assert pec.rated_u is None
    assert pec.inverter_standard is None
    assert pec.sustain_op_overvolt_limit is None
    assert pec.stop_at_over_freq is None
    assert pec.stop_at_under_freq is None
    assert pec.inv_volt_watt_resp_mode is None
    assert pec.inv_watt_resp_v1 is None
    assert pec.inv_watt_resp_v2 is None
    assert pec.inv_watt_resp_v3 is None
    assert pec.inv_watt_resp_v4 is None
    assert pec.inv_watt_resp_p_at_v1 is None
    assert pec.inv_watt_resp_p_at_v2 is None
    assert pec.inv_watt_resp_p_at_v3 is None
    assert pec.inv_watt_resp_p_at_v4 is None
    assert pec.inv_volt_var_resp_mode is None
    assert pec.inv_var_resp_v1 is None
    assert pec.inv_var_resp_v2 is None
    assert pec.inv_var_resp_v3 is None
    assert pec.inv_var_resp_v4 is None
    assert pec.inv_var_resp_q_at_v1 is None
    assert pec.inv_var_resp_q_at_v2 is None
    assert pec.inv_var_resp_q_at_v3 is None
    assert pec.inv_var_resp_q_at_v4 is None
    assert pec.inv_reactive_power_mode is None
    assert pec.inv_fix_reactive_power is None
    assert not list(pec.units)
    assert not list(pec.phases)


@given(**power_electronics_connection_kwargs)
def test_power_electronics_connection_constructor_kwargs(max_i_fault, p, q, max_q, min_q, rated_s, rated_u, inverter_standard, sustain_op_overvolt_limit,
                                                         stop_at_over_freq,
                                                         stop_at_under_freq,
                                                         inv_volt_watt_resp_mode,
                                                         inv_watt_resp_v1,
                                                         inv_watt_resp_v2,
                                                         inv_watt_resp_v3,
                                                         inv_watt_resp_v4,
                                                         inv_watt_resp_p_at_v1,
                                                         inv_watt_resp_p_at_v2,
                                                         inv_watt_resp_p_at_v3,
                                                         inv_watt_resp_p_at_v4,
                                                         inv_volt_var_resp_mode,
                                                         inv_var_resp_v1,
                                                         inv_var_resp_v2,
                                                         inv_var_resp_v3,
                                                         inv_var_resp_v4,
                                                         inv_var_resp_q_at_v1,
                                                         inv_var_resp_q_at_v2,
                                                         inv_var_resp_q_at_v3,
                                                         inv_var_resp_q_at_v4,
                                                         inv_reactive_power_mode,
                                                         inv_fix_reactive_power, power_electronics_units, power_electronics_connection_phases, **kwargs):
    pec = PowerElectronicsConnection(max_i_fault=max_i_fault, p=p, q=q, max_q=max_q, min_q=min_q, rated_s=rated_s, rated_u=rated_u,
                                     inverter_standard=inverter_standard,
                                     sustain_op_overvolt_limit=sustain_op_overvolt_limit,
                                     stop_at_over_freq=stop_at_over_freq,
                                     stop_at_under_freq=stop_at_under_freq,
                                     inv_volt_watt_resp_mode=inv_volt_watt_resp_mode,
                                     inv_watt_resp_v1=inv_watt_resp_v1,
                                     inv_watt_resp_v2=inv_watt_resp_v2,
                                     inv_watt_resp_v3=inv_watt_resp_v3,
                                     inv_watt_resp_v4=inv_watt_resp_v4,
                                     inv_watt_resp_p_at_v1=inv_watt_resp_p_at_v1,
                                     inv_watt_resp_p_at_v2=inv_watt_resp_p_at_v2,
                                     inv_watt_resp_p_at_v3=inv_watt_resp_p_at_v3,
                                     inv_watt_resp_p_at_v4=inv_watt_resp_p_at_v4,
                                     inv_volt_var_resp_mode=inv_volt_var_resp_mode,
                                     inv_var_resp_v1=inv_var_resp_v1,
                                     inv_var_resp_v2=inv_var_resp_v2,
                                     inv_var_resp_v3=inv_var_resp_v3,
                                     inv_var_resp_v4=inv_var_resp_v4,
                                     inv_var_resp_q_at_v1=inv_var_resp_q_at_v1,
                                     inv_var_resp_q_at_v2=inv_var_resp_q_at_v2,
                                     inv_var_resp_q_at_v3=inv_var_resp_q_at_v3,
                                     inv_var_resp_q_at_v4=inv_var_resp_q_at_v4,
                                     inv_reactive_power_mode=inv_reactive_power_mode,
                                     inv_fix_reactive_power=inv_fix_reactive_power,
                                     power_electronics_units=power_electronics_units,
                                     power_electronics_connection_phases=power_electronics_connection_phases, **kwargs)

    verify_regulating_cond_eq_constructor_kwargs(pec, **kwargs)
    assert pec.max_i_fault == max_i_fault
    assert pec.p == p
    assert pec.q == q
    assert pec.max_q == max_q
    assert pec.min_q == min_q
    assert pec.rated_s == rated_s
    assert pec.rated_u == rated_u
    assert pec.inverter_standard == inverter_standard
    assert pec.sustain_op_overvolt_limit == sustain_op_overvolt_limit
    assert pec.stop_at_over_freq == stop_at_over_freq
    assert pec.stop_at_under_freq == stop_at_under_freq
    assert pec.inv_volt_watt_resp_mode == inv_volt_watt_resp_mode
    assert pec.inv_watt_resp_v1 == inv_watt_resp_v1
    assert pec.inv_watt_resp_v2 == inv_watt_resp_v2
    assert pec.inv_watt_resp_v3 == inv_watt_resp_v3
    assert pec.inv_watt_resp_v4 == inv_watt_resp_v4
    assert pec.inv_watt_resp_p_at_v1 == inv_watt_resp_p_at_v1
    assert pec.inv_watt_resp_p_at_v2 == inv_watt_resp_p_at_v2
    assert pec.inv_watt_resp_p_at_v3 == inv_watt_resp_p_at_v3
    assert pec.inv_watt_resp_p_at_v4 == inv_watt_resp_p_at_v4
    assert pec.inv_volt_var_resp_mode == inv_volt_var_resp_mode
    assert pec.inv_var_resp_v1 == inv_var_resp_v1
    assert pec.inv_var_resp_v2 == inv_var_resp_v2
    assert pec.inv_var_resp_v3 == inv_var_resp_v3
    assert pec.inv_var_resp_v4 == inv_var_resp_v4
    assert pec.inv_var_resp_q_at_v1 == inv_var_resp_q_at_v1
    assert pec.inv_var_resp_q_at_v2 == inv_var_resp_q_at_v2
    assert pec.inv_var_resp_q_at_v3 == inv_var_resp_q_at_v3
    assert pec.inv_var_resp_q_at_v4 == inv_var_resp_q_at_v4
    assert pec.inv_reactive_power_mode == inv_reactive_power_mode
    assert pec.inv_fix_reactive_power == inv_fix_reactive_power
    assert list(pec.units) == power_electronics_units
    assert list(pec.phases) == power_electronics_connection_phases


def test_power_electronics_connection_constructor_args():
    pec = PowerElectronicsConnection(*power_electronics_connection_args)

    verify_regulating_cond_eq_constructor_args(pec)
    assert pec.max_i_fault == power_electronics_connection_args[-33]
    assert pec.p == power_electronics_connection_args[-32]
    assert pec.q == power_electronics_connection_args[-31]
    assert pec.max_q == power_electronics_connection_args[-30]
    assert pec.min_q == power_electronics_connection_args[-29]
    assert pec.rated_s == power_electronics_connection_args[-28]
    assert pec.rated_u == power_electronics_connection_args[-27]
    assert pec.inverter_standard == power_electronics_connection_args[-26]
    assert pec.sustain_op_overvolt_limit == power_electronics_connection_args[-25]
    assert pec.stop_at_over_freq == power_electronics_connection_args[-24]
    assert pec.stop_at_under_freq == power_electronics_connection_args[-23]
    assert pec.inv_volt_watt_resp_mode == power_electronics_connection_args[-22]
    assert pec.inv_watt_resp_v1 == power_electronics_connection_args[-21]
    assert pec.inv_watt_resp_v2 == power_electronics_connection_args[-20]
    assert pec.inv_watt_resp_v3 == power_electronics_connection_args[-19]
    assert pec.inv_watt_resp_v4 == power_electronics_connection_args[-18]
    assert pec.inv_watt_resp_p_at_v1 == power_electronics_connection_args[-17]
    assert pec.inv_watt_resp_p_at_v2 == power_electronics_connection_args[-16]
    assert pec.inv_watt_resp_p_at_v3 == power_electronics_connection_args[-15]
    assert pec.inv_watt_resp_p_at_v4 == power_electronics_connection_args[-14]
    assert pec.inv_volt_var_resp_mode == power_electronics_connection_args[-13]
    assert pec.inv_var_resp_v1 == power_electronics_connection_args[-12]
    assert pec.inv_var_resp_v2 == power_electronics_connection_args[-11]
    assert pec.inv_var_resp_v3 == power_electronics_connection_args[-10]
    assert pec.inv_var_resp_v4 == power_electronics_connection_args[-9]
    assert pec.inv_var_resp_q_at_v1 == power_electronics_connection_args[-8]
    assert pec.inv_var_resp_q_at_v2 == power_electronics_connection_args[-7]
    assert pec.inv_var_resp_q_at_v3 == power_electronics_connection_args[-6]
    assert pec.inv_var_resp_q_at_v4 == power_electronics_connection_args[-5]
    assert pec.inv_reactive_power_mode == power_electronics_connection_args[-4]
    assert pec.inv_fix_reactive_power == power_electronics_connection_args[-3]
    assert list(pec.units) == power_electronics_connection_args[-2]
    assert list(pec.phases) == power_electronics_connection_args[-1]


def test_power_electronics_units_collection():
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsUnit(mrid),
                                  PowerElectronicsConnection.num_units,
                                  PowerElectronicsConnection.get_unit,
                                  PowerElectronicsConnection.units,
                                  PowerElectronicsConnection.add_unit,
                                  PowerElectronicsConnection.remove_unit,
                                  PowerElectronicsConnection.clear_units)


def test_power_electronics_connection_phases_collection():
    # noinspection PyArgumentList
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsConnectionPhase(mrid),
                                  PowerElectronicsConnection.num_phases,
                                  PowerElectronicsConnection.get_phase,
                                  PowerElectronicsConnection.phases,
                                  PowerElectronicsConnection.add_phase,
                                  PowerElectronicsConnection.remove_phase,
                                  PowerElectronicsConnection.clear_phases)


def test_power_electronics_connection_property_bounds():
    with raises(ValueError, match=re.escape("inv_watt_resp_v1 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v1=199)
    with raises(ValueError, match=re.escape("inv_watt_resp_v1 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v1=301)
    with raises(ValueError, match=re.escape("inv_watt_resp_v2 [215] must be between 216 and 230.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v2=215)
    with raises(ValueError, match=re.escape("inv_watt_resp_v2 [231] must be between 216 and 230.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v2=231)
    with raises(ValueError, match=re.escape("inv_watt_resp_v3 [234] must be between 235 and 255.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v3=234)
    with raises(ValueError, match=re.escape("inv_watt_resp_v3 [256] must be between 235 and 255.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v3=256)
    with raises(ValueError, match=re.escape("inv_watt_resp_v4 [243] must be between 244 and 265.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v4=243)
    with raises(ValueError, match=re.escape("inv_watt_resp_v4 [266] must be between 244 and 265.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_v4=266)

    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v1 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v1=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v1 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v1=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v2 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v2=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v2 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v2=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v3 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v3=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v3 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v3=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v4 [-0.01] must be between 0.0 and 0.2.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v4=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v4 [0.21] must be between 0.0 and 0.2.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_watt_resp_p_at_v4=0.21)

    with raises(ValueError, match=re.escape("inv_var_resp_v1 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v1=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v1 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v1=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v2 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v2=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v2 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v2=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v3 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v3=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v3 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v3=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v4 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v4=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v4 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_v4=301)

    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v1 [-0.01] must be between 0.0 and 0.6.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v1=-0.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v1 [0.61] must be between 0.0 and 0.6.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v1=0.61)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v2 [-1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v2=-1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v2 [1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v2=1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v3 [-1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v3=-1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v3 [1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v3=1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v4 [-0.61] must be between -0.6 and 0.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v4=-0.61)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v4 [0.01] must be between -0.6 and 0.0.")):
        PowerElectronicsConnection(*power_electronics_connection_args, inv_var_resp_q_at_v4=0.01)
