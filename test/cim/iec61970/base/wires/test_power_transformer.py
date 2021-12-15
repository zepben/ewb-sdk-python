#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, lists, floats
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from test.cim import extract_testing_args
from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_kwargs, conducting_equipment_args
from test.cim.property_validator import validate_property_accessor
from zepben.evolve import PowerTransformer, VectorGroup, PowerTransformerEnd, PowerTransformerInfo, TransformerConstructionKind, TransformerFunctionKind
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_power_transformer


power_transformer_kwargs = {
    **conducting_equipment_kwargs,
    "vector_group": sampled_from(VectorGroup),
    "power_transformer_ends": lists(builds(PowerTransformerEnd), max_size=2),
    "transformer_utilisation": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "construction_kind": sampled_from(TransformerConstructionKind),
    "function": sampled_from(TransformerFunctionKind)
}

power_transformer_args = [*conducting_equipment_args, VectorGroup.DD6, [PowerTransformerEnd], 1.1, TransformerConstructionKind.padmountFeedThrough,
                          TransformerFunctionKind.secondaryTransformer]


def test_power_transformer_constructor_default():
    pt = PowerTransformer()
    pt2 = create_power_transformer()
    validate_default_power_transformer_constructor(pt)
    validate_default_power_transformer_constructor(pt2)


def validate_default_power_transformer_constructor(pt):
    verify_conducting_equipment_constructor_default(pt)
    assert pt.vector_group == VectorGroup.UNKNOWN
    assert pt.construction_kind == TransformerConstructionKind.unknown
    assert pt.function == TransformerFunctionKind.other
    assert not list(pt.ends)
    assert pt.transformer_utilisation is None


@given(**power_transformer_kwargs)
def test_power_transformer_constructor_kwargs(vector_group, power_transformer_ends, transformer_utilisation, construction_kind, function, **kwargs):
    args = extract_testing_args(locals())
    pt = PowerTransformer(**args, **kwargs)
    validate_power_transformer_values(pt, **args, **kwargs)


@given(**power_transformer_kwargs)
def test_power_transformer_creator(vector_group, power_transformer_ends, transformer_utilisation, construction_kind, function, **kwargs):
    args = extract_testing_args(locals())
    pt = create_power_transformer(**args, **kwargs)
    validate_power_transformer_values(pt, **args, **kwargs)


def validate_power_transformer_values(pt, vector_group, power_transformer_ends, transformer_utilisation, construction_kind, function, **kwargs):
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


def test_auto_two_way_connections_for_power_transformer_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    pte = PowerTransformerEnd()
    pt = create_power_transformer(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t],
                                  power_transformer_ends=[pte])

    check_conducting_equipment_two_way_link_test(pt, up, ec, opr, f, t)
    assert pte.power_transformer == pt
