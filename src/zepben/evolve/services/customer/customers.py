#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclassy import dataclass

from zepben.evolve.services.common.base_service import BaseService

__all__ = ["CustomerService"]


class CustomerService(BaseService):
    """
    Used to store Customer related types.
    """
    name: str = "customer"
