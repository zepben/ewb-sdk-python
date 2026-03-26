#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import lv_substation_kwargs
from cim.iec61970.base.core.test_equipment_container import equipment_container_args, \
    verify_equipment_container_constructor_default, verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args
from cim.private_collection_validator import validate_unordered
from util import assert_or_empty
from zepben.ewb import generate_id, LvFeeder, Feeder, Terminal, PowerTransformer, Fuse
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation

lv_substation_args = equipment_container_args


def test_lv_substation_constructor_default():
    verify_equipment_container_constructor_default(LvSubstation(mrid=generate_id()))


@given(**lv_substation_kwargs())
def test_lv_substation_constructor_kwargs(
    normal_energizing_feeders,
    current_energizing_feeders,
    normal_energized_lv_feeders,
    **kwargs
):
    lv_sub = LvSubstation(
        normal_energizing_feeders=normal_energizing_feeders,
        current_energizing_feeders=current_energizing_feeders,
        normal_energized_lv_feeders=normal_energized_lv_feeders,
        **kwargs
    )

    verify_equipment_container_constructor_kwargs(lv_sub, **kwargs)

    assert_or_empty(lv_sub.normal_energizing_feeders, normal_energizing_feeders)
    assert_or_empty(lv_sub.current_energizing_feeders, current_energizing_feeders)
    assert_or_empty(lv_sub.normal_energized_lv_feeders, normal_energized_lv_feeders)


def test_lv_substation_constructor_args():
    verify_equipment_container_constructor_args(LvSubstation(*lv_substation_args))


def test_normal_energized_lv_feeder_collection():
    validate_unordered(
        LvSubstation,
        lambda mrid: LvFeeder(mrid),
        LvSubstation.normal_energized_lv_feeders,
        LvSubstation.num_normal_energized_lv_feeders,
        LvSubstation.get_normal_energized_lv_feeder,
        LvSubstation.add_normal_energized_lv_feeder,
        LvSubstation.remove_normal_energized_lv_feeder,
        LvSubstation.clear_normal_energized_lv_feeders
    )


def test_normal_energizing_feeder_collection():
    validate_unordered(
        LvSubstation,
        lambda mrid: Feeder(mrid),
        LvSubstation.normal_energizing_feeders,
        LvSubstation.num_normal_energizing_feeders,
        LvSubstation.get_normal_energizing_feeder,
        LvSubstation.add_normal_energizing_feeder,
        LvSubstation.remove_normal_energizing_feeder,
        LvSubstation.clear_normal_energizing_feeders
    )


def test_current_energizing_feeder_collection():
    validate_unordered(
        LvSubstation,
        lambda mrid: Feeder(mrid),
        LvSubstation.current_energizing_feeders,
        LvSubstation.num_current_energizing_feeders,
        LvSubstation.get_current_energizing_feeder,
        LvSubstation.add_current_energizing_feeder,
        LvSubstation.remove_current_energizing_feeder,
        LvSubstation.clear_current_energizing_feeders
    )


def test_lv_switch_feeders():
    ptt = Terminal(mrid=generate_id())
    ft = Terminal(mrid=generate_id())
    PowerTransformer(mrid=generate_id()).add_terminal(ptt)
    Fuse(mrid=generate_id()).add_terminal(ft)
    (lvf1 := LvFeeder(mrid=generate_id())).normal_head_terminal = ptt
    (lvf2 := LvFeeder(mrid=generate_id())).normal_head_terminal = ft
    (lv_sub := LvSubstation(mrid=generate_id())) \
        .add_normal_energized_lv_feeder(lvf1) \
        .add_normal_energized_lv_feeder(lvf2)

    assert lvf2 in list(lv_sub.normal_energized_lv_switch_feeders())
