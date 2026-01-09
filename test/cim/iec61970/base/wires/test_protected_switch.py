#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, lists, builds

from util import mrid_strategy
from zepben.ewb import ProtectionRelayFunction, ProtectedSwitch, generate_id

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.wires.test_switch import switch_kwargs, verify_switch_constructor_default, verify_switch_constructor_kwargs, \
    verify_switch_constructor_args, switch_args
from cim.private_collection_validator import validate_unordered

protected_switch_kwargs = {
    **switch_kwargs,
    "breaking_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "relay_functions": lists(builds(ProtectionRelayFunction, mrid=mrid_strategy), max_size=2)
}
protected_switch_args = [*switch_args, 1, [ProtectionRelayFunction(mrid=generate_id())]]


def verify_protected_switch_constructor_default(ps: ProtectedSwitch):
    verify_switch_constructor_default(ps)

    assert ps.breaking_capacity is None
    assert list(ps.relay_functions) == []


def verify_protected_switch_constructor_kwargs(ps: ProtectedSwitch, breaking_capacity, relay_functions, **kwargs):
    verify_switch_constructor_kwargs(ps, **kwargs)

    assert ps.breaking_capacity == breaking_capacity
    assert list(ps.relay_functions) == relay_functions


def verify_protected_switch_constructor_args(ps: ProtectedSwitch):
    verify_switch_constructor_args(ps)

    assert protected_switch_args[-2:] == [
        ps.breaking_capacity,
        list(ps.relay_functions)
    ]


def test_relay_function_collection():
    validate_unordered(
        ProtectedSwitch,
        lambda mrid: ProtectionRelayFunction(mrid),
        ProtectedSwitch.relay_functions,
        ProtectedSwitch.num_relay_functions,
        ProtectedSwitch.get_relay_function,
        ProtectedSwitch.add_relay_function,
        ProtectedSwitch.remove_relay_function,
        ProtectedSwitch.clear_relay_functions
    )
