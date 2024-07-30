#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import floats, booleans, integers, sampled_from

from cim.iec61970.base.wires.test_regulating_cond_eq import regulating_cond_eq_kwargs, verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args, regulating_cond_eq_args
from cim.property_validator import validate_property_accessor
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import ShuntCompensator, PhaseShuntConnectionKind, ShuntCompensatorInfo

shunt_compensator_kwargs = {
    **regulating_cond_eq_kwargs,
    "grounded": booleans(),
    "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_connection": sampled_from(PhaseShuntConnectionKind),
    "sections": floats(min_value=-100.0, max_value=100.0)
}

shunt_compensator_args = [*regulating_cond_eq_args, True, 1, PhaseShuntConnectionKind.G, 2.2]


def verify_shunt_compensator_constructor_default(sc: ShuntCompensator):
    verify_regulating_cond_eq_constructor_default(sc)
    assert not sc.grounded
    assert sc.nom_u is None
    assert sc.phase_connection == PhaseShuntConnectionKind.UNKNOWN
    assert sc.sections is None


def verify_shunt_compensator_constructor_kwargs(sc: ShuntCompensator, grounded, nom_u, phase_connection, sections, **kwargs):
    verify_regulating_cond_eq_constructor_kwargs(sc, **kwargs)
    assert sc.grounded == grounded
    assert sc.nom_u == nom_u
    assert sc.phase_connection == phase_connection
    assert sc.sections == sections


def verify_shunt_compensator_constructor_args(sc: ShuntCompensator):
    verify_regulating_cond_eq_constructor_args(sc)
    assert sc.grounded == shunt_compensator_args[-4]
    assert sc.nom_u == shunt_compensator_args[-3]
    assert sc.phase_connection == shunt_compensator_args[-2]
    assert sc.sections == shunt_compensator_args[-1]


def test_shunt_compensator_info_accessor():
    validate_property_accessor(ShuntCompensator, ShuntCompensatorInfo, ShuntCompensator.shunt_compensator_info)
