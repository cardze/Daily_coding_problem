# Problem Index

This document provides an index of all coding problems in this repository.

## Problems List

### Problem 2023-12-04
**Directory:** `problems/2023_1204/`  
**Asked by:** Google  
**Description:** Given a string, return the first recurring character in it, or null if there is no recurring character.

**Example:**
- Input: `"acbbac"` → Output: `"b"`
- Input: `"abcdef"` → Output: `null`

---

### Problem 2023-12-15
**Directory:** `problems/2023_1215/`  
**Description:** Given a start word, an end word, and a dictionary of valid words, find the shortest transformation sequence from start to end such that only one letter is changed at each step of the sequence, and each transformed word exists in the dictionary.

**Example:**
- Input: start = `"dog"`, end = `"cat"`, dictionary = `{"dot", "dop", "dat", "cat"}`
- Output: `["dog", "dot", "dat", "cat"]`

---

### Problem 2023-12-18
**Directory:** `problems/2023_1218/`  
**Description:** Write a function to flatten a nested dictionary. Namespace the keys with a period.

**Example:**
```python
Input: {
    "key": 3,
    "foo": {
        "a": 5,
        "bar": {
            "baz": 8
        }
    }
}

Output: {
    "key": 3,
    "foo.a": 5,
    "foo.bar.baz": 8
}
```

---

### Problem 2023-12-20
**Directory:** `problems/2023_1220/`  
**Description:** Given a string s and a list of words where each word is the same length, find all starting indices of substrings in s that is a concatenation of every word in words exactly once.

**Example:**
- Input: s = `"dogcatcatcodecatdog"`, words = `["cat", "dog"]`
- Output: `[0, 13]`

---

### Problem 2023-12-21
**Directory:** `problems/2023_1221/`  
**Description:** Determine whether there exists a one-to-one character mapping from one string s1 to another s2.

**Example:**
- Input: s1 = `"abc"`, s2 = `"bcd"` → Output: `true` (map a→b, b→c, c→d)
- Input: s1 = `"foo"`, s2 = `"bar"` → Output: `false` (o cannot map to two characters)

---

### Problem 2024-03-03
**Directory:** `problems/2024_0303/`  
**Description:** Activity scheduling problem - given total days (n), start days (s), end days (e), scores (a), and max activities per day (m), find the maximum score achievable.

**Parameters:**
- n: total number of days
- s: list of start days for activities
- e: list of end days for activities
- a: list of scores for activities
- m: maximum number of activities that can be attended in one day

---

## Contributing New Problems

When adding a new problem, please:
1. Create a new directory with the date format `YYYY_MMDD`
2. Include a `readme.md` with the full problem description
3. If known, include the source (e.g., "This problem was asked by [Company]")
4. Add your solution in `python/main.py` and tests in `python/test.py`
5. Update this index file with the new problem details
