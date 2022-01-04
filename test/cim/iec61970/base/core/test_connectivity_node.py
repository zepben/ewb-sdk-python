#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds, data

from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import ConnectivityNode, Terminal
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_connectivity_node

connectivity_node_kwargs = {
    **identified_object_kwargs,
    "terminals": lists(builds(Terminal), max_size=2)
}

connectivity_node_args = [*identified_object_args, [Terminal()]]


def test_connectivity_node_constructor_default():
    cn = ConnectivityNode()
    cn2 = create_connectivity_node()
    verify_default_connectivity_node(cn)
    verify_default_connectivity_node(cn2)


def verify_default_connectivity_node(cn):
    verify_identified_object_constructor_default(cn)
    assert not list(cn.terminals)


# noinspection PyShadowingNames
@given(data())
def test_connectivity_node_constructor_kwargs(data):
    verify(
        [ConnectivityNode, create_connectivity_node],
        data, connectivity_node_kwargs, verify_connectivity_node_values
    )


def verify_connectivity_node_values(cn, terminals, **kwargs):
    verify_identified_object_constructor_kwargs(cn, **kwargs)
    assert list(cn.terminals) == terminals


def test_connectivity_node_constructor_args():
    cn = ConnectivityNode(*connectivity_node_args)

    verify_identified_object_constructor_args(cn)
    assert list(cn.terminals) == connectivity_node_args[-1]


def test_terminals_collection():
    verify_collection_unordered(ConnectivityNode,
                                lambda mrid, _: Terminal(mrid),
                                ConnectivityNode.num_terminals,
                                ConnectivityNode.get_terminal,
                                ConnectivityNode.terminals,
                                ConnectivityNode.add_terminal,
                                ConnectivityNode.remove_terminal,
                                ConnectivityNode.clear_terminals)


def test_auto_two_way_connections_for_connectivity_node_constructor():
    t = Terminal()
    cn = create_connectivity_node(terminals=[t])

    assert t.connectivity_node == cn
