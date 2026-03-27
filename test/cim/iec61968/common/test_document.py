#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.ewb import Document

document_args = [*identified_object_args, "a", datetime(2021, 1, 1), "b", "c", "d", "e"]


def verify_document_constructor_default(d: Document):
    verify_identified_object_constructor_default(d)
    assert d.title is None
    assert not d.created_date_time
    assert d.author_name is None
    assert d.type is None
    assert d.status is None
    assert d.comment is None


# noinspection PyShadowingBuiltins
def verify_document_constructor_kwargs(d: Document, title, created_date_time, author_name, type, status, comment, **kwargs):
    verify_identified_object_constructor_kwargs(d, **kwargs)
    assert d.title == title
    assert d.created_date_time == created_date_time
    assert d.author_name == author_name
    assert d.type == type
    assert d.status == status
    assert d.comment == comment


def verify_document_constructor_args(d: Document):
    verify_identified_object_constructor_args(d)
    assert document_args[-6:] == [
        d.title,
        d.created_date_time,
        d.author_name,
        d.type,
        d.status,
        d.comment
    ]
