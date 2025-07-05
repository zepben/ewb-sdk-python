#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists
from pytest import raises
from zepben.evolve import Terminal, Substation, Equipment, LvFeeder, Switch
from zepben.evolve.model.cim.iec61970.base.core.feeder import Feeder

from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from cim.private_collection_validator import validate_unordered_1234567890

feeder_kwargs = {
    **equipment_container_kwargs,
    "normal_head_terminal": builds(Terminal),
    "normal_energizing_substation": builds(Substation),
    "normal_energized_lv_feeders": lists(builds(LvFeeder), max_size=2),
    "current_equipment": lists(builds(Equipment), max_size=2),
    "current_energized_lv_feeders": lists(builds(LvFeeder), max_size=2)
}

feeder_args = [*equipment_container_args, Terminal(), Substation(), {"lvf": LvFeeder()}, {"ce": Equipment()}, {"celvf": Equipment()}]


def test_feeder_constructor_default():
    f = Feeder()

    verify_equipment_container_constructor_default(f)
    assert not f.normal_head_terminal
    assert not f.normal_energizing_substation
    assert not list(f.normal_energized_lv_feeders)
    assert not list(f.current_equipment)
    assert not list(f.current_energized_lv_feeders)


@given(**feeder_kwargs)
def test_feeder_constructor_kwargs(normal_head_terminal, normal_energizing_substation, normal_energized_lv_feeders, current_equipment, current_energized_lv_feeders, **kwargs):
    f = Feeder(normal_head_terminal=normal_head_terminal,
               normal_energizing_substation=normal_energizing_substation,
               normal_energized_lv_feeders=normal_energized_lv_feeders,
               current_equipment=current_equipment,
               current_energized_lv_feeders=current_energized_lv_feeders,
               **kwargs)

    verify_equipment_container_constructor_kwargs(f, **kwargs)
    assert f.normal_head_terminal == normal_head_terminal
    assert f.normal_energizing_substation == normal_energizing_substation
    assert list(f.normal_energized_lv_feeders) == normal_energized_lv_feeders
    assert list(f.current_equipment) == current_equipment
    assert list(f.current_energized_lv_feeders) == current_energized_lv_feeders


def test_feeder_constructor_args():
    f = Feeder(*feeder_args)

    verify_equipment_container_constructor_args(f)

    assert feeder_args[-5:-3] == [
        f.normal_head_terminal,
        f.normal_energizing_substation
    ]
    # We use a different style of matching here as the passed in args for current_equipment and normal_energized_lv_feeders
    # are maps and the stored collections are lists.
    assert list(f.current_equipment) == list(feeder_args[-3].values())
    assert list(f.normal_energized_lv_feeders) == list(feeder_args[-2].values())
    assert list(f.current_energized_lv_feeders) == list(feeder_args[-1].values())


def test_current_equipment_collection():
    validate_unordered_1234567890(
        Feeder,
        lambda mrid: Equipment(mrid),
        Feeder.current_equipment,
        Feeder.num_current_equipment,
        Feeder.get_current_equipment,
        Feeder.add_current_equipment,
        Feeder.remove_current_equipment,
        Feeder.clear_current_equipment
    )


def test_normal_energized_lv_feeder_collection():
    validate_unordered_1234567890(
        Feeder,
        lambda mrid: LvFeeder(mrid),
        Feeder.normal_energized_lv_feeders,
        Feeder.num_normal_energized_lv_feeders,
        Feeder.get_normal_energized_lv_feeder,
        Feeder.add_normal_energized_lv_feeder,
        Feeder.remove_normal_energized_lv_feeder,
        Feeder.clear_normal_energized_lv_feeders
    )


def test_current_energized_lv_feeder_collection():
    validate_unordered_1234567890(
        Feeder,
        lambda mrid: LvFeeder(mrid),
        Feeder.current_energized_lv_feeders,
        Feeder.num_current_energized_lv_feeders,
        Feeder.get_current_energized_lv_feeder,
        Feeder.add_current_energized_lv_feeder,
        Feeder.remove_current_energized_lv_feeder,
        Feeder.clear_current_energized_lv_feeders
    )


def test_can_update_normal_head_terminal_on_empty_feeder():
    empty_feeder = Feeder()
    terminal1 = Terminal()
    terminal2 = Terminal()

    empty_feeder.normal_head_terminal = terminal1
    assert empty_feeder.normal_head_terminal == terminal1

    empty_feeder.normal_head_terminal = terminal2
    assert empty_feeder.normal_head_terminal == terminal2

    empty_feeder.normal_head_terminal = None
    assert empty_feeder.normal_head_terminal is None

    equipment = Switch()
    empty_feeder.add_equipment(equipment).add_current_equipment(equipment)
    empty_feeder.clear_equipment().clear_current_equipment()

    empty_feeder.normal_head_terminal = terminal1
    assert empty_feeder.normal_head_terminal == terminal1


def test_block_normal_head_terminal_update_when_equipment_assigned():
    feeder = Feeder(mrid="fdr")
    terminal1 = Terminal()
    terminal2 = Terminal()

    equipment = Switch()

    feeder.add_equipment(equipment)

    # allows initial assignment
    feeder.normal_head_terminal = terminal1
    assert feeder.normal_head_terminal == terminal1

    # doesn't raise exception on trying to reassign the same terminal
    feeder.normal_head_terminal = terminal1
    assert feeder.normal_head_terminal == terminal1

    with raises(ValueError, match="Feeder fdr has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned."):
        feeder.normal_head_terminal = terminal2
    assert feeder.normal_head_terminal == terminal1


def test_block_normal_head_terminal_update_when_current_equipment_assigned():
    feeder = Feeder(mrid="fdr")
    terminal1 = Terminal()
    terminal2 = Terminal()

    equipment = Switch()

    feeder.add_current_equipment(equipment)

    # allows initial assignment
    feeder.normal_head_terminal = terminal1
    assert feeder.normal_head_terminal == terminal1

    # doesn't raise exception on trying to reassign the same terminal
    feeder.normal_head_terminal = terminal1
    assert feeder.normal_head_terminal == terminal1

    with raises(ValueError, match="Feeder fdr has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned."):
        feeder.normal_head_terminal = terminal2
    assert feeder.normal_head_terminal == terminal1
