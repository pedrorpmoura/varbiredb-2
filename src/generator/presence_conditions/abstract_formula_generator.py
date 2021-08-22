import random
from typing import List

from z3 import BoolRef

from src.generator.presence_conditions.abstract_formulas import AOr, AVar, ANot, AAnd, ATrue


def decision(p: float) -> bool:
    return random.uniform(0, 1) <= p


def generate_conjunction(
        features: List[BoolRef],
        feature_presence_probability: float
):
    result = [AVar(f) if decision(0.5) else ANot(AVar(f))
              for f in features
              if decision(feature_presence_probability)]

    if not result:
        return ATrue()

    return AAnd(*result)


def generate_disjunction(
        features: List[BoolRef],
        disjunction_probability: float,
        feature_presence_probability: float
):
    result = [generate_conjunction(features, feature_presence_probability)]

    while decision(disjunction_probability):
        result.append(generate_conjunction(features, feature_presence_probability))

    return AOr(*result)


def generate_abstract_formula(
        features: List[BoolRef],
        disjunction_probability: float,
        feature_presence_probability: float
):
    return generate_disjunction(features, disjunction_probability, feature_presence_probability)
