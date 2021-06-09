#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import builds

from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim_creators import sampled_asset_info
from zepben.evolve import PowerSystemResource, Location, PowerTransformerInfo

power_system_resource_kwargs = {
    **identified_object_kwargs,
    "location": builds(Location),
    "asset_info": sampled_asset_info()
}

power_system_resource_args = [*identified_object_args, Location(), PowerTransformerInfo()]


def verify_power_system_resource_constructor_default(psr: PowerSystemResource):
    verify_identified_object_constructor_default(psr)
    assert psr.location is None
    assert psr.asset_info is None


def verify_power_system_resource_constructor_kwargs(psr: PowerSystemResource, location, asset_info, **kwargs):
    verify_identified_object_constructor_kwargs(psr, **kwargs)
    assert psr.location is location
    assert psr.asset_info is asset_info


def verify_power_system_resource_constructor_args(psr: PowerSystemResource):
    verify_identified_object_constructor_args(psr)
    assert psr.location is power_system_resource_args[-2]
    assert psr.asset_info is power_system_resource_args[-1]
