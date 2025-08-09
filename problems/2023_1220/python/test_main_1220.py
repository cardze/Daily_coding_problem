from main_1220 import *    

def test_answer():
    input_output = [
        {
            'input':{
                's': "dogcatcatcodecatdog",
                'words' : ["cat", "dog"]
            }
            ,
            'output': [0, 13]
        },
        {
            'input':{
                's': "dogcatcatcodecatdog",
                'words' : ["code", "cat"]
            }
            ,
            'output': [6, 9]
        }
    ]
    for i in input_output:
        assert solution(**i['input']) == i['output']
