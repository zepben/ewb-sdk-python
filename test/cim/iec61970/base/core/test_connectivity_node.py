#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import ConnectivityNode, Terminal

connectivity_node_kwargs = {
    **identified_object_kwargs,
    "terminals": lists(builds(Terminal), max_size=2)
}

connectivity_node_args = [*identified_object_args, [Terminal()]]


def test_connectivity_node_constructor_default():
    cn = ConnectivityNode()

    verify_identified_object_constructor_default(cn)
    assert not list(cn.terminals)


@given(**connectivity_node_kwargs)
def test_connectivity_node_constructor_kwargs(terminals, **kwargs):
    cn = ConnectivityNode(terminals=terminals, **kwargs)

    verify_identified_object_constructor_kwargs(cn, **kwargs)
    assert list(cn.terminals) == terminals


def test_connectivity_node_constructor_args():
    cn = ConnectivityNode(*connectivity_node_args)

    verify_identified_object_constructor_args(cn)
    assert list(cn.terminals) == connectivity_node_args[-1]


def test_terminals_collection():
    validate_collection_unordered(ConnectivityNode,
                                  lambda mrid, _: Terminal(mrid),
                                  ConnectivityNode.num_terminals,
                                  ConnectivityNode.get_terminal,
                                  ConnectivityNode.terminals,
                                  ConnectivityNode.add_terminal,
                                  ConnectivityNode.remove_terminal,
                                  ConnectivityNode.clear_terminals)
