#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.assets.test_asset_container import verify_asset_container_constructor_default, verify_asset_container_constructor_kwargs
from zepben.ewb import Structure


def verify_structure_constructor_default(wi: Structure):
    verify_asset_container_constructor_default(wi)


def verify_structure_constructor_kwargs(wi: Structure, **kwargs):
    verify_asset_container_constructor_kwargs(wi, **kwargs)
