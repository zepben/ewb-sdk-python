#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pytest import raises

from zepben.evolve import GrpcResult


def test_value_works_if_valid():
    # noinspection PyArgumentList
    assert GrpcResult(12).value == 12


def test_value_throws_if_invalid():
    exception = Exception()
    with raises(TypeError, match="You can only call value on a successful result."):
        # noinspection PyArgumentList
        assert GrpcResult(exception).value == exception


def test_thrown_works_if_invalid():
    exception = Exception()
    # noinspection PyArgumentList
    assert GrpcResult(exception).thrown == exception


def test_thrown_throws_if_valid():
    with raises(TypeError, match="You can only call thrown on an unsuccessful result."):
        # noinspection PyArgumentList
        assert GrpcResult(12).thrown == 12
