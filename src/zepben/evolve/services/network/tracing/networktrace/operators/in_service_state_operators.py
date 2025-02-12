#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment

from abc import abstractmethod

from zepben.evolve.services.network.tracing.networktrace.operators import StateOperator


class InServiceStateOperators(StateOperator):
    """
    Interface for managing the in-service status of equipment.
    """

    @abstractmethod
    def is_in_service(self, equipment: Equipment):
        """
        Checks if the specified equipment is in service.

        `equipment` The equipment to check.
        Returns `true` if the equipment is in service; `false` otherwise.
        """
        pass

    @abstractmethod
    def set_in_service(self, equipment: Equipment, in_service: bool) -> bool:
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
    def is_in_service(self, equipment: Equipment):
        return equipment.normally_in_service

    def set_in_service(self, equipment: Equipment, in_service: bool) -> bool:
        equipment.normally_in_service = in_service


class CurrentInServiceStateOperators(InServiceStateOperators):
    """
    Operates on the current state of the `equipment`
    """
    def is_in_service(self, equipment: Equipment):
        return equipment.in_service

    def set_in_service(self, equipment: Equipment, in_service: bool) -> bool:
        equipment.in_service = in_service

InServiceStateOperators.NORMAL = NormalInServiceStateOperators()
InServiceStateOperators.CURRENT = CurrentInServiceStateOperators()