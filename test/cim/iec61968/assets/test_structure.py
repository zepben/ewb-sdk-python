#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.assets.test_asset_container import asset_container_kwargs, verify_asset_container_constructor_default, \
    verify_asset_container_constructor_kwargs, verify_asset_container_constructor_args, asset_container_args
from zepben.evolve import Structure

structure_kwargs = asset_container_kwargs
structure_args = asset_container_args


def verify_structure_constructor_default(wi: Structure):
    verify_asset_container_constructor_default(wi)


def verify_structure_constructor_kwargs(wi: Structure, **kwargs):
    verify_asset_container_constructor_kwargs(wi, **kwargs)


def verify_structure_constructor_args(wi: Structure):
    verify_asset_container_constructor_args(wi)
