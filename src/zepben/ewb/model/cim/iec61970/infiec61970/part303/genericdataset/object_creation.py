#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["ObjectCreation"]

from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember


class ObjectCreation(ChangeSetMember):
    """
    An object is to be created in the context.
    """
