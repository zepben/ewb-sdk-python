#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType

class TestName(object):

    def test_constructor_coverage(self):
        type = NameType("type")
        id_obj = IdentifiedObject()
        name = Name("name", type, id_obj)

        assert name.name == "name"
        assert name.type == type
        assert name.identified_object == id_obj

