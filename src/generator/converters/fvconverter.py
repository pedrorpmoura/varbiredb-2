import copy


def fv_convert(info):
    result = copy.deepcopy(info)

    for r in result['relations']:
        for e in result['relations'][r]:
            result['relations'][r][e] = result['relations'][r][e].to_z3()

    return result
