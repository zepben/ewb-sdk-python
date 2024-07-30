#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.wires.test_connector import verify_connector_constructor_default, \
    verify_connector_constructor_kwargs, verify_connector_constructor_args, connector_kwargs, connector_args
from zepben.evolve import BusbarSection

busbar_section_kwargs = connector_kwargs
busbar_section_args = connector_args


def test_busbar_section_constructor_default():
    verify_connector_constructor_default(BusbarSection())


@given(**busbar_section_kwargs)
def test_busbar_section_constructor_kwargs(**kwargs):
    verify_connector_constructor_kwargs(BusbarSection(**kwargs), **kwargs)


def test_busbar_section_constructor_args():
    verify_connector_constructor_args(BusbarSection(*busbar_section_args))
