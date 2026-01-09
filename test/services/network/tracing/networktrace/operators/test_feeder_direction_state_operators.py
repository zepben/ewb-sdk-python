#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import Terminal, FeederDirection, generate_id
from zepben.ewb.services.network.tracing.networktrace.operators.feeder_direction_state_operations import FeederDirectionStateOperations


class TestFeederDirectionStateOperators:

    normal = FeederDirectionStateOperations.NORMAL
    current = FeederDirectionStateOperations.CURRENT

    def test_get_direction(self):
        for operations, attr in ((self.normal, 'normal_feeder_direction'), (self.current, 'current_feeder_direction')):
            terminal = Terminal(mrid=generate_id())
            setattr(terminal, attr, FeederDirection.UPSTREAM)
            assert operations.get_direction(terminal) == FeederDirection.UPSTREAM


    def test_set_direction(self):
        for operations, attr in ((self.normal, 'normal_feeder_direction'), (self.current, 'current_feeder_direction')):
            terminal = Terminal(mrid=generate_id())
            setattr(terminal, attr, FeederDirection.NONE)
            assert operations.set_direction(terminal, FeederDirection.UPSTREAM)
            assert getattr(terminal, attr) == FeederDirection.UPSTREAM

            # Attempting to add a direction to the terminal already has should return False
            assert not operations.set_direction(terminal, FeederDirection.UPSTREAM)

            # Setting direction should replace the existing direction
            assert operations.set_direction(terminal, FeederDirection.DOWNSTREAM)
            assert getattr(terminal, attr) == FeederDirection.DOWNSTREAM

    def test_add_direction(self):
        for operations, attr in ((self.normal, 'normal_feeder_direction'), (self.current, 'current_feeder_direction')):
            terminal = Terminal(mrid=generate_id())
            setattr(terminal, attr, FeederDirection.NONE)
            assert operations.add_direction(terminal, FeederDirection.UPSTREAM)
            assert getattr(terminal, attr) == FeederDirection.UPSTREAM

            # Attempting to add a direction the terminal already has should return False
            assert not operations.add_direction(terminal, FeederDirection.UPSTREAM)

            # Adding a direction should end up with a combination of the directions
            assert operations.add_direction(terminal, FeederDirection.DOWNSTREAM)
            assert getattr(terminal, attr) == FeederDirection.BOTH

    def test_remove_direction(self):
        for operations, attr in ((self.normal, 'normal_feeder_direction'), (self.current, 'current_feeder_direction')):
            terminal = Terminal(mrid=generate_id())
            setattr(terminal, attr, FeederDirection.BOTH)
            assert operations.remove_direction(terminal, FeederDirection.UPSTREAM)
            assert getattr(terminal, attr) == FeederDirection.DOWNSTREAM

            # Attempting to remove a direction the terminal does not have should return False
            assert not operations.remove_direction(terminal, FeederDirection.UPSTREAM)
