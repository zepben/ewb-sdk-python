#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, DiagramService, CustomerService
from zepben.evolve.services.services import Services

expected_ns = NetworkService()
expected_ds = DiagramService()
expected_cs = CustomerService()

services = Services(expected_ns, expected_ds, expected_cs)


def test_accessors():
    assert services.network_service is expected_ns
    assert services.diagram_service is expected_ds
    assert services.customer_service is expected_cs


def test_supports_destructuring():
    (ns, ds, cs) = services

    assert ns is expected_ns
    assert ds is expected_ds
    assert cs is expected_cs
