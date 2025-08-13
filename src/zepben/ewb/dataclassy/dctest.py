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
        print("BOOOOP")
        self.strings: Wrappa = _strings

class Child(Example):
    ints: List[int] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        _ints = Wrappa(self.ints)
        self.ints: Wrappa = _ints

if __name__ == '__main__':
    ex2 = Child(strings=['a', 'b'])
    ex2.strings.add('ccc')
    print(ex2.strings)