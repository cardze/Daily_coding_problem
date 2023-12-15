from main import solution

def test_answer():
    io_mapping = {
        {
            "start":"dog",
            "end":"cat",
            "dictionary":{"dot", "dop", "dat", "cat"}
        } :  ["dog", "dot", "dat", "cat"],
        
    }
    for k,v in io_mapping.items():
        assert solution(k) == v


