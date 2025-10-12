#!/usr/bin/env python3
"""
Dataview Query Tester

This script tests Dataview queries in dashboard files to ensure they are syntactically correct
and would work in Obsidian with the Dataview plugin.

Usage:
    python test_dataview_queries.py [options]

Options:
    --path PATH          Path to dashboard files (default: AI/001_Tools)
    --output FILE        Output file for results (default: dataview_test_report.txt)
    --verbose            Enable verbose output
"""

import os
import re
import sys
import argparse
from typing import List, Dict, Tuple
import logging
from datetime import datetime

class DataviewTester:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Results storage
        self.results = {
            'files_processed': 0,
            'queries_found': 0,
            'valid_queries': 0,
            'invalid_queries': 0,
            'errors': []
        }
    
    def extract_dataview_queries(self, content: str) -> List[Tuple[str, int, str]]:
        """
        Extract Dataview queries from markdown content.
        Returns list of tuples: (query, line_number, context)
        """
        queries = []
        lines = content.split('\n')
        
        in_dataview_block = False
        current_query = []
        start_line = 0
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```dataview'):
                in_dataview_block = True
                start_line = i
                current_query = []
            elif line.strip() == '```' and in_dataview_block:
                in_dataview_block = False
                if current_query:
                    query_text = '\n'.join(current_query)
                    context = f"Lines {start_line}-{i}"
                    queries.append((query_text, start_line, context))
                current_query = []
            elif in_dataview_block:
                current_query.append(line)
        
        return queries
    
    def validate_dataview_query(self, query: str) -> Dict[str, any]:
        """
        Validate a Dataview query for syntax and structure.
        Returns validation results.
        """
        result = {
            'query': query,
            'valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Basic syntax checks
        query_lower = query.lower().strip()
        
        # Check for basic Dataview commands
        valid_commands = ['list', 'table', 'task', 'calendar', 'from', 'where', 'sort', 'group by', 'limit']
        
        # Check if query starts with a valid command
        first_word = query_lower.split()[0] if query_lower else ''
        if first_word not in valid_commands:
            result['errors'].append(f"Query should start with a valid Dataview command: {valid_commands}")
            result['valid'] = False
        
        # Check for FROM clause
        if 'from' not in query_lower:
            result['warnings'].append("Query should include a FROM clause to specify data source")
        
        # Check for proper path formatting
        from_match = re.search(r'from\s+["\']([^"\']+)["\']', query_lower)
        if from_match:
            path = from_match.group(1)
            if not path.startswith('AI/'):
                result['warnings'].append(f"Path '{path}' should start with 'AI/' for consistency")
        
        # Check for tag usage
        if 'contains(tags' in query_lower:
            # Check if tag format is correct
            tag_matches = re.findall(r'contains\(tags,\s*["\']([^"\']+)["\']', query_lower)
            for tag in tag_matches:
                if not tag.startswith('AI/'):
                    result['warnings'].append(f"Tag '{tag}' should start with 'AI/' for consistency")
        
        # Check for SORT clause
        if 'sort' in query_lower:
            sort_match = re.search(r'sort\s+(\w+)', query_lower)
            if sort_match:
                sort_field = sort_match.group(1)
                if sort_field not in ['file.name', 'file.mtime', 'rating', 'pricing']:
                    result['suggestions'].append(f"Consider using standard sort fields: file.name, file.mtime, rating, pricing")
        
        # Check for LIMIT clause
        if 'limit' in query_lower:
            limit_match = re.search(r'limit\s+(\d+)', query_lower)
            if limit_match:
                limit_value = int(limit_match.group(1))
                if limit_value > 50:
                    result['warnings'].append(f"Large limit ({limit_value}) may impact performance")
        
        return result
    
    def test_file(self, file_path: str) -> Dict:
        """
        Test Dataview queries in a single file.
        Returns test results.
        """
        file_results = {
            'file': file_path,
            'queries': [],
            'total_queries': 0,
            'valid_queries': 0,
            'invalid_queries': 0,
            'has_issues': False
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            queries = self.extract_dataview_queries(content)
            file_results['total_queries'] = len(queries)
            
            for query, line_num, context in queries:
                validation_result = self.validate_dataview_query(query)
                validation_result['line_number'] = line_num
                validation_result['context'] = context
                
                file_results['queries'].append(validation_result)
                
                if validation_result['valid']:
                    file_results['valid_queries'] += 1
                else:
                    file_results['invalid_queries'] += 1
                    file_results['has_issues'] = True
            
            self.results['queries_found'] += len(queries)
            self.results['valid_queries'] += file_results['valid_queries']
            self.results['invalid_queries'] += file_results['invalid_queries']
        
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            file_results['has_issues'] = True
            self.results['errors'].append(f"Error in {file_path}: {e}")
        
        return file_results
    
    def test_directory(self, directory_path: str) -> List[Dict]:
        """
        Test Dataview queries in all markdown files in a directory.
        Returns list of file test results.
        """
        all_results = []
        
        if not os.path.exists(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return all_results
        
        markdown_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        self.logger.info(f"Found {len(markdown_files)} markdown files")
        
        for file_path in markdown_files:
            self.results['files_processed'] += 1
            file_results = self.test_file(file_path)
            all_results.append(file_results)
        
        return all_results
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Generate a comprehensive test report.
        Returns report as string and optionally saves to file.
        """
        report_lines = []
        report_lines.append("Dataview Query Test Report")
        report_lines.append("=" * 30)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall summary
        total_files = len(results)
        files_with_issues = sum(1 for r in results if r['has_issues'])
        total_queries = sum(r['total_queries'] for r in results)
        total_valid = sum(r['valid_queries'] for r in results)
        total_invalid = sum(r['invalid_queries'] for r in results)
        
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Files processed: {total_files}")
        report_lines.append(f"Files with issues: {files_with_issues}")
        report_lines.append(f"Total queries: {total_queries}")
        report_lines.append(f"Valid queries: {total_valid}")
        report_lines.append(f"Invalid queries: {total_invalid}")
        report_lines.append("")
        
        # Files with issues
        if files_with_issues > 0:
            report_lines.append("FILES WITH ISSUES")
            report_lines.append("-" * 20)
            
            for file_result in results:
                if file_result['has_issues']:
                    report_lines.append(f"\nFile: {file_result['file']}")
                    report_lines.append(f"  Total queries: {file_result['total_queries']}")
                    report_lines.append(f"  Valid queries: {file_result['valid_queries']}")
                    report_lines.append(f"  Invalid queries: {file_result['invalid_queries']}")
                    
                    for query_result in file_result['queries']:
                        if not query_result['valid']:
                            report_lines.append(f"    Line {query_result['line_number']}: Invalid query")
                            for error in query_result['errors']:
                                report_lines.append(f"      Error: {error}")
                        
                        if query_result['warnings']:
                            report_lines.append(f"    Line {query_result['line_number']}: Warnings")
                            for warning in query_result['warnings']:
                                report_lines.append(f"      Warning: {warning}")
                        
                        if query_result['suggestions']:
                            report_lines.append(f"    Line {query_result['line_number']}: Suggestions")
                            for suggestion in query_result['suggestions']:
                                report_lines.append(f"      Suggestion: {suggestion}")
        
        # Best practices
        report_lines.append("\nBEST PRACTICES")
        report_lines.append("-" * 15)
        report_lines.append("1. Always include a FROM clause to specify data source")
        report_lines.append("2. Use consistent tag formats starting with 'AI/'")
        report_lines.append("3. Use standard sort fields: file.name, file.mtime, rating, pricing")
        report_lines.append("4. Limit results to reasonable numbers (< 50)")
        report_lines.append("5. Use proper path formatting for consistency")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                self.logger.info(f"Report saved to {output_file}")
            except Exception as e:
                self.logger.error(f"Error saving report: {e}")
        
        return report_text

def main():
    parser = argparse.ArgumentParser(description='Test Dataview queries in dashboard files')
    parser.add_argument('--path', default='AI/001_Tools', 
                       help='Path to dashboard files directory')
    parser.add_argument('--output', default='dataview_test_report.txt',
                       help='Output file for results')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = DataviewTester(verbose=args.verbose)
    
    # Test queries
    print(f"Testing Dataview queries in: {args.path}")
    results = tester.test_directory(args.path)
    
    # Generate report
    report = tester.generate_report(results, args.output)
    
    # Print summary
    total_files = len(results)
    files_with_issues = sum(1 for r in results if r['has_issues'])
    total_queries = sum(r['total_queries'] for r in results)
    total_invalid = sum(r['invalid_queries'] for r in results)
    
    print(f"\nTest complete!")
    print(f"Files processed: {total_files}")
    print(f"Total queries: {total_queries}")
    print(f"Invalid queries: {total_invalid}")
    
    if files_with_issues > 0:
        print(f"\nIssues found. Check {args.output} for details.")
        return 1
    else:
        print("\nAll queries are valid!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
