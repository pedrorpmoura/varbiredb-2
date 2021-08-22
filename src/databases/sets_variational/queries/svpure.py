from typing import List, Set

from src.configurations import cunion, cintersection
from src.databases.sets_variational.helpers import complementary
from src.types import Configuration, SVRelation, SConfiguration


# Atomic formulas
class SVPureQSome:
    def __init__(self, r: SVRelation) -> None:
        self.r = r

    def __call__(self) -> Set[Configuration]:
        return set.union(*self.r.values())


class SVPureQNo:
    def __init__(self, configurations: Set[SConfiguration], r: SVRelation) -> None:
        self.r = r
        self.configurations = configurations

    def __call__(self) -> Set[SConfiguration]:
        complements = []
        for pc in self.r.values():
            complement = self.configurations.difference(pc)
            complements.append(complement)

        return set.intersection(self.configurations, *complements)


class SVPureQIn:
    def __init__(self, configurations: Set[SConfiguration], r: SVRelation, s: SVRelation) -> None:
        self.configurations = configurations
        self.r = r
        self.s = s

    def __call__(self) -> Set[SConfiguration]:
        sets = []
        for t in self.r:
            complement = self.configurations.difference(self.r[t])
            if t in self.s:
                sets.append(set.union(complement, self.s[t]))
            else:
                sets.append(complement)

        return set.intersection(*sets)


# Compose formulas
class SVPureQNot:
    def __init__(self, configurations: Set[SConfiguration], predicate) -> None:
        self.configurations = configurations
        self.predicate = predicate

    def __call__(self):
        return self.configurations.difference(self.predicate())


class SVPureQAnd:
    def __init__(self, configurations: Set[SConfiguration], *predicates):
        self.configurations = configurations
        self.predicates = predicates

    def __call__(self):
        return set.intersection(self.configurations, *[p() for p in self.predicates])


class SVPureQOr:
    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self):
        return set.union(*[p() for p in self.predicates])
