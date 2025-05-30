#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING


from abc import abstractmethod

from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment

__all__ = ['InServiceStateOperators', 'NormalInServiceStateOperators', 'CurrentInServiceStateOperators']


class InServiceStateOperators(StateOperator):
    """
    Interface for managing the in-service status of equipment.
    """

    @staticmethod
    @abstractmethod
    def is_in_service(equipment: Equipment):
        """
        Checks if the specified equipment is in service.

        `equipment` The equipment to check.
        Returns `true` if the equipment is in service; `false` otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def set_in_service(equipment: Equipment, in_service: bool) -> bool:
        """
        Sets the in-service status of the specified equipment.

        `equipment` The equipment for which to set the in-service status.
        `inService` The desired in-service status (`true` for in service, `false` for out of service).
        """
        pass


class NormalInServiceStateOperators(InServiceStateOperators):
    """
    Operates on the normal state of the `equipment`
    """
    @staticmethod
    def is_in_service(equipment: Equipment):
        return equipment.normally_in_service

    @staticmethod
    def set_in_service(equipment: Equipment, in_service: bool) -> None:
        equipment.normally_in_service = in_service


class CurrentInServiceStateOperators(InServiceStateOperators):
    """
    Operates on the current state of the `equipment`
    """
    @staticmethod
    def is_in_service(equipment: Equipment):
        return equipment.in_service

    @staticmethod
    def set_in_service(equipment: Equipment, in_service: bool) -> None:
        equipment.in_service = in_service

InServiceStateOperators.NORMAL = NormalInServiceStateOperators
InServiceStateOperators.CURRENT = CurrentInServiceStateOperators
