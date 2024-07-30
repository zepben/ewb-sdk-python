#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import UnresolvedReference, Terminal, resolver, BoundReferenceResolver, AcLineSegment, ReferenceResolver, ConductingEquipment
from zepben.evolve.services.common.reference_resolvers import term_to_ce_resolver, term_to_cn_resolver


def test_unresolved_reference_equality():
    t1 = Terminal("t1")
    ur1 = UnresolvedReference(from_ref=t1, to_mrid="j1", resolver=resolver.conducting_equipment(t1))
    ur2 = UnresolvedReference(from_ref=t1, to_mrid="j1", resolver=resolver.conducting_equipment(t1))
    assert ur1 == ur2
    assert not ur1 != ur2

    t2 = Terminal("t2")
    ur3 = UnresolvedReference(from_ref=t2, to_mrid="j1", resolver=resolver.conducting_equipment(t1))
    assert ur1 != ur3
    assert not ur1 == ur3

    ur4 = UnresolvedReference(from_ref=t1, to_mrid="j1", resolver=resolver.conducting_equipment(t2))
    assert ur1 != ur4
    assert ur3 != ur4

    ur5 = UnresolvedReference(from_ref=t1, to_mrid="j2", resolver=resolver.conducting_equipment(t1))
    assert ur1 != ur5


def test_bound_reference_equality():
    t1 = Terminal("t1")
    br1 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=None)
    br2 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=None)
    assert br1 == br2
    assert not br1 != br2

    t2 = Terminal("t1")
    br3 = BoundReferenceResolver(from_obj=t2, resolver=resolver.conducting_equipment(t1), reverse_resolver=None)
    assert br1 != br3
    assert not br1 == br3

    br4 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t2), reverse_resolver=None)
    assert br1 != br4
    assert br3 != br4

    ce1 = AcLineSegment("acls1")
    br5 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=resolver.ce_terminals(ce1))
    br6 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=resolver.ce_terminals(ce1))
    assert br5 == br6
    assert br5 != br1

    ce2 = AcLineSegment("acls1")
    br7 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=resolver.ce_terminals(ce2))
    assert br5 != br7

    br8 = BoundReferenceResolver(from_obj=t1, resolver=resolver.conducting_equipment(t1), reverse_resolver=None)
    assert br7 != br8
    assert br8 != br7


def test_reference_resolver_equality():
    ur1 = ReferenceResolver(from_class=Terminal, to_class=Terminal, resolve=term_to_ce_resolver)
    ur2 = ReferenceResolver(from_class=Terminal, to_class=Terminal, resolve=term_to_ce_resolver)
    assert ur1 == ur2
    assert not ur1 != ur2

    ur3 = ReferenceResolver(from_class=Terminal, to_class=Terminal, resolve=term_to_cn_resolver)
    assert ur1 != ur3
    assert not ur1 == ur3

    ur4 = ReferenceResolver(from_class=Terminal, to_class=ConductingEquipment, resolve=term_to_cn_resolver)
    assert ur1 != ur4
    assert ur3 != ur4

    ur5 = ReferenceResolver(from_class=Terminal, to_class=ConductingEquipment, resolve=term_to_ce_resolver)
    assert ur1 != ur5
    assert not ur1 == ur5

    ur6 = ReferenceResolver(from_class=ConductingEquipment, to_class=Terminal, resolve=term_to_ce_resolver)
    assert ur1 != ur6
    assert not ur1 == ur6
