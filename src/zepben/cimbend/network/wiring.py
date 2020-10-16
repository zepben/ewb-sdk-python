

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy

from zepben.cimbend.cores import validate_core, SUPPORTED_CORES
from zepben.cimbend.exceptions import WiringException

__all__ = ["Wiring"]


class Wiring(object):
    """
    Represents the physical wiring of `zepben.cimbend.cim.iec61970.base.core.Terminal`'s to `zepben.cimbend.ConnectivityNode`'s
    """

    def __init__(self, num_cores: int):
        validate_core(num_cores)
        self.num_cores = num_cores
        self.term_to_cn = [-1 for _ in range(num_cores)]
        self.max_connectivity_node_wires = num_cores - 1

    def wire(self, terminal_wire: int, connectivity_node_wire: int):
        """
        Wire a terminal to a ConnectivityNode
        `terminal_wire` The terminal wire to connect to
        `connectivity_node_wire` The ConnectivityNode wire to connect to
        Returns
        """
        if terminal_wire < 0 or terminal_wire > self.num_cores:
            raise WiringException(f"Invalid terminal wire specified, was {terminal_wire}")
        if connectivity_node_wire < 0 or connectivity_node_wire >= SUPPORTED_CORES:
            raise WiringException(f"Invalid ConnectivityNode wire specified, was {connectivity_node_wire}")

        if connectivity_node_wire > self.max_connectivity_node_wires:
            self.max_connectivity_node_wires = connectivity_node_wire

        self.term_to_cn[terminal_wire] = connectivity_node_wire
        return self

    def terminal_to_connectivity_node(self):
        """
        Create wiring from terminal to the ConnectivityNode
        Returns A list of `self.num_cores` int's between [0, :data:`zepben.cimbend.cores.SUPPORTED_CORES`] representing
                the wiring between cores from the `zepben.cimbend.iec61970.base.core.terminal.Terminal` to the `ConnectivityNode`
        """
        for i, v in enumerate(self.term_to_cn):
            if v == -1:
                raise WiringException(f"Wiring {i} was unspecified. All wirings need to be specified.")
        return deepcopy(self.term_to_cn)

    def connectivity_node_to_terminal(self):
        """
        Create wiring from terminal to the ConnectivityNode
        Returns A list of `self.num_cores` int's between [0, :data:`zepben.cimbend.cores.SUPPORTED_CORES`] representing
                the wiring between cores from the `ConnectivityNode` to the `zepben.cimbend.iec61970.base.core.terminal.Terminal`
        """
        cn_to_term = [-1 for _ in range(self.max_connectivity_node_wires + 1)]
        for i in range(len(self.term_to_cn)):
            if self.term_to_cn[i] == -1:
                raise WiringException(f"Wiring {i} was unspecified. All wirings need to be specified.")
            if cn_to_term[self.term_to_cn[i]] != -1:
                raise WiringException(
                    f"Duplicate wiring detected. Wiring {i} was already set to {cn_to_term[self.term_to_cn[i]]}")
            cn_to_term[self.term_to_cn[i]] = i
        return cn_to_term


def _gen_implicits(num_cores):
    implicits = {}
    for i in range(num_cores):
        for j in range(i, num_cores):
            if j + 1 in implicits:
                implicits[j + 1].wire(i, i)
            else:
                implicits[j + 1] = Wiring(j + 1).wire(i, i)
    return implicits


IMPLICIT_WIRING = _gen_implicits(SUPPORTED_CORES)
