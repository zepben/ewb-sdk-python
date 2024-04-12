#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import uuid
from typing import Union, List

import pytest
from dataclassy import dataclass
from hypothesis import settings, Verbosity
from pytest import fixture

from zepben.evolve import Terminal, ConnectivityNode, IdentifiedObject, PowerTransformerEnd, RatioTapChanger
from zepben.evolve.services.network.network_service import NetworkService
# noinspection PyUnresolvedReferences
from .network_fixtures import *

settings.register_profile("ci", max_examples=1000)
settings.register_profile("dev", max_examples=10)
settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'dev'))


def _get_mrid(mrid=None):
    if mrid is None:
        return uuid.uuid4()
    else:
        return mrid


def _get_result_nodes(terminals):
    """
    Helper function to get a list of connectivity nodes from a list of terminals if there are more than 2,
    or the last connectivity node if there is 2, or the only connectivity node if there is only one terminal.
    """
    try:
        if len(terminals) > 2:
            return [n.connectivity_node for n in terminals[1:]]
        else:
            return terminals[1].connectivity_node
    except IndexError:
        return terminals[0].connectivity_node


def _get_terminal(mrid, phases, connectivity_node, name, **kwargs):
    term = Terminal(mrid=mrid, phases=phases, connectivity_node=connectivity_node, name=name, **kwargs)
    # Implicit wiring needs to take a phase and return the wiring between them, rather than the number of cores
    connectivity_node.add_terminal(term)
    return term


def gen_trafo_end(**kwargs):
    mrid = _get_mrid()
    return PowerTransformerEnd(mrid=mrid, **kwargs)


def gen_tap_changer(**kwargs):
    return RatioTapChanger(**kwargs)


@dataclass()
class AddResult:
    io: IdentifiedObject
    node: Union[ConnectivityNode, List[ConnectivityNode]] = None


@fixture()
def network_service():
    return NetworkService()


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item):
    """
    A hook wrapper that fails the test report if there were any "never awaited" warnings captured by pytest.

    Additionally, we will print the captured log on all tests failures, or if you set `caplog.unmute = True`

    See `_pytest/hookspec.py` for typing information and additional hooks.
    """

    # We want to yield to the actual hook before doing anything, so that is there are any other initialisation issues they are not hidden by our processing. For
    # example, trying to use unknown fixtures in the tests can cause `recwarn` to go missing from the function args, so that warning would be replaced with the
    # complaint about using `recwarn`, even thought it is included with the auto-use fixture below.
    res = yield
    report = res.get_result()

    # We only want to run our checks on the "call" stage, leaving "setup" and "teardown" to be handled by pytest only. This prevents us from failing the wrong
    # parts of the test when there are warnings detected, and double printing the log.
    if report.when != "call":
        return

    if 'recwarn' in item.fixturenames:
        recwarn = item.funcargs['recwarn']
    else:
        raise ValueError("recwarn not found, please enable it by including it in an auto-use fixture.")

    if 'caplog' in item.fixturenames:
        caplog = item.funcargs['caplog']
    else:
        raise ValueError("caplog not found, please enable it by including it in an auto-use fixture.")

    # We only want to print the log for failed tests, or if caplog has been deliberately unmuted.
    if report.outcome == "failed" or getattr(caplog, 'unmute', False):
        print()
        print("----------------------------------------")
        print()
        print(caplog.text)
        print("----------------------------------------")

    # Check to see if there were any async calls that were not awaited. This is done as there are cases where the IDE does not warn you of this happening, and
    # the behaviour can cause strange issues, or even tests successes with failing code.
    never_awaited = list(filter(lambda warning: "never awaited" in warning.message.args[0], recwarn.list))
    if never_awaited:
        for warn in recwarn.list:
            print(warn.message.args[0])

        # Update the report outcome rather than using `pytest.fail("Missing awaits...")` to get the correct behaviour in the test output.
        report.outcome = "failed"
        report.longrepr = "You must await all calls to make your tests run correctly."


@fixture(autouse=True)
def include_hook_fixtures(caplog, recwarn):
    """
    A fixture to enable caplog and recwarn for all tests, so they can be used in our hook wrapper above.
    """
