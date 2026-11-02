#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import lv_feeder_kwargs
from cim.iec61970.base.core.test_equipment_container import verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs
from cim.private_collection_validator import validate_unordered
from zepben.ewb import Equipment, LvFeeder, generate_id
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder


def test_lv_feeder_constructor_default():
    lvf = LvFeeder(mrid=generate_id())

    verify_equipment_container_constructor_default(lvf)
    assert lvf.normal_head_terminal is None
    assert not list(lvf.normal_energizing_feeders)
    assert not list(lvf.current_equipment)
    assert not list(lvf.current_energizing_feeders)
    assert lvf.normal_energizing_lv_substation is None


@given(**lv_feeder_kwargs())
def test_lv_feeder_constructor_kwargs(
    normal_head_terminal,
    normal_energizing_feeders,
    current_equipment,
    current_energizing_feeders,
    normal_energizing_lv_substation,
    **kwargs,
):
    lvf = LvFeeder(
        normal_head_terminal=normal_head_terminal,
        normal_energizing_feeders=normal_energizing_feeders,
        current_equipment=current_equipment,
        current_energizing_feeders=current_energizing_feeders,
        normal_energizing_lv_substation=normal_energizing_lv_substation,
        **kwargs,
    )

    verify_equipment_container_constructor_kwargs(lvf, **kwargs)
    assert lvf.normal_head_terminal == normal_head_terminal
    assert list(lvf.normal_energizing_feeders) == normal_energizing_feeders
    assert list(lvf.current_equipment) == current_equipment
    assert list(lvf.current_energizing_feeders) == current_energizing_feeders
    assert lvf.normal_energizing_lv_substation == normal_energizing_lv_substation


def test_current_equipment_collection():
    validate_unordered(
        LvFeeder,
        lambda mrid: Equipment(mrid),
        LvFeeder.current_equipment,
        LvFeeder.num_current_equipment,
        LvFeeder.get_current_equipment,
        LvFeeder.add_current_equipment,
        LvFeeder.remove_current_equipment,
        LvFeeder.clear_current_equipment,
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
        LvFeeder.clear_normal_energizing_feeders,
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
        LvFeeder.clear_current_energizing_feeders,
    )
