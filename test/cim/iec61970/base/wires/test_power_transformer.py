#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, lists, floats

from test.cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_kwargs, conducting_equipment_args
from test.cim.property_validator import validate_property_accessor
from test.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PowerTransformer, VectorGroup, PowerTransformerEnd, PowerTransformerInfo

power_transformer_kwargs = {
    **conducting_equipment_kwargs,
    "vector_group": sampled_from(VectorGroup),
    "power_transformer_ends": lists(builds(PowerTransformerEnd), max_size=2),
    "transformer_utilisation": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

power_transformer_args = [*conducting_equipment_args, VectorGroup.DD6, [PowerTransformerEnd], 1.1]


def test_power_transformer_constructor_default():
    pt = PowerTransformer()

    verify_conducting_equipment_constructor_default(pt)
    assert pt.vector_group == VectorGroup.UNKNOWN
    assert not list(pt.ends)
    assert pt.transformer_utilisation is None


@given(**power_transformer_kwargs)
def test_power_transformer_constructor_kwargs(vector_group, power_transformer_ends, transformer_utilisation, **kwargs):
    pt = PowerTransformer(vector_group=vector_group, power_transformer_ends=power_transformer_ends, transformer_utilisation=transformer_utilisation, **kwargs)

    verify_conducting_equipment_constructor_kwargs(pt, **kwargs)
    assert pt.vector_group == vector_group
    assert list(pt.ends) == power_transformer_ends
    assert pt.transformer_utilisation == transformer_utilisation


def test_power_transformer_constructor_args():
    pt = PowerTransformer(*power_transformer_args)

    verify_conducting_equipment_constructor_args(pt)
    assert pt.vector_group == power_transformer_args[-3]
    assert list(pt.ends) == power_transformer_args[-2]
    assert pt.transformer_utilisation == power_transformer_args[-1]


def test_power_transformer_info_accessor():
    validate_property_accessor(PowerTransformer, PowerTransformerInfo, PowerTransformer.power_transformer_info)


