

#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["TransformerFunctionKind"]


class TransformerFunctionKind(Enum):
    other = 0
    """ Another type of transformer. """

    voltageRegulator = 1
    """ A transformer that changes the voltage magnitude at a certain point in the power system. """

    distributionTransformer = 2
    """ A transformer that provides the final voltage transformation in the electric power distribution system. """

    isolationTransformer = 3
    """ A transformer whose primary purpose is to isolate circuits. """

    autotransformer = 4
    """ A transformer with a special winding divided into several sections enabling the voltage to be varied at will. (IEC ref 811-26-04). """

    powerTransformer = 5
    """"""

    secondaryTransformer = 6
    """"""

    @property
    def short_name(self):
        return str(self)[24:]
