#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from grpc import Channel
from zepben.evolve.streaming.grpc.grpc import GrpcClient
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from
from zepben.evolve.streaming.mutations.switch_state_update import SwitchStateUpdate as PBSwitchStateUpdate

stub: SwitchStateServiceGrpc.SwitchStateServiceBlocking

class SwitchStateClient(object):
    GrpcClient()

    constructor(channel: Channel): self.SwitchStateServiceGrpc.newBlockingStub(channel))





