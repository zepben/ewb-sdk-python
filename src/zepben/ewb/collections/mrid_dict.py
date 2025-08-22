#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from typing import Optional, Dict, Iterable

from zepben.ewb import IdentifiedObject
from zepben.ewb.collections.mrid_list import MRIDList


class MRIDDict(MRIDList):
    """
    Generic list class
    """

    def __init__(self, data: Optional[Iterable[IdentifiedObject]] = None):
        super().__init__()
        self._data: Optional[Dict[str, IdentifiedObject]] = None
        if data is not None:
            self.update(data)

    def __iter__(self):
        values = [] if self._data is None else self._data.values()
        yield from values

    def __next__(self):
        ...

    def add(self, item: IdentifiedObject, safe: bool=False):
        """
        Add an item to this Zepben List
        """
        if self._data is None:
            self._data = dict()

        if not safe:
            if item.mrid in self._data:
                if self.get_by_mrid(item.mrid) is not object:
                    self.error_duplicate(item)

        self._data[item.mrid] = item

    def remove(self, item: IdentifiedObject):
        """
        Remove an item from this Zepben List by item value
        """
        if item in self:
            local = self._data[item.mrid]
            if local is item:
                del self._data[item.mrid]


    def clear(self):
        """
        Clear the contents of this Zepben List
        """
        self._data = None

    def has_mrid(self, mrid: str):
        if self._data is None:
            return False
        return mrid in self._data

    def __contains__(self, identifier: str | T):
        if self._data is None:
            return False
        if isinstance(identifier, str):
            return self.has_mrid(identifier)
        return identifier in self._data.values()


def ralign(msg, n):
    return ' ' * max(0, n-len(msg)) + msg

def run_timer_test(cls: type, inp: Iterable[IdentifiedObject]):
    start = time.time()
    cls(inp)
    return time.time() - start

def run_n_tests(cls: type, n: int, ntests: int=100):
    inp = [IdentifiedObject(str(i)) for i in range(n)]

    results = []
    for i in range(ntests):
        results += [run_timer_test(cls, inp)]

    # print(len(results), len(inp), len(cls(inp)))

    return sum(results) / n * 1e9

def time_stuff():
    volumes = [1, 3, 10, 100]
    ntests = 10000

    for n in volumes:
        print()
        print(f'\tRunning {ntests} tests with {n} objects:')
        print('Dict (ns):', ralign(str(int(run_n_tests(MRIDDict, n, ntests))), 9))
        print('List (ns):', ralign(str(int(run_n_tests(MRIDList, n, ntests))), 9))

if __name__ == '__main__':
    # z  = ZbList()
    # z : MRIDDict = MRIDDict()
    #
    # for v in z:
    #     print(v)
    #
    # z.add(IdentifiedObject('1'))
    # z.add(IdentifiedObject('2'))
    # # z.add('24')
    # for v in z: print(v)
    #
    # z.clear()
    #
    # print(z)
    # for v in z: print('>', v)
    #
    # z.print_contents()
    #
    # z.add(IdentifiedObject('3'))
    # for v in z: print(v)
    # print('4' in z)
    # print('3' in z)
    #
    # print(len(z))

    time_stuff()