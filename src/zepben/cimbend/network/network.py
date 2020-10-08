"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

from zepben.cimbend.common.base_service import BaseService
from zepben.cimbend.cim.iec61970.base.core import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.cimbend.cim.iec61970.base.wires import EnergySource
from zepben.cimbend.measurement.metrics_store import MetricsStore
from zepben.cimbend.tracing.phasing import SetPhases
from pathlib import Path

__all__ = ["connect", "NetworkService"]
logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class ProcessStatus(Enum):
    PROCESSED = 0
    INVALID = 1
    SKIPPED = 2


def connect(terminal: Terminal, connectivity_node: ConnectivityNode):
    """
    Connect a ``Terminal`` to a ``ConnectivityNode``
    :param terminal: The ``Terminal`` to connect.
    :param connectivity_node: The ``ConnectivityNode`` to connect ``terminal`` to.
    """
    terminal.connect(connectivity_node)
    connectivity_node.add_terminal(terminal)


def _attempt_to_reuse_connection(terminal1: Terminal, terminal2: Terminal) -> ProcessStatus:
    """
    Attempt to connect two ``Terminal``s.
    :return: ``ProcessStatus`` reflecting whether the connection was reused. PROCESSED if a connection was
    established, INVALID if it couldn't be, and SKIPPED if neither terminal had an existing ``ConnectivityNode``.
    """
    cn1 = terminal1.connectivity_node
    cn2 = terminal2.connectivity_node

    if cn1 is not None:
        if cn2 is not None:
            if cn1 is cn2:
                return ProcessStatus.PROCESSED
            elif connect(terminal2, cn1.mrid):
                return ProcessStatus.PROCESSED
            return ProcessStatus.INVALID
    elif cn2 is not None:
        return ProcessStatus.PROCESSED if connect(terminal1, cn2.mrid) else ProcessStatus.INVALID
    return ProcessStatus.SKIPPED


