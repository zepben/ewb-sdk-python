#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists, integers, booleans, sampled_from, floats, data

from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.common_testing_functions import verify
from test.cim.collection_verifier import verify_collection_unordered
from test.cim.iec61970.base.wires.test_energy_connection import verify_energy_connection_constructor_default, \
    verify_energy_connection_constructor_kwargs, verify_energy_connection_constructor_args, energy_connection_kwargs, energy_connection_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import EnergyConsumer, EnergyConsumerPhase, PhaseShuntConnectionKind
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_energy_consumer

energy_consumer_kwargs = {
    **energy_connection_kwargs,
    "energy_consumer_phases": lists(builds(EnergyConsumerPhase)),
    "customer_count": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "grounded": booleans(),
    "phase_connection": sampled_from(PhaseShuntConnectionKind),
    "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "p_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

energy_consumer_args = [*energy_connection_args, [EnergyConsumerPhase()], 1, True, PhaseShuntConnectionKind.Y, 2.2, 3.3, 4.4, 5.5]


def test_energy_consumer_constructor_default():
    ec = EnergyConsumer()
    ec2 = create_energy_consumer()
    verify_default_energy_consumer_constructor(ec)
    verify_default_energy_consumer_constructor(ec2)


def verify_default_energy_consumer_constructor(ec):
    verify_energy_connection_constructor_default(ec)
    assert not list(ec.phases)
    assert ec.customer_count is None
    assert not ec.grounded
    assert ec.phase_connection == PhaseShuntConnectionKind.D
    assert ec.p is None
    assert ec.p_fixed is None
    assert ec.q is None
    assert ec.q_fixed is None


# noinspection PyShadowingNames
@given(data())
def test_energy_consumer_constructor_kwargs(data):
    verify(
        [EnergyConsumer, create_energy_consumer],
        data, energy_consumer_kwargs, verify_energy_consumer_values
    )


def verify_energy_consumer_values(ec, energy_consumer_phases, customer_count, grounded, phase_connection, p, p_fixed, q, q_fixed, **kwargs):
    verify_energy_connection_constructor_kwargs(ec, **kwargs)
    assert list(ec.phases) == energy_consumer_phases
    assert ec.customer_count == customer_count
    assert ec.grounded == grounded
    assert ec.phase_connection == phase_connection
    assert ec.p == p
    assert ec.p_fixed == p_fixed
    assert ec.q == q
    assert ec.q_fixed == q_fixed


def test_energy_consumer_constructor_args():
    ec = EnergyConsumer(*energy_consumer_args)

    verify_energy_connection_constructor_args(ec)
    assert list(ec.phases) == energy_consumer_args[-8]
    assert ec.customer_count == energy_consumer_args[-7]
    assert ec.grounded == energy_consumer_args[-6]
    assert ec.phase_connection == energy_consumer_args[-5]
    assert ec.p == energy_consumer_args[-4]
    assert ec.p_fixed == energy_consumer_args[-3]
    assert ec.q == energy_consumer_args[-2]
    assert ec.q_fixed == energy_consumer_args[-1]


def test_phases_collection():
    verify_collection_unordered(EnergyConsumer,
                                lambda mrid, _: EnergyConsumerPhase(mrid),
                                EnergyConsumer.num_phases,
                                EnergyConsumer.get_phase,
                                EnergyConsumer.phases,
                                EnergyConsumer.add_phase,
                                EnergyConsumer.remove_phase,
                                EnergyConsumer.clear_phases)


def test_auto_two_way_connections_for_energy_consumer_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    ecp = EnergyConsumerPhase()
    enc = create_energy_consumer(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t],
                                 energy_consumer_phases=[ecp])

    check_conducting_equipment_two_way_link_test(enc, up, ec, opr, f, t)
    assert ecp.energy_consumer == enc
