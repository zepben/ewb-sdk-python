#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TransformerTest"]

from zepben.ewb.dataslot import dataslot
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@dataslot
class TransformerTest(IdentifiedObject):
    """
    Test result for transformer ends, such as short-circuit, open-circuit (excitation) or no-load test.
    """

    base_power: int | None = None
    """
    Base power at which the tests are conducted, usually equal to the ratedS of one of the involved transformer ends in VA.
    """

    temperature: float | None = None
    """
    Temperature at which the test is conducted in degrees Celsius.
    """
