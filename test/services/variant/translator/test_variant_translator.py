#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.
#
# Ported from `com.zepben.ewb.services.variant.translator.VariantTranslatorTest`.
#
# NOTE: The JVM test is entirely commented out — it subclasses `TranslatorTestBase`, which needs the
# variant database tables (ported separately, in the DB phase) for its "number of validated items ==
# number of database tables" check, and its `abstractCreatorsIdentifiable` used a placeholder that could
# never produce a matching computed mRID. The previous port of `testdata/fill_fields.py` (the only
# consumer of which is this test) shows the intended shape. So this class ports the *self-contained*
# part of the JVM `ValidationInfo` round-trip — the blank and populated legs (CIM -> protobuf -> CIM,
# compared with the `VariantServiceComparator`) — driven by the `fill_fields` helpers, and drops the
# DB-table-count check (no variant tables exist in Python yet).
import pytest

from zepben.ewb import NameType, generate_id
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_component import NetworkModelProjectComponent
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.services.common.translator.base_proto2cim import get_nullable
from zepben.ewb.services.variant.translator.variant_cim2proto import variant_object_to_pb
from zepben.ewb.services.variant.translator.variant_proto2cim import add_from_pb
from zepben.ewb.services.variant.variant_service import VariantService
from zepben.ewb.services.variant.variant_service_comparator import VariantServiceComparator

from test.services.variant.testdata.fill_fields import (
    annotated_project_dependency_fill_fields,
    change_set_fill_fields,
    network_model_project_fill_fields,
    network_model_project_stage_fill_fields,
    object_creation_fill_fields,
    object_deletion_fill_fields,
    object_modification_fill_fields,
)

# Abstract reference classes -> concrete creators, mirroring the JVM `abstractCreators` map
# (the parent of a `NetworkModelProjectComponent` reference must be a concrete type).
_ABSTRACT_CREATORS = {NetworkModelProjectComponent: NetworkModelProjectStage}


def _construct(cim_type):
    """Build a blank instance: members have no-arg constructors, the rest take a single mRID."""
    if issubclass(cim_type, ChangeSetMember):
        return cim_type()
    return cim_type(generate_id())


def _fill_required(obj, service):
    """
    Python port of the JVM `SchemaServices.fillRequired`: give a blank `ChangeSetMember` a
    `change_set` and `target_object_mrid` so its computed mRID is resolvable (mirrors the JVM
    `io.changeSet = ChangeSet(generateId()); io.targetObjectMRID = "member"`).
    """
    if isinstance(obj, ChangeSetMember):
        cs = ChangeSet(generate_id())
        service.add(cs)
        obj.change_set = cs
        obj.target_object_mrid = "member"


def _create_reference(to_class, to_mrid, service):
    """
    Create a fresh reference object for an unresolved `to_mrid` (mirrors the JVM
    `addWithUnresolvedReferences`, which builds concrete objects to satisfy deferred references).
    """
    creator = _ABSTRACT_CREATORS.get(to_class)
    if creator is not None:
        return creator(to_mrid)
    if issubclass(to_class, ChangeSetMember):
        # ChangeSetMembers compute their mRID as `{change_set}_{target}` and the resolver's `to_class`
        # is the abstract `ChangeSetMember`, so build a concrete member with the right parts (mirrors
        # the JVM `abstractCreatorsIdentifiable` map).
        change_set_mrid, _, target_mrid = to_mrid.rpartition("_")
        member = ObjectCreation()
        member.change_set = service.get(change_set_mrid)
        member.target_object_mrid = target_mrid
        return member
    return to_class(to_mrid)


def _resolve_unresolved_references(service):
    """Resolve deferred references by creating fresh reference objects until none remain."""
    guard = 0
    while True:
        refs = [ref for ref in service.unresolved_references() if service.get(ref.to_mrid, default=None) is None]
        if not refs:
            return
        guard += 1
        if guard > 100:
            raise AssertionError(f"unresolved references did not converge: {[r.to_mrid for r in refs]}")
        for ref in refs:
            service.add(_create_reference(ref.resolver.to_class, ref.to_mrid, service))


