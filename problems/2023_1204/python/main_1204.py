def solution(input:str)->str:
    mapping = []
    for ch in input:
        if mapping.count(ch) > 0:
            return ch
        else:
            mapping.append(ch)
    return None