#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.ewb import NetworkService, DiagramService, CustomerService
from zepben.ewb.services.variant.variant_service import VariantService


class Services:
    """
    A convenience class for storing the data supported by the SDK.

    :param network_service: An optional `NetworkService` to add to the services, otherwise an empty `NetworkService` will be created.
    :param diagram_service: An optional `DiagramService` to add to the services, otherwise an empty `DiagramService` will be created.
    :param customer_service: An optional `CustomerService` to add to the services, otherwise an empty `CustomerService` will be created.
    :param variant_service: An optional `VariantService` to add to the services, otherwise an empty `VariantService` will be created.
    """

    def __init__(
        self,
        network_service: Optional[NetworkService] = NetworkService(),
        diagram_service: Optional[DiagramService] = DiagramService(),
        customer_service: Optional[CustomerService] = CustomerService(),
        variant_service: Optional[VariantService] = VariantService()
    ):
        super().__init__()
        self.network_service = network_service
        """The `NetworkService` of these services."""

        self.diagram_service = diagram_service
        """The `DiagramService` of these services."""

        self.customer_service = customer_service
        """The `CustomerService` of these services."""

        self.variant_service = variant_service
        """The `VariantService` of these services."""

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        self._iter_index += 1
        if self._iter_index == 1:
            return self.network_service
        elif self._iter_index == 2:
            return self.diagram_service
        elif self._iter_index == 3:
            return self.customer_service
        elif self._iter_index == 4:
            return self.variant_service
        else:
            raise StopIteration
