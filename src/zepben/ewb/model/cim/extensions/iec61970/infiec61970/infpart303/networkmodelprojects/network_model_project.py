#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["NetworkModelProject"]

import datetime
from typing import List, Generator

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.util import get_by_mrid, ngen, nlen


@zbex
@zb_dataclass
class NetworkModelProject(NetworkModelProjectComponent):
    """
    [ZBEX] A grouping of network model stages. Primarily used to organize the stages of an overall project.

    :
    """

    external_status: str | None = None
    """[ZBEX] The status of the project in the external system."""

    forecast_commission_date: datetime.datetime | None = None
    """[ZBEX] When the project is expected to be commissioned."""

    external_driver: str | None = None
    """[ZBEX] The driver of the project."""

    _children: List[NetworkModelProjectComponent] | None = None

    @property
    def children(self) -> Generator[NetworkModelProjectComponent, None, None]:
        """[ZBEX] Contained NetworkModelProjectComponent classes of this Project."""
        return ngen(self._children)

    def num_children(self) -> int:
        """Get the number of entries in the `children` collection."""
        return nlen(self._children)

    def get_child(self, mrid: str) -> NetworkModelProjectComponent | None:
        """
        Get the child `NetworkModelProjectComponent` identified by `mrid`.

        :param mrid: the mRID of the required `NetworkModelProjectComponent`.
        :return: The `NetworkModelProjectComponent` with the specified `mrid` if it exists, otherwise None.
        :raises KeyError: if no child with the given `mrid` exists.
        """
        return get_by_mrid(self._children, mrid)

    def add_child(self, child: NetworkModelProjectComponent) -> NetworkModelProject:
        """
        Add a child `NetworkModelProjectComponent` to this project.

        :param child: the `NetworkModelProjectComponent` to add.
        :return: A reference to this `NetworkModelProject` to allow fluent use.
        """
        if self._validate_reference(child, self.get_child, "A NetworkModelProjectComponent"):
            return self

        if self._children is None:
            self._children = []
        self._children.append(child)

        return self

    def remove_child(self, child: NetworkModelProjectComponent) -> bool:
        if self._children is None:
            return False
        try:
            self._children.remove(child)
        except ValueError:
            return False
        if not self._children:
            self._children = None
        return True

    def clear_children(self) -> NetworkModelProject:
        """
        Clear the collection of `NetworkModelProjectComponent`s.

        :return: A reference to this `NetworkModelProject` to allow fluent use.
        """
        self._children = None
        return self
