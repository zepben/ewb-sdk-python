#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar

from hypothesis import given

from cim.cim_creators import *
from services.common.translator.base_test_translator import validate_service_translations
from zepben.evolve import IdentifiedObject, DiagramService, NameType
from zepben.evolve.services.diagram.diagram_service_comparator import DiagramServiceComparator

T = TypeVar("T", bound=IdentifiedObject)

types_to_test = {

    ################################
    # IEC61970 BASE DIAGRAM LAYOUT #
    ################################

    "create_diagram": create_diagram(),
    "create_diagram_object": create_diagram_object(),

}


@given(**types_to_test)
def test_diagram_service_translations(**kwargs):
    validate_service_translations(DiagramService, DiagramServiceComparator(), **kwargs)


#
# NOTE: NameType is not sent via any grpc messages at this stage, so test it separately
#

def test_creates_new_name_type():
    # noinspection PyArgumentList, PyUnresolvedReferences
    pb = NameType("nt1 name", "nt1 desc").to_pb()

    # noinspection PyUnresolvedReferences
    cim = DiagramService().add_from_pb(pb)

    assert cim.name == pb.name
    assert cim.description == pb.description


def test_updates_existing_name_type():
    # noinspection PyArgumentList, PyUnresolvedReferences
    pb = NameType("nt1 name", "nt1 desc").to_pb()

    # noinspection PyArgumentList
    nt = NameType("nt1 name")
    ds = DiagramService()
    ds.add_name_type(nt)
    # noinspection PyUnresolvedReferences
    cim = ds.add_from_pb(pb)

    assert cim is nt
    assert cim.description == pb.description
