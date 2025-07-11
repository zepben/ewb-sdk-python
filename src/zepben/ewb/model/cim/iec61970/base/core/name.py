#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Name"]

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
    from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType


#
# NOTE: unsafe_hash is used as we can't mark this class frozen due to needing to update/lazy initialise the identified_object, which shouldn't change once
#       it has been initialised.
#
@dataclass(unsafe_hash=True)
class Name:
    """
    The Name class provides the means to define any number of human-readable names for an object. A name is **not** to be used for defining inter-object
    relationships. For inter-object relationships instead use the object identification 'mRID'.
    """

    name: str
    """Any free text that name the object."""

    type: NameType
    """Type of this name."""

    identified_object: Optional[IdentifiedObject] = None
    """Identified object that this name designates."""
