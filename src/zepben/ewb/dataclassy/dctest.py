from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING


class Wrappa:
    def __init__(self, data: List = None) :
        self._data = data or []

    def __str__(self):
        return f"WRAPPED {self._data}"

    def add(self, item):
        self._data.append(item)


@dataclass(slots=True)
class Example:

    a: int = 42
    b: int = 24
    strings: List[str] = field(default_factory=list)

    def __post_init__(self):
        _strings = Wrappa(self.strings)
        self.strings: Wrappa = _strings

if __name__ == '__main__':
    ex = Example(strings=['a', 'b'])
    ex.strings.add('ccc')
    print(ex.strings)