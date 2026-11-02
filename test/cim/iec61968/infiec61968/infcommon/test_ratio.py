#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from pytest import raises

from cim.fill_fields import ratio_kwargs
from zepben.ewb import Ratio


# noinspection PyArgumentList
def test_ratio_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both values.
    #
    with raises(TypeError):
        Ratio()
    with raises(TypeError):
        Ratio(1.0)
    with raises(TypeError):
        Ratio(denominator=2.0)
    with raises(TypeError):
        Ratio(numerator=2.0)


@given(**ratio_kwargs())
def test_ratio_constructor_kwargs(denominator, numerator, **kwargs):
    assert not kwargs

    ratio = Ratio(denominator=denominator, numerator=numerator)

    assert ratio.denominator == denominator
    assert ratio.numerator == numerator


def test_quotient_nonzero_denominator():
    ratio = Ratio(9.0, 6.0)

    assert ratio.quotient == 1.5


def test_quotient_zero_denominator():
    ratio = Ratio(9.0, 0)

    with raises(AttributeError, match="Cannot calculate the quotient of a Ratio with a denominator of zero."):
        # noinspection PyStatementEffect
        ratio.quotient
