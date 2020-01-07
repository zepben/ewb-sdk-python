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
from zepben.cim.iec61970 import WindingConnection, VectorGroup
from zepben.model.network import EquipmentContainer
from zepben.model.metrics_store import MetricsStore
from zepben.model import EnergySource, EnergyConsumer, Terminal, ConnectivityNode, IdentifiedObject, ACLineSegment, \
    PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Breaker, EquipmentContainerType, \
    UNKNOWN_SUBSTATION, EnergySourcePhase, Junction
from zepben.model.phases import Phases, PhaseCode
from zepben.model.wiring import IMPLICIT_WIRING, Wiring
from typing import Union, List, Callable


WIRING_0112 = Wiring(2).wire(0, 1).wire(1, 2)
WIRING_01 = Wiring(1).wire(0, 1)


def _get_mrid(mrid=None):
    if mrid is None:
        return uuid.uuid4()
    else:
        return mrid


def _get_result_nodes(terminals):
    """
    Helper function to get a list of connectivity nodes from a list of terminals if there are more than 2,
    or the last connectivity node if there is 2, or the only connectivity node if there is only one terminal.
    """
    try:
        if len(terminals) > 2:
            return [n.connectivity_node for n in terminals[1:]]
        else:
            return terminals[1].connectivity_node
    except IndexError:
        return terminals[0].connectivity_node


def _get_terminal(mrid, phases, connectivity_node, name, wiring=None, **kwargs):
    term = Terminal(mrid=mrid, phases=phases, connectivity_node=connectivity_node, name=name, **kwargs)
    # Implicit wiring needs to take a phase and return the wiring between them, rather than the number of cores
    if wiring is None:
        term.connect(IMPLICIT_WIRING[term.num_cores])
    else:
        term.connect(wiring)
    connectivity_node.add_terminal(term)
    return term


def gen_trafo_end(**kwargs):
    mrid = _get_mrid()
    return PowerTransformerEnd(mrid=mrid, **kwargs)


def gen_tap_changer(**kwargs):
    return RatioTapChanger(**kwargs)


