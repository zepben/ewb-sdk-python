#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from typing import List, Union

import pytest
from pytest import fixture

from zepben.evolve import Terminal, resolver, UnresolvedReference, NetworkService, IdentifiedObject, \
    BaseService, PowerTransformerInfo, CableInfo, OverheadWireInfo, Streetlight, Pole, Meter, Location, Organisation, AssetOwner, \
    Customer, CustomerAgreement, Tariff, PricingStructure, OperationalRestriction, UsagePoint, Junction, BusbarSection, PowerElectronicsConnection, \
    LinearShuntCompensator, EnergySource, EnergyConsumer, PowerTransformer, AcLineSegment, Breaker, Recloser, \
    LoadBreakSwitch, Disconnector, Fuse, Jumper, RegulatingCondEq, BatteryUnit, PowerElectronicsWindUnit, PhotoVoltaicUnit, \
    FaultIndicator, Feeder, Site, Circuit, Substation, PowerElectronicsConnectionPhase, ConnectivityNodeContainer, Equipment, RatioTapChanger, \
    EnergyConsumerPhase, EnergySourcePhase, GeographicalRegion, SubGeographicalRegion, ConnectivityNode, BaseVoltage, Accumulator, Analog, Discrete, \
    Control, RemoteControl, RemoteSource, PerLengthSequenceImpedance, PowerTransformerEnd, DiagramObject, Diagram, Loop, AssetInfo, \
    AssetContainer, OrganisationRole, Document, Agreement, LvFeeder, EvChargingUnit, TapChangerControl


@fixture
def service():
    # noinspection PyArgumentList
    service = BaseService(name="base_service")
    yield service


def test_add(service: BaseService):
    b1 = Breaker(mrid="b1")
    b2 = Breaker(mrid="b2")
    b1_dup = Breaker(mrid="b1")

    assert service.add(b1)
    assert service.add(b2)
    assert service.add(b1)
    assert not service.add(b1_dup)


def test_get(service: BaseService):
    b1 = Breaker(mrid="b1")
    service.add(b1)

    assert service.get("b1") is b1
    assert service["b1"] is b1
    assert service.get("b2", default=None) is None

    with pytest.raises(TypeError, match=re.escape("Invalid type for b1. Found Breaker, expected Junction.")):
        service.get("b1", Junction)

    with pytest.raises(KeyError, match=re.escape("Failed to find Breaker[b3]")):
        service.get("b3", Breaker)

    with pytest.raises(KeyError, match=re.escape("my error: mrid=b4, typ=Junction")):
        service.get("b4", Junction, generate_error=lambda mrid, typ: f"my error: mrid={mrid}, typ={typ}")

    with pytest.raises(KeyError, match=re.escape("You must specify an mRID to get. Empty/None is invalid.")):
        service.get(mrid="")


def test_remove(service: BaseService):
    b1 = Breaker(mrid="b1")
    b2 = Breaker(mrid="b2")

    service.add(b1)
    service.add(b2)

    assert service.remove(b1)

    assert service.get("b1", default=None) is None
    assert service.get("b2", default=None) is b2


def test_unresolved_bidirectional_references(service: BaseService):
    term = Terminal(mrid="t1")
    assert service.add(term)
    assert service.resolve_or_defer_reference(resolver.conducting_equipment(term), "j1") is False

    # noinspection PyArgumentList
    assert list(service.unresolved_references())[0] == UnresolvedReference(term, "j1", resolver.conducting_equipment(term).resolver)
    assert "j1" in service.get_unresolved_reference_mrids_by_resolver(resolver.conducting_equipment(term))
    assert "j1" in service.get_unresolved_reference_mrids_by_resolver([resolver.conducting_equipment(term)])

    j1 = Junction(mrid="j1")
    assert service.resolve_or_defer_reference(resolver.ce_terminals(j1), term.mrid)
    assert not list(service.unresolved_references())  # no unresolved refs now
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.conducting_equipment(term)))
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.ce_terminals(j1)))
    assert not service.has_unresolved_references()

    assert term.conducting_equipment is j1
    assert j1.get_terminal_by_mrid(term.mrid) is term
    assert service.add(j1)


