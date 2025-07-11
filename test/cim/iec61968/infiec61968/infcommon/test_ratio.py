#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import floats

from zepben.ewb import Ratio

ratio_kwargs = {
    "denominator": floats(min_value=0.1, max_value=1000),
    "numerator": floats(min_value=0.0, max_value=1000)
}

ratio_args = [9.0, 6.0]


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


@given(**ratio_kwargs)
def test_ratio_constructor_kwargs(denominator, numerator, **kwargs):
    assert not kwargs

    ratio = Ratio(denominator=denominator, numerator=numerator)

    assert ratio.denominator == denominator
    assert ratio.numerator == numerator


def test_ratio_constructor_args():
    ratio = Ratio(*ratio_args)

    # non-alphabetic order is due to mathematical convention (numerator before denominator)
    assert ratio_args[-2:] == [
        ratio.numerator,
        ratio.denominator
    ]


def test_quotient_nonzero_denominator():
    ratio = Ratio(9.0, 6.0)

    assert ratio.quotient == 1.5


def test_quotient_zero_denominator():
    ratio = Ratio(9.0, 0)

    with raises(AttributeError, match="Cannot calculate the quotient of a Ratio with a denominator of zero."):
        # noinspection PyStatementEffect
        ratio.quotient
