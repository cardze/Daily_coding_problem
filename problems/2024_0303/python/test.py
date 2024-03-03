from main import *    
from time import time, process_time
def test_answer_with_slow():
    input_output = [
        {
            'input':{
                'n': 10,
                's' : [1, 2, 3, 4],
                'e' : [3, 4, 5, 6],
                'a' : [30, 40, 50, 60],
                'm' : 2,
            }
            ,
            'output': 110
        },
        {
            'input':{
                'n': 10,
                's' : [1, 2, 3, 4],
                'e' : [9, 4, 5, 6],
                'a' : [1000, 40, 50, 60],
                'm' : 2,
            }
            ,
            'output': 1060
        },
    ]
    input_output.append(generate_big_input())
    for i in input_output:
        assert solution1(**i['input']) == i['output']

def test_answer():
    input_output = [
        {
            'input':{
                'n': 10,
                's' : [1, 2, 3, 4],
                'e' : [3, 4, 5, 6],
                'a' : [30, 40, 50, 60],
                'm' : 2,
            }
            ,
            'output': 110
        },
        {
            'input':{
                'n': 10,
                's' : [1, 2, 3, 4],
                'e' : [9, 4, 5, 6],
                'a' : [1000, 40, 50, 60],
                'm' : 2,
            }
            ,
            'output': 1060
        },
    ]
    input_output.append(generate_big_input())
    for i in input_output:
        assert solution(**i['input']) == i['output']