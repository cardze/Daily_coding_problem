# Flatten Nested Dictionary

**Date:** 2023-12-18

## Problem Description

Write a function to flatten a nested dictionary. Namespace the keys with a period.

You can assume keys do not contain dots in them, i.e. no clobbering will occur.

## Examples

**Example:**

Input:
```python
{
    "key": 3,
    "foo": {
        "a": 5,
        "bar": {
            "baz": 8
        }
    }
}
```

Output:
```python
{
    "key": 3,
    "foo.a": 5,
    "foo.bar.baz": 8
}
```