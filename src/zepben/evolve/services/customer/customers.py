#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CustomerService"]

from typing import Optional

from zepben.evolve.services.common.base_service import BaseService
from zepben.evolve.services.common.meta.metadata_collection import MetadataCollection


class CustomerService(BaseService):
    """
    Used to store Customer related types.
    """

    def __init__(
        self,
        metadata: Optional[MetadataCollection] = None
    ):
        super().__init__("customer", metadata)
