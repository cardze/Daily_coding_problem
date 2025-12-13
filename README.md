# Daily_coding_problem

## About
This repository contains solutions to problems from [Daily Coding Problem](https://www.dailycodingproblem.com/).

## Testing
- trying pytest
    - run using `pytest test.py`
    - `pytest test.py --durations=0` show all tests' execution time
    - `pytest test.py --durations=1` show only slowest execution time
- try solving the problems from [here](https://www.dailycodingproblem.com/)

## Subscribing to Daily Coding Problem

This repository includes a Selenium automation script to subscribe to Daily Coding Problem.

### Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

You can subscribe using the Selenium automation script in two ways:

#### Option 1: Using command-line argument

```bash
python selenium_subscriber.py --email your.email@example.com
```

#### Option 2: Using environment variable

```bash
export DCP_EMAIL=your.email@example.com
python selenium_subscriber.py
```

#### Additional Options

- `--no-headless`: Run the browser in visible mode (useful for debugging)

```bash
python selenium_subscriber.py --email your.email@example.com --no-headless
```

### Configuration

You can create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your email address
```

Then source it before running the script:

```bash
source .env
python selenium_subscriber.py
```

### What the Script Does

The `selenium_subscriber.py` script:
1. Opens the Daily Coding Problem website
2. Finds the email subscription field
3. Enters your email address
4. Clicks the subscribe button
5. Takes a screenshot for verification

After running the script, check your email for a confirmation message from Daily Coding Problem.

