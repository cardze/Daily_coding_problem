"""Tests for email_parser module."""

import pytest
from pathlib import Path
import tempfile
import shutil
from email_parser import DailyProblemParser, ProblemTemplateGenerator
from datetime import datetime


class TestDailyProblemParser:
    """Tests for DailyProblemParser class."""
    
    def test_parse_text_basic(self):
        """Test parsing a basic problem text."""
        parser = DailyProblemParser()
        text = """This problem was asked by Google.
        
Given an array of integers, find the maximum sum of any contiguous subarray.

For example, given [34, -50, 42, 14, -5, 86], return 137 (sum of [42, 14, -5, 86]).
"""
        result = parser.parse_text(text)
        
        assert 'problem_text' in result
        assert 'company' in result
        assert 'difficulty' in result
        assert result['company'] == 'Google'
        assert 'array of integers' in result['problem_text']
    
    def test_parse_text_no_company(self):
        """Test parsing text without company information."""
        parser = DailyProblemParser()
        text = """Given a list of numbers, return the largest number.

For example, given [3, 5, 1, 9, 2], return 9.
"""
        result = parser.parse_text(text)
        
        assert result['company'] is None
        assert 'Given a list of numbers' in result['problem_text']
    
    def test_extract_company(self):
        """Test company extraction."""
        parser = DailyProblemParser()
        
        text1 = "This problem was asked by Google."
        assert parser._extract_company(text1) == "Google"
        
        text2 = "This problem was recently asked by Facebook."
        assert parser._extract_company(text2) == "Facebook"
        
        text3 = "Asked by Amazon."
        assert parser._extract_company(text3) == "Amazon"
        
        text4 = "No company here."
        assert parser._extract_company(text4) is None
    
    def test_extract_difficulty(self):
        """Test difficulty extraction."""
        parser = DailyProblemParser()
        
        assert parser._extract_difficulty("This is a hard problem.") == "Hard"
        assert parser._extract_difficulty("This is medium difficulty.") == "Medium"
        assert parser._extract_difficulty("This is an easy problem.") == "Easy"
        assert parser._extract_difficulty("No difficulty mentioned.") is None
    
    def test_clean_text(self):
        """Test text cleaning."""
        parser = DailyProblemParser()
        
        text = "Too   many    spaces\n\n\n\nand lines"
        cleaned = parser._clean_text(text)
        
        assert "   " not in cleaned
        assert "\n\n\n" not in cleaned


class TestProblemTemplateGenerator:
    """Tests for ProblemTemplateGenerator class."""
    
    def test_generate_creates_directory(self):
        """Test that generate creates the correct directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'Test problem',
                'company': 'TestCo',
                'difficulty': 'Easy'
            }
            
            date = datetime(2024, 3, 15)
            result_path = generator.generate(problem_data, date=date)
            
            expected_dir = Path(tmpdir) / "2024_0315"
            assert expected_dir.exists()
            assert (expected_dir / "readme.md").exists()
            assert (expected_dir / "python").exists()
            assert (expected_dir / "python" / "main.py").exists()
            assert (expected_dir / "python" / "test.py").exists()
    
    def test_generate_readme_content(self):
        """Test that readme.md contains correct content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'This is a test problem.',
                'company': 'TestCo',
                'difficulty': 'Medium'
            }
            
            generator.generate(problem_data, date=datetime(2024, 3, 15))
            
            readme_path = Path(tmpdir) / "2024_0315" / "readme.md"
            content = readme_path.read_text()
            
            assert "TestCo" in content
            assert "Medium" in content
            assert "This is a test problem." in content
    
    def test_generate_main_py_content(self):
        """Test that main.py has correct template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'Test',
                'company': None,
                'difficulty': None
            }
            
            generator.generate(problem_data, date=datetime(2024, 3, 15))
            
            main_path = Path(tmpdir) / "2024_0315" / "python" / "main.py"
            content = main_path.read_text()
            
            assert "def solution()" in content
            assert "TODO" in content
            assert "pass" in content
    
    def test_generate_test_py_content(self):
        """Test that test.py has correct template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'Test',
                'company': None,
                'difficulty': None
            }
            
            generator.generate(problem_data, date=datetime(2024, 3, 15))
            
            test_path = Path(tmpdir) / "2024_0315" / "python" / "test.py"
            content = test_path.read_text()
            
            assert "from main import *" in content
            assert "def test_answer()" in content
            assert "TODO" in content
    
    def test_generate_raises_on_existing_directory(self):
        """Test that generate raises error if directory exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'Test',
                'company': None,
                'difficulty': None
            }
            
            date = datetime(2024, 3, 15)
            generator.generate(problem_data, date=date)
            
            # Try to generate again with same date
            with pytest.raises(FileExistsError):
                generator.generate(problem_data, date=date)
    
    def test_generate_with_default_date(self):
        """Test that generate uses current date when none provided."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ProblemTemplateGenerator(base_path=tmpdir)
            problem_data = {
                'problem_text': 'Test',
                'company': None,
                'difficulty': None
            }
            
            result_path = generator.generate(problem_data)
            
            # Should create directory with today's date
            today = datetime.now().strftime('%Y_%m%d')
            expected_dir = Path(tmpdir) / today
            assert expected_dir.exists()
