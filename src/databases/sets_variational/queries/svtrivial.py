from src.types import SVRelation, Configuration


def svtrivial_qsome(r: SVRelation, configuration: Configuration) -> bool:
    pass


def svtrivial_qno(r: SVRelation, configuration: Configuration) -> bool:
    pass


def svtrivial_qin(r: SVRelation, s: SVRelation, configuration: Configuration) -> bool:
    pass


def svtrivial_qnot(query, configuration: Configuration) -> bool:
    pass


def svtrivial_qand(*queries, configuration: Configuration) -> bool:
    pass


def svtrivial_qor(*queries, configuration: Configuration) -> bool:
    pass
