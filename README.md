# Daily_coding_problem
- try solving the problems from [here](https://www.dailycodingproblem.com/)

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

## Adding New Problems

You can automatically create problem templates from Daily Coding Problem emails or text files using the email parser:

### From a text file:
```bash
python add_problem.py --text problem.txt
```

### From an email file (.eml format):
```bash
python add_problem.py --email daily_problem.eml
```

### From stdin:
```bash
cat problem.txt | python add_problem.py --stdin
```

### Specify a custom date:
```bash
python add_problem.py --text problem.txt --date 2024-03-15
```

This will automatically create:
- `problems/YYYY_MMDD/readme.md` - Problem description
- `problems/YYYY_MMDD/python/main.py` - Solution template
- `problems/YYYY_MMDD/python/test.py` - Test template

## Testing

### Run tests for a specific problem:
```bash
pytest problems/YYYY_MMDD/python/test.py
```

### Run tests with execution time:
```bash
pytest test.py --durations=0  # show all tests' execution time
pytest test.py --durations=1  # show only slowest execution time
```

### Run email parser tests:
```bash
pytest test_email_parser.py
```