@dataclass
class AddResult:
    io: IdentifiedObject
    node: Union[ConnectivityNode, List[ConnectivityNode]] = None


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
        plsi = self.add_plsi()
        ar = self.add_acls(ar.node, mrid=f"{name}-acls-1", plsi=plsi, **acls_args)
        return self.add_feeder_cb(ar.node, mrid=f"{name}-cb", **cb_args)

    def add_energysource(self, mrid: str = None, with_phases: PhaseCode = PhaseCode.NONE, wiring_supplier=None, **kwargs):
        """
        :param with_phases: If a `PhaseCode` is specified, the EnergySource will be added with an `EnergySourcePhase` for
                            each phase specified.
        :param esp: List of EnergySourcePhase to specify for this EnergySource, overrides with_phases.
        :param kwargs: Args to pass to `EnergySource.__init__`
        :return: AddResult(io=created EnergySource, node=created ConnectivityNode)
        """
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(1, mrid=mrid, wiring_supplier=wiring_supplier)
        try:
            esp = kwargs["esp"]
            del kwargs["esp"]  # Remove reference to stop duplicate key when creating EnergySource
        except KeyError:
            esp = []
            if with_phases != PhaseCode.NONE:
                for spk in with_phases.single_phases:
                    esp.append(EnergySourcePhase(spk))

        es = EnergySource(mrid, terminals=terms, esp=esp, **kwargs)
        self.network.add(es)
        return AddResult(es, terms[0].connectivity_node)

    def add_energyconsumer(self, connectivity_node, mrid: str = None, num_terms=1, phases=PhaseCode.ABCN, wiring_supplier=None, **kwargs):
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, conn_nodes=connectivity_node, mrid=mrid, phases=phases, wiring_supplier=wiring_supplier)
        ec = EnergyConsumer(mrid, terminals=terms, **kwargs)
        self.network.add(ec)
        return AddResult(ec, terms[0].connectivity_node)

    def add_acls(self, connectivity_nodes, mrid: str = None, num_terms=2, phases=PhaseCode.ABCN, wiring_supplier=None, **kwargs):
        try:
            plsi = kwargs["plsi"]
            del kwargs["plsi"]  # Remove reference to stop duplicate key when creating EnergySource
        except KeyError:
            plsi = self.add_plsi()
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, conn_nodes=connectivity_nodes, mrid=mrid, phases=phases, wiring_supplier=wiring_supplier)
        acls = ACLineSegment(mrid, terminals=terms, plsi=plsi, **kwargs)
        self.network.add(acls)
        return AddResult(acls, _get_result_nodes(terms))

    def add_junction(self, connectivity_node, mrid: str = None, num_terms=2, phases=PhaseCode.ABCN, wiring_supplier=None, **kwargs):
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, conn_nodes=connectivity_node, mrid=mrid, phases=phases, wiring_supplier=wiring_supplier)
        junction = Junction(mrid, terminals=terms, **kwargs)
        self.network.add(junction)
        return AddResult(junction, _get_result_nodes(terms))

    def add_plsi(self, mrid: str = "default-plsi", wiring_supplier=None, **kwargs):
        try:
            plsi = self.network[mrid]
        except KeyError:
            mrid = _get_mrid(mrid)
            plsi = PerLengthSequenceImpedance(mrid=mrid, **kwargs)
            self.network.add(plsi)
        return plsi

    def add_dyn11_trafo(self, connectivity_node, mrid: str = None, wiring_supplier=None, **kwargs):
        mrid = _get_mrid(mrid)
        rtc1 = gen_tap_changer(high_step=4, low_step=1, step_voltage_increment=0.25, step=2)
        end1 = gen_trafo_end(rated_s=200, rated_u=22000, r=100, x=200, r0=10, x0=20, winding=WindingConnection.D,
                             tap_changer=rtc1)
        rtc2 = gen_tap_changer(high_step=4, low_step=1, step_voltage_increment=0.25, step=2)
        end2 = gen_trafo_end(rated_s=100, rated_u=11000, r=50, x=100, r0=5, x0=10, winding=WindingConnection.Yn,
                             tap_changer=rtc2)
        terms = self.gen_terminals(2, connectivity_node, mrid=mrid, wiring_supplier=wiring_supplier)
        trafo = PowerTransformer(mrid=mrid, vector_group=VectorGroup.DYN11, ends=[end1, end2], terminals=terms, **kwargs)
        self.network.add(trafo)
        return AddResult(trafo, terms[1].connectivity_node)

    def add_cb(self, connectivity_nodes, mrid: str = None, num_terms=2, phases=PhaseCode.ABCN, wiring_supplier=None, **kwargs):
        mrid = _get_mrid(mrid)
        terms = self.gen_terminals(num_terms, connectivity_nodes, mrid=mrid, phases=phases, wiring_supplier=wiring_supplier)
        br = Breaker(mrid=mrid, terminals=terms, **kwargs)
        self.network.add(br)
        return AddResult(br, _get_result_nodes(terms))

    def add_feeder_cb(self, connectivity_node, mrid: str = None, substation=None, phases=PhaseCode.ABCN, wiring_supplier=None, **kwargs):
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
        terms = self.gen_terminals(2, connectivity_node, mrid=mrid, phases=phases, wiring_supplier=wiring_supplier)
        br = Breaker(mrid=mrid, terminals=terms, **kwargs)
        if substation is not None:
            br.link_equipment_container(EquipmentContainerType.SUBSTATION, substation)

        self.network.add(br)
        return AddResult(br, terms[0].connectivity_node)

    def gen_terminals(self,
                      count,
                      conn_nodes: Union[ConnectivityNode, List[ConnectivityNode], None] = None,
                      phases=PhaseCode.ABCN,
                      mrid=None,
                      wiring_supplier: Callable[[ConnectivityNode], Union[Wiring, None]] = lambda cn: None,
                      **kwargs):
        """
        Helper function to generate terminals for a piece of equipment. Supports the following cases:
            - Single terminal equipment with no existing ConnectivityNode (e.g, the start of a network - EnergySource or Breaker)
            - Multi terminal equipment, where any Terminal can map to an existing ConnectivityNode. (e.g a loop in the
            network where an ACLineSegment can connect to an existing ConnectivityNode)
            - Multi terminal equipment, where some Terminals can map to existing ConnectivityNode's, but new
              ConnectivityNode's are required for some Terminals. (e.g, a junction with three terminals, two connecting
              to existing ConnectivityNode's, and one new ConnectivityNode to be created for a new branch)
        If you require differing phases between Terminals, you should call this function multiple times with different
        phases for each Terminal as required. This function is only built to handle all the simpler cases described here
        to simplify building test networks.
        :param wiring_supplier: A callback for providing the wiring for a Terminal to a specific `ConnectivityNode`.
                                This callback will be passed the corresponding ConnectivityNode for the Terminal being
                                generated, and expects a `Wiring` returned, or `None` if implicit wiring is desired.
        :param mrid: If provided, will be used as the base for the terminal MRID, and tN will be appended for each terminal.
        :param count: The number of terminals to generate
        :param conn_nodes: The connectivity nodes to use for the terminals. If count > len(conn_nodes) or conn_nodes == None,
                           new `ConnectivityNode`s will be created for each extra Terminal.
        :param phases: The phase to use for the terminals. All generated terminals will get the provided phase.
        :param kwargs: Passed to `Terminal` constructor
        :return: List of `Terminal`'s
        """
        if wiring_supplier is None:
            wiring_supplier = lambda cn: None
        terms = []
        mrid = _get_mrid(mrid)
        try:
            if count > len(conn_nodes):
                # We need extra terminals than connectivity nodes provided. Map one terminal to each ConnectivityNode
                # and then create new ConnectivityNodes for the rest
                for i, node in enumerate(conn_nodes):
                    wiring = wiring_supplier(node)
                    terms.append(_get_terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=node, name=f"Terminal {i}", wiring=wiring, **kwargs))

                for j in range(start=i+1, stop=count):
                    conn_node = self.network.add_connectivitynode(uuid.uuid4())
                    wiring = wiring_supplier(conn_node)
                    terms.append(_get_terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=conn_node, name=f"Terminal {j}", wiring=wiring, **kwargs))
            elif count == len(conn_nodes):
                # We have same number of connectivity nodes as we need terminals, map terminals to ConnectivityNode's in order
                for i, node in enumerate(conn_nodes):
                    wiring = wiring_supplier(node)
                    terms.append(_get_terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=node, name=f"Terminal {i}", wiring=wiring, **kwargs))
            else:
                raise Exception("Count must either be greater than or equal to the number of connectivity nodes created")
            return terms
        except TypeError:
            # only one connectivity node was provided.
            for i, _ in enumerate(range(count), start=0):
                if conn_nodes is None or i > 0:
                    # These conditions require creating new connectivity nodes.
                    conn_node = self.network.add_connectivitynode(uuid.uuid4())
                    wiring = wiring_supplier(conn_node)
                    terms.append(_get_terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=conn_node, name=f"Terminal {i}", wiring=wiring, **kwargs))
                elif i == 0 and conn_nodes is not None:
                    wiring = wiring_supplier(conn_nodes)
                    # this requires connecting the terminal to an existing ConnectivityNode
                    terms.append(_get_terminal(mrid=f"{mrid}-t{i}", phases=Phases(phases), connectivity_node=conn_nodes, name=f"Terminal {i}", wiring=wiring, **kwargs))
            return terms


