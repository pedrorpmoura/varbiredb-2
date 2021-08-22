from typing import List

from src.types import Configuration


def complementary(universe: List[Configuration], configurations: List[Configuration]) -> List[Configuration]:
    return [c for c in universe if c not in configurations]