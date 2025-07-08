#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["OrganisationRole"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.common.organisation import Organisation


class OrganisationRole(IdentifiedObject):
    """
    Identifies a way in which an organisation may participate in the utility enterprise (e.g., customer, manufacturer, etc).
    """

    organisation: Optional['Organisation'] = None
    """The `zepben.ewb.model.cim.iec61968.common.organisation.Organisation` having this role."""
