#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from zepben.ewb import Connector, Conductor, CableInfo, generate_id

connector_kwargs = conducting_equipment_kwargs
connector_args = conducting_equipment_args


def verify_connector_constructor_default(c: Connector):
    verify_conducting_equipment_constructor_default(c)


def verify_connector_constructor_kwargs(c: Connector, **kwargs):
    verify_conducting_equipment_constructor_kwargs(c, **kwargs)


def verify_connector_constructor_args(c: Connector):
    verify_conducting_equipment_constructor_args(c)


def test_is_underground():
    c = Conductor(mrid=generate_id())
    assert not c.is_underground()

    c.wire_info = CableInfo(mrid=generate_id())
    assert c.is_underground()
