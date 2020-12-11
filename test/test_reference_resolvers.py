#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, PerLengthSequenceImpedance, AcLineSegment, Pole, Streetlight
from zepben.evolve import resolver


def test_resolves_acls_plsi():
    ns = NetworkService()
    plsi = PerLengthSequenceImpedance()
    acls = AcLineSegment(per_length_sequence_impedance=plsi)
    br = resolver.per_length_sequence_impedance(acls)
    ns.resolve_or_defer_reference(br, plsi.mrid)
    assert plsi.mrid in ns.get_unresolved_reference_mrids(br)
    ns.add(acls)
    acls_fetched = ns.get(acls.mrid)
    assert acls_fetched.per_length_sequence_impedance == plsi

    ns = NetworkService()
    ns.add(plsi)
    ns.resolve_or_defer_reference(resolver.per_length_sequence_impedance(acls), plsi.mrid)
    assert len(list(ns.get_unresolved_reference_mrids(br))) == 0
    ns.add(acls)
    acls_fetched = ns.get(acls.mrid)
    assert acls_fetched.per_length_sequence_impedance == plsi


def test_resolves_pole_streetlight():
    ns = NetworkService()
    pole = Pole()
    streetlight = Streetlight(pole=pole)
    pole.add_streetlight(streetlight)
    br = resolver.streetlights(pole)
    ns.resolve_or_defer_reference(br, streetlight.mrid)
    assert streetlight.mrid in ns.get_unresolved_reference_mrids(br)
    ns.add(streetlight)
    assert len(list(ns.get_unresolved_reference_mrids(br))) == 0
    streetlight_fetched = ns.get(streetlight.mrid)
    assert streetlight == streetlight_fetched