def test_unresolved_unidirectional_references(service: BaseService):
    j1 = Junction(mrid="j1")
    assert service.add(j1)
    assert service.resolve_or_defer_reference(resolver.ce_base_voltage(j1), "bv1") is False
    # noinspection PyArgumentList
    assert list(service.unresolved_references())[0] == UnresolvedReference(j1, "bv1", resolver.ce_base_voltage(j1).resolver)
    assert "bv1" in service.get_unresolved_reference_mrids_by_resolver(resolver.ce_base_voltage(j1))

    # noinspection PyArgumentList
    bv1 = BaseVoltage(mrid="bv1")
    assert service.add(bv1)
    assert not service.has_unresolved_references()
    assert not list(service.get_unresolved_reference_mrids_by_resolver(resolver.ce_base_voltage(j1)))

    assert j1.base_voltage is bv1


def test_mrid_must_be_unique(service):
    j1 = Junction(mrid="id1")
    assert service.add(j1)

    loc = Location(mrid=j1.mrid)
    assert not service.add(loc)


def test_unresolved_references(service: BaseService):
    f = Feeder(mrid="f")
    acls1 = AcLineSegment(mrid="acls1")
    acls2 = AcLineSegment(mrid="acls2")
    # noinspection PyArgumentList
    plsi1 = PerLengthSequenceImpedance(mrid="plsi1")
    service.resolve_or_defer_reference(resolver.per_length_sequence_impedance(acls1), "plsi1")
    t1 = Terminal(mrid="t1")
    t2 = Terminal(mrid="t2")
    service.resolve_or_defer_reference(resolver.ce_terminals(acls1), "t1")
    service.resolve_or_defer_reference(resolver.ce_terminals(acls1), "t2")
    # noinspection PyArgumentList
    ci1 = CableInfo(mrid="ci1")
    service.resolve_or_defer_reference(resolver.wire_info(acls1), "ci1")
    service.resolve_or_defer_reference(resolver.containers(acls1), "f")
    service.resolve_or_defer_reference(resolver.containers(acls2), "f")

    assert service.add(acls1)
    assert service.add(acls2)
    assert service.num_unresolved_references() == 6
    refs_for_acls1 = [x.to_mrid for x in service.get_unresolved_references_from("acls1")]
    for expected in (plsi1.mrid, t1.mrid, t2.mrid, ci1.mrid):
        assert expected in refs_for_acls1

    refs = list(service.get_unresolved_reference_mrids_by_resolver(resolver.per_length_sequence_impedance(acls1)))
    assert plsi1.mrid in refs

    _check_unresolved_reference(t1.mrid, acls1.mrid, service.get_unresolved_references_to)
    _check_unresolved_reference(t2.mrid, acls1.mrid, service.get_unresolved_references_to)
    _check_unresolved_reference(plsi1.mrid, acls1.mrid, service.get_unresolved_references_to)
    _check_unresolved_reference(ci1.mrid, acls1.mrid, service.get_unresolved_references_to)

    _add_and_check(service, f, [acls1, acls2], "containers")
    assert service.num_unresolved_references() == 4
    _add_and_check(service, plsi1, acls1, "per_length_sequence_impedance")
    assert service.num_unresolved_references() == 3
    _add_and_check(service, ci1, acls1, "wire_info")
    assert service.num_unresolved_references() == 2
    _add_and_check(service, t1, acls1, "terminals")
    assert service.num_unresolved_references() == 1
    _add_and_check(service, t2, acls1, "terminals")
    assert service.num_unresolved_references() == 0


def test_add_resolves_reverse_relationship():
    or1 = OperationalRestriction(mrid="or1")
    eq1 = AcLineSegment(mrid="eq1", operational_restrictions=[or1])
    or1.add_equipment(eq1)

    # noinspection PyArgumentList
    ns = NetworkService(name="test")
    # noinspection PyUnresolvedReferences
    ns.add_from_pb(eq1.to_pb())
    # noinspection PyUnresolvedReferences
    ns.add_from_pb(or1.to_pb())

    assert ns.get("eq1") in ns.get("or1").equipment
    assert ns.get("or1") in ns.get("eq1").operational_restrictions


