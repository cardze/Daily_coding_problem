#!/usr/bin/env python3
"""
Selenium automation script to subscribe to Daily Coding Problem.

This script automates the process of subscribing to dailycodingproblem.com
as a new subscriber to receive daily coding problems via email.
"""

import os
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


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


def main():
    """Main function to run the subscriber."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Subscribe to Daily Coding Problem using Selenium automation'
    )
    parser.add_argument(
        '--email',
        help='Email address to subscribe with (or set DCP_EMAIL environment variable)',
        default=None
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode (not headless)'
    )
    
    args = parser.parse_args()
    
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


if __name__ == "__main__":
    main()
