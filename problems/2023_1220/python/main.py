def solution(s:str, words:list)->list:
    total_len = 0
    single_len = len(words[0])
    ret = []
    for i in words :
        total_len += len(i)
    for j in range(len(s) - total_len +1):
        tmp = s[j:j+total_len]
        print(tmp)
        legal = True
        for word in words:
            if tmp.count(word) ==0:
                legal = False
        if legal:
            ret.append(j)
    return ret