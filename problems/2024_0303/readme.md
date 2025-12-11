# Activity Scheduling - Maximum Score

**Date:** 2024-03-03

## Problem Description

Given activity scheduling information, find the maximum score that can be acquired in a single day.

## Input Parameters

- `n` (int): Total number of days
- `s` (list[int]): Start day for each activity
- `e` (list[int]): End day for each activity  
- `a` (list[int]): Score acquired for each activity
- `m` (int): Maximum number of activities that can be attended in one day

## Objective

Calculate the maximum score that can be obtained on any single day, given that:
- An activity is available on day d if s[i] <= d < e[i]
- At most m activities can be attended on the same day
- You want to maximize the total score on the best day
