from main_1221 import *    

def test_answer():
    input_output = [
        {
            'input':{
                's1': "abc",
                's2' : "bcd"
            }
            ,
            'output': True
        },
        {
            'input':{
                's1': "foo",
                's2' : "bar"
            }
            ,
            'output': False
        },
        {
            'input':{
                's1': "abccccccc",
                's2' : "bcd"
            }
            ,
            'output': False
        }
    ]
    for i in input_output:
        assert solution(**i['input']) == i['output']
