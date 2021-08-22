from itertools import combinations, chain
from typing import List, Dict

from z3 import BoolRef


def generate_configurations(features: List[BoolRef]) -> List[Dict[BoolRef, bool]]:
    n = len(features)
    configurations = []
    for i in range(2 ** n):
        binary = [bool(int(x)) for x in format(i, f'#0{n + 2}b')[2:]]
        configurations.append({f: b for (f, b) in zip(features, binary)})

    return configurations


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return set(map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s)+1))))