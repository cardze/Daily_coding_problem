from main_1218 import *

def test_answer():
    input_output = [
        {
            'input':{
                'input_dict':{
                    "key": 3,
                    "foo": {
                        "a": 5,
                        "bar": {
                            "baz": 8
                        }
                    }
                }
            }
            ,
            'output':{
                "key": 3,
                "foo.a": 5,
                "foo.bar.baz": 8
            }
        }
    ]
    for i in input_output:
        assert solution(**i['input']) == i['output']
