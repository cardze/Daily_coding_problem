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
        from selenium_subscriber import DailyCodingProblemEmailChecker
        
        checker = DailyCodingProblemEmailChecker(
            email="test@gmail.com",
            password="app_password",
            use_oauth=False  # Explicitly disable OAuth for this test
        )
        
        self.assertEqual(checker.email, "test@gmail.com")
        self.assertEqual(checker.password, "app_password")
        self.assertEqual(checker.imap_server, "imap.gmail.com")
        self.assertFalse(checker.use_oauth)
    
    @patch.dict(os.environ, {'DCP_EMAIL': 'env@gmail.com', 'DCP_EMAIL_PASSWORD': 'env_pass'})
    def test_initialization_with_env_vars(self):
        """Test that email checker can use credentials from environment."""
        from selenium_subscriber import DailyCodingProblemEmailChecker
        
        checker = DailyCodingProblemEmailChecker(use_oauth=False)
        
        self.assertEqual(checker.email, "env@gmail.com")
        self.assertEqual(checker.password, "env_pass")
        self.assertFalse(checker.use_oauth)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_email_raises_error(self):
        """Test that initialization fails without email."""
        from selenium_subscriber import DailyCodingProblemEmailChecker
        
        with self.assertRaises(ValueError) as context:
            checker = DailyCodingProblemEmailChecker(password="test", use_oauth=False)
        
        self.assertIn("Email must be provided", str(context.exception))
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_password_raises_error_when_not_oauth(self):
        """Test that initialization fails without password when not using OAuth."""
        from selenium_subscriber import DailyCodingProblemEmailChecker
        
        with self.assertRaises(ValueError) as context:
            checker = DailyCodingProblemEmailChecker(email="test@example.com", use_oauth=False)
        
        self.assertIn("Password must be provided", str(context.exception))
    
    def test_oauth_enabled_for_gmail(self):
        """Test that OAuth is auto-enabled for Gmail when available."""
        from selenium_subscriber import DailyCodingProblemEmailChecker, OAUTH_AVAILABLE
        
        if OAUTH_AVAILABLE:
            # OAuth should be auto-enabled for Gmail when libraries are available
            checker = DailyCodingProblemEmailChecker(email="test@gmail.com")
            self.assertTrue(checker.use_oauth)
    
    def test_auto_detect_imap_server(self):
        """Test IMAP server auto-detection for various email providers."""
        from selenium_subscriber import DailyCodingProblemEmailChecker
        
        test_cases = [
            ("test@gmail.com", "imap.gmail.com"),
            ("test@yahoo.com", "imap.mail.yahoo.com"),
            ("test@outlook.com", "imap-mail.outlook.com"),
            ("test@hotmail.com", "imap-mail.outlook.com"),
        ]
        
        for email, expected_server in test_cases:
            checker = DailyCodingProblemEmailChecker(
                email=email,
                password="test_password",
                use_oauth=False
            )
            self.assertEqual(checker.imap_server, expected_server)


if __name__ == '__main__':
    # Add the parent directory to the path so we can import selenium_subscriber
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    unittest.main()

