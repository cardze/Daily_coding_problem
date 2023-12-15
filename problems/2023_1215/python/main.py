def solution(start:str, end:str, dictionary:list)->list:
    ret = []
    # check the dictionary if the end is in it or not
    if dictionary.count(end) == 0:
        return None

    # generate a dict for every possible next step
    next_step = { key:[] for key in dictionary }
    next_step[start] = []
    for step in dictionary:
        if legal_next(key=start, attender=step):
            next_step[start].append(step)
    for key in dictionary:
        for step in dictionary:
            if legal_next(key=key, attender=step):
                next_step[key].append(step)
    print(next_step)
    # Start evaluate the shortest answer
    start_list = [start]
    ret.append(start_list)
    while len(ret) > 0:
        top = ret.pop(0)
        print(top)
        for i in next_step[top[-1]]:
            copy = top.copy()
            copy.append(i)
            ret.append(copy)
            if i == end:
                return copy
        print(ret)

    return None

def legal_next(key:str , attender:str)->bool:
    if key == attender:
        return False
    
    torrence = 2
    for i in range(len(key)):
        if torrence == 0:
            return False
        if key[i] != attender[i]:
            torrence -= 1
    if torrence == 1:
        return True
    return False