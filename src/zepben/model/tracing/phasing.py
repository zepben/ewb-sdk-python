from zepben.model.switch import Breaker
from zepben.model.tracing.queue import PriorityQueue
from zepben.model.tracing.tracing import SearchType
from zepben.model.tracing.branch_recursive_tracing import BranchRecursiveTraversal
from queue import PriorityQueue
from typing import Dict


class SetPhases(object):
    def __init__(self):
        self.normal_traversal = BranchRecursiveTraversal(queue_next=self.set_normal_phases_and_queue_next,
                                                         search_type=SearchType.PRIORITY,
                                                         branch_queue=PriorityQueue())
        self.current_traversal = BranchRecursiveTraversal(queue_next=self.set_current_phases_and_queue_next,
                                                          search_type=SearchType.PRIORITY,
                                                          branch_queue=PriorityQueue())

    def set_normal_phases_and_queue_next(self, equip, trav, excludes):
        res = []
        return res

    def set_current_phases_and_queue_next(self, equip, trav, excludes):
        res = []
        return res

    def run(self, network):
        self.apply_phases_from_sources(network)
        terminals = [es.terminals for es in network.energy_sources.values() if es.has_phases()]
        self.run_complete(terminals, network.breakers)

    def apply_phases_from_sources(self, network):
        pass

    def run_complete(self, terminals: list, breakers: Dict[str, Breaker]):
        feeder_cbs = [br.is_substation_breaker() for br in breakers.values()]
        self._run_normal(terminals, feeder_cbs)
        self._run_current(terminals, feeder_cbs)

    def _run_normal(self, terminals, feeder_cbs):
        self.run_set_phasing(terminals, feeder_cbs, self.normal_traversal, OpenTest.NORMALLY_OPEN, PhaseSelector.NORMAL_PHASES)

    def _run_current(self, terminals, feeder_cbs):
        self.run_set_phasing(terminals, feeder_cbs, self.current_traversal, OpenTest.CURRENTLY_OPEN, PhaseSelector.CURRENT_PHASES)

    def run_set_phasing(self, start_terminals, feeder_cbs, traversal, open_test, phase_selector):
        pass
