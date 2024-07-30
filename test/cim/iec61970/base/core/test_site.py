#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Site

site_kwargs = equipment_container_kwargs
site_args = equipment_container_args


def test_site_constructor_default():
    verify_equipment_container_constructor_default(Site())


@given(**site_kwargs)
def test_site_constructor_kwargs(**kwargs):
    verify_equipment_container_constructor_kwargs(Site(**kwargs), **kwargs)


def test_site_constructor_args():
    verify_equipment_container_constructor_args(Site(*site_args))
