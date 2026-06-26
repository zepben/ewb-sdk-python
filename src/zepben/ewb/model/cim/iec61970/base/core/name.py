#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Name"]

from typing import TYPE_CHECKING, Optional

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.dataclass_descriptors import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
    from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType


@zb_dataclass
class Name(Identifiable):
    """
    The Name class provides the means to define any number of human-readable names for an object. A name is **not** to be used for defining inter-object
    relationships. For inter-object relationships instead use the object identification 'mRID'.
    """

    # This is required because python dataclasses don't support overwriting a field with a @property.
    # We need to force-attach it after the class is created.
    def _get_mrid(self):
        return f"{self.name}-{self.type.name}-{self.identified_object.mrid}"

    name: str
    """Any free text that name the object."""

    type: NameType
    """Type of this name."""

    identified_object: Optional[IdentifiedObject] = None
    """Identified object that this name designates."""


# Can't error on mrid being set - dataclass init auto-assigns it
def _ignore_set(*_):
    pass

# Force dataclass to reckon with our property overwrite - otherwise it get ignored
# noinspection PyProtectedMember,PyTypeChecker
Name.mrid = property(Name._get_mrid, _ignore_set)
