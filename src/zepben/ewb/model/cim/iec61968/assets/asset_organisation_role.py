#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AssetOrganisationRole"]

from abc import ABCMeta

from zepben.ewb.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.ewb.dataclass_descriptors import zb_dataclass


@zb_dataclass
class AssetOrganisationRole(OrganisationRole, metaclass=ABCMeta):
    """ Role an organisation plays with respect to asset. """
    pass
