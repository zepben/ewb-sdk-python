#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import floats, booleans, integers, sampled_from, builds

from util import mrid_strategy
from zepben.ewb import ShuntCompensator, PhaseShuntConnectionKind, ShuntCompensatorInfo, Terminal, generate_id

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.wires.test_regulating_cond_eq import regulating_cond_eq_kwargs, verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args, regulating_cond_eq_args
from cim.property_validator import validate_property_accessor

shunt_compensator_kwargs = {
    **regulating_cond_eq_kwargs,
    "grounded": booleans(),
    "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "phase_connection": sampled_from(PhaseShuntConnectionKind),
    "grounding_terminal": builds(Terminal, mrid=mrid_strategy),
    "sections": floats(min_value=-100.0, max_value=100.0),
}

shunt_compensator_args = [*regulating_cond_eq_args, True, 1, PhaseShuntConnectionKind.G, Terminal(mrid=generate_id()), 2.2]


def verify_shunt_compensator_constructor_default(sc: ShuntCompensator):
    verify_regulating_cond_eq_constructor_default(sc)
    assert sc.grounded is None
    assert sc.nom_u is None
    assert sc.phase_connection == PhaseShuntConnectionKind.UNKNOWN
    assert sc.sections is None
    assert sc.grounding_terminal is None


def verify_shunt_compensator_constructor_kwargs(sc: ShuntCompensator, grounded, nom_u, phase_connection, grounding_terminal, sections, **kwargs):
    verify_regulating_cond_eq_constructor_kwargs(sc, **kwargs)
    assert sc.grounded == grounded
    assert sc.nom_u == nom_u
    assert sc.phase_connection == phase_connection
    assert sc.sections == sections
    assert sc.grounding_terminal == grounding_terminal


def verify_shunt_compensator_constructor_args(sc: ShuntCompensator):
    verify_regulating_cond_eq_constructor_args(sc)
    assert shunt_compensator_args[-5:] == [
        sc.grounded,
        sc.nom_u,
        sc.phase_connection,
        sc.grounding_terminal,
        sc.sections,
    ]


def test_shunt_compensator_info_accessor():
    validate_property_accessor(ShuntCompensator, ShuntCompensatorInfo, ShuntCompensator.shunt_compensator_info)
