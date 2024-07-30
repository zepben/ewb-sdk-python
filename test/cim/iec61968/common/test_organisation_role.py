#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import builds

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import OrganisationRole, Organisation

organisation_role_kwargs = {
    **identified_object_kwargs,
    "organisation": builds(Organisation)
}

organisation_role_args = [*identified_object_args, Organisation()]


def verify_organisation_role_constructor_default(or_: OrganisationRole):
    verify_identified_object_constructor_default(or_)
    assert not or_.organisation


def verify_organisation_role_constructor_kwargs(or_: OrganisationRole, organisation, **kwargs):
    verify_identified_object_constructor_kwargs(or_, **kwargs)
    assert or_.organisation == organisation


def verify_organisation_role_constructor_args(or_: OrganisationRole):
    verify_identified_object_constructor_args(or_)
    assert or_.organisation == organisation_role_args[-1]
