from z3 import is_true

from src.databases.formula_variational.helpers import feval
from src.types import FVRelation, Configuration


# Atomic formulas
def fvtrivial_qsome(r: FVRelation, configuration: Configuration) -> bool:
    for t in r:
        if feval(configuration, r[t]):
            return True

    return False


def fvtrivial_qno(r: FVRelation, configuration: Configuration) -> bool:
    for t in r:
        if feval(configuration, r[t]):
            return False

    return True


def fvtrivial_qin(r: FVRelation, s: FVRelation, configuration: Configuration) -> bool:
    projected_r = set(t for t in r if is_true(feval(configuration, r[t])))
    projected_s = set(t for t in s if is_true(feval(configuration, s[t])))

    return projected_r.issubset(projected_s)


# Compose formulas
def fvqnot(query, configuration: Configuration) -> bool:
    return not query(configuration=configuration)


def fvqand(*queries, configuration: Configuration) -> bool:
    return all(query(configuration=configuration) for query in queries)


def fvqor(*queries, configuration: Configuration) -> bool:
    return any(query(configuration=configuration) for query in queries)
