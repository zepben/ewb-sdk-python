#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["XyPhaseStep"]

from dataclassy import dataclass

from zepben.evolve import Terminal, PhaseCode


@dataclass(slots=True)
class XyPhaseStep(object):

    terminal: Terminal
    """
    The incoming terminal
    """

    phase_code: PhaseCode
    """
    The phases used to get to this step (should only be, XY, X or Y)
    """