@fixture()
def network1():
    """
    Simple network, starting with a branch at the feeder (closed) CB:
                    .
                   cb
       es|..|acls|...|trafo|..|acls|..|ec
    """
    nb = NetworkBuilder()
    cb_ar = nb.create_feeder_start(es_args={'with_phases': PhaseCode.ABCN}, cb_args={'substation': UNKNOWN_SUBSTATION})
    ar = nb.add_dyn11_trafo(cb_ar.node, mrid="trafo-1")
    ar = nb.add_acls(ar.node, mrid="acls-1")
    ar = nb.add_energyconsumer(ar.node, mrid="ec-1")
    return nb.network


@fixture()
def network2():
    """
    Simple network, one ES, one Breaker, 4 branches and a loop - all lines joined by junctions.
                fcb
    es|..|acls0|...|acls1|..|junc0|..|acls2|...|acls3|..|junc1
                 |                           ^--------------------acls9------------------------|.|
               acls4|..|junc2|..|acls5|..|junc3|..|acls6|..|br0|..|acls7|..|junc4|..|acls8|..|junc5|
                                          |..|             |..|
                                junc6|..|acls10           acls11|..|junc7
    """
    nb = NetworkBuilder()
    ar = nb.add_energysource(mrid='es', with_phases=PhaseCode.ABCN)
    ar = nb.add_acls(ar.node, mrid="acls0")
    ar = nb.add_feeder_cb(ar.node, mrid=f"feeder-cb", substation=UNKNOWN_SUBSTATION)
    node2 = ar.node
    # Branch 1
    ar_b1 = nb.add_acls(node2, mrid="acls1")
    ar_b1 = nb.add_junction(ar_b1.node, mrid="junc0")
    ar_b1 = nb.add_acls(ar_b1.node, mrid="acls2")
    node4 = ar_b1.node
    ar_b1 = nb.add_acls(node4, mrid="acls3")
    ar_b1 = nb.add_junction(ar_b1.node, mrid="junc1", num_terms=1)

    # Branch 2 - 2 phases/cores
    ar_b2 = nb.add_acls(node2, mrid="acls4", phases=PhaseCode.AB)
    ar_b2 = nb.add_junction(ar_b2.node, mrid="junc2", phases=PhaseCode.AB)
    ar_b2 = nb.add_acls(ar_b2.node, mrid="acls5", phases=PhaseCode.AB)
    node8 = ar_b2.node
    ar_b2 = nb.add_junction(node8, mrid="junc3", num_terms=3, phases=PhaseCode.AB)
    node9 = ar_b2.node[0]
    node16 = ar_b2.node[1]
    ar_b2 = nb.add_acls(node9, mrid="acls6", phases=PhaseCode.AB)
    node10 = ar_b2.node
    ar_b2 = nb.add_junction(node10, mrid="junc4", num_terms=3, phases=PhaseCode.AB)
    node11 = ar_b2.node[0]
    node18 = ar_b2.node[1]
    ar_b2 = nb.add_acls(node11, mrid="acls7", phases=PhaseCode.AB)
    ar_b2 = nb.add_cb(ar_b2.node, mrid="br0", open_=[True, True], phases=PhaseCode.AB)  # TODO: Phases?
    ar_b2 = nb.add_acls(ar_b2.node, mrid="acls8", phases=PhaseCode.AB)
    ar_b2 = nb.add_junction(ar_b2.node, mrid="junc5", phases=PhaseCode.AB)

    # Loops back from branch 2 to branch 1
    ar_b2 = nb.add_acls([ar_b2.node, node4], mrid="acls9", phases=PhaseCode.AB, wiring_supplier=lambda cn: WIRING_0112 if cn == node4 else None)
    # Branch 3 - 1 phase/core
    ar_b3 = nb.add_acls(node16, mrid="acls10", phases=PhaseCode.A)
    ar_b3 = nb.add_junction(ar_b3.node, mrid="junc6", num_terms=1, phases=PhaseCode.A)

    # branch 4 - 1 phase/core
    ar_b3 = nb.add_acls(node18, mrid="acls11", phases=PhaseCode.B, wiring_supplier=lambda cn: WIRING_01 if cn == node18 else None)
    ar_b3 = nb.add_junction(ar_b3.node, mrid="junc7", num_terms=1, phases=PhaseCode.B)

    return nb.network
