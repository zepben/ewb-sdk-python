#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from util import mrid_strategy
from zepben.ewb import Terminal, Equipment, LvFeeder, generate_id
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder

from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from cim.private_collection_validator import validate_unordered

lv_feeder_kwargs = {
    **equipment_container_kwargs,
    "normal_head_terminal": builds(Terminal, mrid=mrid_strategy),
    "normal_energizing_feeders": lists(builds(Feeder, mrid=mrid_strategy), max_size=2),
    "current_equipment": lists(builds(Equipment, mrid=mrid_strategy), max_size=2),
    "current_energizing_feeders": lists(builds(Feeder, mrid=mrid_strategy), max_size=2),
    "normal_energizing_lv_substation": builds(LvSubstation, mrid=mrid_strategy),
}

lv_feeder_args = [
    *equipment_container_args,
    Terminal(mrid=generate_id()),
    {"f": Feeder(mrid=generate_id())},
    {"ce": Equipment(mrid=generate_id())},
    {"cef": Feeder(mrid=generate_id())},
    LvSubstation(mrid=generate_id()),
]


def test_lv_feeder_constructor_default():
    lvf = LvFeeder(mrid=generate_id())

    verify_equipment_container_constructor_default(lvf)
    assert lvf.normal_head_terminal is None
    assert not list(lvf.normal_energizing_feeders)
    assert not list(lvf.current_equipment)
    assert not list(lvf.current_energizing_feeders)
    assert lvf.normal_energizing_lv_substation is None


@given(**lv_feeder_kwargs)
def test_lv_feeder_constructor_kwargs(
    normal_head_terminal,
    normal_energizing_feeders,
    current_equipment,
    current_energizing_feeders,
    normal_energizing_lv_substation,
    **kwargs
):
    lvf = LvFeeder(
        normal_head_terminal=normal_head_terminal,
        normal_energizing_feeders=normal_energizing_feeders,
        current_equipment=current_equipment,
        current_energizing_feeders=current_energizing_feeders,
        normal_energizing_lv_substation=normal_energizing_lv_substation,
        **kwargs
    )

    verify_equipment_container_constructor_kwargs(lvf, **kwargs)
    assert lvf.normal_head_terminal == normal_head_terminal
    assert list(lvf.normal_energizing_feeders) == normal_energizing_feeders
    assert list(lvf.current_equipment) == current_equipment
    assert list(lvf.current_energizing_feeders) == current_energizing_feeders
    assert lvf.normal_energizing_lv_substation == normal_energizing_lv_substation


def test_lv_feeder_constructor_args():
    lvf = LvFeeder(*lv_feeder_args)

    verify_equipment_container_constructor_args(lvf)
    assert lv_feeder_args[-5:-4] == [
        lvf.normal_head_terminal
    ]
    # We use a different style of matching here as the passed in args for normal_energizing_feeders and current_equipment
    # are maps and the stored collections are lists.
    assert list(lvf.normal_energizing_feeders) == list(lv_feeder_args[-4].values())
    assert list(lvf.current_equipment) == list(lv_feeder_args[-3].values())
    assert list(lvf.current_energizing_feeders) == list(lv_feeder_args[-2].values())
    assert lvf.normal_energizing_lv_substation == lv_feeder_args[-1]


def test_current_equipment_collection():
    validate_unordered(
        LvFeeder,
        lambda mrid: Equipment(mrid),
        LvFeeder.current_equipment,
        LvFeeder.num_current_equipment,
        LvFeeder.get_current_equipment,
        LvFeeder.add_current_equipment,
        LvFeeder.remove_current_equipment,
        LvFeeder.clear_current_equipment
    )


def test_normal_energizing_feeder_collection():
    validate_unordered(
        LvFeeder,
        lambda mrid: Feeder(mrid),
        LvFeeder.normal_energizing_feeders,
        LvFeeder.num_normal_energizing_feeders,
        LvFeeder.get_normal_energizing_feeder,
        LvFeeder.add_normal_energizing_feeder,
        LvFeeder.remove_normal_energizing_feeder,
        LvFeeder.clear_normal_energizing_feeders
    )


def test_current_energizing_feeder_collection():
    validate_unordered(
        LvFeeder,
        lambda mrid: Feeder(mrid),
        LvFeeder.current_energizing_feeders,
        LvFeeder.num_current_energizing_feeders,
        LvFeeder.get_current_energizing_feeder,
        LvFeeder.add_current_energizing_feeder,
        LvFeeder.remove_current_energizing_feeder,
        LvFeeder.clear_current_energizing_feeders
    )
