#!/usr/bin/env python3
"""
Test script for selenium_subscriber.py

This tests the basic functionality of the DailyCodingProblemSubscriber class
without actually making requests to the website.
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


if __name__ == '__main__':
    # Add the parent directory to the path so we can import selenium_subscriber
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    unittest.main()
