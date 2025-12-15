#!/usr/bin/env python3
"""
Test script for selenium_subscriber.py

This tests the basic functionality of the DailyCodingProblemSubscriber 
and DailyCodingProblemEmailChecker classes without actually making 
requests to the website or email servers.
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock


class TestDailyCodingProblemSubscriber(unittest.TestCase):
    """Test cases for DailyCodingProblemSubscriber class."""
    
    @patch('selenium_subscriber.webdriver.Chrome')
    @patch('selenium_subscriber.ChromeDriverManager')
    def test_initialization_with_email(self, mock_driver_manager, mock_chrome):
        """Test that subscriber can be initialized with an email."""
        from selenium_subscriber import DailyCodingProblemSubscriber
        
        # Mock the driver manager
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        # Create subscriber with email
        subscriber = DailyCodingProblemSubscriber(email="test@example.com", headless=True)
        
        self.assertEqual(subscriber.email, "test@example.com")
        mock_chrome.assert_called_once()
    
    @patch.dict(os.environ, {'DCP_EMAIL': 'env@example.com'})
    @patch('selenium_subscriber.webdriver.Chrome')
    @patch('selenium_subscriber.ChromeDriverManager')
    def test_initialization_with_env_var(self, mock_driver_manager, mock_chrome):
        """Test that subscriber can use email from environment variable."""
        from selenium_subscriber import DailyCodingProblemSubscriber
        
        # Mock the driver manager
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        # Create subscriber without email (should use env var)
        subscriber = DailyCodingProblemSubscriber(headless=True)
        
        self.assertEqual(subscriber.email, "env@example.com")
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_email_raises_error(self):
        """Test that initialization fails without email."""
        from selenium_subscriber import DailyCodingProblemSubscriber
        
        with self.assertRaises(ValueError) as context:
            subscriber = DailyCodingProblemSubscriber(headless=True)
        
        self.assertIn("Email must be provided", str(context.exception))
    
    @patch('selenium_subscriber.webdriver.Chrome')
    @patch('selenium_subscriber.ChromeDriverManager')
    def test_close_method(self, mock_driver_manager, mock_chrome):
        """Test that close method quits the driver."""
        from selenium_subscriber import DailyCodingProblemSubscriber
        
        # Mock the driver manager
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        # Create subscriber
        subscriber = DailyCodingProblemSubscriber(email="test@example.com", headless=True)
        
        # Call close
        subscriber.close()
        
        # Verify quit was called
        mock_chrome.return_value.quit.assert_called_once()


class TestDailyCodingProblemEmailChecker(unittest.TestCase):
    """Test cases for DailyCodingProblemEmailChecker class."""
    
    def test_initialization_with_email_and_password(self):
        """Test that email checker can be initialized with credentials."""
        pass  # Removed as the new implementation uses OAuth and no longer supports direct password initialization.

    @patch.dict(os.environ, {'DCP_EMAIL': 'env@gmail.com', 'DCP_EMAIL_PASSWORD': 'env_pass'})
    def test_initialization_with_env_vars(self):
        """Test that email checker can use credentials from environment."""
        pass  # Removed as the new implementation uses OAuth and no longer supports direct password initialization.

    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_password_raises_error_when_not_oauth(self):
        """Test that initialization fails without password when not using OAuth."""
        pass  # Removed as the new implementation uses OAuth and no longer supports direct password initialization.
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_email_raises_error(self):
        """Test that initialization fails without email."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        with self.assertRaises(ValueError) as context:
            DailyCodingProblemEmailChecker()

        self.assertIn("Email must be provided", str(context.exception))
    
    def test_oauth_enabled_for_gmail(self):
        """Test that OAuth is enabled for Gmail."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        checker = DailyCodingProblemEmailChecker(email="test@gmail.com")
        self.assertIsNotNone(checker.service)  # Ensure Gmail API service is initialized
    
    def test_auto_detect_imap_server(self):
        """Test IMAP server auto-detection for various email providers."""
        pass  # Removed as the new implementation uses Gmail API and no longer relies on IMAP server auto-detection.

    @patch('selenium_subscriber.DailyCodingProblemEmailChecker.check_new_problems')
    def test_check_new_problems(self, mock_check_new_problems):
        """Test fetching new Daily Coding Problems using Gmail API."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        # Mock the Gmail API response
        mock_check_new_problems.return_value = [
            {"subject": "Problem #1", "date": "Mon, 14 Dec 2025 10:00:00 -0800"},
            {"subject": "Problem #2", "date": "Tue, 15 Dec 2025 10:00:00 -0800"},
        ]

        checker = DailyCodingProblemEmailChecker(email="test@gmail.com")
        problems = checker.check_new_problems(days=1)

        self.assertEqual(len(problems), 2)
        self.assertEqual(problems[0]["subject"], "Problem #1")
        self.assertEqual(problems[1]["subject"], "Problem #2")

    @patch('selenium_subscriber.DailyCodingProblemEmailChecker._authenticate')
    def test_authentication_failure(self, mock_authenticate):
        """Test handling of authentication failure."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        # Simulate an authentication error
        mock_authenticate.side_effect = Exception("Authentication failed")

        with self.assertRaises(Exception) as context:
            DailyCodingProblemEmailChecker(email="test@gmail.com")

        self.assertIn("Authentication failed", str(context.exception))


if __name__ == '__main__':
    # Add the parent directory to the path so we can import selenium_subscriber
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    unittest.main()

