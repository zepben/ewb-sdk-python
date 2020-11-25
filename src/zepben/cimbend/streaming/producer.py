#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import abstractmethod

from zepben.cimbend.streaming.grpc import GrpcClient


class CimProducerClient(GrpcClient):

    @abstractmethod
    def send(self, service: BaseService):
        raise NotImplementedError()

