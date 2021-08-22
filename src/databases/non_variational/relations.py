from src.types import Relation


def converse(r: Relation) -> Relation:
    return set(map(lambda t: t[::-1], r))


def union(r: Relation, s: Relation) -> Relation:
    return set.union(r, s)


def intersection(r: Relation, s: Relation) -> Relation:
    return set.intersection(r, s)


def difference(r: Relation, s: Relation) -> Relation:
    return set.difference(r, s)


def composition(r: Relation, s: Relation) -> Relation:
    return set((*x[:-1], *y[1:])
               for x in r
               for y in s
               if x[-1] == y[0])
