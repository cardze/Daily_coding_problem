# Daily_coding_problem

## About
This repository contains solutions to problems from [Daily Coding Problem](https://www.dailycodingproblem.com/).

## Testing
- trying pytest
    - run using `pytest test.py`
    - `pytest test.py --durations=0` show all tests' execution time
    - `pytest test.py --durations=1` show only slowest execution time
- try solving the problems from [here](https://www.dailycodingproblem.com/)

## Daily Coding Problem Automation

This repository includes automation tools to subscribe to Daily Coding Problem and check for new problems in your email.

### Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 1. Subscribing to Daily Coding Problem

You can subscribe using the Selenium automation script:

#### Using command-line argument

```bash
python selenium_subscriber.py subscribe --email your.email@example.com
```

#### Using environment variable

```bash
export DCP_EMAIL=your.email@example.com
python selenium_subscriber.py subscribe
```

#### Additional Options

- `--no-headless`: Run the browser in visible mode (useful for debugging)

```bash
python selenium_subscriber.py subscribe --email your.email@example.com --no-headless
```

### 2. Checking for New Problems in Your Email

After subscribing, you can check your Gmail inbox for new Daily Coding Problems every time you open the app.

#### Easy Method: OAuth2 (Gmail Only - Required)

For Gmail users, the script uses OAuth2 browser-based authentication (no password needed):

```bash
python selenium_subscriber.py check-email --email your@gmail.com
```

The first time you run this, you'll need to:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop app type)
5. Download the credentials JSON file
6. Save it as `credentials.json` in this directory
7. Run the command above - a browser will open for you to authorize the app
8. The authorization is saved, so you won't need to login again

After the first setup, subsequent checks are automatic - no password needed!

#### Important Notes:
- Only Gmail accounts are supported.
- Ensure that you have enabled the Gmail API and set up OAuth2 credentials as described above.
- You can specify `--days N` to check for problems from the last N days (default is 1).

#### Using environment variables for email checking

```bash
export DCP_EMAIL=your.email@example.com
# For OAuth2 (Gmail):
python selenium_subscriber.py check-email
```

#### Check problems from the last 7 days

```bash
python selenium_subscriber.py check-email --days 7
```

### 3. Download and Save New Problems

You can automatically download new problems from your email and save them to the repository structure:

```bash
python selenium_subscriber.py download-problems --email your@gmail.com
```

This command will:
1. Connect to your Gmail inbox using OAuth2
2. Search for new Daily Coding Problem emails
3. Extract the problem content from each email
4. Create a new directory for each problem in `problems/YYYY_MMDD/` format
5. Copy template files from `template/` directory
6. Save the problem description to `readme.md`
7. Create Python files (`main.py` and `test.py`) from templates with problem-specific data

#### Download problems from the last 7 days

```bash
python selenium_subscriber.py download-problems --days 7
```

#### Using environment variables

```bash
export DCP_EMAIL=your@gmail.com
python selenium_subscriber.py download-problems
```

#### Customizing Templates

The script uses template files from the `template/` directory:
- `template/readme.md` - Problem description template
- `template/python/main.py` - Solution implementation template
- `template/python/test.py` - Unit tests template

You can customize these templates to match your preferred structure and coding style. The automation script will use these templates when creating new problem directories.

### Configuration

You can create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your email address and app password
```

Then source it before running the script:

```bash
source .env
python selenium_subscriber.py check-email
```

### What the Script Does

**Subscribe command:**
1. Opens the Daily Coding Problem website
2. Finds the email subscription field
3. Enters your email address
4. Clicks the subscribe button
5. Takes a screenshot for verification

**Check-email command:**
1. Connects to your Gmail inbox via Gmail API using OAuth2
2. Searches for emails from dailycodingproblem.com
3. Displays new problems received in the specified time period
4. Shows the problem subject and date

**Download-problems command:**
1. Connects to your Gmail inbox via Gmail API using OAuth2
2. Searches for emails from dailycodingproblem.com
3. Downloads and extracts the problem content from each email
4. Creates a new directory structure for each problem (`problems/YYYY_MMDD/`)
5. Saves the problem description to `readme.md`
6. Creates placeholder Python solution and test files

After running the subscribe command, check your email for a confirmation message from Daily Coding Problem.


