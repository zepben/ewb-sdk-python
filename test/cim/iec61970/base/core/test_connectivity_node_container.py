#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_power_system_resource import power_system_resource_kwargs, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_args
from zepben.evolve import ConnectivityNodeContainer

connectivity_node_container_kwargs = power_system_resource_kwargs
connectivity_node_container_args = power_system_resource_args


def verify_connectivity_node_container_constructor_default(cnc: ConnectivityNodeContainer):
    verify_power_system_resource_constructor_default(cnc)


def verify_connectivity_node_container_constructor_kwargs(cnc: ConnectivityNodeContainer, **kwargs):
    verify_power_system_resource_constructor_kwargs(cnc, **kwargs)


def verify_connectivity_node_container_constructor_args(cnc: ConnectivityNodeContainer):
    verify_power_system_resource_constructor_args(cnc)
