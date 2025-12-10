#!/usr/bin/env python3
"""
Sync script for Daily Coding Problem repository.

This script helps track and manage problems from dailycodingproblem.com.
It provides tools to:
- List all problems in the repository with their DCP numbers (if known)
- Add DCP problem numbers to existing solutions
- Check which problems are missing DCP attribution
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re

try:
    import requests
    from bs4 import BeautifulSoup
    FETCH_AVAILABLE = True
except ImportError:
    FETCH_AVAILABLE = False

# Problem tracking data - maps directory names to DCP problem numbers
PROBLEM_TRACKING_FILE = "problem_tracking.json"

class ProblemSync:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path(__file__).parent
        self.problems_dir = self.repo_root / "problems"
        self.tracking_file = self.repo_root / PROBLEM_TRACKING_FILE
        self.tracking_data = self._load_tracking_data()
    
    def _load_tracking_data(self) -> Dict:
        """Load problem tracking data from JSON file."""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: Corrupted tracking file {PROBLEM_TRACKING_FILE}")
                print(f"Details: {e}")
                print("Run 'python sync_problems.py init' to recreate the file")
                return {"problems": {}}
        return {"problems": {}}
    
    def _save_tracking_data(self):
        """Save problem tracking data to JSON file."""
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.tracking_data, f, indent=2)
        print(f"✓ Saved tracking data to {PROBLEM_TRACKING_FILE}")
    
    def _get_problem_directories(self) -> List[str]:
        """Get sorted list of problem directory names."""
        if not self.problems_dir.exists():
            return []
        return sorted([d.name for d in self.problems_dir.iterdir() if d.is_dir()])
    
    def list_problems(self):
        """List all problems in the repository."""
        print("\n=== Daily Coding Problem Repository - Problem List ===\n")
        
        problem_dirs = self._get_problem_directories()
        
        if not problem_dirs:
            print("No problems found in repository")
            return
        
        print(f"Found {len(problem_dirs)} problem(s):\n")
        
        for dir_name in problem_dirs:
            problem_dir = self.problems_dir / dir_name
            readme_path = problem_dir / "readme.md"
            
            # Get DCP number if tracked
            dcp_number = self.tracking_data["problems"].get(dir_name, {}).get("dcp_number")
            
            # Try to read problem title and company from readme
            title = "Unknown"
            company = None
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Get title from first line
                    if lines and lines[0].startswith('#'):
                        title = lines[0].lstrip('#').strip()
                    
                    # Check for company attribution
                    if "Asked by:" in content:
                        for line in lines:
                            if "Asked by:" in line:
                                company = line.split("Asked by:")[-1].strip().rstrip('*')
                                break
            
            # Format output
            dcp_str = f"DCP #{dcp_number}" if dcp_number else "DCP #???"
            company_str = f" (by {company})" if company else ""
            
            print(f"  [{dcp_str}] {dir_name} - {title}{company_str}")
        
        print(f"\nTracking file: {PROBLEM_TRACKING_FILE}")
        print("Use 'sync_problems.py add <directory> <dcp_number>' to add DCP numbers")
    
    def add_dcp_number(self, directory: str, dcp_number: int):
        """Add DCP problem number to a directory."""
        problem_path = self.problems_dir / directory
        
        if not problem_path.exists():
            print(f"✗ Error: Directory '{directory}' not found in problems/")
            return False
        
        if dcp_number <= 0:
            print(f"✗ Error: DCP number must be positive, got {dcp_number}")
            return False
        
        # Update tracking data
        if directory not in self.tracking_data["problems"]:
            self.tracking_data["problems"][directory] = {}
        
        self.tracking_data["problems"][directory]["dcp_number"] = dcp_number
        self.tracking_data["problems"][directory]["notes"] = f"DCP #{dcp_number} identified"
        self._save_tracking_data()
        
        print(f"✓ Added DCP #{dcp_number} to {directory}")
        return True
    
    def _is_untracked(self, dir_name: str) -> bool:
        """Check if a problem directory is missing DCP number."""
        if dir_name not in self.tracking_data["problems"]:
            return True
        if "dcp_number" not in self.tracking_data["problems"][dir_name]:
            return True
        if self.tracking_data["problems"][dir_name]["dcp_number"] is None:
            return True
        return False
    
    def show_untracked(self):
        """Show problems without DCP numbers."""
        print("\n=== Problems Missing DCP Numbers ===\n")
        
        problem_dirs = self._get_problem_directories()
        untracked = [dir_name for dir_name in problem_dirs if self._is_untracked(dir_name)]
        
        if not untracked:
            print("✓ All problems have DCP numbers assigned!")
        else:
            print(f"Found {len(untracked)} problem(s) without DCP numbers:\n")
            for dir_name in untracked:
                print(f"  - {dir_name}")
            print(f"\nAdd DCP numbers with: python sync_problems.py add <directory> <number>")
    
    def init_tracking(self):
        """Initialize tracking file with current problems."""
        problem_dirs = self._get_problem_directories()
        
        print(f"\nInitializing tracking for {len(problem_dirs)} problem(s)...")
        
        for dir_name in problem_dirs:
            if dir_name not in self.tracking_data["problems"]:
                self.tracking_data["problems"][dir_name] = {
                    "dcp_number": None,
                    "notes": "DCP number not yet identified"
                }
        
        self._save_tracking_data()
        print("✓ Tracking initialized. Use 'list' to see all problems.")
    
    def fetch_problem(self, dcp_number: int, create_dir: bool = True):
        """Fetch a problem from Daily Coding Problem website.
        
        Args:
            dcp_number: The DCP problem number to fetch
            create_dir: If True, create directory and files for the problem
        """
        if not FETCH_AVAILABLE:
            print("✗ Error: BeautifulSoup and requests libraries are required for fetching")
            print("Install with: pip install beautifulsoup4 requests")
            return False
        
        if dcp_number <= 0:
            print(f"✗ Error: DCP number must be positive, got {dcp_number}")
            return False
        
        print(f"\n🔍 Fetching DCP #{dcp_number} from dailycodingproblem.com...")
        
        try:
            # Note: dailycodingproblem.com requires login for full access
            # This is a basic implementation that may need adjustment based on site structure
            url = f"https://www.dailycodingproblem.com/problem/{dcp_number}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                print(f"✗ Error: Problem #{dcp_number} not found on website")
                return False
            elif response.status_code != 200:
                print(f"✗ Error: Failed to fetch problem (status code: {response.status_code})")
                print("Note: Daily Coding Problem requires a subscription for full access")
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract problem information
            # Note: This may need adjustment based on actual site structure
            problem_title = None
            problem_description = None
            company = None
            
            # Look for title
            title_elem = soup.find('h1') or soup.find('h2', class_='problem-title')
            if title_elem:
                problem_title = title_elem.get_text(strip=True)
            
            # Look for company/description
            content_div = soup.find('div', class_='problem-content') or soup.find('div', class_='content')
            if content_div:
                problem_description = content_div.get_text(strip=True)
                # Try to extract company
                if "This problem was asked by" in problem_description:
                    match = re.search(r'This problem was asked by ([^.]+)', problem_description)
                    if match:
                        company = match.group(1).strip()
            
            if not problem_title and not problem_description:
                print(f"⚠️  Warning: Could not extract problem details (may require login)")
                print(f"📋 Problem exists at: {url}")
                if create_dir:
                    print("\nYou can manually:")
                    print(f"  1. Visit {url} and copy the problem")
                    print(f"  2. Create directory: mkdir -p problems/{datetime.now().strftime('%Y_%m%d')}")
                    print(f"  3. Add readme.md with the problem description")
                    print(f"  4. Run: python sync_problems.py add <directory> {dcp_number}")
                return False
            
            print(f"✓ Found problem: {problem_title or 'Problem #' + str(dcp_number)}")
            if company:
                print(f"  Asked by: {company}")
            
            if create_dir:
                # Create directory structure
                date_str = datetime.now().strftime('%Y_%m%d')
                problem_dir = self.problems_dir / date_str
                python_dir = problem_dir / "python"
                
                # Check if directory exists
                counter = 1
                original_date_str = date_str
                while problem_dir.exists():
                    date_str = f"{original_date_str}_{counter}"
                    problem_dir = self.problems_dir / date_str
                    python_dir = problem_dir / "python"
                    counter += 1
                
                try:
                    python_dir.mkdir(parents=True, exist_ok=True)
                    print(f"✓ Created directory: {problem_dir.name}")
                    
                    # Create readme.md
                    readme_path = problem_dir / "readme.md"
                    readme_content = f"# {problem_title or f'Problem #{dcp_number}'}\n\n"
                    readme_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
                    if company:
                        readme_content += f"**Asked by:** {company}\n"
                    readme_content += f"**DCP #:** {dcp_number}\n\n"
                    readme_content += "## Problem Description\n\n"
                    if problem_description:
                        readme_content += problem_description + "\n\n"
                    else:
                        readme_content += "TODO: Add problem description\n\n"
                    readme_content += "## Examples\n\nTODO: Add examples\n"
                    
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(readme_content)
                    print(f"✓ Created {readme_path.relative_to(self.repo_root)}")
                    
                    # Create main.py template
                    main_path = python_dir / "main.py"
                    main_content = "def solution(input):\n    # TODO: Implement solution\n    pass\n"
                    with open(main_path, 'w', encoding='utf-8') as f:
                        f.write(main_content)
                    print(f"✓ Created {main_path.relative_to(self.repo_root)}")
                    
                    # Create test.py template
                    test_path = python_dir / "test.py"
                    test_content = "from main import solution\n\n"
                    test_content += "def test_answer():\n"
                    test_content += "    # TODO: Add test cases\n"
                    test_content += "    assert solution(None) is not None\n"
                    with open(test_path, 'w', encoding='utf-8') as f:
                        f.write(test_content)
                    print(f"✓ Created {test_path.relative_to(self.repo_root)}")
                    
                    # Add to tracking
                    self.tracking_data["problems"][problem_dir.name] = {
                        "dcp_number": dcp_number,
                        "notes": f"DCP #{dcp_number} identified - fetched from website"
                    }
                    self._save_tracking_data()
                    
                    print(f"\n✓ Successfully created problem structure for DCP #{dcp_number}")
                    print(f"  Directory: problems/{problem_dir.name}/")
                    print(f"  Next steps:")
                    print(f"    1. Review and complete readme.md")
                    print(f"    2. Implement solution in python/main.py")
                    print(f"    3. Add test cases in python/test.py")
                    
                    return True
                    
                except Exception as e:
                    print(f"✗ Error creating directory structure: {e}")
                    return False
            
            return True
            
        except requests.exceptions.Timeout:
            print("✗ Error: Request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching problem: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False


def main():
    syncer = ProblemSync()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sync_problems.py list              - List all problems")
        print("  python sync_problems.py add <dir> <num>   - Add DCP number to problem")
        print("  python sync_problems.py untracked         - Show problems without DCP numbers")
        print("  python sync_problems.py init              - Initialize tracking file")
        if FETCH_AVAILABLE:
            print("  python sync_problems.py fetch <num>       - Fetch problem from website")
        print("\nExamples:")
        print("  python sync_problems.py list")
        print("  python sync_problems.py add 2023_1204 387")
        print("  python sync_problems.py untracked")
        if FETCH_AVAILABLE:
            print("  python sync_problems.py fetch 500")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        syncer.list_problems()
    elif command == "add":
        if len(sys.argv) != 4:
            print("Error: add command requires <directory> and <dcp_number>")
            print("Example: python sync_problems.py add 2023_1204 387")
            sys.exit(1)
        directory = sys.argv[2]
        try:
            dcp_number = int(sys.argv[3])
        except ValueError:
            print(f"Error: DCP number must be an integer, got '{sys.argv[3]}'")
            sys.exit(1)
        syncer.add_dcp_number(directory, dcp_number)
    elif command == "fetch":
        if not FETCH_AVAILABLE:
            print("Error: fetch command requires beautifulsoup4 and requests")
            print("Install with: pip install beautifulsoup4 requests")
            sys.exit(1)
        if len(sys.argv) != 3:
            print("Error: fetch command requires <dcp_number>")
            print("Example: python sync_problems.py fetch 500")
            sys.exit(1)
        try:
            dcp_number = int(sys.argv[2])
        except ValueError:
            print(f"Error: DCP number must be an integer, got '{sys.argv[2]}'")
            sys.exit(1)
        syncer.fetch_problem(dcp_number, create_dir=True)
    elif command == "untracked":
        syncer.show_untracked()
    elif command == "init":
        syncer.init_tracking()
    else:
        print(f"Unknown command: {command}")
        available_cmds = "list, add, untracked, init"
        if FETCH_AVAILABLE:
            available_cmds += ", fetch"
        print(f"Available commands: {available_cmds}")
        sys.exit(1)


if __name__ == "__main__":
    main()
