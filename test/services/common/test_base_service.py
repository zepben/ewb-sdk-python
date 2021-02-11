#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Union

from pytest import fixture
from zepben.evolve import BaseService, Terminal, resolver, UnresolvedReference, Junction, BaseVoltage, Location, AcLineSegment, CableInfo, \
    PerLengthSequenceImpedance, IdentifiedObject, ConnectivityNode, Feeder


@fixture
def service():
    service = BaseService("base_service")
    yield service


def test_unresolved_bidirectional_references(service: BaseService):
    term = Terminal("t1")
    assert service.add(term)
    assert service.resolve_or_defer_reference(resolver.conducting_equipment(term), "j1") is False

    assert list(service.unresolved_references())[0] == UnresolvedReference(term.mrid, "j1", resolver.conducting_equipment(term).resolver)
    assert "j1" in service.get_unresolved_reference_mrids_by_resolver(resolver.conducting_equipment(term))

    j1 = Junction("j1")
    assert service.resolve_or_defer_reference(resolver.ce_terminals(j1), term.mrid)
    assert not list(service.unresolved_references())  # no unresolved refs now
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.conducting_equipment(term)))
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.ce_terminals(j1)))
    assert not service.has_unresolved_references()

    assert term.conducting_equipment is j1
    assert j1.get_terminal_by_mrid(term.mrid) is term
    assert service.add(j1)


def test_unresolved_unidirectional_references(service: BaseService):
    j1 = Junction("j1")
    assert service.add(j1)
    assert service.resolve_or_defer_reference(resolver.ce_base_voltage(j1), "bv1") is False
    assert list(service.unresolved_references())[0] == UnresolvedReference(j1.mrid, "bv1", resolver.ce_base_voltage(j1).resolver)
    assert "bv1" in service.get_unresolved_reference_mrids_by_resolver(resolver.ce_base_voltage(j1))

    bv1 = BaseVoltage("bv1")
    assert service.add(bv1)
    assert not service.has_unresolved_references()
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.ce_base_voltage(j1)))

    assert j1.base_voltage is bv1


def test_mrid_must_be_unique(service):
    j1 = Junction("id1")
    assert service.add(j1)

    loc = Location(j1.mrid)
    assert not service.add(loc)


def test_unresolved_references(service: BaseService):
    f = Feeder("f")
    acls1 = AcLineSegment("acls1")
    acls2 = AcLineSegment("acls2")
    plsi1 = PerLengthSequenceImpedance("plsi1")
    service.resolve_or_defer_reference(resolver.per_length_sequence_impedance(acls1), "plsi1")
    t1 = Terminal("t1")
    t2 = Terminal("t2")
    service.resolve_or_defer_reference(resolver.ce_terminals(acls1), "t1")
    service.resolve_or_defer_reference(resolver.ce_terminals(acls1), "t2")
    ci1 = CableInfo("ci1")
    service.resolve_or_defer_reference(resolver.asset_info(acls1), "ci1")
    service.resolve_or_defer_reference(resolver.containers(acls1), "f")
    service.resolve_or_defer_reference(resolver.containers(acls2), "f")

    assert service.add(acls1)
    assert service.add(acls2)
    assert service.num_unresolved_references() == 6
    refs_for_acls1 = list(service.get_unresolved_reference_mrids_from("acls1"))
    for expected in (plsi1.mrid, t1.mrid, t2.mrid, ci1.mrid):
        assert expected in refs_for_acls1

    refs = list(service.get_unresolved_reference_mrids_by_resolver(resolver.per_length_sequence_impedance(acls1)))
    assert plsi1.mrid in refs

    check_unresolved_reference(t1.mrid, acls1.mrid, service.get_unresolved_reference_mrids_to)
    check_unresolved_reference(t2.mrid, acls1.mrid, service.get_unresolved_reference_mrids_to)
    check_unresolved_reference(plsi1.mrid, acls1.mrid, service.get_unresolved_reference_mrids_to)
    check_unresolved_reference(ci1.mrid, acls1.mrid, service.get_unresolved_reference_mrids_to)

    add_and_check(service, f, [acls1, acls2], "equipment_containers")
    assert service.num_unresolved_references() == 4
    add_and_check(service, plsi1, acls1, "per_length_sequence_impedance")
    assert service.num_unresolved_references() == 3
    add_and_check(service, ci1, acls1, "wire_info")
    assert service.num_unresolved_references() == 2
    add_and_check(service, t1, acls1, "terminals")
    assert service.num_unresolved_references() == 1
    add_and_check(service, t2, acls1, "terminals")
    assert service.num_unresolved_references() == 0


def add_and_check(service: BaseService, to_add, to_check: Union[IdentifiedObject, List[IdentifiedObject]], to_check_reference):
    service.add(to_add)
    if isinstance(to_check, IdentifiedObject):
        to_check = [to_check]
    for io in to_check:
        refs = list(service.get_unresolved_reference_mrids_from(io.mrid))
        assert to_add.mrid not in refs
        assert to_add.mrid not in service.get_unresolved_reference_mrids_to(to_add.mrid)
        attr = getattr(io, to_check_reference)
        if isinstance(attr, IdentifiedObject):
            assert attr is to_add
        else:  # Assume an iterable/generator property (e.g terminals)
            assert to_add in attr


def check_unresolved_reference(to_check, expected_from, getter):
    refs = list(getter(to_check))
    assert expected_from in refs
