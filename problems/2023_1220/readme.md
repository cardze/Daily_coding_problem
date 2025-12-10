# Substring Concatenation

**Date:** 2023-12-20

## Problem Description

Given a string s and a list of words words, where each word is the same length, find all starting indices of substrings in s that is a concatenation of every word in words exactly once.

The order of the indices does not matter.

## Examples

**Example 1:**
- Input: s = `"dogcatcatcodecatdog"`, words = `["cat", "dog"]`
- Output: `[0, 13]`
- Explanation: `"dogcat"` starts at index 0 and `"catdog"` starts at index 13

**Example 2:**
- Input: s = `"barfoobazbitbyte"`, words = `["dog", "cat"]`
- Output: `[]`
- Explanation: No substrings composed of "dog" and "cat" in s