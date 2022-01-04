#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, identified_object_kwargs, identified_object_args, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args
from zepben.evolve import Organisation
from zepben.evolve.model.cim.iec61968.common.create_common_components import create_organisation


organisation_kwargs = identified_object_kwargs
organisation_args = identified_object_args


def test_organisation_constructor_default():
    verify_identified_object_constructor_default(Organisation())
    verify_identified_object_constructor_default(create_organisation())


# noinspection PyShadowingNames
@given(data())
def test_organisation_constructor_kwargs(data):
    verify(
        [Organisation, create_organisation],
        data, organisation_kwargs, verify_identified_object_constructor_kwargs
    )


def test_asset_owner_constructor_args():
    # noinspection PyArgumentList
    verify_identified_object_constructor_args(Organisation(*organisation_args))
