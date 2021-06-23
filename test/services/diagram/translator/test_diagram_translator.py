#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim_creators import *
from test.services.common.translator.base_test_translator import validate_service_translations
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
