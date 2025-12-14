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

After subscribing, you can check your email inbox for new Daily Coding Problems every time you open the app:

```bash
python selenium_subscriber.py check-email --email your.email@example.com --password your_app_password
```

**Important Notes:**
- For Gmail, Yahoo, and most email providers, you need to use an **app-specific password**, not your regular password
- The IMAP server is auto-detected based on your email domain (Gmail, Yahoo, Outlook, etc.)
- You can specify `--days N` to check for problems from the last N days (default is 1)

#### Setting up App-Specific Passwords

**For Gmail:**
1. Go to your Google Account settings
2. Enable 2-factor authentication if not already enabled
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Use this password with the script

**For Yahoo:**
1. Go to Account Security settings
2. Generate an app password
3. Use this password with the script

#### Using environment variables for email checking

```bash
export DCP_EMAIL=your.email@example.com
export DCP_EMAIL_PASSWORD=your_app_specific_password
python selenium_subscriber.py check-email
```

#### Check problems from the last 7 days

```bash
python selenium_subscriber.py check-email --days 7
```

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
1. Connects to your email inbox via IMAP
2. Searches for emails from dailycodingproblem.com
3. Displays new problems received in the specified time period
4. Shows the problem subject and date

After running the subscribe command, check your email for a confirmation message from Daily Coding Problem.


