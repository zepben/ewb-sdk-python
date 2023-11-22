#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, ConductingEquipment
from zepben.evolve.processors.simplification.conducting_equipment_remover import removeEquipment
from zepben.evolve.processors.simplification.reshape import Reshape
from zepben.evolve.processors.simplification.reshaper import Reshaper


class OutOfServiceRemover(Reshaper):

    def process(self, service: [NetworkService], cumulativeReshapes: [Reshape] = None) -> Reshape:
        originalToSimplified = dict()

        # using normally in service
        out_of_service = filter(lambda it: it.normally_in_service is False, service.objects(ConductingEquipment))

        for ce in out_of_service:
            removeEquipment(ce, service)
            originalToSimplified[ce.mrid] = {}

        return Reshape(originalToSimplified, dict())
