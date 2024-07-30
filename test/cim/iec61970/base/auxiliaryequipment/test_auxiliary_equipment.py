#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import builds

from cim.iec61970.base.core.test_equipment import equipment_kwargs, verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs, verify_equipment_constructor_args, equipment_args
from zepben.evolve import AuxiliaryEquipment, Terminal

auxiliary_equipment_kwargs = {
    **equipment_kwargs,
    "terminal": builds(Terminal)
}

auxiliary_equipment_args = [*equipment_args, Terminal()]


def verify_auxiliary_equipment_constructor_default(ae: AuxiliaryEquipment):
    verify_equipment_constructor_default(ae)
    assert not ae.terminal


def verify_auxiliary_equipment_constructor_kwargs(ae: AuxiliaryEquipment, terminal, **kwargs):
    verify_equipment_constructor_kwargs(ae, **kwargs)
    assert ae.terminal == terminal


def verify_auxiliary_equipment_constructor_args(ae: AuxiliaryEquipment):
    verify_equipment_constructor_args(ae)
    assert ae.terminal == auxiliary_equipment_args[-1]
