# Email Parser Examples

This directory contains example problem files that can be used with the email parser.

## Using the Examples

### Example 1: Basic problem text file

```bash
python add_problem.py --text examples/sample_problem.txt --date 2024-12-15
```

This will create:
- `problems/2024_1215/readme.md`
- `problems/2024_1215/python/main.py`
- `problems/2024_1215/python/test.py`

### Example 2: Without specifying date (uses today's date)

```bash
python add_problem.py --text examples/sample_problem.txt
```

### Example 3: From stdin

```bash
cat examples/sample_problem.txt | python add_problem.py --stdin --date 2024-12-16
```

## Email Format

Daily Coding Problem emails typically contain:
- Optional company name (e.g., "This problem was asked by Google")
- Problem description with examples
- Optional difficulty level

The parser automatically extracts this information and creates a structured template for you to implement and test your solution.
