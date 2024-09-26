#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import lists, builds
from zepben.evolve import ConductingEquipment, BaseVoltage, Terminal

from cim.iec61970.base.core.test_equipment import equipment_kwargs, verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs, verify_equipment_constructor_args, equipment_args
from cim.private_collection_validator import validate_ordered_1234567890

conducting_equipment_kwargs = {
    **equipment_kwargs,
    "base_voltage": builds(BaseVoltage),
    "terminals": lists(builds(Terminal), max_size=2)
}

conducting_equipment_args = [*equipment_args, BaseVoltage(), [Terminal(), Terminal()]]


def verify_conducting_equipment_constructor_default(ce: ConductingEquipment):
    verify_equipment_constructor_default(ce)
    assert not ce.base_voltage
    assert not list(ce.terminals)


def verify_conducting_equipment_constructor_kwargs(ce: ConductingEquipment, base_voltage, terminals, **kwargs):
    verify_equipment_constructor_kwargs(ce, **kwargs)
    assert ce.base_voltage == base_voltage
    assert list(ce.terminals) == terminals


def verify_conducting_equipment_constructor_args(ce: ConductingEquipment):
    verify_equipment_constructor_args(ce)
    assert conducting_equipment_args[-2:] == [
        ce.base_voltage,
        list(ce.terminals)
    ]


def test_terminals_collection():
    validate_ordered_1234567890(
        ConductingEquipment,
        lambda mrid, sn: Terminal(mrid, sequence_number=sn),
        ConductingEquipment.terminals,
        ConductingEquipment.num_terminals,
        ConductingEquipment.get_terminal_by_mrid,
        ConductingEquipment.get_terminal_by_sn,
        ConductingEquipment.add_terminal,
        ConductingEquipment.remove_terminal,
        ConductingEquipment.clear_terminals,
        lambda t: t.sequence_number
    )
