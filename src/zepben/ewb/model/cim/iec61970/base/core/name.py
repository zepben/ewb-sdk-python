#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Name"]

from typing import TYPE_CHECKING, Optional

from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass
from zepben.ewb.dataclass_descriptors.descriptor_fix import remove_descriptor_annotations
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
    from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType


@zb_dataclass
@remove_descriptor_annotations
class Name(Identifiable):
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

    def __init__(self,
                 name: str,
                 *_,
                 type: NameType,
                 identified_object: IdentifiedObject | None = None,
                 **kwargs):
        if "mrid" in kwargs:
            raise TypeError("NameType.mrid and NameType.name are equivalent - cannot pass both")
        io_mrid = "" if identified_object is None else identified_object.mrid
        mrid = f"{name}-{type.name}-{io_mrid}"
        super(Name, self).__init__(mrid=mrid, name=name, type=type, identified_object=identified_object, **kwargs)

    def __eq__(self, other):
        # Names are recreated when added to an IdObj, so we cannot check equality on identity
        return isinstance(other, Name) and other.mrid == self.mrid

    def __hash__(self):
        # Objects implementing __eq__ require a __hash__ because Python
        return object.__hash__(self)
