from typing import Dict

from src.types import Relation


# Atomic formulas
class NVQSome:
    def __init__(self, r: Relation) -> None:
        self.relation = r

    def __call__(self) -> bool:
        return len(self.relation) > 0


class NVQNo:
    def __init__(self, r: Relation) -> None:
        self.relation = r

    def __call__(self) -> bool:
        return len(self.relation) == 0

    def __repr__(self):
        return 'No(' + str(self.relation) + ')'


class NVQIn:
    def __init__(self, r: Relation, s: Relation) -> None:
        self.r = r
        self.s = s

    def __call__(self) -> bool:
        return self.r.issubset(self.s)


# Compose formulas
class NVQNot:
    def __init__(self, predicate) -> None:
        self.predicate = predicate

    def __call__(self) -> bool:
        return not self.predicate()


class NVQAnd:
    def __init__(self, *predicates) -> None:
        self.predicates = predicates

    def __call__(self) -> bool:
        return all(p() for p in self.predicates)


class NVQOr:
    def __init__(self, *predicates) -> None:
        self.predicates = predicates

    def __call__(self) -> bool:
        return any(p() for p in self.predicates)