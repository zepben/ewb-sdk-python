#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import Type

from services.common.service_comparator_validator import ServiceComparatorValidator

from zepben.evolve import IdentifiedObject, Document, OrganisationRole, Organisation, Junction, ObjectDifference, ValueDifference, CollectionDifference, \
    BaseService, BaseServiceComparator
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType


class TestBaseServiceComparator:
    # noinspection PyArgumentList
    validator: ServiceComparatorValidator = ServiceComparatorValidator(lambda: BaseService("base"), lambda _: BaseServiceComparator())

    def _compare_identified_object(self, create_identified_object: Type[IdentifiedObject]):
        self.validator.validate_compare(create_identified_object(mrid="mRID"), create_identified_object(mrid="mRID"))
        self.validator.validate_property(IdentifiedObject.name, create_identified_object, lambda _: "name", lambda _: "diff name")
        self.validator.validate_property(IdentifiedObject.description, create_identified_object, lambda _: "description", lambda _: "other description")

        # noinspection PyArgumentList
        self.validator.validate_name_collection(
            IdentifiedObject.names,
            IdentifiedObject.add_name,
            create_identified_object,
            NameType("type1"),
            "name1",
            "name2"
        )

    def _compare_document(self, create_document: Type[Document]):
        self._compare_identified_object(create_document)

        self.validator.validate_property(Document.title, create_document, lambda _: "title", lambda _: "diff title")
        self.validator.validate_property(Document.created_date_time, create_document, lambda _: datetime(2020, 1, 1), lambda _: datetime(2021, 1, 1))
        self.validator.validate_property(Document.author_name, create_document, lambda _: "authorName", lambda _: "diff authorName")
        self.validator.validate_property(Document.type, create_document, lambda _: "type", lambda _: "diff type")
        self.validator.validate_property(Document.status, create_document, lambda _: "status", lambda _: "diff status")
        self.validator.validate_property(Document.comment, create_document, lambda _: "comment", lambda _: "diff comment")

    def _compare_organisation_role(self, create_organisation_role: Type[OrganisationRole]):
        self._compare_identified_object(create_organisation_role)

        self.validator.validate_property(
            OrganisationRole.organisation,
            create_organisation_role,
            lambda it: Organisation(mrid="org1"),
            lambda it: Organisation(mrid="org2")
        )

    def test_compare_organisation(self, ):
        self._compare_identified_object(Organisation)

    def test_validate_name_types(self, ):
        subject = _create_name_type("type", "desc", "name", "id")
        match = _create_name_type("type", "desc", "name", "id")
        diff_name = _create_name_type("diff type", "desc", "name", "id")
        diff_description = _create_name_type("type", "diff desc", "name", "id")
        diff_name_name = _create_name_type("type", "desc", "diff name", "id")
        diff_name_identified_object = _create_name_type("type", "desc", "name", "diff id")

        self.validator.validate_name_types(subject, match)
        self.validator.validate_name_types(subject, diff_name, expect_missing_from_target=subject, expect_missing_from_source=diff_name)
        self.validator.validate_name_types(
            subject,
            diff_description,
            expect_modification=ObjectDifference(subject, diff_description, {
                "description": ValueDifference(subject.description, diff_description.description)
            })
        )
        # noinspection PyArgumentList
        self.validator.validate_name_types(
            subject,
            diff_name_name,
            expect_modification=ObjectDifference(subject, diff_name_name, {
                "names": CollectionDifference(missing_from_target=list(subject.names), missing_from_source=list(diff_name_name.names))
            })
        )
        # noinspection PyArgumentList
        self.validator.validate_name_types(
            subject,
            diff_name_identified_object,
            expect_modification=ObjectDifference(subject, diff_name_identified_object, {
                "names": CollectionDifference(missing_from_target=list(subject.names), missing_from_source=list(diff_name_identified_object.names))
            })
        )

        source_type = _create_name_type("type", "desc", "name", "id")
        target_type = _create_name_type("type", "desc", "name", "id")

        self.validator.validate_name_types(source_type, target_type)


def _create_name_type(name_type: str, desc: str, name: str, io_mrid: str) -> NameType:
    # noinspection PyArgumentList
    nt = NameType(name_type, desc)
    nt.get_or_add_name(name, Junction(mrid=io_mrid))
    return nt
