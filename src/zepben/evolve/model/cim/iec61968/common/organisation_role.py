#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Organisation

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["OrganisationRole"]


class OrganisationRole(IdentifiedObject):
    """
    Identifies a way in which an organisation may participate in the utility enterprise (e.g., customer, manufacturer, etc).
    """

    organisation: Optional[Organisation] = None
    """The `zepben.evolve.cim.iec61968.common.organisation.Organisation` having this role."""
