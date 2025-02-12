#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator
from zepben.evolve.services.network.tracing.networktrace.operators.equipment_container_state_operators import EquipmentContainerStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.feeder_direction_state_operations import FeederDirectionStateOperations
from zepben.evolve.services.network.tracing.networktrace.operators.in_service_state_operators import InServiceStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.open_state_operators import OpenStateOperators, NormalOpenStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.phase_state_operators import PhaseStateOperators


class NetworkStateOperators(StateOperator):
    """
    Interface providing access to and operations on specific network state properties and functions for items within a network.
    This interface consolidates several other state operator interfaces, enabling unified management of operations for a network state.
    Refer to the individual state operator interfaces for detailed information on each available operation.

    Although this is an open interface allowing for custom implementations, this is generally unnecessary. The standard
    instances, [NetworkStateOperators.NORMAL] for the normal state and [NetworkStateOperators.CURRENT] for the current state,
    should suffice for most use cases.

    This interface is primarily utilized by the [NetworkTrace], enabling trace definitions to be reused across different network states.
    By using this interface, you can apply identical conditions and steps without needing to track which state is active
    or creating redundant trace implementations for different network states.
    """
    open_state_operators = None
    feeder_direction_state_operations = None
    equipment_container_state_operators = None
    in_service_state_operators = None
    phase_state_operators = None

class NormalNetworkStateOperators(NetworkStateOperators):
    """
    Instance that operates on the normal state of network objects.
    """
    open_state_operators = OpenStateOperators.NORMAL
    feeder_direction_state_operations = FeederDirectionStateOperations.NORMAL
    equipment_container_state_operators = EquipmentContainerStateOperators.NORMAL
    in_service_state_operators = InServiceStateOperators.NORMAL
    phase_state_operators = PhaseStateOperators.NORMAL

class CurrentNetworkStateOperators(NetworkStateOperators):
    """
    Instance that operates on the current state of network objects.
    """
    open_state_operators = OpenStateOperators.CURRENT
    feeder_direction_state_operations = FeederDirectionStateOperations.CURRENT
    equipment_container_state_operators = EquipmentContainerStateOperators.CURRENT
    in_service_state_operators = InServiceStateOperators.CURRENT
    phase_state_operators = PhaseStateOperators.CURRENT


NetworkStateOperators.NORMAL = NormalNetworkStateOperators()
NetworkStateOperators.CURRENT = CurrentNetworkStateOperators()
