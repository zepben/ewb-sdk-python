from zepben.model.tracing.tracing import BaseTraversal, Traversal, SearchType
from zepben.model.tracing.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.model.tracing.tracker import Tracker
from zepben.model.tracing.exceptions import *
from zepben.model.tracing.connectivity import ConnectivityResult


def queue_next_equipment(item, exclude=None):
    return item.get_connections(exclude=exclude)

