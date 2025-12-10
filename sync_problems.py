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
from pathlib import Path
from typing import Dict, List, Optional

# Problem tracking data - maps directory names to DCP problem numbers
PROBLEM_TRACKING_FILE = "problem_tracking.json"

class ProblemSync:
    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent
        self.problems_dir = self.repo_root / "problems"
        self.tracking_file = self.repo_root / PROBLEM_TRACKING_FILE
        self.tracking_data = self._load_tracking_data()
    
    def _load_tracking_data(self) -> Dict:
        """Load problem tracking data from JSON file."""
        if self.tracking_file.exists():
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        return {"problems": {}}
    
    def _save_tracking_data(self):
        """Save problem tracking data to JSON file."""
        with open(self.tracking_file, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
        print(f"✓ Saved tracking data to {PROBLEM_TRACKING_FILE}")
    
    def list_problems(self):
        """List all problems in the repository."""
        print("\n=== Daily Coding Problem Repository - Problem List ===\n")
        
        if not self.problems_dir.exists():
            print("Error: problems/ directory not found")
            return
        
        # Get all problem directories
        problem_dirs = sorted([d for d in self.problems_dir.iterdir() if d.is_dir()])
        
        if not problem_dirs:
            print("No problems found in repository")
            return
        
        print(f"Found {len(problem_dirs)} problem(s):\n")
        
        for problem_dir in problem_dirs:
            dir_name = problem_dir.name
            readme_path = problem_dir / "readme.md"
            
            # Get DCP number if tracked
            dcp_number = self.tracking_data["problems"].get(dir_name, {}).get("dcp_number")
            
            # Try to read problem title from readme
            title = "Unknown"
            company = None
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        title = first_line.lstrip('#').strip()
                    
                    # Check for company attribution
                    content = f.read()
                    if "Asked by:" in content:
                        for line in content.split('\n'):
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
        
        problem_dirs = sorted([d.name for d in self.problems_dir.iterdir() if d.is_dir()])
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
        problem_dirs = sorted([d.name for d in self.problems_dir.iterdir() if d.is_dir()])
        
        print(f"\nInitializing tracking for {len(problem_dirs)} problem(s)...")
        
        for dir_name in problem_dirs:
            if dir_name not in self.tracking_data["problems"]:
                self.tracking_data["problems"][dir_name] = {
                    "dcp_number": None,
                    "notes": "DCP number not yet identified"
                }
        
        self._save_tracking_data()
        print("✓ Tracking initialized. Use 'list' to see all problems.")


def main():
    import sys
    
    syncer = ProblemSync()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sync_problems.py list              - List all problems")
        print("  python sync_problems.py add <dir> <num>   - Add DCP number to problem")
        print("  python sync_problems.py untracked         - Show problems without DCP numbers")
        print("  python sync_problems.py init              - Initialize tracking file")
        print("\nExamples:")
        print("  python sync_problems.py list")
        print("  python sync_problems.py add 2023_1204 387")
        print("  python sync_problems.py untracked")
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
    elif command == "untracked":
        syncer.show_untracked()
    elif command == "init":
        syncer.init_tracking()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: list, add, untracked, init")
        sys.exit(1)


if __name__ == "__main__":
    main()
