#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pytest import raises
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, lists, floats

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_kwargs, conducting_equipment_args
from cim.property_validator import validate_property_accessor
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PowerTransformer, VectorGroup, PowerTransformerEnd, PowerTransformerInfo, TransformerConstructionKind, TransformerFunctionKind, \
    Terminal

power_transformer_kwargs = {
    **conducting_equipment_kwargs,
    "vector_group": sampled_from(VectorGroup),
    "power_transformer_ends": lists(builds(PowerTransformerEnd), max_size=2),
    "transformer_utilisation": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "construction_kind": sampled_from(TransformerConstructionKind),
    "function": sampled_from(TransformerFunctionKind)
}

power_transformer_args = [*conducting_equipment_args, VectorGroup.DD6, [PowerTransformerEnd()], 1.1, TransformerConstructionKind.padmountFeedThrough,
                          TransformerFunctionKind.secondaryTransformer]


def test_power_transformer_constructor_default():
    pt = PowerTransformer()

    verify_conducting_equipment_constructor_default(pt)
    assert pt.vector_group == VectorGroup.UNKNOWN
    assert pt.construction_kind == TransformerConstructionKind.unknown
    assert pt.function == TransformerFunctionKind.other
    assert not list(pt.ends)
    assert pt.transformer_utilisation is None


@given(**power_transformer_kwargs)
def test_power_transformer_constructor_kwargs(vector_group, power_transformer_ends, transformer_utilisation, construction_kind, function, **kwargs):
    pt = PowerTransformer(vector_group=vector_group, power_transformer_ends=power_transformer_ends, transformer_utilisation=transformer_utilisation,
                          construction_kind=construction_kind, function=function, **kwargs)

    verify_conducting_equipment_constructor_kwargs(pt, **kwargs)
    assert pt.vector_group == vector_group
    assert list(pt.ends) == power_transformer_ends
    assert pt.transformer_utilisation == transformer_utilisation
    assert pt.construction_kind == construction_kind
    assert pt.function == function


def test_power_transformer_constructor_args():
    pt = PowerTransformer(*power_transformer_args)

    verify_conducting_equipment_constructor_args(pt)
    assert pt.vector_group == power_transformer_args[-5]
    assert list(pt.ends) == power_transformer_args[-4]
    assert pt.transformer_utilisation == power_transformer_args[-3]
    assert pt.construction_kind == power_transformer_args[-2]
    assert pt.function == power_transformer_args[-1]


def test_power_transformer_info_accessor():
    validate_property_accessor(PowerTransformer, PowerTransformerInfo, PowerTransformer.power_transformer_info)


def test_get_end_by_terminal():
    t1 = Terminal(mrid="t1")
    t2 = Terminal(mrid="t2")
    t3 = Terminal(mrid="t3")

    pt = PowerTransformer(mrid="pt")
    pt.add_terminal(t1)
    pt.add_terminal(t2)
    pt.add_terminal(t3)

    e1 = PowerTransformerEnd(mrid="e1")
    e1.terminal = t3
    e2 = PowerTransformerEnd(mrid="e2")
    e2.terminal = t1

    pt.add_end(e1)
    pt.add_end(e2)

    assert pt.get_end_by_terminal(t1) is e2
    assert pt.get_end_by_terminal(t3) is e1

    with raises(IndexError, match="No TransformerEnd with terminal Terminal{t2} was found in PowerTransformer PowerTransformer{pt}"):
        pt.get_end_by_terminal(t2)
