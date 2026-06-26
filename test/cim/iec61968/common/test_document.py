#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs
from zepben.ewb import Document


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
