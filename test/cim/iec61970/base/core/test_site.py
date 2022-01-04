#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from test.cim.common_testing_functions import verify
from test.cim.test_common_two_way_connections import check_equipment_container_connection
from test.cim.iec61970.base.core.test_equipment_container import equipment_container_kwargs, verify_equipment_container_constructor_default, \
    verify_equipment_container_constructor_kwargs, verify_equipment_container_constructor_args, equipment_container_args
from zepben.evolve import Site, Equipment
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_site

site_kwargs = equipment_container_kwargs
site_args = equipment_container_args


def test_site_constructor_default():
    verify_equipment_container_constructor_default(Site())
    verify_equipment_container_constructor_default(create_site())


# noinspection PyShadowingNames
@given(data())
def test_site_constructor_kwargs(data):
    verify(
        [Site, create_site],
        data, site_kwargs, verify_equipment_container_constructor_kwargs
    )


def test_site_constructor_args():
    verify_equipment_container_constructor_args(Site(*site_args))


def test_auto_two_way_connections_for_site_constructor():
    e = Equipment()
    p = create_site(equipment=[e])

    check_equipment_container_connection(e=e, ec=p)
