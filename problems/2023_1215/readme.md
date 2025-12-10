# Word Transformation Problem

**Date:** 2023-12-15

## Problem Description

Given a start word, an end word, and a dictionary of valid words, find the shortest transformation sequence from start to end such that only one letter is changed at each step of the sequence, and each transformed word exists in the dictionary. If there is no possible transformation, return null. Each word in the dictionary have the same length as start and end and is lowercase.

## Examples

**Example 1:**
- Input: start = `"dog"`, end = `"cat"`, dictionary = `{"dot", "dop", "dat", "cat"}`
- Output: `["dog", "dot", "dat", "cat"]`

**Example 2:**
- Input: start = `"dog"`, end = `"cat"`, dictionary = `{"dot", "tod", "dat", "dar"}`
- Output: `null` (no possible transformation from dog to cat)