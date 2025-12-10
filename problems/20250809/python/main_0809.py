
# find faster solution
def solution(n:int, s:list , e:list, a:list, m:int)->int:
    ret = 0 
    # main idea is to make list that contains
    # the day to check from s list and e list
    check_point = []
    for i in range(len(s)):
        check_point.append((s[i], a[i]))
        check_point.append((e[i], -a[i]))
    check_point.sort()
    temp = {
        'total': 0,
        'list':[],
    }
    for pair in check_point:
        if pair[1] > 0:
            temp['total'] += pair[1]
            temp['list'].append(pair[1])
            temp['list'].sort(reverse=True)
            if len(temp['list']) > m:
                temp['total'] -= temp['list'][-1]
                temp['list'].pop()
        else:
            if -pair[1] in temp['list']:
                temp['total'] += pair[1]
                temp['list'].remove(-pair[1])
        ret = max(ret, temp['total'])
    return ret

# accurate but slow
def solution1(n:int, s:list , e:list, a:list, m:int)->int:
    ret = 0 
    for day in range(n):
        tmp = []
        for j in range(len(s)):
            if day in range(s[j], e[j]):
                tmp.append(a[j])
        tmp.sort(reverse=True)
        ret = max(ret, sum(tmp[:m]))
    return ret

def generate_big_input():
    n = 10**3
    s = [1]*n
    e = [ i for i in range(1, n+1) ]
    a = [ i*10 for i in range(1, n+1)]
    m = 2
    ret = {
        'input':{
            'n': n,
            's' : s,
            'e' : e,
            'a' : a,
            'm' : m,
        },
        'output': solution1(n, s, e, a, m)
    }
    return ret