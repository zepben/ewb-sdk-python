#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import Terminal, NetworkService, Feeder, ConnectivityNode, IdentifiedObject, FeederDirection
from zepben.evolve.processors.simplification.reshape_post_processor import ReshapePostProcessor


class IssueTracker:
    logger: logging.Logger = logging.getLogger(__name__)
    description: str = None
    count: int = 0

    def __init__(self, logger=None, description: str = None):
        if logger is not None:
            self.logger = logger
        if description is not None:
            self.description = description

    def __str__(self):
        return f'{self.count} {self.description}'

    def track(self, log_message: str = None):
        self.count += 1
        if log_message is not None:
            self.logger.warning(log_message)


class FeederHeadTerminalResolverIssues:
    headTerminalMappedToMultipleObjects: IssueTracker = IssueTracker("instances where a head terminal mapped to multiple objects.")
    headTerminalMappedToNothing: IssueTracker = IssueTracker("instances where a head terminal mapped to nothing.")
    headTerminalMappedToInvalidObject = IssueTracker("instances where a head terminal mapped to an object other than a terminal or connectivity node.")
    noValidTerminalFoundForTargetNode = IssueTracker("instances where a head terminal mapped to a connectivity node that had no valid connected terminal.")


class FeederHeadTerminalResolver(ReshapePostProcessor):
    issues: FeederHeadTerminalResolverIssues = FeederHeadTerminalResolverIssues()
    feederDirectionPropertyName: str = "normal_feeder_direction"

    def __init__(self, issues: FeederHeadTerminalResolverIssues = None, feederDirectionPropertyName: str = None):
        if issues is not None:
            self.issues = issues
        if feederDirectionPropertyName is not None:
            self.feederDirectionPropertyName = feederDirectionPropertyName

    async def process(self, service: NetworkService, cumulativeReshapes: Reshape):
        original_list = list(service.objects(Feeder))

        for feeder in original_list:
            if feeder.normal_head_terminal is not None:
                headTerminal = feeder.normal_head_terminal
                if headTerminal.mrid in cumulativeReshapes.originalToNew and cumulativeReshapes.originalToNew[headTerminal.mrid] is not None:
                    equipment = list(feeder.equipment)  # not sure if this is needed
                    current_equipment = list(feeder.current_equipment)
                    feeder.clear_equipment()
                    feeder.clear_current_equipment()
                    feeder.normal_head_terminal = None

                    newIOs = cumulativeReshapes.originalToNew[headTerminal.mrid]

                    if len(newIOs) == 1:
                        io: IdentifiedObject = newIOs.pop()
                        if isinstance(io, Terminal):
                            feeder.normal_head_terminal = io
                        elif isinstance(io, ConnectivityNode):
                            found_valid_connectivity_node = False
                            for terminal in io.terminals:
                                if getattr(terminal, self.feederDirectionPropertyName) != FeederDirection.UPSTREAM:
                                    feeder.normal_head_terminal = terminal
                                    setattr(terminal,
                                            self.feederDirectionPropertyName,
                                            getattr(terminal, self.feederDirectionPropertyName) + FeederDirection.DOWNSTREAM)
                                    found_valid_connectivity_node = True
                                    break
                            if not found_valid_connectivity_node:
                                self.issues.noValidTerminalFoundForTargetNode.track(f'Feeder {feeder.mrid}\'s head terminal {headTerminal.mrid} was replaced '
                                                                                    f'by connectivity node {io.mrid}, which had no valid connected terminal. '
                                                                                    f'The head terminal will be unassigned.')
                        else:
                            self.issues.headTerminalMappedToInvalidObject.track(f'Feeder {feeder.mrid}\'s head terminal {headTerminal.mrid} was replaced by '
                                                                                f'something other than a terminal or connectivity node: {io}. '
                                                                                f'The head terminal will be unassigned.')
                    elif len(newIOs) == 0:
                        self.issues.headTerminalMappedToNothing.track(f'Feeder {feeder.mrid}\'s head terminal {headTerminal.mrid} was replaced by nothing. '
                                                                      f'The head terminal will be unassigned.')
                    else:
                        self.issues.headTerminalMappedToMultipleObjects.track(f'Feeder {feeder.mrid}\'s head terminal {headTerminal.mrid} was replaced by '
                                                                              f'multiple objects. The head terminal will be unassigned.')
                    for eq in equipment:
                        feeder.add_equipment(eq)
                    for ceq in current_equipment:
                        feeder.add_current_equipment(ceq)
