#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.
#
# Ported from `com.zepben.ewb.services.variant.ChangeSetServicesTest`.
import pytest

from zepben.ewb import AcLineSegment
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.services.variant.change_set_services import ChangeSetServices
from zepben.ewb.services.variant.variant_service import VariantService


class TestChangeSetServices(object):

    def test_add_creation(self):
        cs = ChangeSet("cs")
        services = ChangeSetServices(cs)
        variant_service = VariantService()
        io = AcLineSegment("test")

        services.add_creation(variant_service, cs, io)

        obj = cs.get_member("test")
        assert isinstance(obj, ObjectCreation)
        assert obj.target_object_mrid == io.mrid
        assert obj.change_set == cs
        assert services[obj] == io

    def test_add_modification(self):
        cs = ChangeSet("cs")
        services = ChangeSetServices(cs)
        variant_service = VariantService()
        io = AcLineSegment("test")
        io_original = AcLineSegment("test")

        # Required Check for addModification has been disabled as that should be picked up later
        # with conflict detection with different handling.

        services.add_modification(variant_service, cs, io, io_original)

        obj = cs.get_member("test")
        assert isinstance(obj, ObjectModification)
        assert obj.target_object_mrid == io.mrid
        assert obj.change_set == cs
        assert services[obj] == io
        assert services.get_reverse_modification(obj) == io_original

    def test_add_deletion(self):
        cs = ChangeSet("cs")
        services = ChangeSetServices(cs)
        variant_service = VariantService()
        io = AcLineSegment("test")

        services.add_deletion(variant_service, cs, io)

        obj = cs.get_member("test")
        assert isinstance(obj, ObjectDeletion)
        assert obj.target_object_mrid == io.mrid
        assert obj.change_set == cs
        assert services[obj] == io

    def test_errors_on_missing_change_set_or_members(self):
        member = ObjectCreation()
        member.target_object_mrid = "id"
        member.change_set = ChangeSet("cs1")

        # Kotlin `check` -> Python `require` (a `ValueError`, mirroring Kotlin's `IllegalArgumentException`
        # for the second case; both are raised by `require` in this SDK).
        with pytest.raises(ValueError, match="You must have a change set to access its members"):
            ChangeSetServices(change_set=None)[member]

        with pytest.raises(ValueError, match="ObjectCreation cs1_id must be present in ChangeSet cs2"):
            ChangeSetServices(ChangeSet("cs2"))[member]
