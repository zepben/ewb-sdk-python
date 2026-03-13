#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Name"]

from typing import TYPE_CHECKING, Optional

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
    from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType


class Name(Identifiable):
    """
    The Name class provides the means to define any number of human-readable names for an object. A name is **not** to be used for defining inter-object
    relationships. For inter-object relationships instead use the object identification 'mRID'.
    """

    @property
    def mrid(self) -> str:
        return f"{self.name}-{self.type.name}-{self.identified_object.mrid}"

    def __getattribute__(self, item):
        # This is a workaround for self.mrid being a property, when we're expecting a string.
        if item == "mrid":
            return object.__getattribute__(self, 'mrid').fget(self)
        return object.__getattribute__(self, item)

    name: str
    """Any free text that name the object."""

    type: NameType
    """Type of this name."""

    identified_object: Optional[IdentifiedObject] = None
    """Identified object that this name designates."""

    def __str__(self) -> str:
        class_name = f'{self.__class__.__name__}'
        if self.name:
            return f'{class_name}{{{self.mrid}|{self.name}}}'
        return f'{class_name}{{{self.mrid}}}'
