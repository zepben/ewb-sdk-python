#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists

from util import mrid_strategy
from zepben.ewb import ProtectionRelaySystem, ProtectionRelayFunction, ProtectionRelayScheme, generate_id

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, identified_object_args, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args
from cim.private_collection_validator import validate_unordered

protection_relay_scheme_kwargs = {
    **identified_object_kwargs,
    "system": builds(ProtectionRelaySystem, mrid=mrid_strategy),
    "functions": lists(builds(ProtectionRelayFunction, mrid=mrid_strategy))
}

protection_relay_scheme_args = [
    *identified_object_args,
    ProtectionRelaySystem(mrid=generate_id()),
    [ProtectionRelayFunction(mrid=generate_id()), ProtectionRelayFunction(mrid=generate_id())]
]


def test_protection_relay_scheme_constructor_default():
    prs = ProtectionRelayScheme(mrid=generate_id())

    verify_identified_object_constructor_default(prs)
    assert prs.system is None
    assert len(list(prs.functions)) == 0


@given(**protection_relay_scheme_kwargs)
def test_protection_relay_scheme_constructor_kwargs(system, functions, **kwargs):
    prs = ProtectionRelayScheme(
        system=system,
        functions=functions,
        **kwargs
    )

    verify_identified_object_constructor_kwargs(prs, **kwargs)
    assert prs.system == system
    assert list(prs.functions) == functions


def test_protection_relay_scheme_constructor_args():
    prs = ProtectionRelayScheme(*protection_relay_scheme_args)

    verify_identified_object_constructor_args(prs)
    assert protection_relay_scheme_args[-2:] == [
        prs.system,
        list(prs.functions)
    ]


def test_functions_collection():
    validate_unordered(
        ProtectionRelayScheme,
        lambda mrid: ProtectionRelayFunction(mrid),
        ProtectionRelayScheme.functions,
        ProtectionRelayScheme.num_functions,
        ProtectionRelayScheme.get_function,
        ProtectionRelayScheme.add_function,
        ProtectionRelayScheme.remove_function,
        ProtectionRelayScheme.clear_function
    )
