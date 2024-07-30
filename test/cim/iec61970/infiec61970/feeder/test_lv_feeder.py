#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Feeder, Terminal, Substation, Equipment, LvFeeder

lv_feeder_kwargs = {
    **equipment_container_kwargs,
    "normal_head_terminal": builds(Terminal),
    "normal_energizing_feeders": lists(builds(Feeder), max_size=2),
    "current_equipment": lists(builds(Equipment), max_size=2)
}

lv_feeder_args = [*equipment_container_args, Terminal(), {"f": Feeder()}, {"ce": Equipment()}]


def test_lv_feeder_constructor_default():
    lvf = LvFeeder()

    verify_equipment_container_constructor_default(lvf)
    assert not lvf.normal_head_terminal
    assert not list(lvf.normal_energizing_feeders)
    assert not list(lvf.current_equipment)


@given(**lv_feeder_kwargs)
def test_lv_feeder_constructor_kwargs(normal_head_terminal, normal_energizing_feeders, current_equipment, **kwargs):
    lvf = LvFeeder(normal_head_terminal=normal_head_terminal,
                   normal_energizing_feeders=normal_energizing_feeders,
                   current_equipment=current_equipment,
                   **kwargs)

    verify_equipment_container_constructor_kwargs(lvf, **kwargs)
    assert lvf.normal_head_terminal == normal_head_terminal
    assert list(lvf.normal_energizing_feeders) == normal_energizing_feeders
    assert list(lvf.current_equipment) == current_equipment


def test_lv_feeder_constructor_args():
    lvf = LvFeeder(*lv_feeder_args)

    verify_equipment_container_constructor_args(lvf)
    assert lvf.normal_head_terminal == lv_feeder_args[-3]
    assert list(lvf.normal_energizing_feeders) == list(lv_feeder_args[-2].values())
    assert list(lvf.current_equipment) == list(lv_feeder_args[-1].values())


def test_current_equipment_collection():
    validate_collection_unordered(LvFeeder,
                                  lambda mrid, _: Equipment(mrid),
                                  LvFeeder.num_current_equipment,
                                  LvFeeder.get_current_equipment,
                                  LvFeeder.current_equipment,
                                  LvFeeder.add_current_equipment,
                                  LvFeeder.remove_current_equipment,
                                  LvFeeder.clear_current_equipment,
                                  KeyError)


def test_normal_energizing_feeder_collection():
    validate_collection_unordered(LvFeeder,
                                  lambda mrid, _: Feeder(mrid),
                                  LvFeeder.num_normal_energizing_feeders,
                                  LvFeeder.get_normal_energizing_feeder,
                                  LvFeeder.normal_energizing_feeders,
                                  LvFeeder.add_normal_energizing_feeder,
                                  LvFeeder.remove_normal_energizing_feeder,
                                  LvFeeder.clear_normal_energizing_feeders,
                                  KeyError)
