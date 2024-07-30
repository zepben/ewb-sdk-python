#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, PerLengthSequenceImpedance, AcLineSegment, Pole, Streetlight, PowerTransformerInfo, PowerTransformer
from zepben.evolve import resolver


def test_resolves_acls_plsi():
    ns = NetworkService()
    plsi = PerLengthSequenceImpedance()
    acls = AcLineSegment(per_length_sequence_impedance=plsi)
    br = resolver.per_length_sequence_impedance(acls)
    ns.resolve_or_defer_reference(br, plsi.mrid)
    assert plsi.mrid in ns.get_unresolved_reference_mrids_by_resolver(br)
    ns.add(acls)
    acls_fetched = ns.get(acls.mrid)
    assert acls_fetched.per_length_sequence_impedance == plsi

    ns = NetworkService()
    ns.add(plsi)
    ns.resolve_or_defer_reference(resolver.per_length_sequence_impedance(acls), plsi.mrid)
    assert len(list(ns.get_unresolved_reference_mrids_by_resolver(br))) == 0
    ns.add(acls)
    acls_fetched = ns.get(acls.mrid)
    assert acls_fetched.per_length_sequence_impedance == plsi


def test_resolves_pt_pti():
    ns = NetworkService()
    pti = PowerTransformerInfo()
    pt = PowerTransformer()
    pt.asset_info = pti

    br = resolver.power_transformer_info(pt)
    ns.resolve_or_defer_reference(br, pti.mrid)

    assert pti.mrid in ns.get_unresolved_reference_mrids_by_resolver(br)

    ns.add(pt)
    pt_fetched = ns.get(pt.mrid)
    assert pt_fetched.asset_info == pti

    ns = NetworkService()
    ns.add(pti)
    ns.resolve_or_defer_reference(resolver.power_transformer_info(pt), pti.mrid)
    assert len(list(ns.get_unresolved_reference_mrids_by_resolver(br))) == 0
    ns.add(pt)
    pt_fetched = ns.get(pt.mrid)
    assert pt_fetched.asset_info == pti


def test_resolves_pole_streetlight():
    ns = NetworkService()
    pole = Pole()
    streetlight = Streetlight(pole=pole)
    pole.add_streetlight(streetlight)
    br = resolver.streetlights(pole)
    ns.resolve_or_defer_reference(br, streetlight.mrid)
    assert str(streetlight.mrid) in ns.get_unresolved_reference_mrids_by_resolver(br)
    ns.add(pole)
    assert len(list(ns.get_unresolved_reference_mrids_by_resolver(br))) == 1
    ns.add(streetlight)
    assert len(list(ns.get_unresolved_reference_mrids_by_resolver(br))) == 0
    streetlight_fetched = ns.get(streetlight.mrid)
    assert streetlight == streetlight_fetched
