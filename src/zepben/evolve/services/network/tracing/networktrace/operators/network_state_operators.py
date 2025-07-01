#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import abstractmethod
from functools import lru_cache
from typing import Type, Generator, TYPE_CHECKING

from zepben.evolve.services.network.tracing.networktrace.network_trace_step_path_provider import NetworkTraceStepPathProvider
from zepben.evolve.services.network.tracing.networktrace.operators.equipment_container_state_operators import EquipmentContainerStateOperators, \
    NormalEquipmentContainerStateOperators, CurrentEquipmentContainerStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.feeder_direction_state_operations import FeederDirectionStateOperations, \
    NormalFeederDirectionStateOperations, CurrentFeederDirectionStateOperations
from zepben.evolve.services.network.tracing.networktrace.operators.in_service_state_operators import InServiceStateOperators, NormalInServiceStateOperators, \
    CurrentInServiceStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.open_state_operators import OpenStateOperators, NormalOpenStateOperators, \
    CurrentOpenStateOperators
from zepben.evolve.services.network.tracing.networktrace.operators.phase_state_operators import PhaseStateOperators, NormalPhaseStateOperators, \
    CurrentPhaseStateOperators
from zepben.evolve.util import classproperty

if TYPE_CHECKING:
    from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

__all__ = ['NetworkStateOperators', 'NormalNetworkStateOperators', 'CurrentNetworkStateOperators']


# noinspection PyPep8Naming
class NetworkStateOperators(
    OpenStateOperators,
    FeederDirectionStateOperations,
    EquipmentContainerStateOperators,
    InServiceStateOperators,
    PhaseStateOperators
):
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

    description: str

    @classproperty
    def NORMAL(cls) -> Type['NormalNetworkStateOperators']:
        return NormalNetworkStateOperators

    @classproperty
    def CURRENT(cls) -> Type['CurrentNetworkStateOperators']:
        return CurrentNetworkStateOperators

    @classmethod
    @abstractmethod
    def next_paths(cls, path: NetworkTraceStep.Path) -> Generator[NetworkTraceStep.Path, None, None]:
        pass


class NormalNetworkStateOperators(
    NetworkStateOperators,
    NormalOpenStateOperators,
    NormalFeederDirectionStateOperations,
    NormalEquipmentContainerStateOperators,
    NormalInServiceStateOperators,
    NormalPhaseStateOperators
):
    """
    Instance that operates on the normal state of network objects.
    """

    description = 'normal'

    CURRENT = False
    NORMAL = True

    @classmethod
    @lru_cache
    def network_trace_step_path_provider(cls):
        return NetworkTraceStepPathProvider(cls)

    @classmethod
    def next_paths(cls, path: NetworkTraceStep.Path) -> Generator[NetworkTraceStep.Path, None, None]:
        yield from cls.network_trace_step_path_provider().next_paths(path)


class CurrentNetworkStateOperators(
    NetworkStateOperators,
    CurrentOpenStateOperators,
    CurrentFeederDirectionStateOperations,
    CurrentEquipmentContainerStateOperators,
    CurrentInServiceStateOperators,
    CurrentPhaseStateOperators
):
    """
    Instance that operates on the current state of network objects.
    """

    description = 'current'

    CURRENT = True
    NORMAL = False

    @classmethod
    @lru_cache
    def network_trace_step_path_provider(cls):
        return NetworkTraceStepPathProvider(cls)

    @classmethod
    def next_paths(cls, path: NetworkTraceStep.Path) -> Generator[NetworkTraceStep.Path, None, None]:
        yield from cls.network_trace_step_path_provider().next_paths(path)
