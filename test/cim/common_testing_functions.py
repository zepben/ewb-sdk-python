#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy


# noinspection PyShadowingBuiltins
def extract_testing_args(locals):
    """
    :param locals: The output of locals()
    :return: Shallow copy of locals without the kwargs
    """
    args = copy.copy(locals)
    del args['kwargs']
    return args


def verify(creators, hypothesis, args, verifier):
    for creator in creators:
        kwargs = {k: hypothesis.draw(v) for k, v in args.items()}
        verifier(creator(**kwargs), **kwargs)
