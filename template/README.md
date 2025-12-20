# Problem Template

This directory contains template files for new Daily Coding Problems.

## Structure

```
template/
├── readme.md           # Problem description template
└── python/
    ├── main.py        # Solution implementation template
    └── test.py        # Unit tests template
```

## Usage

When using `selenium_subscriber.py download-problems`, these templates are automatically copied and populated with problem-specific information:

- `{PROBLEM_TITLE}` - Replaced with the problem subject from email
- `{PROBLEM_DATE}` - Replaced with the problem date from email

## Customization

Feel free to modify these templates to match your preferred structure and coding style. The automation script will use these templates when creating new problem directories.

## Example

After running:
```bash
python selenium_subscriber.py download-problems --email your@gmail.com
```

A new problem directory will be created following this structure:
```
problems/YYYY_MMDD/
├── readme.md           # Problem description (extracted from email)
└── python/
    ├── main.py        # Solution file (from template)
    └── test.py        # Test file (from template)
```
