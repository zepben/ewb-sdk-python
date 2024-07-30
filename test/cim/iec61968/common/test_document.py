#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from hypothesis.strategies import text, datetimes

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Document

document_kwargs = {
    **identified_object_kwargs,
    "title": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "created_date_time": datetimes(),
    "author_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "status": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "comment": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
}

document_args = [*identified_object_args, "a", datetime(2021, 1, 1), "b", "c", "d", "e"]


def verify_document_constructor_default(d: Document):
    verify_identified_object_constructor_default(d)
    assert d.title == ""
    assert not d.created_date_time
    assert d.author_name == ""
    assert d.type == ""
    assert d.status == ""
    assert d.comment == ""


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
    assert d.title == document_args[-6]
    assert d.created_date_time == document_args[-5]
    assert d.author_name == document_args[-4]
    assert d.type == document_args[-3]
    assert d.status == document_args[-2]
    assert d.comment == document_args[-1]
