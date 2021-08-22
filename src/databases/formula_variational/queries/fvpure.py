from z3 import BoolRef, simplify, Or, And, Not, Implies

from src.types import FVRelation


# Atomic formulas
class FVPureQSome:
    def __init__(self, r: FVRelation) -> None:
        self.r = r

    def __call__(self) -> BoolRef:
        return simplify(Or(*self.r.values()))


class FVPureQNo:
    def __init__(self, r: FVRelation) -> None:
        self.r = r

    def __call__(self) -> BoolRef:
        return simplify(And(*map(Not, self.r.values())))


class FVPureQIn:
    def __init__(self, r: FVRelation, s: FVRelation) -> None:
        self.r = r
        self.s = s

    def __call__(self) -> BoolRef:
        return simplify(And(*[
            Implies(self.r[t], self.s[t]) if t in self.s else Not(self.r[t])
            for t in self.r
        ]))


# Compose formulas
class FVPureQNot:
    def __init__(self, predicate) -> None:
        self.predicate = predicate

    def __call__(self) -> BoolRef:
        return simplify(Not(self.predicate()))


class FVPureQAnd:
    def __init__(self, *predicates) -> None:
        self.predicates = predicates

    def __call__(self) -> BoolRef:
        return simplify(And(*[p() for p in self.predicates]))


class FVPureQOr:
    def __init__(self, *predicates) -> None:
        self.predicates = predicates

    def __call__(self) -> BoolRef:
        return simplify(Or(*[p() for p in self.predicates]))
