from main_1204 import solution

def test_answer():
    io_mapping = {
        "acbbac" : "b",
        "abcdef" : None,
        "fuhsiuhgifhd" : "u"
    }
    for k,v in io_mapping.items():
        assert solution(k) == v
