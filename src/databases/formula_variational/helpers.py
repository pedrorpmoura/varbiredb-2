from typing import Set, List

from z3 import BoolRef, Solver, Not, unsat, substitute, BoolVal, simplify, is_true, Or, sat

from src.types import Configuration, SConfiguration


def is_valid(f: BoolRef) -> bool:
    s = Solver()
    s.add(Not(f))

    return s.check() == unsat


def feval(configuration: Configuration, formula: BoolRef) -> BoolRef:
    for feature in configuration:
        formula = substitute(formula, (feature, BoolVal(configuration[feature])))

    return simplify(formula)


def solve(features: Set[BoolRef], formula: BoolRef) -> Set[SConfiguration]:
    s = Solver()
    s.add(formula)

    solutions = set()

    while s.check() == sat:
        model = s.model()
        block = []
        solution = set()

        for feature in features:
            v = model.eval(feature, model_completion=True)
            block.append(feature != v)
            if is_true(v):
                solution.add(feature)

        s.add(Or(block))
        solutions.add(frozenset(solution))

    return solutions
