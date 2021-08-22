from typing import Set, FrozenSet

from z3 import Not, And, simplify, Or, BoolRef, BoolVal

from src.generator.helpers import powerset


class ATrue:
    def __init__(self) -> None:
        self.value = True

    def evaluate(self, configuration):
        return self.value

    def to_z3(self):
        return BoolVal(self.value)

    def to_configurations(self, all_configurations):
        return all_configurations

    def __repr__(self):
        return 'tt'


class AFalse:
    def __init__(self) -> None:
        self.value = False

    def evaluate(self, configuration):
        return self.value

    def to_z3(self):
        return BoolVal(self.value)

    def to_configurations(self, all_configurations):
        return set()

    def __repr__(self):
        return 'ff'


class AVar:
    def __init__(self, variable) -> None:
        self.variable = variable

    def evaluate(self, configuration):
        return self.variable in configuration

    def to_configurations(self, all_configurations):
        return set(c for c in all_configurations if self.variable in c)

    def to_z3(self):
        return self.variable

    def to_dict(self):
        return {self.variable: True}

    def __repr__(self):
        return str(self.variable)


class ANot:
    def __init__(self, formula) -> None:
        self.formula = formula

    def evaluate(self, configuration):
        return not self.formula.evaluate(configuration)

    def to_configurations(self, all_configurations):
        aux = self.formula.to_configurations(all_configurations)
        return all_configurations.difference(aux)

    def to_z3(self):
        return simplify(Not(self.formula.to_z3()))

    def to_dict(self):
        [(v, _)] = self.formula.to_dict().items()
        return {v: False}

    def __repr__(self):
        return '-' + str(self.formula)


class AAnd:
    def __init__(self, *formulas):
        self.formulas = formulas

    def evaluate(self, configuration):
        return all(f.evaluate(configuration) for f in self.formulas)

    def to_configurations(self, all_configurations):
        return set.intersection(*(f.to_configurations(all_configurations)
                                  for f in self.formulas))

    def to_z3(self):
        return simplify(And(*[f.to_z3() for f in self.formulas]))

    def to_dict(self):
        result = {}
        for f in self.formulas:
            d = f.to_dict()
            result.update(d)

        return [result]

    def __repr__(self):
        return '(' + ' /\\ '.join(map(str, self.formulas)) + ')'


class AOr:
    def __init__(self, *formulas):
        self.formulas = formulas

    def evaluate(self, configuration):
        return any(f.evaluate(configuration) for f in self.formulas)

    def to_configurations(self, all_configurations):
        return set.union(*(f.to_configurations(all_configurations)
                           for f in self.formulas))

    def to_z3(self):
        return simplify(Or(*[f.to_z3() for f in self.formulas]))

    def to_dict(self):
        result = []
        for f in self.formulas:
            d = f.to_dict()
            result += d

        return result

    def __repr__(self):
        return ' \\/ '.join(map(str, self.formulas))
