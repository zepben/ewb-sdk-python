#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import NetworkService, DiagramService, CustomerService
from zepben.ewb.services.services import Services
from zepben.ewb.services.variant.variant_service import VariantService

expected_ns = NetworkService()
expected_ds = DiagramService()
expected_cs = CustomerService()
expected_vs = VariantService()

services = Services(expected_ns, expected_ds, expected_cs, expected_vs)


def test_accessors():
    assert services.network_service is expected_ns
    assert services.diagram_service is expected_ds
    assert services.customer_service is expected_cs
    assert services.variant_service is expected_vs


def test_supports_destructuring():
    (ns, ds, cs, vs) = services

    assert ns is expected_ns
    assert ds is expected_ds
    assert cs is expected_cs
    assert vs is expected_vs
