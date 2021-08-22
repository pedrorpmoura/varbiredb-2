import copy

from src.generator.helpers import generate_configurations, powerset


def nv_convert(info):
    copied_info = copy.deepcopy(info)
    #print(copied_info)

    features = copied_info['features']
    configurations = powerset(features)

    result = []
    for c in configurations:
        db = {'configuration': c, 'relations': {}}

        for r in copied_info['relations']:
            db['relations'][r] = set()
            for e in copied_info['relations'][r]:
                if copied_info['relations'][r][e].evaluate(c):
                    db['relations'][r].add(e)

        result.append(db)

    return result
