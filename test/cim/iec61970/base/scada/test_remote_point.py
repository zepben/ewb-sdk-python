#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import RemotePoint

remote_point_kwargs = identified_object_kwargs
remote_point_args = identified_object_args


def verify_remote_point_constructor_default(rp: RemotePoint):
    verify_identified_object_constructor_default(rp)


def verify_remote_point_constructor_kwargs(rp: RemotePoint, **kwargs):
    verify_identified_object_constructor_kwargs(rp, **kwargs)


def verify_remote_point_constructor_args(rp: RemotePoint):
    verify_identified_object_constructor_args(rp)
