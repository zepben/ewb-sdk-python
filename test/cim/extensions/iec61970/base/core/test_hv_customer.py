#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.core.test_equipment_container import verify_equipment_container_constructor_default, verify_equipment_container_constructor_kwargs, \
    verify_equipment_container_constructor_args, equipment_container_kwargs, equipment_container_args
from zepben.ewb import generate_id
from zepben.ewb.model.cim.extensions.iec61970.base.core.hv_customer import HvCustomer

hv_customer_kwargs = equipment_container_kwargs
hv_customer_args = equipment_container_args


def test_hv_customer_constructor_default():
    verify_equipment_container_constructor_default(HvCustomer(mrid=generate_id()))


@given(**hv_customer_kwargs)
def test_hv_customer_constructor_kwargs(**kwargs):
    verify_equipment_container_constructor_kwargs(HvCustomer(**kwargs), **kwargs)


def test_hv_customer_constructor_args():
    verify_equipment_container_constructor_args(HvCustomer(*hv_customer_args))
