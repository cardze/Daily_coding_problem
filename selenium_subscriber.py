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
    """Checks email inbox for new Daily Coding Problems."""
    
    # Gmail OAuth2 scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, email=None, password=None, imap_server=None, use_oauth=None):
        """
        Initialize the email checker.
        
        Args:
            email (str): Email address to check. If None, reads from DCP_EMAIL environment variable.
            password (str): Email password (optional, for non-OAuth). If None, reads from DCP_EMAIL_PASSWORD.
            imap_server (str): IMAP server address. If None, reads from DCP_IMAP_SERVER or auto-detects.
            use_oauth (bool): Use OAuth2 for Gmail. If None, auto-detects based on email domain and OAuth availability.
        """
        self.email = email or os.getenv('DCP_EMAIL')
        self.password = password or os.getenv('DCP_EMAIL_PASSWORD')
        self.imap_server = imap_server or os.getenv('DCP_IMAP_SERVER')
        
        if not self.email:
            raise ValueError("Email must be provided either as argument or DCP_EMAIL environment variable")
        
        # Determine authentication method
        domain = self.email.split('@')[1].lower() if '@' in self.email else ''
        
        # Auto-determine OAuth usage
        if use_oauth is None:
            # Use OAuth for Gmail if available, otherwise require password
            self.use_oauth = (domain == 'gmail.com' and OAUTH_AVAILABLE)
        else:
            self.use_oauth = use_oauth
        
        # Check if we have necessary credentials
        if not self.use_oauth and not self.password:
            if domain == 'gmail.com' and OAUTH_AVAILABLE:
                print("Tip: For Gmail, you can use OAuth2 authentication (browser-based login)")
                print("     Run with --use-oauth flag or just omit --password")
            raise ValueError("Password must be provided either as argument or DCP_EMAIL_PASSWORD environment variable")
        
        # Auto-detect IMAP server if not provided
        if not self.imap_server:
            self.imap_server = self._auto_detect_imap_server()
        
        self.mail = None
        self.creds = None
    
    def _auto_detect_imap_server(self):
        """Auto-detect IMAP server based on email domain."""
        domain = self.email.split('@')[1].lower()
        
        imap_servers = {
            'gmail.com': 'imap.gmail.com',
            'yahoo.com': 'imap.mail.yahoo.com',
            'outlook.com': 'imap-mail.outlook.com',
            'hotmail.com': 'imap-mail.outlook.com',
            'icloud.com': 'imap.mail.me.com',
            'aol.com': 'imap.aol.com',
        }
        
        return imap_servers.get(domain, f'imap.{domain}')
    
    def _get_oauth_credentials(self):
        """Get OAuth2 credentials for Gmail."""
        if not OAUTH_AVAILABLE:
            raise RuntimeError("OAuth2 libraries not available. Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2")
        
        creds = None
        token_file = Path.home() / '.dcp_gmail_token.pickle'
        
        # Load existing token if available
        if token_file.exists():
            try:
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Warning: Could not load saved token: {e}")
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("Refreshing OAuth2 token...")
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Warning: Could not refresh token: {e}")
                    creds = None
            
            if not creds:
                # Need to create OAuth client configuration
                print("\n" + "="*60)
                print("Gmail OAuth2 Setup Required")
                print("="*60)
                print("\nTo use OAuth2 with Gmail, you need to:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project (or select existing)")
                print("3. Enable Gmail API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download the credentials JSON file")
                print("6. Save it as 'gmail_credentials.json' in this directory")
                print("\nAlternatively, use --password with an app-specific password")
                print("="*60 + "\n")
                
                # Check if credentials file exists
                creds_file = Path('gmail_credentials.json')
                if not creds_file.exists():
                    raise FileNotFoundError(
                        "gmail_credentials.json not found. "
                        "Please follow the setup instructions above or use --password authentication."
                    )
                
                # Run OAuth flow
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(creds_file), self.SCOPES)
                    creds = flow.run_local_server(port=0)
                    
                    # Save credentials for future use
                    with open(token_file, 'wb') as token:
                        pickle.dump(creds, token)
                    print(f"✓ OAuth2 credentials saved to {token_file}")
                    
                except Exception as e:
                    raise RuntimeError(f"OAuth2 flow failed: {e}")
        
        return creds
    
    def _generate_oauth2_string(self, email, access_token):
        """
        Generate OAuth2 authentication string for IMAP XOAUTH2.
        
        Format: user={email}\1auth=Bearer {token}\1\1
        where \1 is the ASCII character 1 (used as separator in SASL)
        """
        # SASL XOAUTH2 format requires \1 (ASCII 1) as field separator
        auth_string = f'user={email}\1auth=Bearer {access_token}\1\1'
        return auth_string
    
    def connect(self):
        """Connect to the email server."""
        try:
            print(f"Connecting to {self.imap_server}...")
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            
            if self.use_oauth:
                # OAuth2 authentication
                print("Using OAuth2 authentication...")
                self.creds = self._get_oauth_credentials()
                auth_string = self._generate_oauth2_string(self.email, self.creds.token)
                # authenticate expects a callback that returns encoded auth string
                # The parameter x is the server challenge (not used for XOAUTH2 initial auth)
                self.mail.authenticate('XOAUTH2', lambda _: auth_string.encode())
                print(f"✓ Successfully connected to email: {self.email}")
            else:
                # Password-based authentication
                print("Using password authentication...")
                self.mail.login(self.email, self.password)
                print(f"✓ Successfully connected to email: {self.email}")
            
            return True
            
        except imaplib.IMAP4.error as e:
            print(f"✗ Failed to connect: {str(e)}")
            if not self.use_oauth:
                print(f"  Make sure you're using an app-specific password for Gmail/Yahoo/etc.")
            return False
        except FileNotFoundError as e:
            print(f"✗ {str(e)}")
            return False
        except Exception as e:
            print(f"✗ Connection error: {str(e)}")
            return False
    
    def check_new_problems(self, days=1):
        """
        Check for new Daily Coding Problems in the inbox.
        
        Args:
            days (int): Number of days to look back for emails.
        
        Returns:
            list: List of email subjects and dates for new problems.
        """
        if not self.mail:
            if not self.connect():
                return []
        
        try:
            # Select the inbox
            self.mail.select('INBOX')
            
            # Search for emails from Daily Coding Problem
            # Looking for emails from the last N days
            since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
            
            # Search for emails from dailycodingproblem.com
            search_criteria = f'(FROM "dailycodingproblem.com" SINCE {since_date})'
            _, message_numbers = self.mail.search(None, search_criteria)
            
            problems = []
            
            if message_numbers[0]:
                for num in message_numbers[0].split():
                    _, msg_data = self.mail.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Decode subject
                    subject = email_message['subject']
                    if subject:
                        decoded_subject = decode_header(subject)[0]
                        if isinstance(decoded_subject[0], bytes):
                            subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
                        else:
                            subject = decoded_subject[0]
                    
                    # Get date
                    date_str = email_message['date']
                    
                    problems.append({
                        'subject': subject,
                        'date': date_str,
                        'from': email_message['from']
                    })
            
            return problems
            
        except Exception as e:
            print(f"✗ Error checking emails: {str(e)}")
            return []
    
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
                print(f"   From: {problem['from']}")
                print()
        
        print(f"{'='*60}\n")
    
    def close(self):
        """Close the email connection."""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
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
    
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        print("\nPlease specify a command: 'subscribe' or 'check-email'")
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
                password=args.password,
                imap_server=args.imap_server,
                use_oauth=args.use_oauth
            )
            checker.display_new_problems(days=args.days)
            exit(0)
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            exit(1)
        finally:
            if checker:
                checker.close()




if __name__ == "__main__":
    main()
