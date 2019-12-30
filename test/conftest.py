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


import uuid
from dataclasses import dataclass
from pytest import fixture
from zepben.cim.iec61970 import PhaseCode, WindingConnection, VectorGroup
from zepben.model.network import EquipmentContainer
from zepben.model.metrics_store import MetricsStore
from zepben.model import EnergySource, EnergyConsumer, Terminal, ConnectivityNode, IdentifiedObject, ACLineSegment, \
    PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Breaker, EquipmentContainerType, \
    UNKNOWN_SUBSTATION, EnergySourcePhase
from zepben.model.phases import Phases, get_single_phases
from zepben.model.wiring import IMPLICIT_WIRING


def _get_mrid(mrid=None):
    if mrid is None:
        return uuid.uuid4()
    else:
        return mrid


def gen_trafo_end(**kwargs):
    mrid = _get_mrid()
    return PowerTransformerEnd(mrid=mrid, **kwargs)


def gen_tap_changer(**kwargs):
    return RatioTapChanger(**kwargs)

@dataclass
class AddResult:
    io: IdentifiedObject
    node: ConnectivityNode = None


class NetworkBuilder(object):
    def __init__(self):
        self.metrics_store = MetricsStore()
        self.network = EquipmentContainer(self.metrics_store)

    def create_feeder_start(self, name="default", es_args=None, cb_args=None, acls_args=None):
        if cb_args is None:
            cb_args = {}
        if acls_args is None:
            acls_args = {}
        if es_args is None:
            es_args = {}
        ar = self.add_energysource(mrid=f"{name}-es", **es_args)
        plsi_ar = self.add_plsi()
        ar = self.add_acls(ar.node, mrid=f"{name}-acls-1", plsi=plsi_ar.io, **acls_args)
        return self.add_feeder_cb(ar.node, mrid=f"{name}-cb", **cb_args)

    def add_energysource(self, mrid: str = None, with_phases: PhaseCode = PhaseCode.NONE, **kwargs):
        """
        :param with_phases: If a `PhaseCode` is specified, the EnergySource will be added with an `EnergySourcePhase` for
                            each phase specified.
        :param esp: List of EnergySourcePhase to specify for this EnergySource
        :param kwargs: Args to pass to `EnergySource.__init__`
        :return: AddResult(io=created EnergySource, node=created ConnectivityNode)
        """
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(1, mrid=mrid)
        try:
            esp = kwargs["esp"]
            del kwargs["esp"]  # Remove reference to stop duplicate key when creating EnergySource
        except KeyError:
            esp = []
            if with_phases != PhaseCode.NONE:
                for spk in get_single_phases(with_phases):
                    esp.append(EnergySourcePhase(spk))

        es = EnergySource(mrid, terminals=terms, esp=esp, **kwargs)
        self.network.add(es)
        return AddResult(es, terms[0].connectivity_node)

    def add_energyconsumer(self, connectivity_node, mrid: str = None, num_terms=1, **kwargs):
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, start_conn_node=connectivity_node, mrid=mrid)
        ec = EnergyConsumer(mrid, terminals=terms, **kwargs)
        self.network.add(ec)
        return AddResult(ec, terms[0].connectivity_node)

    def add_acls(self, connectivity_node, mrid: str = None, num_terms=2, **kwargs):
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, start_conn_node=connectivity_node, mrid=mrid)
        acls = ACLineSegment(mrid, terminals=terms, **kwargs)
        self.network.add(acls)
        return AddResult(acls, terms[1].connectivity_node)

    def add_plsi(self, mrid: str = None, **kwargs):
        mrid = _get_mrid(mrid)
        plsi = PerLengthSequenceImpedance(mrid=mrid, **kwargs)
        self.network.add(plsi)
        return AddResult(plsi)

    def add_dyn11_trafo(self, connectivity_node, mrid: str = None, **kwargs):
        mrid = _get_mrid(mrid)
        rtc1 = gen_tap_changer(high_step=4, low_step=1, step_voltage_increment=0.25, step=2)
        end1 = gen_trafo_end(rated_s=200, rated_u=22000, r=100, x=200, r0=10, x0=20, winding=WindingConnection.D,
                             tap_changer=rtc1)
        rtc2 = gen_tap_changer(high_step=4, low_step=1, step_voltage_increment=0.25, step=2)
        end2 = gen_trafo_end(rated_s=100, rated_u=11000, r=50, x=100, r0=5, x0=10, winding=WindingConnection.Yn,
                             tap_changer=rtc2)
        terms = self.gen_terminals(2, connectivity_node, mrid=mrid)
        trafo = PowerTransformer(mrid=mrid, vector_group=VectorGroup.DYN11, ends=[end1, end2], terminals=terms, **kwargs)
        self.network.add(trafo)
        return AddResult(trafo, terms[1].connectivity_node)

    def add_feeder_cb(self, connectivity_node, mrid: str = None, substation=None, **kwargs):
        """
        For a feeder CB we return the passed in connectivity_node rather than the newly created one.
        This is so network builders can continue building downstream from the feeder CB, rather than receiving a node
        above the feeder.
        :param connectivity_node:
        :param mrid:
        :param substation:
        :param kwargs:
        :return:
        """
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(2, connectivity_node, mrid=mrid)
        br = Breaker(mrid=mrid, terminals=terms, **kwargs)
        if substation is not None:
            br.link_equipment_container(EquipmentContainerType.SUBSTATION, substation)

        self.network.add(br)
        return AddResult(br, terms[0].connectivity_node)

    def gen_terminals(self, count, start_conn_node=None, phases=PhaseCode.ABCN, mrid=None, **kwargs):
        """
        Will generate a connectivity_node for every terminal after the first.
        :param count: The number of terminals to generate
        :param start_conn_node: The connectivity node for the first terminal.
        :param phases: The phase to use for this terminal
        :param kwargs: Passed to `Terminal` constructor
        :return: List of `Terminal`'s
        """
        terms = []
        mrid = _get_mrid(mrid)
        for i, _ in enumerate(range(count), start=0):
            if start_conn_node is None or i > 0:
                conn_node = self.network.add_connectivitynode(uuid.uuid4())
                term = Terminal(mrid=f"{mrid}-t{i}",phases=Phases(phases), connectivity_node=conn_node, name=f"Terminal {i}", **kwargs)
                terms.append(term)
                term.connect(IMPLICIT_WIRING[term.num_cores])
                conn_node.add_terminal(term)
            elif i == 0 and start_conn_node is not None:
                term = Terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=start_conn_node, name=f"Terminal {i}", **kwargs)
                terms.append(term)
                term.connect(IMPLICIT_WIRING[term.num_cores])
                start_conn_node.add_terminal(term)

        return terms


@fixture()
def network1():
    nb = NetworkBuilder()
    cb_ar = nb.create_feeder_start(es_args={'with_phases': PhaseCode.ABCN}, cb_args={'substation': UNKNOWN_SUBSTATION})
    ar = nb.add_dyn11_trafo(cb_ar.node, mrid="trafo-1")
    plsi_ar = nb.add_plsi()
    ar = nb.add_acls(ar.node, plsi=plsi_ar.io, mrid="acls-1")
    ar = nb.add_energyconsumer(ar.node, mrid="ec-1")
    return nb.network

