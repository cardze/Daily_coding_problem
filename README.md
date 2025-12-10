# Daily Coding Problem Solutions

This repository contains solutions to coding problems from various sources, including [Daily Coding Problem](https://www.dailycodingproblem.com/).

## Repository Structure

Problems are organized by date in the `problems/` directory:
- Each problem is in a folder named `YYYY_MMDD` (e.g., `2023_1204`)
- Each problem folder contains:
  - `readme.md` - Problem description
  - `python/` - Python solutions and tests

## Problem Index

See [PROBLEMS.md](PROBLEMS.md) for a complete list of all problems with descriptions and dates.

## Testing

This repository uses pytest for testing:
- Run all tests: `pytest test.py`
- Show all test execution times: `pytest test.py --durations=0`
- Show only slowest test: `pytest test.py --durations=1`

## Running Tests for Individual Problems

Navigate to the problem's Python directory and run:
```bash
cd problems/YYYY_MMDD/python
pytest test.py
```

## Contributing

When adding new problems:
1. Create a new folder with date format `YYYY_MMDD`
2. Add a `readme.md` with the problem description
3. Include the problem source (company name or problem number if known)
4. Create `python/main.py` with your solution
5. Create `python/test.py` with test cases
6. Update [PROBLEMS.md](PROBLEMS.md) with the new problem
