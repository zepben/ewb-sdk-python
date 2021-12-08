#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import lists, builds

from test.cim.extract_testing_args import extract_testing_args
from test.cim.collection_validator import validate_collection_unordered
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
    validate_default_connectivity_node(cn)
    validate_default_connectivity_node(cn2)


def validate_default_connectivity_node(cn):
    verify_identified_object_constructor_default(cn)
    assert not list(cn.terminals)


@given(**connectivity_node_kwargs)
def test_connectivity_node_constructor_kwargs(terminals, **kwargs):
    args = extract_testing_args(locals())
    cn = ConnectivityNode(**args, **kwargs)
    validate_connectivity_node_values(cn, **args, **kwargs)


@given(**connectivity_node_kwargs)
def test_connectivity_node_creator(terminals, **kwargs):
    args = extract_testing_args(locals())
    cn = create_connectivity_node(**args, **kwargs)
    validate_connectivity_node_values(cn, **args, **kwargs)


def validate_connectivity_node_values(cn, terminals, **kwargs):
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
