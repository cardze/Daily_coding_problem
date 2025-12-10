from main_1215 import *

def test_answer():
    input_output = [
        {
            'input':{
                'start':'dog',
                'end':'cat',
                'dictionary':["dot", "dop", "dat", "cat"]
            },
            'output':["dog", "dot", "dat", "cat"]
        },
        {
            'input':{
                'start':'dog',
                'end':'cat',
                'dictionary':["dot", "tod", "dat", "dar"]
            },
            'output':None
        },
        {
            'input':{
                'start':'dog',
                'end':'you',
                'dictionary':["dot", "tod", "dat", "dar", "dou", "you"]
            },
            'output' : ['dog', 'dou', 'you']
        }
    ]
    for i in input_output:
        assert solution(**i['input']) == i['output']

def test_legal_next():
    assert legal_next('dog', 'dot') == True
    assert legal_next('dog', 'cat') == False



