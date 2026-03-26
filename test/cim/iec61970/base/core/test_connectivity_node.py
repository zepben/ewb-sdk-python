#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import connectivity_node_kwargs
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.private_collection_validator import validate_unordered
from zepben.ewb import ConnectivityNode, Terminal, generate_id

connectivity_node_args = [*identified_object_args, [Terminal(mrid=generate_id())]]


def test_connectivity_node_constructor_default():
    cn = ConnectivityNode(mrid=generate_id())

    verify_identified_object_constructor_default(cn)
    assert not list(cn.terminals)


@given(**connectivity_node_kwargs())
def test_connectivity_node_constructor_kwargs(terminals, **kwargs):
    cn = ConnectivityNode(terminals=terminals, **kwargs)

    verify_identified_object_constructor_kwargs(cn, **kwargs)
    assert list(cn.terminals) == terminals


def test_connectivity_node_constructor_args():
    cn = ConnectivityNode(*connectivity_node_args)

    verify_identified_object_constructor_args(cn)
    assert connectivity_node_args[-1:] == [
        list(cn.terminals)
    ]


def test_terminals_collection():
    validate_unordered(
        ConnectivityNode,
        lambda mrid: Terminal(mrid),
        ConnectivityNode.terminals,
        ConnectivityNode.num_terminals,
        ConnectivityNode.get_terminal,
        ConnectivityNode.add_terminal,
        ConnectivityNode.remove_terminal,
        ConnectivityNode.clear_terminals
    )
