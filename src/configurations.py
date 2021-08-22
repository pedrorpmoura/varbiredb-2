import copy
import functools
from typing import List, Set, FrozenSet

from z3 import BoolRef

from src.types import Configuration


def foldl(func, acc, xs):
    return functools.reduce(func, xs, acc)


def cunion_bin(c: List[Configuration], d: List[Configuration]) -> List[Configuration]:
    result = copy.deepcopy(c)
    for x in d:
        if x not in result:
            result.append(x)

    return result


def cunion(*configurations: List[Configuration]) -> List[Configuration]:
    return foldl(cunion_bin, [], configurations)


def cintersection_bin(c: List[Configuration], d: List[Configuration]) -> List[Configuration]:
    return [x for x in c if x in d]


def cintersection(universe: List[Configuration], *configurations: List[Configuration]) -> List[Configuration]:
    return foldl(cintersection_bin, universe, configurations)


def convert_to_set(lc: List[Configuration]) -> Set[FrozenSet[BoolRef]]:
    result = set()
    for c in lc:
        result.add(frozenset([f for f in c if c[f]]))

    return result
