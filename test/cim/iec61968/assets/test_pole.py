#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import text, lists, builds

from cim.collection_validator import validate_collection_unordered
from cim.iec61968.assets.test_structure import structure_kwargs, verify_structure_constructor_default, \
    verify_structure_constructor_kwargs, verify_structure_constructor_args, structure_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Pole, Streetlight

pole_kwargs = {
    **structure_kwargs,
    "classification": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "streetlights": lists(builds(Streetlight), max_size=2)
}

pole_args = [*structure_args, "a", [Streetlight()]]


def test_pole_constructor_default():
    p = Pole()

    verify_structure_constructor_default(p)
    assert p.classification == ""
    assert not list(p.streetlights)


@given(**pole_kwargs)
def test_pole_constructor_kwargs(classification, streetlights, **kwargs):
    p = Pole(classification=classification,
             streetlights=streetlights,
             **kwargs)

    verify_structure_constructor_kwargs(p, **kwargs)
    assert p.classification == classification
    assert list(p.streetlights) == streetlights


def test_pole_constructor_args():
    p = Pole(*pole_args)

    verify_structure_constructor_args(p)
    assert p.classification == pole_args[-2]
    assert list(p.streetlights) == pole_args[-1]


def test_streetlights_collection():
    validate_collection_unordered(Pole,
                                  lambda mrid, _: Streetlight(mrid),
                                  Pole.num_streetlights,
                                  Pole.get_streetlight,
                                  Pole.streetlights,
                                  Pole.add_streetlight,
                                  Pole.remove_streetlight,
                                  Pole.clear_streetlights)
