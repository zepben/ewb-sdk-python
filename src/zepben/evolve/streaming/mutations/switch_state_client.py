#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Callable
from zepben.protobuf.nm.set_switch_state_data_pb2 import SwitchStateUpdate as PBSwitchStateUpdate
from zepben.protobuf.nm.set_switch_state_requests_pb2 import SetCurrentSwitchStatesRequest
from zepben.evolve.streaming.grpc.grpc import GrpcClient
from zepben.protobuf.nm.set_switch_state_pb2_grpc import SwitchStateServiceStub
from zepben.evolve.streaming.mutations.switch_state_update import SwitchStateUpdate


class SwitchStateClient(GrpcClient):
    _stub: SwitchStateServiceStub = None

    def __init__(self, channel=None, stub: SwitchStateServiceStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = SwitchStateServiceStub(channel)

    def set_current_switch_state(self, PBSwitchStateUpdate):
        """
        Send a request to the server to update the current state of a switch.
        switchToUpdate -> The switch and its state to be updated.
        return - GrpcResult that indicates success or failure of the remote call.
        """

        self.set_current_switch_states(list(PBSwitchStateUpdate))

    def set_current_switch_states(self, switches_to_update: List[PBSwitchStateUpdate]):
        """
        Send a request to the server to update the current state of a group of switches as a batch.
        All switches included in the request will be treated as a batch. That is, the resulting network state will
        only be calculated once all the new switch states have been applied. This can then avoid
        where the model may be in an 'inconsistent' state if you know a set of switch operations should for some reason
        be applied all together.

        Note: This should not be used to send large amounts of switch updates for unrelated groups of switching,
        as excessively large state updates can starve consumers / readers getting access to the model.
        """
        request = SetCurrentSwitchStatesRequest(switchesToUpdate=[x.to_pb() for x in switches_to_update])
        return self.try_rpc(lambda: self._stub.setCurrentSwitchStates(request))


def switch_state_update_to_pb(cim: SwitchStateUpdate) -> PBSwitchStateUpdate:
    return PBSwitchStateUpdate(mRID=cim.mrid,
                               setOpen=cim.set_open,
                               timestamp=cim.timestamp.timestamp())
