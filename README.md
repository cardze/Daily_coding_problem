# Daily Coding Problem Solutions

This repository contains solutions to coding problems from [Daily Coding Problem](https://www.dailycodingproblem.com/).

## Syncing with Daily Coding Problem

This repository provides a sync script to help track which Daily Coding Problem numbers correspond to solutions in this repository.

**Usage:**
```bash
# List all problems and their DCP numbers (if assigned)
python sync_problems.py list

# Add a DCP number to a problem
python sync_problems.py add 2023_1204 387

# Show problems that don't have DCP numbers yet
python sync_problems.py untracked

# Initialize tracking file (first time setup)
python sync_problems.py init
```

The script maintains a `problem_tracking.json` file that maps problem directories to their Daily Coding Problem numbers, making it easy to reference the original problems on dailycodingproblem.com.

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
7. Use `python sync_problems.py add <directory> <dcp_number>` to track the DCP number
