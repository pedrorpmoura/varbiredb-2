from z3 import Bool

from src.databases.formula_variational.fvrelations import fvcomposition, fvdifference
from src.databases.sets_variational.svrelations import svdifference, svcomposition
from src.generator.converters.fvconverter import fv_convert
from src.generator.converters.nvconverter import nv_convert
from src.generator.converters.svconverter import sv_convert
from src.generator.presence_conditions.abstract_formulas import AVar, ATrue


class EvenElementsError(Exception):
    """The number of elements is not an odd number."""


def linear(s, p, elements):
    if elements % 2 == 0:
        raise EvenElementsError

    number_of_topics = elements // 2
    number_of_nodes = number_of_topics + 1

    nodes = []
    topics = []
    for i in range(number_of_nodes):
        nodes.append('node' + str(i))
        if i < number_of_topics:
            topics.append('topic' + str(i))

    subscribes = {}
    publishes = {}

    features_subscribes = list(map(Bool, ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'][:s]))
    features_publishes = list(map(Bool, ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'][:p]))
    # features_publishes  = ['P1', 'P2', 'P3', 'P4']

    for i in range(len(nodes)):
        for j, feature in enumerate(features_subscribes):
            try:
                if i - (j + 1) >= 0:
                    subscribes[(nodes[i], topics[i - (j + 1)])] = AVar(feature)
            except IndexError:
                pass

    for i in range(len(nodes)):
        for j, feature in enumerate(features_publishes):
            try:
                publishes[(nodes[i], topics[i + j])] = AVar(feature)
            except IndexError:
                pass

    node = dict(map(lambda n: ((n,), ATrue()), nodes))
    topic = dict(map(lambda t: ((t,), ATrue()), topics))

    return {
        'features': set.union(set(features_subscribes), set(features_publishes)),
        'relations': {
            'Node': node,
            'Topic': topic,
            'subscribes': subscribes,
            'publishes': publishes
        }
    }


from pympler import asizeof
def generate_linear(p, s, elements):
    result = linear(p, s, elements)
    nv = nv_convert(result)
    print('NV: ', asizeof.asizeof(nv))
    fv = fv_convert(result)
    print('FV: ', asizeof.asizeof(fv))
    sv = sv_convert(result)
    print('SV: ', asizeof.asizeof(sv))


    return nv, fv, sv
