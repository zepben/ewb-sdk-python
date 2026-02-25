#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, equipment_container_args, \
    verify_equipment_container_constructor_default, verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args
from zepben.ewb import generate_id
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation

lv_substation_kwargs = equipment_container_kwargs
lv_substation_args = equipment_container_args


def test_lv_substation_constructor_default():
    verify_equipment_container_constructor_default(LvSubstation(mrid=generate_id()))


@given(**lv_substation_kwargs)
def test_lv_substation_constructor_kwargs(**kwargs):
    verify_equipment_container_constructor_kwargs(LvSubstation(**kwargs), **kwargs)


def test_lv_substation_constructor_args():
    verify_equipment_container_constructor_args(LvSubstation(*lv_substation_args))

# TODO: collection validation