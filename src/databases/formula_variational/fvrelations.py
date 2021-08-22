from z3 import simplify, Or, And, Implies, Not

from src.databases.formula_variational.helpers import is_valid
from src.types import FVRelation


def fvconverse(r: FVRelation):
    return {t[::-1]: r[t] for t in r}


def fvunion(r: FVRelation, s: FVRelation) -> FVRelation:
    result = {}

    tmp = dict(s)
    for t in r:
        if t in tmp:
            result[t] = simplify(Or(r[t], tmp[t]))
            del tmp[t]
        else:
            result[t] = r[t]

    for t in tmp:
        result[t] = tmp[t]

    return result


def fvintersection(r: FVRelation, s: FVRelation) -> FVRelation:
    return {t: simplify(And(r[t], s[t])) for t in r if t in s}


def fvdifference(r: FVRelation, s: FVRelation) -> FVRelation:
    result = {}
    for t in r:
        if t not in s:
            result[t] = r[t]
        else:
            result[t] = simplify(And(r[t], Not(s[t])))

    return result


def fvcomposition(r: FVRelation, s: FVRelation) -> FVRelation:
    result = {}

    for x in r:
        for y in s:
            if x[-1] == y[0]:
                t = (*x[:-1], *y[1:])
                if t not in result:
                    result[t] = simplify(And(r[x], s[y]))
                else:
                    result[t] = simplify(Or(result[t], And(r[x], s[y])))

    return result