@dataclass
class NetworkService(BaseService):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    **All** `IdentifiedObject's` submitted to this Network **MUST** have unique mRID's!

    Attributes -
        metrics_store : Storage for meter measurement data associated with this network.
    """

    name: str = "network"
    _connectivity_nodes: Dict[str, ConnectivityNode] = field(init=False, default_factory=dict)
    metrics_store: MetricsStore = None
    _auto_cn_index: int = field(init=False, default=0)

    def replace(self, mrid: str, replacement: ConductingEquipment) -> ConductingEquipment:
        """
        Replace a ConductingEquipment by ``mrid`` in this network
        :param mrid: The ``mrid`` of the ``ConductingEquipment`` to be replaced.
        :param replacement: The replacement ``ConductingEquipment``. Must at least have the same number of ``Terminal``s
                            and the same ``PhaseCode`` on each ``Terminal``.
        :return: The original ``ConductingEquipment`` that was replaced.
        :raises: ValueError if the replacement was incompatible with the existing ``ConductingEquipment``.
        :raises: KeyError if ``mrid`` was not stored as a ``ConductingEquipment`` in this ``Network``.
        """
        original = self.get(mrid, ConductingEquipment)
        connected_terms = []
        for term in original.terminals:
            if term.is_connected:
                connected_terms.append(term)

        if len(connected_terms) > replacement.num_terminals:
            raise ValueError(
                f"Replacement terminal needed {len(connected_terms)} but only had {replacement.num_terminals}")

        for i, term in enumerate(connected_terms):
            replacement_term = replacement[i]
            cn = term.connectivity_node
            if term.phases is not replacement_term.phases:
                raise ValueError(
                    f"Replacement terminal needed phase {term.phases.short_name} but had {replacement_term.phases.short_name}")

            connect(replacement_term, cn)
            self.disconnect(term)

        self.remove(original)
        self.add(replacement)
        return original

    def connect_by_mrid(self, terminal: Terminal, connectivity_node_mrid: str) -> bool:
        """
        Connect a ``Terminal`` to the ``ConnectivityNode`` with mRID ``connectivity_node_mrid``
        :param terminal: The ``Terminal`` to connect.
        :param connectivity_node_mrid: The mRID of the ``ConnectivityNode``. Will be created in the ``Network`` if it
        doesn't already exist.
        :return: True if the connection was made or already existed, False if ``terminal`` was already connected to a
        different ``ConnectivityNode``
        """
        if not connectivity_node_mrid:
            return False

        if terminal.connectivity_node:
            return connectivity_node_mrid == terminal.connectivity_node.mrid

        cn = self.add_connectivitynode(connectivity_node_mrid)
        connect(terminal, cn)
        return True

    def connect_terminals(self, terminal1: Terminal, terminal2: Terminal) -> bool:
        """
        Connect two ``Terminal``s
        :return: True if the ``Terminal``s could be connected, False otherwise.
        """
        status = _attempt_to_reuse_connection(terminal1, terminal2)
        if status == ProcessStatus.PROCESSED:
            return True
        elif status == ProcessStatus.INVALID:
            return False

        cn = self.add_connectivitynode(self._generate_cn_mrid())
        connect(terminal2, cn)
        connect(terminal1, cn)

        return True

    def _generate_cn_mrid(self):
        mrid = f"generated_cn_{self._auto_cn_index}"
        while mrid in self._connectivity_nodes:
            self._auto_cn_index += 1
            mrid = f"generated_cn_{self._auto_cn_index}"
        return mrid

    def disconnect(self, terminal: Terminal):
        """
        Disconnect a ``Terminal`` from its ``ConnectivityNode``. Will also remove the ``ConnectivityNode`` from this
        ``Network`` if it no longer has any terminals.
        :param terminal: The ``Terminal`` to disconnect.
        """
        cn = terminal.connectivity_node
        if cn is None:
            return
        cn.remove_terminal(terminal)
        terminal.disconnect()
        if cn.num_terminals == 0:
            del self._connectivity_nodes[cn.mrid]

    def disconnect_by_mrid(self, connectivity_node_mrid: str):
        """
        Disconnect a ``ConnectivityNode`` from this ``Network``. Will disconnect all ``Terminal``s from the
        ``ConnectivityNode``
        :param connectivity_node_mrid: The mRID of the ``ConnectivityNode`` to disconnect.
        :raises: KeyError if there is no ``ConnectivityNode`` for ``connectivity_node_mrid``
        """
        cn = self._connectivity_nodes[connectivity_node_mrid]
        if cn is not None:
            for term in cn.terminals:
                term.disconnect()
            cn.clear_terminals()
            del self._connectivity_nodes[connectivity_node_mrid]

    def get_primary_sources(self):
        """
        Get the primary source for this network. All directions are applied relative to this EnergySource
        :return: The primary EnergySource
        """
        return [source for source in self._objectsByType[EnergySource].values() if source.has_phases()]

    def add_connectivitynode(self, mrid: str):
        """
        Add a connectivity node to the network.
        :param mrid: mRID of the ConnectivityNode
        :return: A new ConnectivityNode with `mrid` if it doesn't already exist, otherwise the existing
                 ConnectivityNode represented by `mrid`
        """
        if mrid not in self._connectivity_nodes:
            self._connectivity_nodes[mrid] = ConnectivityNode(mrid)
            return self._connectivity_nodes[mrid]
        else:
            return self._connectivity_nodes[mrid]

    async def set_phases(self):
        set_phases = SetPhases()
        await set_phases.run(self)

    def _dumpTracing(self):
        with open(TRACED_NETWORK_FILE, "w") as f:
            for e in self.depth_first_trace_and_apply():
                assert len(e.terminals) < 3
                upstream_count = 0
                f.write(str(e) + "\n")
                for term in e.terminals:
                    if term.direction:
                        upstream_count += 1
                    f.write("\t" + str(term) + "\n")
                try:
                    if isinstance(e, EnergySource):
                        assert upstream_count == 0, "energy source had more than 0 upstreams"
                    else:
                        assert upstream_count == 1, "Need at least 1 upstream terminal"
                except AssertionError as a:
                    logger.error(a)
                    logger.error(str(e))
                    for term in e._terminals:
                        logger.error(str(term))
                f.write("\n\n")
