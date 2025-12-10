def solution(s1:str, s2:str)->bool:
    # if the length of two string is different
    # the one to void case should ocur
    # return false
    if len(s1) != len(s2):
        return False
    mapping = {}
    for i in range(len(s1)):
        if s1[i] in mapping:
            if mapping[s1[i]] != s2[i]:
                return False
        mapping[s1[i]] = s2[i]
    return True