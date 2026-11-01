#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["NetworkModelProjectComponent"]

import datetime
from typing import TYPE_CHECKING
from abc import ABCMeta

from zepben.ewb import require
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.extensions.zbex import zbex

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject


@zbex
@zb_dataclass
class NetworkModelProjectComponent(IdentifiedObject, metaclass=ABCMeta):
    """
    [ZBEX] Abstract class for both a network model project and network model change.
    """

    created: datetime.datetime | None = None
    """[ZBEX] When the component was created."""

    updated: datetime.datetime | None = None
    """[ZBEX] When the component was last updated."""

    closed: datetime.datetime | None = None
    """[ZBEX] When the component was deleted."""

    _parent: NetworkModelProject | None = None

    def __init__(self, mrid: str, *_, parent: NetworkModelProject | None = None, **kwargs):
        super(NetworkModelProjectComponent, self).__init__(mrid=mrid, **kwargs)
        if parent is not None:
            self.parent = parent

    @property
    def parent(self) -> NetworkModelProject | None:
        """[ZBEX] The contained Network Model Project Component (Restricted to just NetworkModelProject)."""
        return self._parent

    @parent.setter
    def parent(self, value: NetworkModelProject | None):
        require(self._parent is None, lambda: f"Parent already set for NetworkModelProjectComponent {self.mrid}.")
        self._parent = value

    def delete(self) -> bool:
        """
        Delete this `NetworkModelProject`.

        :return: true if the `NetworkModelProjectComponent` was deleted, false otherwise.
        """
        if self.closed is not None:
            return False

        self.closed = datetime.datetime.now(datetime.timezone.utc)
        return True
