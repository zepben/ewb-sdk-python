#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import energy_source_kwargs
from cim.iec61970.base.wires.test_energy_connection import verify_energy_connection_constructor_default, \
    verify_energy_connection_constructor_kwargs
from cim.private_collection_validator import validate_unordered

from test.cim.private_collection_validator import validate_backfill
from zepben.ewb import EnergySource, EnergySourcePhase, generate_id


def test_energy_source_constructor_default():
    es = EnergySource(mrid=generate_id())

    verify_energy_connection_constructor_default(es)
    assert not list(es.phases)
    assert es.active_power is None
    assert es.reactive_power is None
    assert es.voltage_angle is None
    assert es.voltage_magnitude is None
    assert es.p_max is None
    assert es.p_min is None
    assert es.r is None
    assert es.r0 is None
    assert es.rn is None
    assert es.x is None
    assert es.x0 is None
    assert es.xn is None
    assert es.is_external_grid is None
    assert es.r_min is None
    assert es.rn_min is None
    assert es.r0_min is None
    assert es.x_min is None
    assert es.xn_min is None
    assert es.x0_min is None
    assert es.r_max is None
    assert es.rn_max is None
    assert es.r0_max is None
    assert es.x_max is None
    assert es.xn_max is None
    assert es.x0_max is None


@given(**energy_source_kwargs())
def test_energy_source_constructor_kwargs(
    energy_source_phases, active_power, reactive_power, voltage_angle, voltage_magnitude, p_max, p_min,
    r, r0, rn, x, x0, xn, is_external_grid, r_min, rn_min, r0_min, x_min, xn_min, x0_min,
    r_max, rn_max, r0_max, x_max, xn_max, x0_max, **kwargs,
):
    es = EnergySource(
        energy_source_phases=energy_source_phases,
        active_power=active_power,
        reactive_power=reactive_power,
        voltage_angle=voltage_angle,
        voltage_magnitude=voltage_magnitude,
        p_max=p_max,
        p_min=p_min,
        r=r,
        r0=r0,
        rn=rn,
        x=x,
        x0=x0,
        xn=xn,
        is_external_grid=is_external_grid,
        r_min=r_min,
        rn_min=rn_min,
        r0_min=r0_min,
        x_min=x_min,
        xn_min=xn_min,
        x0_min=x0_min,
        r_max=r_max,
        rn_max=rn_max,
        r0_max=r0_max,
        x_max=x_max,
        xn_max=xn_max,
        x0_max=x0_max,
        **kwargs,
    )

    verify_energy_connection_constructor_kwargs(es, **kwargs)
    assert list(es.phases) == energy_source_phases
    assert es.active_power == active_power
    assert es.reactive_power == reactive_power
    assert es.voltage_angle == voltage_angle
    assert es.voltage_magnitude == voltage_magnitude
    assert es.p_max == p_max
    assert es.p_min == p_min
    assert es.r == r
    assert es.r0 == r0
    assert es.rn == rn
    assert es.x == x
    assert es.x0 == x0
    assert es.xn == xn
    assert es.is_external_grid == is_external_grid
    assert es.r_min == r_min
    assert es.rn_min == rn_min
    assert es.r0_min == r0_min
    assert es.x_min == x_min
    assert es.xn_min == xn_min
    assert es.x0_min == x0_min
    assert es.r_max == r_max
    assert es.rn_max == rn_max
    assert es.r0_max == r0_max
    assert es.x_max == x_max
    assert es.xn_max == xn_max
    assert es.x0_max == x0_max


def test_phases_collection():
    validate_unordered(
        EnergySource,
        EnergySourcePhase,
        EnergySource.phases,
        EnergySource.num_phases,
        EnergySource.get_phase,
        EnergySource.add_phase,
        EnergySource.remove_phase,
        EnergySource.clear_phases,
    )


def test_phases_backfill():
    validate_backfill(
        EnergySource,
        lambda mrid: EnergySourcePhase(mrid),
        lambda mrid, es: EnergySourcePhase(mrid, energy_source=es),
        lambda other: other.energy_source,
        EnergySource.num_phases,
        EnergySource.add_phase,
    )
