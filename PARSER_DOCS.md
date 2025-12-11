# Email Parser Developer Documentation

## Overview

The email parser system consists of two main components:
- `DailyProblemParser`: Parses Daily Coding Problem emails and extracts problem information
- `ProblemTemplateGenerator`: Generates problem directory structure and template files

## Architecture

### DailyProblemParser

Handles parsing of email content in multiple formats:
- Email files (.eml format) 
- Plain text files
- HTML emails (automatically converted to text)

**Key Methods:**
- `parse_email_file(email_path)`: Parse from .eml file
- `parse_email_message(msg)`: Parse email message object
- `parse_text(text)`: Parse raw text directly

**Extracted Information:**
- Problem description
- Company name (if mentioned)
- Difficulty level (if mentioned)

### ProblemTemplateGenerator

Creates standardized problem directory structure:
```
problems/
  YYYY_MMDD/
    readme.md          # Problem description
    python/
      main.py          # Solution template
      test.py          # Test template
```

## Usage

### Programmatic Usage

```python
from email_parser import DailyProblemParser, ProblemTemplateGenerator
from datetime import datetime

# Parse problem
parser = DailyProblemParser()
problem_data = parser.parse_text(problem_text)

# Generate template
generator = ProblemTemplateGenerator()
problem_dir = generator.generate(problem_data, date=datetime(2024, 3, 15))
```

### CLI Usage

See `add_problem.py --help` for command-line options.

## Testing

Run tests with:
```bash
pytest test_email_parser.py -v
```

## Pattern Matching

The parser recognizes common patterns in Daily Coding Problem emails:

**Company Detection:**
- "This problem was asked by [Company]"
- "This problem was recently asked by [Company]"
- "Asked by [Company]"

**Difficulty Detection:**
- Looks for keywords: "easy", "medium", "hard" (case-insensitive)

## Extending the Parser

To add new parsing capabilities:

1. Add new extraction method to `DailyProblemParser`
2. Update `parse_text()` to call the new method
3. Add corresponding tests in `test_email_parser.py`
4. Update template generation if needed

## Error Handling

The parser handles:
- Missing company/difficulty information (returns None)
- Multiple email formats (HTML, plain text)
- Existing problem directories (raises FileExistsError)
- Invalid date formats (CLI raises ValueError)

## Future Enhancements

Potential improvements:
- Support for problem numbers/IDs
- Multiple language support (not just Python)
- Automatic test case extraction from examples
- Email subscription integration
- Batch processing of multiple problems
