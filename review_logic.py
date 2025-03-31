#!/usr/bin/env python3
"""
Automated code review logic for identifying common code issues.
This module analyzes Python code for various issues related to quality,
security, and performance.
"""

import ast
import re
import os
import sys
from typing import Dict, List, Tuple, Set, Optional


class CodeReviewAssistant:
    """Main class for code review assistant functionality."""
    
    def __init__(self, template_dir: str = "review_templates"):
        """Initialize the code review assistant with template directory.
        
        Args:
            template_dir: Directory containing review templates
        """
        self.template_dir = template_dir
        self.issues_found: Dict[str, List[Dict]] = {
            "general": [],
            "security": [],
            "performance": []
        }
    
    def load_template(self, template_type: str) -> str:
        """Load a review template from file.
        
        Args:
            template_type: Type of template to load (general, security, performance)
            
        Returns:
            The template content as a string
        """
        template_path = os.path.join(self.template_dir, f"{template_type}.md")
        try:
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Template {template_path} not found")
            return ""
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a Python file for code issues.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            Dictionary containing all issues found
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return self.issues_found
        
        # Reset issues
        self.issues_found = {
            "general": [],
            "security": [],
            "performance": []
        }
        
        # Run different analyzers
        self._analyze_general_issues(code, file_path)
        self._analyze_security_issues(code, file_path)
        self._analyze_performance_issues(code, file_path)
        
        return self.issues_found
    
    def _analyze_general_issues(self, code: str, file_path: str) -> None:
        """Analyze code for general quality issues.
        
        Args:
            code: Source code as string
            file_path: Path to the source file
        """
        # Check for commented out code
        commented_code_pattern = re.compile(r'^\s*#\s*(def|class|if|for|while|return)\b', re.MULTILINE)
        commented_code_matches = commented_code_pattern.finditer(code)
        for match in commented_code_matches:
            line_number = code[:match.start()].count('\n') + 1
            self.issues_found["general"].append({
                "type": "commented_code",
                "message": "Commented out code should be removed",
                "line": line_number,
                "severity": "minor"
            })
        
        # Check for inconsistent naming conventions
        try:
            parsed = ast.parse(code)
            for node in ast.walk(parsed):
                if isinstance(node, ast.FunctionDef):
                    # Check if function names follow snake_case
                    if not re.match(r'^[a-z][a-z0-9_]*$', node.name):
                        self.issues_found["general"].append({
                            "type": "naming_convention",
                            "message": f"Function name '{node.name}' doesn't follow snake_case convention",
                            "line": node.lineno,
                            "severity": "minor"
                        })
                        
                elif isinstance(node, ast.ClassDef):
                    # Check if class names follow PascalCase
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                        self.issues_found["general"].append({
                            "type": "naming_convention",
                            "message": f"Class name '{node.name}' doesn't follow PascalCase convention",
                            "line": node.lineno,
                            "severity": "minor"
                        })
        except SyntaxError as e:
            self.issues_found["general"].append({
                "type": "syntax_error",
                "message": f"Syntax error: {str(e)}",
                "line": e.lineno,
                "severity": "critical"
            })
    
    def _analyze_security_issues(self, code: str, file_path: str) -> None:
        """Analyze code for security issues.
        
        Args:
            code: Source code as string
            file_path: Path to the source file
        """
        # Check for hardcoded credentials
        password_pattern = re.compile(
            r'(?:password|passwd|pwd|secret|key|token|auth)(?:\s*=\s*)(\'[^\']+\'|\"[^\"]+\")',
            re.IGNORECASE
        )
        password_matches = password_pattern.finditer(code)
        for match in password_matches:
            line_number = code[:match.start()].count('\n') + 1
            self.issues_found["security"].append({
                "type": "hardcoded_credentials",
                "message": "Hardcoded credentials detected",
                "line": line_number,
                "severity": "critical"
            })
        
        # Check for SQL injection vulnerabilities
        sql_pattern = re.compile(r'f["\'](?:\s*)(?:SELECT|INSERT|UPDATE|DELETE|DROP).*?\{', re.IGNORECASE)
        sql_matches = sql_pattern.finditer(code)
        for match in sql_matches:
            line_number = code[:match.start()].count('\n') + 1
            self.issues_found["security"].append({
                "type": "sql_injection",
                "message": "Potential SQL injection vulnerability detected",
                "line": line_number,
                "severity": "critical"
            })
    
    def _analyze_performance_issues(self, code: str, file_path: str) -> None:
        """Analyze code for performance issues.
        
        Args:
            code: Source code as string
            file_path: Path to the source file
        """
        # Check for nested loops (potential O(n²) complexity)
        try:
            parsed = ast.parse(code)
            for node in ast.walk(parsed):
                if isinstance(node, ast.For):
                    for child in ast.walk(node):
                        if isinstance(child, ast.For) and child is not node:
                            self.issues_found["performance"].append({
                                "type": "nested_loops",
                                "message": "Nested loops detected (potential O(n²) complexity)",
                                "line": node.lineno,
                                "severity": "moderate"
                            })
                            break
        except SyntaxError:
            # Already reported in general issues
            pass
    
    def generate_review(self, issues: Dict, template_type: str = "general") -> str:
        """Generate a code review based on template and issues found.
        
        Args:
            issues: Dictionary of issues found
            template_type: Type of template to use
            
        Returns:
            Formatted review as string
        """
        template = self.load_template(template_type)
        if not template:
            return "No template found"
        
        # Add issue details to the review
        review = template + "\n\n## Issues Found\n\n"
        
        if template_type in issues and issues[template_type]:
            for issue in issues[template_type]:
                review += f"- **{issue['type']}** (Line {issue['line']}, {issue['severity']}): {issue['message']}\n"
        else:
            review += "No issues found for this category.\n"
        
        return review


def main():
    if len(sys.argv) < 2:
        print("Usage: python review_logic.py <file_to_review>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    reviewer = CodeReviewAssistant()
    issues = reviewer.analyze_file(file_path)
    
    # Generate reviews
    for template_type in ["general", "security", "performance"]:
        review = reviewer.generate_review(issues, template_type)
        print(f"\n{'=' * 50}\n{template_type.upper()} REVIEW\n{'=' * 50}\n")
        print(review)


if __name__ == "__main__":
    main()