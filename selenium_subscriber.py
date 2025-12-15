#!/usr/bin/env python3
"""
Selenium automation script to subscribe to Daily Coding Problem.

This script automates the process of subscribing to dailycodingproblem.com
as a new subscriber to receive daily coding problems via email.
It also provides functionality to check for new problems in your email inbox.
"""

import os
import sys
import time
import tempfile
import imaplib
import email
import base64
import json
import pickle
from pathlib import Path
from email.header import decode_header
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# OAuth2 imports (optional, for Gmail)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False


class DailyCodingProblemSubscriber:
    """Automates subscription to Daily Coding Problem."""
    
    def __init__(self, email=None, headless=True):
        """
        Initialize the subscriber.
        
        Args:
            email (str): Email address to subscribe with. If None, reads from environment.
            headless (bool): Whether to run browser in headless mode.
        """
        self.email = email or os.getenv('DCP_EMAIL')
        if not self.email:
            raise ValueError("Email must be provided either as argument or DCP_EMAIL environment variable")
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Initialize the driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
    
    def subscribe(self):
        """
        Navigate to Daily Coding Problem website and subscribe.
        
        Returns:
            bool: True if subscription was successful, False otherwise.
        """
        try:
            # Navigate to the website
            print(f"Navigating to Daily Coding Problem website...")
            self.driver.get("https://www.dailycodingproblem.com/")
            
            # Wait for page to load
            time.sleep(2)
            
            # Find the email input field
            # The website typically has an input field for email subscription
            print(f"Looking for email input field...")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[placeholder*='email' i]"))
            )
            
            # Enter email address
            print(f"Entering email: {self.email}")
            email_input.clear()
            email_input.send_keys(self.email)
            
            # Find and click the subscribe button
            print(f"Looking for subscribe button...")
            # Try different possible button selectors
            button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Subscribe')",
                ".subscribe-button",
                "#subscribe-button"
            ]
            
            submit_button = None
            for selector in button_selectors:
                try:
                    if 'contains' in selector:
                        # XPath for text content (case-insensitive)
                        submit_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Subscribe') or contains(., 'subscribe') or contains(., 'SUBSCRIBE')]")
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button:
                        break
                except (NoSuchElementException, Exception):
                    continue
            
            if not submit_button:
                # Try to find the closest button to the email input
                submit_button = email_input.find_element(By.XPATH, "following::button[1] | following::input[@type='submit'][1]")
            
            print(f"Clicking subscribe button...")
            submit_button.click()
            
            # Wait for confirmation
            time.sleep(3)
            
            # Check for success message
            try:
                # Look for common success keywords
                success_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(., 'success') or contains(., 'Success') or "
                    "contains(., 'thank') or contains(., 'Thank') or "
                    "contains(., 'subscribed') or contains(., 'Subscribed')]"
                )
                if success_elements:
                    print(f"✓ Successfully subscribed with email: {self.email}")
                    return True
            except (NoSuchElementException, Exception):
                pass
            
            print(f"✓ Subscription request submitted for: {self.email}")
            print(f"  Please check your email to confirm the subscription.")
            return True
            
        except Exception as e:
            print(f"✗ Error during subscription: {str(e)}")
            return False
        
        finally:
            # Take a screenshot for debugging
            try:
                screenshot_path = os.path.join(tempfile.gettempdir(), "subscription_screenshot.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
            except Exception:
                pass
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")


class DailyCodingProblemEmailChecker:
    """Checks email inbox for new Daily Coding Problems using Gmail API."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, email=None):
        """
        Initialize the email checker.

        Args:
            email (str): Email address to check. If None, reads from DCP_EMAIL environment variable.
        """
        self.email = email or os.getenv('DCP_EMAIL')
        if not self.email:
            raise ValueError("Email must be provided either as argument or DCP_EMAIL environment variable")

        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API and initialize the service."""
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("gmail", "v1", credentials=self.creds)

    def check_new_problems(self, days=1):
        """
        Check for new Daily Coding Problems in the inbox using Gmail API.

        Args:
            days (int): Number of days to look back for emails.

        Returns:
            list: List of email details including subject, date, and content.
        """
        try:
            results = self.service.users().messages().list(
                userId="me",
                q=f"from:dailycodingproblem.com newer_than:{days}d"
            ).execute()

            messages = results.get("messages", [])
            problems = []

            for message in messages:
                msg = self.service.users().messages().get(userId="me", id=message["id"], format="full").execute()
                payload = msg.get("payload", {})
                headers = payload.get("headers", [])

                subject = next((header["value"] for header in headers if header["name"].lower() == "subject"), "")
                date = next((header["value"] for header in headers if header["name"].lower() == "date"), "")
                
                # Extract email body
                body = self._get_email_body(payload)

                problems.append({
                    "subject": subject, 
                    "date": date,
                    "body": body,
                    "message_id": message["id"]
                })

            return problems

        except Exception as e:
            print(f"✗ Error checking emails: {str(e)}")
            return []
    
    def _get_email_body(self, payload):
        """
        Extract email body from Gmail API payload.
        
        Args:
            payload: Email payload from Gmail API
            
        Returns:
            str: Decoded email body content
        """
        body = ""
        
        if "parts" in payload:
            # Multi-part email
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    if "data" in part.get("body", {}):
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break
                elif part.get("mimeType") == "text/html" and not body:
                    # Fallback to HTML if plain text not available
                    if "data" in part.get("body", {}):
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        else:
            # Single part email
            if "data" in payload.get("body", {}):
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        
        return body
    
    def _extract_problem_content(self, body, subject):
        """
        Extract the problem description from email body.
        
        Args:
            body: Email body text
            subject: Email subject
            
        Returns:
            str: Extracted problem content
        """
        # Try to extract the problem statement from the email
        # Daily Coding Problem emails typically have a specific format
        
        lines = body.split('\n')
        problem_lines = []
        in_problem = False
        
        for line in lines:
            # Skip header/greeting lines
            if any(phrase in line.lower() for phrase in ['good morning', 'hello', 'hi there', 'unsubscribe', 'http']):
                continue
            
            # Look for problem content indicators
            if line.strip() and not line.startswith('>'):
                # Skip very short lines that are likely formatting
                if len(line.strip()) > 10 or in_problem:
                    problem_lines.append(line.rstrip())
                    in_problem = True
        
        # If we couldn't extract properly, return the whole body
        if not problem_lines:
            return body
        
        return '\n'.join(problem_lines).strip()
    
    def save_problem(self, problem, base_dir="problems"):
        """
        Save a problem to the repository structure.
        
        Args:
            problem (dict): Problem data including subject, date, and body
            base_dir (str): Base directory for problems
            
        Returns:
            str: Path to the created problem directory, or None if failed
        """
        try:
            # Parse the date to create directory name
            # Try to parse the email date
            from email.utils import parsedate_to_datetime
            try:
                date_obj = parsedate_to_datetime(problem['date'])
            except:
                # Fallback to current date if parsing fails
                date_obj = datetime.now()
            
            # Format: YYYY_MMDD
            dir_name = date_obj.strftime("%Y_%m%d")
            problem_dir = Path(base_dir) / dir_name
            
            # Check if directory already exists
            if problem_dir.exists():
                print(f"⚠ Problem directory {dir_name} already exists, skipping...")
                return None
            
            # Create directory structure
            problem_dir.mkdir(parents=True, exist_ok=True)
            python_dir = problem_dir / "python"
            python_dir.mkdir(exist_ok=True)
            
            # Extract and save problem content
            problem_content = self._extract_problem_content(problem['body'], problem['subject'])
            readme_path = problem_dir / "readme.md"
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(problem_content)
            
            # Create placeholder Python files
            main_py = python_dir / "main.py"
            with open(main_py, 'w', encoding='utf-8') as f:
                f.write(f"# {problem['subject']}\n")
                f.write(f"# Date: {problem['date']}\n\n")
                f.write("def solution():\n")
                f.write("    # TODO: Implement solution\n")
                f.write("    pass\n")
            
            test_py = python_dir / "test.py"
            with open(test_py, 'w', encoding='utf-8') as f:
                f.write("import pytest\n")
                f.write("from main import solution\n\n")
                f.write("def test_solution():\n")
                f.write("    # TODO: Add test cases\n")
                f.write("    pass\n")
            
            print(f"✓ Saved problem to {problem_dir}")
            return str(problem_dir)
            
        except Exception as e:
            print(f"✗ Error saving problem: {str(e)}")
            return None
    
    def download_and_save_problems(self, days=1):
        """
        Download new problems and save them to the repository.
        
        Args:
            days (int): Number of days to look back for emails
            
        Returns:
            list: Paths to created problem directories
        """
        print(f"\n{'='*60}")
        print(f"Downloading Daily Coding Problems (last {days} day(s))...")
        print(f"{'='*60}\n")
        
        problems = self.check_new_problems(days)
        
        if not problems:
            print("No new Daily Coding Problems found.")
            print("Make sure you're subscribed and emails aren't in spam folder.")
            return []
        
        print(f"Found {len(problems)} Daily Coding Problem(s)\n")
        
        saved_paths = []
        for i, problem in enumerate(problems, 1):
            print(f"{i}. {problem['subject']}")
            print(f"   Date: {problem['date']}")
            path = self.save_problem(problem)
            if path:
                saved_paths.append(path)
            print()
        
        print(f"{'='*60}")
        print(f"Successfully saved {len(saved_paths)} problem(s)")
        print(f"{'='*60}\n")
        
        return saved_paths

    def display_new_problems(self, days=1):
        """
        Check and display new Daily Coding Problems.

        Args:
            days (int): Number of days to look back for emails.
        """
        print(f"\n{'='*60}")
        print(f"Checking for Daily Coding Problems (last {days} day(s))...")
        print(f"{'='*60}\n")
        
        problems = self.check_new_problems(days)
        
        if not problems:
            print("No new Daily Coding Problems found.")
            print(f"Make sure you're subscribed and emails aren't in spam folder.")
        else:
            print(f"Found {len(problems)} Daily Coding Problem(s):\n")
            for i, problem in enumerate(problems, 1):
                print(f"{i}. {problem['subject']}")
                print(f"   Date: {problem['date']}")
                # print(f"   From: {problem['from']}")
                print()
        
        print(f"{'='*60}\n")
    
    def close(self):
        """Close the email connection."""
        if self.service:
            try:
                self.service.close()
                self.service.logout()
                print("Email connection closed.")
            except Exception:
                pass



def main():
    """Main function to run the subscriber or email checker."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Subscribe to Daily Coding Problem or check for new problems in email'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Subscribe command
    subscribe_parser = subparsers.add_parser('subscribe', help='Subscribe to Daily Coding Problem')
    subscribe_parser.add_argument(
        '--email',
        help='Email address to subscribe with (or set DCP_EMAIL environment variable)',
        default=None
    )
    subscribe_parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode (not headless)'
    )
    
    # Check email command
    check_parser = subparsers.add_parser('check-email', help='Check email for new Daily Coding Problems')
    check_parser.add_argument(
        '--email',
        help='Email address to check (or set DCP_EMAIL environment variable)',
        default=None
    )
    check_parser.add_argument(
        '--password',
        help='Email password for non-OAuth authentication (or set DCP_EMAIL_PASSWORD)',
        default=None
    )
    check_parser.add_argument(
        '--use-oauth',
        action='store_true',
        help='Use OAuth2 for Gmail (browser-based login, no password needed)'
    )
    check_parser.add_argument(
        '--imap-server',
        help='IMAP server address (or set DCP_IMAP_SERVER, auto-detected if not provided)',
        default=None
    )
    check_parser.add_argument(
        '--days',
        type=int,
        default=1,
        help='Number of days to look back for emails (default: 1)'
    )
    
    # Download problems command
    download_parser = subparsers.add_parser('download-problems', help='Download and save new Daily Coding Problems to repository')
    download_parser.add_argument(
        '--email',
        help='Email address to check (or set DCP_EMAIL environment variable)',
        default=None
    )
    download_parser.add_argument(
        '--days',
        type=int,
        default=1,
        help='Number of days to look back for emails (default: 1)'
    )
    
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        print("\nPlease specify a command: 'subscribe', 'check-email', or 'download-problems'")
        exit(1)
    
    if args.command == 'subscribe':
        subscriber = None
        try:
            subscriber = DailyCodingProblemSubscriber(
                email=args.email,
                headless=not args.no_headless
            )
            success = subscriber.subscribe()
            exit(0 if success else 1)
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            exit(1)
        finally:
            if subscriber:
                subscriber.close()
    
    elif args.command == 'check-email':
        checker = None
        try:
            checker = DailyCodingProblemEmailChecker(
                email=args.email,
                # password=args.password,
                # imap_server=args.imap_server,
                # use_oauth=args.use_oauth
            )
            checker.display_new_problems(days=args.days)
            exit(0)
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            exit(1)
        finally:
            if checker:
                checker.close()
    
    elif args.command == 'download-problems':
        checker = None
        try:
            checker = DailyCodingProblemEmailChecker(email=args.email)
            saved_paths = checker.download_and_save_problems(days=args.days)
            exit(0 if saved_paths else 1)
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            exit(1)
        finally:
            if checker:
                checker.close()




if __name__ == "__main__":
    main()
