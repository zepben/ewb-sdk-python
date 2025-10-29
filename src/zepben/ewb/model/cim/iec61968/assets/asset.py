#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Asset"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import get_by_mrid, nlen, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole
    from zepben.ewb.model.cim.iec61968.common.location import Location
    from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource


@dataslot
@boilermaker
class Asset(IdentifiedObject):
    """
    Tangible resource of the utility, including power system equipment, various end devices, cabinets, buildings,
    etc. For electrical network equipment, the role of the asset is defined through PowerSystemResource and its
    subclasses, defined mainly in the Wires model (refer to IEC61970-301 and model package IEC61970::Wires). Asset
    description places emphasis on the physical characteristics of the equipment fulfilling that role.
    """

    location: Location | None = None
    """`zepben.ewb.model.cim.iec61968.common.location.Location` of this asset"""

    organisation_roles: List[AssetOrganisationRole] | None = MRIDListAccessor()

    power_system_resources: List[PowerSystemResource] | None = MRIDListAccessor()

    def _retype(self):
        self.organisation_roles: MRIDListRouter = ...
        self.power_system_resources: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(organisation_roles) instead")
    def num_organisation_roles(self) -> int:
        return len(self.organisation_roles)

    @deprecated("BOILERPLATE: Use organisation_roles.get_by_mrid(mrid) instead")
    def get_organisation_role(self, mrid: str) -> AssetOrganisationRole:
        return self.organisation_roles.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use organisation_roles.append(role) instead")
    def add_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        return self.organisation_roles.append(role)

    @deprecated("BOILERPLATE: Use organisation_roles.remove(role) instead")
    def remove_organisation_role(self, role: AssetOrganisationRole) -> Asset:
        return self.organisation_roles.remove(role)

    @deprecated("BOILERPLATE: Use organisation_roles.clear() instead")
    def clear_organisation_roles(self) -> Asset:
        return self.organisation_roles.clear()

    @deprecated("BOILERPLATE: Use len(power_system_resources) instead")
    def num_power_system_resources(self) -> int:
        return len(self.power_system_resources)

    @deprecated("BOILERPLATE: Use power_system_resources.get_by_mrid(mrid) instead")
    def get_power_system_resource(self, mrid: str) -> PowerSystemResource:
        return self.power_system_resources.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use power_system_resources.append(resource) instead")
    def add_power_system_resource(self, resource: PowerSystemResource) -> Asset:
        return self.power_system_resources.append(resource)

    @deprecated("BOILERPLATE: Use power_system_resources.remove(resource) instead")
    def remove_power_system_resource(self, resource: PowerSystemResource) -> Asset:
        return self.power_system_resources.remove(resource)

    @deprecated("BOILERPLATE: Use power_system_resources.clear() instead")
    def clear_power_system_resources(self) -> Asset:
        return self.power_system_resources.clear()
        return self
