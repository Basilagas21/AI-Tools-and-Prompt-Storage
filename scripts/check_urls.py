#!/usr/bin/env python3
"""
AI Tools URL Validation Script

This script validates URLs in AI tool markdown files to ensure they are still active
and accessible. It checks for broken links, redirects, and accessibility issues.

Usage:
    python check_urls.py [options]

Options:
    --path PATH          Path to AI tools directory (default: AI/003_Content\\(TheAIs\\))
    --timeout SECONDS    Request timeout in seconds (default: 10)
    --output FILE        Output file for results (default: url_validation_report.txt)
    --verbose            Enable verbose output
    --fix                Attempt to fix common URL issues
"""

import os
import re
import sys
import time
import argparse
import requests
from urllib.parse import urlparse, urljoin
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime

class URLValidator:
    def __init__(self, timeout: int = 10, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Results storage
        self.results = {
            'valid': [],
            'broken': [],
            'redirects': [],
            'timeouts': [],
            'errors': []
        }
    
    def extract_urls_from_markdown(self, file_path: str) -> List[Tuple[str, str, int]]:
        """
        Extract URLs from markdown file.
        Returns list of tuples: (url, context, line_number)
        """
        urls = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')
                
                # Common URL patterns in markdown
                url_patterns = [
                    r'https?://[^\s\)\]\>]+',  # Basic HTTP/HTTPS URLs
                    r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links
                    r'URL:\s*(https?://[^\s]+)',  # URL: prefix
                    r'https://[^\s\)\]\>]+',     # HTTPS URLs
                ]
                
                for line_num, line in enumerate(lines, 1):
                    for pattern in url_patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            if match.groups():
                                # Markdown link format
                                if len(match.groups()) == 2:
                                    url = match.group(2)
                                    context = match.group(1)
                                else:
                                    url = match.group(1)
                                    context = line.strip()
                            else:
                                url = match.group(0)
                                context = line.strip()
                            
                            # Clean up URL
                            url = url.rstrip('.,;:!?')
                            
                            if self.is_valid_url(url):
                                urls.append((url, context, line_num))
        
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
        
        return urls
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL has valid format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def validate_url(self, url: str) -> Dict[str, any]:
        """
        Validate a single URL.
        Returns dictionary with validation results.
        """
        result = {
            'url': url,
            'status': 'unknown',
            'status_code': None,
            'final_url': url,
            'response_time': None,
            'error': None,
            'redirects': []
        }
        
        try:
            start_time = time.time()
            
            response = self.session.head(
                url, 
                timeout=self.timeout,
                allow_redirects=True
            )
            
            end_time = time.time()
            result['response_time'] = end_time - start_time
            result['status_code'] = response.status_code
            result['final_url'] = response.url
            
            # Check for redirects
            if response.history:
                result['redirects'] = [r.url for r in response.history]
            
            # Determine status
            if response.status_code == 200:
                result['status'] = 'valid'
            elif 300 <= response.status_code < 400:
                result['status'] = 'redirect'
            elif 400 <= response.status_code < 500:
                result['status'] = 'client_error'
            elif 500 <= response.status_code < 600:
                result['status'] = 'server_error'
            else:
                result['status'] = 'unknown'
        
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error'] = 'Request timeout'
        
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error'] = 'Connection error'
        
        except requests.exceptions.RequestException as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        except Exception as e:
            result['status'] = 'error'
            result['error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def validate_file(self, file_path: str) -> Dict[str, List[Dict]]:
        """
        Validate all URLs in a markdown file.
        Returns dictionary with validation results.
        """
        file_results = {
            'file': file_path,
            'urls': [],
            'summary': {
                'total': 0,
                'valid': 0,
                'broken': 0,
                'redirects': 0,
                'timeouts': 0,
                'errors': 0
            }
        }
        
        urls = self.extract_urls_from_markdown(file_path)
        
        if not urls:
            self.logger.info(f"No URLs found in {file_path}")
            return file_results
        
        self.logger.info(f"Validating {len(urls)} URLs in {file_path}")
        
        for url, context, line_num in urls:
            if self.verbose:
                print(f"Checking: {url}")
            
            validation_result = self.validate_url(url)
            validation_result.update({
                'context': context,
                'line_number': line_num
            })
            
            file_results['urls'].append(validation_result)
            file_results['summary']['total'] += 1
            
            # Update summary counts
            status = validation_result['status']
            if status == 'valid':
                file_results['summary']['valid'] += 1
            elif status in ['client_error', 'server_error']:
                file_results['summary']['broken'] += 1
            elif status == 'redirect':
                file_results['summary']['redirects'] += 1
            elif status == 'timeout':
                file_results['summary']['timeouts'] += 1
            else:
                file_results['summary']['errors'] += 1
            
            # Add to global results
            self.results[status].append(validation_result)
        
        return file_results
    
    def validate_directory(self, directory_path: str) -> List[Dict]:
        """
        Validate URLs in all markdown files in a directory.
        Returns list of file validation results.
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
            try:
                file_results = self.validate_file(file_path)
                all_results.append(file_results)
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
        
        return all_results
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Generate a comprehensive validation report.
        Returns report as string and optionally saves to file.
        """
        report_lines = []
        report_lines.append("AI Tools URL Validation Report")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall summary
        total_files = len(results)
        total_urls = sum(r['summary']['total'] for r in results)
        total_valid = sum(r['summary']['valid'] for r in results)
        total_broken = sum(r['summary']['broken'] for r in results)
        total_redirects = sum(r['summary']['redirects'] for r in results)
        total_timeouts = sum(r['summary']['timeouts'] for r in results)
        total_errors = sum(r['summary']['errors'] for r in results)
        
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Files processed: {total_files}")
        report_lines.append(f"Total URLs: {total_urls}")
        report_lines.append(f"Valid URLs: {total_valid}")
        report_lines.append(f"Broken URLs: {total_broken}")
        report_lines.append(f"Redirects: {total_redirects}")
        report_lines.append(f"Timeouts: {total_timeouts}")
        report_lines.append(f"Errors: {total_errors}")
        report_lines.append("")
        
        # File-by-file results
        report_lines.append("FILE-BY-FILE RESULTS")
        report_lines.append("-" * 30)
        
        for file_result in results:
            if file_result['summary']['total'] == 0:
                continue
            
            report_lines.append(f"\nFile: {file_result['file']}")
            report_lines.append(f"  Total URLs: {file_result['summary']['total']}")
            report_lines.append(f"  Valid: {file_result['summary']['valid']}")
            report_lines.append(f"  Broken: {file_result['summary']['broken']}")
            report_lines.append(f"  Redirects: {file_result['summary']['redirects']}")
            report_lines.append(f"  Timeouts: {file_result['summary']['timeouts']}")
            report_lines.append(f"  Errors: {file_result['summary']['errors']}")
            
            # List problematic URLs
            problematic_urls = [
                url for url in file_result['urls']
                if url['status'] not in ['valid']
            ]
            
            if problematic_urls:
                report_lines.append("  Problematic URLs:")
                for url_result in problematic_urls:
                    report_lines.append(f"    Line {url_result['line_number']}: {url_result['url']}")
                    report_lines.append(f"      Status: {url_result['status']}")
                    if url_result['error']:
                        report_lines.append(f"      Error: {url_result['error']}")
                    if url_result['redirects']:
                        report_lines.append(f"      Redirects to: {url_result['final_url']}")
        
        # Broken URLs summary
        if total_broken > 0:
            report_lines.append("\nBROKEN URLs SUMMARY")
            report_lines.append("-" * 25)
            
            broken_urls = []
            for file_result in results:
                for url_result in file_result['urls']:
                    if url_result['status'] in ['client_error', 'server_error']:
                        broken_urls.append(url_result)
            
            for url_result in broken_urls:
                report_lines.append(f"  {url_result['url']}")
                report_lines.append(f"    File: {url_result.get('file', 'Unknown')}")
                report_lines.append(f"    Line: {url_result['line_number']}")
                report_lines.append(f"    Status: {url_result['status_code']}")
                if url_result['error']:
                    report_lines.append(f"    Error: {url_result['error']}")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                self.logger.info(f"Report saved to {output_file}")
            except Exception as e:
                self.logger.error(f"Error saving report: {e}")
        
        return report_text
    
    def suggest_fixes(self, url: str) -> List[str]:
        """
        Suggest potential fixes for broken URLs.
        Returns list of suggested URLs to try.
        """
        suggestions = []
        
        # Common fixes
        if url.startswith('http://'):
            suggestions.append(url.replace('http://', 'https://'))
        
        if url.endswith('/'):
            suggestions.append(url.rstrip('/'))
        else:
            suggestions.append(url + '/')
        
        # Remove common problematic characters
        if ' ' in url:
            suggestions.append(url.replace(' ', '%20'))
        
        # Try without www
        if url.startswith('https://www.'):
            suggestions.append(url.replace('https://www.', 'https://'))
        elif url.startswith('http://www.'):
            suggestions.append(url.replace('http://www.', 'http://'))
        
        return suggestions

def main():
    parser = argparse.ArgumentParser(description='Validate URLs in AI tool markdown files')
    parser.add_argument('--path', default='AI/003_Content (TheAIs)', 
                       help='Path to AI tools directory')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Request timeout in seconds')
    parser.add_argument('--output', default='url_validation_report.txt',
                       help='Output file for results')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix common URL issues')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = URLValidator(timeout=args.timeout, verbose=args.verbose)
    
    # Validate URLs
    print(f"Validating URLs in: {args.path}")
    results = validator.validate_directory(args.path)
    
    # Generate report
    report = validator.generate_report(results, args.output)
    
    # Print summary
    total_files = len(results)
    total_urls = sum(r['summary']['total'] for r in results)
    total_valid = sum(r['summary']['valid'] for r in results)
    total_broken = sum(r['summary']['broken'] for r in results)
    
    print(f"\nValidation complete!")
    print(f"Files processed: {total_files}")
    print(f"Total URLs: {total_urls}")
    print(f"Valid URLs: {total_valid}")
    print(f"Broken URLs: {total_broken}")
    
    if total_broken > 0:
        print(f"\nBroken URLs found. Check {args.output} for details.")
        return 1
    else:
        print("\nAll URLs are valid!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
