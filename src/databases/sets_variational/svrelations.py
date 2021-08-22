from typing import List, Set

from src.configurations import cunion, cintersection
from src.databases.sets_variational.helpers import complementary
from src.types import SVRelation, Configuration, SConfiguration


def svconverse(r: SVRelation) -> SVRelation:
    return {t[::-1]: r[t] for t in r}


def svunion(r: SVRelation, s: SVRelation) -> SVRelation:
    result = {}

    tmp = dict(s)
    for t in r:
        if t in tmp:
            result[t] = set.union(r[t], tmp[t])
            #result[t] = r[t] + [i for i in tmp[t] if i not in r[t]]
            del tmp[t]
        else:
            result[t] = r[t]

    for t in tmp:
        result[t] = tmp[t]

    return result


def svintersection(r: SVRelation, s: SVRelation) -> SVRelation:
    result = {}

    for t in r:
        if t in s:
            result[t] = set.intersection(r[t], s[t])

    return result


def svdifference(universe: Set[SConfiguration], r: SVRelation, s: SVRelation) -> SVRelation:
    result = dict(r)

    for t in r:
        if t not in s:
            result[t] = r[t]
        else:
            complement_s_t = universe.difference(s[t])
            result[t] = set.intersection(r[t], complement_s_t)

    return result


def svcomposition(r: SVRelation, s: SVRelation) -> SVRelation:
    result = {}

    for x in r:
        for y in s:
            if x[-1] == y[0]:
                t = (*x[:-1], *y[1:])
                if t not in result:
                    result[t] = set(pc for pc in r[x] if pc in s[y])
                else:
                    result[t] = set.union(result[t], set(pc for pc in r[x] if pc in s[y]))

    return result
