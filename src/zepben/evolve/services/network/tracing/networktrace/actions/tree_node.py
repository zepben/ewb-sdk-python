#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, TypeVar, Generic

from zepben.evolve import IdentifiedObject

T = TypeVar('T')

__all__ = ['TreeNode']


class TreeNode(Generic[T]):
    """
    represents a node in the NetworkTrace tree
    """
    def __init__(self, identified_object: IdentifiedObject, parent=None):
        self.identified_object = identified_object
        self._parent: TreeNode = parent
        self._children: List[TreeNode] = []

    @property
    def parent(self) -> 'TreeNode[T]':
        return self._parent

    @property
    def children(self):
        return list(self._children)

    def add_child(self, child: 'TreeNode'):
        self._children.append(child)

    def __str__(self):
        return f"{{object: {self.identified_object}, parent: {self.parent or ''}, num children: {len(self.children)}}}"

