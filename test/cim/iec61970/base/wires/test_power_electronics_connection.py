#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from hypothesis import given
from pytest import raises

from cim.fill_fields import power_electronics_connection_kwargs
from cim.iec61970.base.wires.test_regulating_cond_eq import verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs
from cim.private_collection_validator import validate_unordered

from test.cim.private_collection_validator import validate_backfill
from zepben.ewb import PowerElectronicsUnit, PowerElectronicsConnection, generate_id
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase


def test_power_electronics_connection_constructor_default():
    pec = PowerElectronicsConnection(mrid=generate_id())

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


@given(**power_electronics_connection_kwargs())
def test_power_electronics_connection_constructor_kwargs(
    max_i_fault,
    p,
    q,
    max_q,
    min_q,
    rated_s,
    rated_u,
    inverter_standard,
    sustain_op_overvolt_limit,
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
    inv_fix_reactive_power,
    power_electronics_units,
    power_electronics_connection_phases,
    **kwargs,
):
    pec = PowerElectronicsConnection(
        max_i_fault=max_i_fault,
        p=p,
        q=q,
        max_q=max_q,
        min_q=min_q,
        rated_s=rated_s,
        rated_u=rated_u,
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
        power_electronics_connection_phases=power_electronics_connection_phases,
        **kwargs,
    )

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


def test_power_electronics_units_collection():
    validate_unordered(
        PowerElectronicsConnection,
        PowerElectronicsUnit,
        PowerElectronicsConnection.units,
        PowerElectronicsConnection.num_units,
        PowerElectronicsConnection.get_unit,
        PowerElectronicsConnection.add_unit,
        PowerElectronicsConnection.remove_unit,
        PowerElectronicsConnection.clear_units,
    )


def test_power_electronics_connection_phases_collection():
    validate_unordered(
        PowerElectronicsConnection,
        PowerElectronicsConnectionPhase,
        PowerElectronicsConnection.phases,
        PowerElectronicsConnection.num_phases,
        PowerElectronicsConnection.get_phase,
        PowerElectronicsConnection.add_phase,
        PowerElectronicsConnection.remove_phase,
        PowerElectronicsConnection.clear_phases,
    )


def test_power_electronics_connection_phases_backfill():
    validate_backfill(
        PowerElectronicsConnection,
        lambda mrid: PowerElectronicsConnectionPhase(mrid),
        lambda mrid, pec: PowerElectronicsConnectionPhase(mrid, power_electronics_connection=pec),
        lambda other: other.power_electronics_connection,
        PowerElectronicsConnection.num_phases,
        PowerElectronicsConnection.add_phase,
    )


def test_power_electronics_connection_property_bounds():
    with raises(ValueError, match=re.escape("inv_watt_resp_v1 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v1=199)
    with raises(ValueError, match=re.escape("inv_watt_resp_v1 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v1=301)
    with raises(ValueError, match=re.escape("inv_watt_resp_v2 [215] must be between 216 and 230.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v2=215)
    with raises(ValueError, match=re.escape("inv_watt_resp_v2 [231] must be between 216 and 230.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v2=231)
    with raises(ValueError, match=re.escape("inv_watt_resp_v3 [234] must be between 235 and 255.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v3=234)
    with raises(ValueError, match=re.escape("inv_watt_resp_v3 [256] must be between 235 and 255.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v3=256)
    with raises(ValueError, match=re.escape("inv_watt_resp_v4 [243] must be between 244 and 265.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v4=243)
    with raises(ValueError, match=re.escape("inv_watt_resp_v4 [266] must be between 244 and 265.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_v4=266)

    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v1 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v1=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v1 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v1=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v2 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v2=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v2 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v2=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v3 [-0.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v3=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v3 [1.01] must be between 0.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v3=1.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v4 [-0.01] must be between 0.0 and 0.2.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v4=-0.01)
    with raises(ValueError, match=re.escape("inv_watt_resp_p_at_v4 [0.21] must be between 0.0 and 0.2.")):
        PowerElectronicsConnection(mrid="mrid", inv_watt_resp_p_at_v4=0.21)

    with raises(ValueError, match=re.escape("inv_var_resp_v1 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v1=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v1 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v1=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v2 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v2=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v2 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v2=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v3 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v3=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v3 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v3=301)
    with raises(ValueError, match=re.escape("inv_var_resp_v4 [199] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v4=199)
    with raises(ValueError, match=re.escape("inv_var_resp_v4 [301] must be between 200 and 300.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_v4=301)

    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v1 [-0.01] must be between 0.0 and 0.6.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v1=-0.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v1 [0.61] must be between 0.0 and 0.6.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v1=0.61)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v2 [-1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v2=-1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v2 [1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v2=1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v3 [-1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v3=-1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v3 [1.01] must be between -1.0 and 1.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v3=1.01)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v4 [-0.61] must be between -0.6 and 0.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v4=-0.61)
    with raises(ValueError, match=re.escape("inv_var_resp_q_at_v4 [0.01] must be between -0.6 and 0.0.")):
        PowerElectronicsConnection(mrid="mrid", inv_var_resp_q_at_v4=0.01)
