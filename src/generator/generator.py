import json
import random
from z3 import Bool

from src.generator.converters.fvconverter import fv_convert
from src.generator.converters.nvconverter import nv_convert
from src.generator.converters.svconverter import sv_convert
from src.generator.presence_conditions.abstract_formula_generator import generate_abstract_formula


class Generator:

    def __init__(self, options: dict) -> None:

        # parse features
        n_features = options['numberOfActivatedFeatures']
        self.features = options['featuresUniverse'][:n_features]
        self.features = list(map(Bool, self.features))

        # presence conditions configurations
        self.feature_presence_probability = options['featurePresenceProbability']
        self.conjunction_probability = options['conjunctionProbability']
        self.disjunction_probability = options['disjunctionProbability']

        # parse sets information
        n_sets = options['numberOfSets']
        self.sets_names = options['setsUniverse'][:n_sets]
        self.n_elements = options['numberOfElements']
        self.sets = {}

        # parse relations information
        n_relations = options['numberOfRelations']
        self.relations_names = options['relationsUniverse'][:n_relations]
        self.relation_types = options['typesOfRelations']
        self.relations_presence_probability = options['presenceProbabilityOfRelations']
        self.relations = {}

    def generate(self):
        self.generate_sets()
        self.generate_relations()

        info = {
            'features': self.features,
            'relations': self.relations
        }

        return nv_convert(info), fv_convert(info), sv_convert(info)

    def generate_sets(self):
        for s in self.sets_names:
            self.relations[s] = {}

            for i in range(self.n_elements):
                element_name = s.lower() + str(i)
                element_pc = generate_abstract_formula(
                    self.features,
                    self.disjunction_probability,
                    self.conjunction_probability
                )

                self.relations[s][(element_name,)] = element_pc

    def generate_relations(self):

        for i, ([a, b], p) in enumerate(
                zip(self.relation_types, self.relations_presence_probability)):
            from_set = self.sets_names[int(a[1:])]
            to_set = self.sets_names[int(b[1:])]

            relation_name = self.relations_names[i]
            self.relations[relation_name] = {}
            for (x,) in self.relations[from_set]:
                for (y,) in self.relations[to_set]:
                    if random.uniform(0, 1) <= p:
                        self.relations[relation_name][(x, y)] = generate_abstract_formula(
                                self.features,
                                self.disjunction_probability,
                                self.conjunction_probability)
