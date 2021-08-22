import copy

from src.generator.helpers import generate_configurations, powerset


def sv_convert(info):
    result = copy.deepcopy(info)
    result['configurations'] = powerset(info['features'])

    for r in result['relations']:
        for e in result['relations'][r]:
            result['relations'][r][e] = result['relations'][r][e].to_configurations(result['configurations'])

    return result
