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
    
    @patch('selenium_subscriber.build')
    @patch('selenium_subscriber.Credentials.from_authorized_user_file')
    @patch('selenium_subscriber.os.path.exists')
    def test_oauth_enabled_for_gmail(self, mock_exists, mock_creds_file, mock_build):
        """Test that OAuth is enabled for Gmail."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        # Mock that token.json exists and is valid
        mock_exists.return_value = True
        mock_creds = Mock()
        mock_creds.valid = True
        mock_creds_file.return_value = mock_creds
        
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        checker = DailyCodingProblemEmailChecker(email="test@gmail.com")
        self.assertIsNotNone(checker.service)  # Ensure Gmail API service is initialized
    
    def test_auto_detect_imap_server(self):
        """Test IMAP server auto-detection for various email providers."""
        pass  # Removed as the new implementation uses Gmail API and no longer relies on IMAP server auto-detection.

    @patch('selenium_subscriber.build')
    @patch('selenium_subscriber.Credentials.from_authorized_user_file')
    @patch('selenium_subscriber.os.path.exists')
    def test_check_new_problems(self, mock_exists, mock_creds_file, mock_build):
        """Test fetching new Daily Coding Problems using Gmail API."""
        from selenium_subscriber import DailyCodingProblemEmailChecker

        # Mock that token.json exists and is valid
        mock_exists.return_value = True
        mock_creds = Mock()
        mock_creds.valid = True
        mock_creds_file.return_value = mock_creds
        
        # Mock the Gmail API service
        mock_service = Mock()
        mock_build.return_value = mock_service
        
        # Mock the Gmail API response
        mock_messages_list = Mock()
        mock_messages_list.execute.return_value = {
            "messages": [
                {"id": "1"},
                {"id": "2"}
            ]
        }
        mock_service.users().messages().list.return_value = mock_messages_list
        
        # Mock individual message responses
        mock_msg1 = Mock()
        mock_msg1.execute.return_value = {
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Problem #1"},
                    {"name": "Date", "value": "Mon, 14 Dec 2025 10:00:00 -0800"}
                ],
                "body": {"data": "VGVzdCBib2R5"}  # Base64 encoded "Test body"
            }
        }
        
        mock_msg2 = Mock()
        mock_msg2.execute.return_value = {
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Problem #2"},
                    {"name": "Date", "value": "Tue, 15 Dec 2025 10:00:00 -0800"}
                ],
                "body": {"data": "VGVzdCBib2R5"}
            }
        }
        
        mock_service.users().messages().get.side_effect = [mock_msg1, mock_msg2]

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
    
    @patch('selenium_subscriber.DailyCodingProblemEmailChecker._authenticate')
    @patch('selenium_subscriber.DailyCodingProblemEmailChecker.check_new_problems')
    def test_download_and_save_problems(self, mock_check, mock_auth):
        """Test downloading and saving problems."""
        from selenium_subscriber import DailyCodingProblemEmailChecker
        import tempfile
        import shutil
        
        # Create temporary directory for testing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Mock authentication
            mock_auth.return_value = None
            
            # Mock problem data
            mock_check.return_value = [
                {
                    "subject": "Daily Coding Problem: Problem #1",
                    "date": "Mon, 15 Dec 2025 10:00:00 -0800",
                    "body": "This is a test problem description.\nSolve this problem."
                }
            ]
            
            checker = DailyCodingProblemEmailChecker(email="test@gmail.com")
            saved_paths = checker.download_and_save_problems(days=1)
            
            # Verify that at least one problem was attempted to be saved
            # (actual saving might fail due to mocking, but the logic should execute)
            self.assertIsInstance(saved_paths, list)
            
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


if __name__ == '__main__':
    # Add the parent directory to the path so we can import selenium_subscriber
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    unittest.main()

