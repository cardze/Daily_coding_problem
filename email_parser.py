"""Email parser for Daily Coding Problem emails.

This module parses emails from Daily Coding Problem and extracts
the problem description to create problem templates.
"""

import re
import email
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import os


class DailyProblemParser:
    """Parser for Daily Coding Problem emails."""
    
    def __init__(self):
        self.problem_text = None
        self.company = None
        self.difficulty = None
        
    def parse_email_file(self, email_path):
        """Parse an email file (.eml format).
        
        Args:
            email_path: Path to the .eml file
            
        Returns:
            dict: Parsed problem information
        """
        with open(email_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        
        return self.parse_email_message(msg)
    
    def parse_email_message(self, msg):
        """Parse an email message object.
        
        Args:
            msg: email.message.EmailMessage object
            
        Returns:
            dict: Parsed problem information with keys:
                - problem_text: str, the problem description
                - company: str or None, the company name if mentioned
                - difficulty: str or None, the difficulty level
        """
        # Extract body content
        body = self._get_email_body(msg)
        
        # Parse the problem
        return self.parse_text(body)
    
    def parse_text(self, text):
        """Parse problem text directly.
        
        Args:
            text: String containing the problem description
            
        Returns:
            dict: Parsed problem information
        """
        # Clean the text
        text = self._clean_text(text)
        
        # Extract problem description
        problem_text = self._extract_problem_text(text)
        
        # Extract metadata
        company = self._extract_company(text)
        difficulty = self._extract_difficulty(text)
        
        return {
            'problem_text': problem_text,
            'company': company,
            'difficulty': difficulty
        }
    
    def _get_email_body(self, msg):
        """Extract body from email message."""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif content_type == "text/html" and not body:
                    html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    body = self._html_to_text(html_content)
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
        return body
    
    def _html_to_text(self, html):
        """Convert HTML to plain text."""
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        return text
    
    def _clean_text(self, text):
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def _extract_problem_text(self, text):
        """Extract the problem description from the text.
        
        This looks for common patterns in Daily Coding Problem emails.
        """
        # Try to find the problem section
        # Common patterns: "Good morning!", "Here's your problem", etc.
        
        # Remove common header/footer patterns
        lines = text.split('\n')
        problem_lines = []
        in_problem = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip header lines
            if any(x in line_lower for x in ['good morning', 'good evening', 'unsubscribe', 
                                              'daily coding problem', 'upgrade to premium']):
                if not in_problem:
                    continue
                else:
                    # We've hit the footer
                    break
            
            # Start capturing when we see problem-related content
            if line.strip() and (in_problem or 
                                 any(x in line_lower for x in ['this problem was asked', 
                                                                'given', 'return', 'find',
                                                                'implement', 'write'])):
                in_problem = True
                problem_lines.append(line)
        
        problem_text = '\n'.join(problem_lines).strip()
        
        # If we didn't find a good problem, return the whole text
        if not problem_text or len(problem_text) < 50:
            problem_text = text
            
        return problem_text
    
    def _extract_company(self, text):
        """Extract company name if mentioned (e.g., 'This problem was asked by Google')."""
        patterns = [
            r'This problem was asked by ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'This problem was recently asked by ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'Asked by ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_difficulty(self, text):
        """Extract difficulty level if mentioned."""
        text_lower = text.lower()
        
        if 'hard' in text_lower:
            return 'Hard'
        elif 'medium' in text_lower:
            return 'Medium'
        elif 'easy' in text_lower:
            return 'Easy'
            
        return None


class ProblemTemplateGenerator:
    """Generate problem template files from parsed email."""
    
    def __init__(self, base_path=None):
        """Initialize generator.
        
        Args:
            base_path: Base path for problems directory. 
                      Defaults to ./problems relative to current directory.
        """
        if base_path is None:
            base_path = Path(__file__).parent / 'problems'
        self.base_path = Path(base_path)
    
    def generate(self, problem_data, date=None):
        """Generate problem template files.
        
        Args:
            problem_data: Dict with problem information from parser
            date: Date string in YYYY-MM-DD format, or datetime object.
                 If None, uses current date.
                 
        Returns:
            str: Path to the created problem directory
        """
        # Parse date
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        # Create directory name in YYYY_MMDD format
        dir_name = date.strftime('%Y_%m%d')
        problem_dir = self.base_path / dir_name
        
        # Check if directory already exists
        if problem_dir.exists():
            raise FileExistsError(f"Problem directory already exists: {problem_dir}")
        
        # Create directory structure
        problem_dir.mkdir(parents=True, exist_ok=True)
        python_dir = problem_dir / 'python'
        python_dir.mkdir(exist_ok=True)
        
        # Generate readme.md
        self._generate_readme(problem_dir, problem_data)
        
        # Generate main.py
        self._generate_main_py(python_dir)
        
        # Generate test.py
        self._generate_test_py(python_dir)
        
        return str(problem_dir)
    
    def _generate_readme(self, problem_dir, problem_data):
        """Generate readme.md file."""
        readme_path = problem_dir / 'readme.md'
        
        content = problem_data['problem_text']
        
        # Add metadata as comments if available
        if problem_data.get('company'):
            content = f"Asked by: {problem_data['company']}\n\n" + content
        if problem_data.get('difficulty'):
            content = f"Difficulty: {problem_data['difficulty']}\n\n" + content
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_main_py(self, python_dir):
        """Generate main.py template."""
        main_path = python_dir / 'main.py'
        
        template = '''def solution():
    """
    TODO: Implement solution here
    
    Args:
        Add your arguments here
        
    Returns:
        Add your return type here
    """
    pass
'''
        
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(template)
    
    def _generate_test_py(self, python_dir):
        """Generate test.py template."""
        test_path = python_dir / 'test.py'
        
        template = '''from main import *    

def test_answer():
    """
    TODO: Add test cases here
    
    Example:
    input_output = [
        {
            'input': {
                'arg1': value1,
                'arg2': value2
            },
            'output': expected_output
        }
    ]
    for i in input_output:
        assert solution(**i['input']) == i['output']
    """
    pass
'''
        
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(template)
