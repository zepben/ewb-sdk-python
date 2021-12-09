#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_meter(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                 organisation_roles: List[AssetOrganisationRole] = None, customer_mrid: str = None, service_location: Location = None, 
                 usage_points: List[UsagePoint] = None) -> Meter:
    """
    Meter(EndDevice(AssetContainer(Asset(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    Asset: location, organisation_roles
    AssetContainer:
    EndDevice:
    Meter:
    """
    return Meter(**locals())


def create_usage_point(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, usage_point_location: Location = None,
                       is_virtual: bool = False, connection_category: str = None, equipment: List[Equipment] = None, end_devices: List[EndDevice] = None
                       ) -> UsagePoint:
    """
    UsagePoint(IdentifiedObject)   
    IdentifiedObject: mrid, name, description, names
    UsagePoint: usage_point_location, is_virtual, connection_category, equipment, end_devices
    """
    return UsagePoint(**locals())