def _round_trip(obj):
    """
    Convert `obj` to protobuf, add the result to a fresh `VariantService`, resolve deferred
    references, and return the (source, converted) pair for assertion.
    """
    target = VariantService()
    # ChangeSetMembers compute their mRID from change_set + target, so the change set must be present
    # to compute it (mirrors the JVM `add(ChangeSet(it.changeSet.mRID))` pre-step in the translator).
    if isinstance(obj, ChangeSetMember) and obj.change_set is not None:
        target.add(ChangeSet(obj.change_set.mrid))
    result = add_from_pb(variant_object_to_pb(obj), target)
    assert result.identifiable is not None, f"add_from_pb returned no identifiable for {type(obj).__name__}"
    converted = result.identifiable
    _resolve_unresolved_references(target)
    return obj, converted


_TYPES = [
    pytest.param(NetworkModelProject, network_model_project_fill_fields, id="network_model_project"),
    pytest.param(NetworkModelProjectStage, network_model_project_stage_fill_fields, id="network_model_project_stage"),
    pytest.param(AnnotatedProjectDependency, annotated_project_dependency_fill_fields, id="annotated_project_dependency"),
    pytest.param(ChangeSet, change_set_fill_fields, id="change_set"),
    pytest.param(ObjectCreation, object_creation_fill_fields, id="object_creation"),
    pytest.param(ObjectDeletion, object_deletion_fill_fields, id="object_deletion"),
    pytest.param(ObjectModification, object_modification_fill_fields, id="object_modification"),
]


class TestVariantTranslator(object):

    @pytest.mark.parametrize("cim_type, filler", _TYPES)
    def test_converts_all_types_correctly(self, cim_type, filler):
        comparator = VariantServiceComparator()

        # --- Blank leg (mirrors the JVM `fillRequired` + blank round-trip). ---
        blank = _construct(cim_type)
        blank_service = VariantService()
        _fill_required(blank, blank_service)
        source, converted = _round_trip(blank)
        assert type(converted) is type(source), f"blank {cim_type.__name__}: {type(converted)} != {type(source)}"
        diff = comparator.compare_objects(source, converted)
        assert not diff.differences, f"Failed to convert blank {cim_type.__name__}: {diff.differences}"

        # --- Populated leg (mirrors the JVM `filler` + populated round-trip). ---
        populated = _construct(cim_type)
        filler(populated, VariantService())
        source, converted = _round_trip(populated)
        assert type(converted) is type(source), f"populated {cim_type.__name__}: {type(converted)} != {type(source)}"
        diff = comparator.compare_objects(source, converted)
        assert not diff.differences, f"Failed to convert populated {cim_type.__name__}: {diff.differences}"

    #
    # NOTE: NameType is not sent via any grpc messages at this stage, so test it separately (these two
    # tests come from `TranslatorTestBase`, which every translator test inherits).
    #

    def test_creates_new_name_type(self):
        # noinspection PyArgumentList, PyUnresolvedReferences
        pb = NameType(name="nt1 name", description="nt1 desc").to_pb()

        # These two are just testing to make sure nullability of description translates correctly.
        pb_null_desc = NameType(name="nt1 name null desc").to_pb()

        # noinspection PyUnresolvedReferences
        cim = VariantService().add_from_pb(pb)
        # noinspection PyUnresolvedReferences
        cim_null_desc = VariantService().add_from_pb(pb_null_desc)

        assert cim.name == pb.name
        assert cim.description == get_nullable(pb, 'description')

        assert cim_null_desc.name == pb_null_desc.name
        assert cim_null_desc.description is None

    def test_updates_existing_name_type(self):
        # noinspection PyArgumentList, PyUnresolvedReferences
        pb = NameType(name="nt1 name", description="nt1 desc").to_pb()

        # noinspection PyArgumentList
        nt = NameType(name="nt1 name")
        cs = VariantService()
        cs.add_name_type(nt)
        # noinspection PyUnresolvedReferences
        cim = cs.add_from_pb(pb)

        assert cim is nt
        assert cim.description == get_nullable(pb, 'description')
