#!/usr/bin/env python3
"""
CLI tool to add a new Daily Coding Problem from email or text.

Usage:
    # From email file
    python add_problem.py --email path/to/email.eml
    
    # From text file
    python add_problem.py --text path/to/problem.txt
    
    # From clipboard/stdin
    python add_problem.py --stdin
    
    # Specify custom date
    python add_problem.py --text problem.txt --date 2024-03-15
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from email_parser import DailyProblemParser, ProblemTemplateGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Add a new Daily Coding Problem from email or text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --email daily_problem.eml
  %(prog)s --text problem.txt --date 2024-03-15
  %(prog)s --stdin < problem.txt
        """
    )
    
    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--email',
        type=str,
        help='Path to email file (.eml format)'
    )
    input_group.add_argument(
        '--text',
        type=str,
        help='Path to text file containing problem description'
    )
    input_group.add_argument(
        '--stdin',
        action='store_true',
        help='Read problem description from stdin'
    )
    
    # Optional arguments
    parser.add_argument(
        '--date',
        type=str,
        help='Date for the problem in YYYY-MM-DD format (default: today)'
    )
    parser.add_argument(
        '--problems-dir',
        type=str,
        default='problems',
        help='Path to problems directory (default: ./problems)'
    )
    
    args = parser.parse_args()
    
    # Initialize parser and generator
    problem_parser = DailyProblemParser()
    template_gen = ProblemTemplateGenerator(base_path=args.problems_dir)
    
    # Parse input
    try:
        if args.email:
            print(f"Parsing email file: {args.email}")
            problem_data = problem_parser.parse_email_file(args.email)
        elif args.text:
            print(f"Parsing text file: {args.text}")
            with open(args.text, 'r', encoding='utf-8') as f:
                text = f.read()
            problem_data = problem_parser.parse_text(text)
        else:  # stdin
            print("Reading from stdin...")
            text = sys.stdin.read()
            problem_data = problem_parser.parse_text(text)
        
        # Display parsed information
        print("\n" + "="*60)
        print("PARSED PROBLEM INFORMATION")
        print("="*60)
        if problem_data.get('company'):
            print(f"Company: {problem_data['company']}")
        if problem_data.get('difficulty'):
            print(f"Difficulty: {problem_data['difficulty']}")
        print(f"\nProblem Description:")
        print("-"*60)
        print(problem_data['problem_text'][:500])
        if len(problem_data['problem_text']) > 500:
            print("... (truncated)")
        print("-"*60)
        
        # Parse date
        date_obj = None
        if args.date:
            try:
                date_obj = datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD format.")
                return 1
        
        # Generate template
        print(f"\nGenerating problem template...")
        problem_dir = template_gen.generate(problem_data, date=date_obj)
        
        print(f"\n✓ Successfully created problem at: {problem_dir}")
        print("\nCreated files:")
        print(f"  - {problem_dir}/readme.md")
        print(f"  - {problem_dir}/python/main.py")
        print(f"  - {problem_dir}/python/test.py")
        
        print("\nNext steps:")
        print(f"  1. Review the problem description in readme.md")
        print(f"  2. Implement the solution in python/main.py")
        print(f"  3. Add test cases in python/test.py")
        print(f"  4. Run tests with: pytest {problem_dir}/python/test.py")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except FileExistsError as e:
        print(f"Error: {e}")
        print("The problem directory for this date already exists.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
