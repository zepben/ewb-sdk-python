#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists, sampled_from

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_equipment import equipment_kwargs, equipment_args, verify_equipment_constructor_default, \
    verify_equipment_constructor_kwargs, verify_equipment_constructor_args
from zepben.evolve import ProtectionRelaySystem, ProtectionKind, ProtectionRelayScheme

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
def test_protection_relay_system_constructor_kwargs(protection_kind,
                                                    schemes,
                                                    **kwargs):
    prs = ProtectionRelaySystem(
        protection_kind=protection_kind,
        schemes=schemes,
        **kwargs
    )

    verify_equipment_constructor_kwargs(prs, **kwargs)
    assert prs.protection_kind == protection_kind
    assert list(prs.schemes) == schemes


def test_protection_relay_system_constructor_args():
    prs = ProtectionRelaySystem(*protection_relay_system_args)

    verify_equipment_constructor_args(prs)
    assert prs.protection_kind == protection_relay_system_args[-2]
    assert list(prs.schemes) == protection_relay_system_args[-1]


def test_schemes_collection():
    validate_collection_unordered(ProtectionRelaySystem,
                                  lambda mrid, _: ProtectionRelayScheme(mrid),
                                  ProtectionRelaySystem.num_schemes,
                                  ProtectionRelaySystem.get_scheme,
                                  ProtectionRelaySystem.schemes,
                                  ProtectionRelaySystem.add_scheme,
                                  ProtectionRelaySystem.remove_scheme,
                                  ProtectionRelaySystem.clear_scheme
                                  )