def test_resolve_thingo(service):
    acls1 = AcLineSegment(mrid="acls1")
    t1 = Terminal(mrid="t1")
    service.resolve_or_defer_reference(resolver.ce_terminals(acls1), "t1")
    service.resolve_or_defer_reference(resolver.conducting_equipment(t1), "acls1")

    service.add(acls1)
    service.add(t1)

    assert t1.conducting_equipment is acls1
    assert list(acls1.terminals) == [t1]


def test_objects():
    for part in _types:
        # noinspection PyArgumentList
        _create_objects_test(BaseService(name=""), part)


def test_objects_exclude(service: BaseService):
    b1 = Breaker()
    acls1 = AcLineSegment()
    j1 = Junction()

    service.add(b1)
    service.add(acls1)
    service.add(j1)

    assert set(service.objects(exc_types=[AcLineSegment])) == {b1, j1}


def test_contains(service: BaseService):
    breaker = Breaker()
    service.add(breaker)

    assert breaker.mrid in service
    assert "unknown" not in service


def test_unresolved_references_by_id(service: BaseService):
    breaker = Breaker()
    service.add(breaker)
    service.resolve_or_defer_reference(resolver.ce_terminals(breaker), "terminal")

    assert len(set(service.get_unresolved_references_from(breaker.mrid))) == 1
    assert service.num_unresolved_references(breaker.mrid) == 0
    assert service.num_unresolved_references("terminal") == 1
    assert service.num_unresolved_references("unknown") == 0


def _add_and_check(service: BaseService, to_add, to_check: Union[IdentifiedObject, List[IdentifiedObject]], to_check_reference):
    service.add(to_add)
    if isinstance(to_check, IdentifiedObject):
        to_check = [to_check]
    for io in to_check:
        refs = [x.from_ref.mrid for x in service.get_unresolved_references_from(io.mrid)]
        assert to_add.mrid not in refs
        assert to_add.mrid not in service.get_unresolved_references_to(to_add.mrid)
        attr = getattr(io, to_check_reference)
        if isinstance(attr, IdentifiedObject):
            assert attr is to_add
        else:  # Assume an iterable/generator property (e.g terminals)
            assert to_add in attr


def _create_objects_test(service, type_):
    obj = type_()
    io = IdentifiedObject()
    service.add(obj)
    service.add(io)
    for obj in service.objects(type_):
        assert obj is obj
        assert obj is not io


def _check_unresolved_reference(to_check, expected_from, getter):
    refs = [x.from_ref.mrid for x in getter(to_check)]
    assert expected_from in refs


_types = [PowerTransformerInfo, CableInfo, OverheadWireInfo, Streetlight,
          Pole, Meter, Location, Organisation, AssetOwner, Customer, CustomerAgreement, Tariff, PricingStructure,
          OperationalRestriction, UsagePoint, Terminal, Junction, BusbarSection, EnergySource, PowerElectronicsConnection,
          LinearShuntCompensator, EnergyConsumer, EnergySource, EnergyConsumer, PowerTransformer, AcLineSegment, Breaker, Recloser,
          LoadBreakSwitch, Disconnector, Fuse, Jumper, RegulatingCondEq, BatteryUnit, PowerElectronicsWindUnit, PhotoVoltaicUnit,
          FaultIndicator, Feeder, Site, Substation, Circuit, Substation, PowerElectronicsConnectionPhase, EnergySourcePhase,
          RatioTapChanger, EnergyConsumerPhase, ConnectivityNodeContainer, Equipment, RatioTapChanger, EnergyConsumerPhase,
          EnergySourcePhase, GeographicalRegion, SubGeographicalRegion, ConnectivityNode, BaseVoltage, Accumulator, Analog, Discrete,
          Control, RemoteControl, RemoteSource, PerLengthSequenceImpedance, PowerTransformerEnd, DiagramObject, Diagram, Loop, AssetInfo,
          AssetContainer, OrganisationRole, Document, Agreement, LvFeeder, EvChargingUnit, TapChangerControl]
