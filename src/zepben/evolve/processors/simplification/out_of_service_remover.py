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
    inServiceTest = lambda ce: ce.normally_in_service

    def __init__(self, inServiceTest=lambda ce: ce.normally_in_service):
        self.inServiceTest = inServiceTest

    async def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        originalToSimplified = dict()

        original_list = list(service.objects(ConductingEquipment))
        out_of_service = filter(lambda ce: not self.inServiceTest(ce), original_list)

        for ce in out_of_service:
            for removedIO in removeEquipment(ce, service):
                originalToSimplified[removedIO.mrid] = set()

        return Reshape(originalToSimplified, dict())
