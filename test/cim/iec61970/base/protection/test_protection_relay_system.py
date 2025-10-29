#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, lists, sampled_from
from zepben.ewb import ProtectionRelaySystem, ProtectionKind, ProtectionRelayScheme

from cim.iec61970.base.core.test_equipment import equipment_kwargs, equipment_args, verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs, verify_equipment_constructor_args
from cim.private_collection_validator import validate_unordered_1234567890

protection_relay_system_kwargs = {
    **equipment_kwargs,
    "protection_kind": sampled_from(ProtectionKind),
    "schemes": lists(builds(ProtectionRelayScheme))
}

protection_relay_system_args = [*equipment_args, ProtectionKind.JDIFF, [ProtectionRelayScheme(), ProtectionRelayScheme(), ProtectionRelayScheme()]]


def test_protection_relay_system_constructor_default():
    prs = ProtectionRelaySystem()

    verify_equipment_constructor_default(prs)
    assert prs.protection_kind == ProtectionKind.UNKNOWN
    assert len(list(prs.schemes)) == 0


@given(**protection_relay_system_kwargs)
def test_protection_relay_system_constructor_kwargs(protection_kind, schemes, **kwargs):
    prs = ProtectionRelaySystem(
        protection_kind=protection_kind,
        schemes=schemes,
        **kwargs
    )

    verify_equipment_constructor_kwargs(prs, **kwargs)
    assert prs.protection_kind == protection_kind
    assert list(prs.schemes) == schemes


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_protection_relay_system_constructor_args():
    prs = ProtectionRelaySystem(*protection_relay_system_args)

    verify_equipment_constructor_args(prs)
    assert protection_relay_system_args[-2:] == [
        prs.protection_kind,
        list(prs.schemes)
    ]


def test_schemes_collection():
    validate_unordered_1234567890(
        ProtectionRelaySystem,
        lambda mrid: ProtectionRelayScheme(mrid),
        ProtectionRelaySystem.schemes,
        ProtectionRelaySystem.num_schemes,
        ProtectionRelaySystem.get_scheme,
        ProtectionRelaySystem.add_scheme,
        ProtectionRelaySystem.remove_scheme,
        ProtectionRelaySystem.clear_scheme
    )
