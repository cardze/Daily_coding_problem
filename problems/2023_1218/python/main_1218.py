def solution(input_dict:dict)->dict:
    ret = {}
    more_layer = False
    # flat one layer
    for k, v in input_dict.items():
        if type(v) is dict:
            prefix = k
            for sub_k, sub_v in v.items():
                ret[prefix + "."+sub_k] = sub_v
                if type(sub_v) is dict:
                    more_layer = True
        else:
            ret[k] = v
    if more_layer :
        return solution(ret)
    return ret

