#!/usr/bin/env python3
"""
AI Tools Tag Validator Script

This script validates and ensures consistency of tags across AI tool markdown files.
It checks for:
- Standardized tag formats
- Missing required tags
- Inconsistent tag usage
- Orphaned tags

Usage:
    python tag_validator.py [options]

Options:
    --path PATH          Path to AI tools directory (default: AI/003_Content\\(TheAIs\\))
    --fix                Attempt to fix common tag issues
    --output FILE        Output file for results (default: tag_validation_report.txt)
    --verbose            Enable verbose output
"""

import os
import re
import sys
import argparse
import yaml
from typing import Dict, List, Set, Tuple
import logging
from collections import defaultdict, Counter
from datetime import datetime

class TagValidator:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Standard tag categories
        self.standard_categories = {
            'AI/TextGeneration',
            'AI/CodingAIs',
            'AI/AI_WritingTools',
            'AI/VideoGeneration',
            'AI/ImageGeneration',
            'AI/AudioGeneration',
            'AI/AI_Benchmarks',
            'AI/AI_Indexes',
            'AI/RoleplayingAIs',
            'AI/SelfHostingTools',
            'AI/AI_Prompts',
            'AI/AI_Agents',
            'AI/Detection',
            'AI/MiscellaneousAI',
            'AI/Productivity'
        }
        
        # Required tags
        self.required_tags = {'ai-tool', 'AI'}
        
        # Results storage
        self.results = {
            'files_processed': 0,
            'files_with_issues': 0,
            'total_tags': 0,
            'invalid_tags': [],
            'missing_tags': [],
            'inconsistent_tags': [],
            'orphaned_tags': [],
            'tag_usage': defaultdict(int)
        }
    
    def extract_frontmatter(self, content: str) -> tuple[Dict, str, str]:
        """Extract YAML frontmatter from markdown content"""
        if not content.startswith('---'):
            return {}, '', content
        
        lines = content.split('\n')
        frontmatter_lines = []
        content_lines = []
        in_frontmatter = False
        
        for i, line in enumerate(lines):
            if line.strip() == '---' and i == 0:
                in_frontmatter = True
                frontmatter_lines.append(line)
            elif line.strip() == '---' and in_frontmatter:
                frontmatter_lines.append(line)
                content_lines = lines[i+1:]
                break
            elif in_frontmatter:
                frontmatter_lines.append(line)
            else:
                content_lines.append(line)
        
        frontmatter_text = '\n'.join(frontmatter_lines)
        remaining_content = '\n'.join(content_lines)
        
        try:
            frontmatter_dict = yaml.safe_load(frontmatter_text)
            if frontmatter_dict is None:
                frontmatter_dict = {}
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML frontmatter: {e}")
            frontmatter_dict = {}
        
        return frontmatter_dict, frontmatter_text, remaining_content
    
    def validate_tags(self, tags: List[str], file_path: str) -> Dict[str, List[str]]:
        """
        Validate tags for a single file.
        Returns dictionary with validation results.
        """
        issues = {
            'invalid_tags': [],
            'missing_tags': [],
            'inconsistent_tags': []
        }
        
        # Check for required tags
        for required_tag in self.required_tags:
            if required_tag not in tags:
                issues['missing_tags'].append(required_tag)
        
        # Check for invalid tags
        for tag in tags:
            self.results['tag_usage'][tag] += 1
            
            # Check if tag follows standard format
            if not self.is_valid_tag_format(tag):
                issues['invalid_tags'].append(tag)
            
            # Check if category tag is standard
            if tag.startswith('AI/') and tag not in self.standard_categories:
                issues['inconsistent_tags'].append(tag)
        
        return issues
    
    def is_valid_tag_format(self, tag: str) -> bool:
        """Check if tag follows valid format"""
        # Basic format validation
        if not tag or not isinstance(tag, str):
            return False
        
        # Check for valid characters (alphanumeric, hyphens, underscores, slashes)
        if not re.match(r'^[a-zA-Z0-9_/-]+$', tag):
            return False
        
        # Check length
        if len(tag) > 50:
            return False
        
        return True
    
    def validate_file(self, file_path: str) -> Dict:
        """
        Validate tags in a single markdown file.
        Returns validation results.
        """
        file_results = {
            'file': file_path,
            'tags': [],
            'issues': {
                'invalid_tags': [],
                'missing_tags': [],
                'inconsistent_tags': []
            },
            'has_issues': False
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            frontmatter_dict, _, _ = self.extract_frontmatter(content)
            
            if 'tags' not in frontmatter_dict:
                self.logger.warning(f"No tags found in {file_path}")
                file_results['issues']['missing_tags'] = list(self.required_tags)
                file_results['has_issues'] = True
                return file_results
            
            tags = frontmatter_dict['tags']
            if not isinstance(tags, list):
                self.logger.warning(f"Tags not in list format in {file_path}")
                return file_results
            
            file_results['tags'] = tags
            
            # Validate tags
            issues = self.validate_tags(tags, file_path)
            file_results['issues'] = issues
            
            # Check if file has issues
            if any(issues.values()):
                file_results['has_issues'] = True
                self.results['files_with_issues'] += 1
            
            self.results['total_tags'] += len(tags)
        
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            file_results['has_issues'] = True
        
        return file_results
    
    def validate_directory(self, directory_path: str) -> List[Dict]:
        """
        Validate tags in all markdown files in a directory.
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
            self.results['files_processed'] += 1
            file_results = self.validate_file(file_path)
            all_results.append(file_results)
        
        return all_results
    
    def find_orphaned_tags(self, all_results: List[Dict]) -> List[str]:
        """
        Find tags that are used in only one file (potential orphans).
        Returns list of potentially orphaned tags.
        """
        tag_file_count = defaultdict(int)
        
        for file_result in all_results:
            for tag in file_result['tags']:
                tag_file_count[tag] += 1
        
        orphaned_tags = []
        for tag, count in tag_file_count.items():
            if count == 1 and tag not in self.required_tags:
                orphaned_tags.append(tag)
        
        return orphaned_tags
    
    def suggest_tag_fixes(self, issues: Dict) -> Dict[str, List[str]]:
        """
        Suggest fixes for tag issues.
        Returns dictionary with suggested fixes.
        """
        suggestions = {}
        
        # Suggest fixes for inconsistent tags
        for tag in issues['inconsistent_tags']:
            if tag.startswith('AI/'):
                # Find closest standard category
                closest_match = self.find_closest_category(tag)
                if closest_match:
                    suggestions[tag] = [closest_match]
        
        # Suggest fixes for missing tags
        if issues['missing_tags']:
            suggestions['missing_tags'] = list(issues['missing_tags'])
        
        return suggestions
    
    def find_closest_category(self, tag: str) -> str:
        """Find the closest standard category for a tag"""
        tag_lower = tag.lower()
        
        # Simple matching logic
        if 'text' in tag_lower or 'chat' in tag_lower:
            return 'AI/TextGeneration'
        elif 'code' in tag_lower or 'coding' in tag_lower:
            return 'AI/CodingAIs'
        elif 'image' in tag_lower or 'art' in tag_lower:
            return 'AI/ImageGeneration'
        elif 'audio' in tag_lower or 'music' in tag_lower:
            return 'AI/AudioGeneration'
        elif 'video' in tag_lower:
            return 'AI/VideoGeneration'
        elif 'writing' in tag_lower:
            return 'AI/AI_WritingTools'
        elif 'agent' in tag_lower:
            return 'AI/AI_Agents'
        elif 'productivity' in tag_lower:
            return 'AI/Productivity'
        
        return None
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Generate a comprehensive tag validation report.
        Returns report as string and optionally saves to file.
        """
        report_lines = []
        report_lines.append("AI Tools Tag Validation Report")
        report_lines.append("=" * 40)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall summary
        total_files = len(results)
        files_with_issues = sum(1 for r in results if r['has_issues'])
        total_tags = sum(len(r['tags']) for r in results)
        
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Files processed: {total_files}")
        report_lines.append(f"Files with issues: {files_with_issues}")
        report_lines.append(f"Total tags: {total_tags}")
        report_lines.append("")
        
        # Tag usage statistics
        report_lines.append("TAG USAGE STATISTICS")
        report_lines.append("-" * 25)
        
        tag_usage = Counter(self.results['tag_usage'])
        for tag, count in tag_usage.most_common(20):
            report_lines.append(f"  {tag}: {count}")
        
        report_lines.append("")
        
        # Files with issues
        if files_with_issues > 0:
            report_lines.append("FILES WITH ISSUES")
            report_lines.append("-" * 20)
            
            for file_result in results:
                if file_result['has_issues']:
                    report_lines.append(f"\nFile: {file_result['file']}")
                    
                    if file_result['issues']['invalid_tags']:
                        report_lines.append(f"  Invalid tags: {file_result['issues']['invalid_tags']}")
                    
                    if file_result['issues']['missing_tags']:
                        report_lines.append(f"  Missing tags: {file_result['issues']['missing_tags']}")
                    
                    if file_result['issues']['inconsistent_tags']:
                        report_lines.append(f"  Inconsistent tags: {file_result['issues']['inconsistent_tags']}")
        
        # Orphaned tags
        orphaned_tags = self.find_orphaned_tags(results)
        if orphaned_tags:
            report_lines.append("\nPOTENTIALLY ORPHANED TAGS")
            report_lines.append("-" * 30)
            for tag in orphaned_tags:
                report_lines.append(f"  {tag}")
        
        # Standard categories not used
        used_categories = set()
        for file_result in results:
            for tag in file_result['tags']:
                if tag in self.standard_categories:
                    used_categories.add(tag)
        
        unused_categories = self.standard_categories - used_categories
        if unused_categories:
            report_lines.append("\nUNUSED STANDARD CATEGORIES")
            report_lines.append("-" * 30)
            for category in sorted(unused_categories):
                report_lines.append(f"  {category}")
        
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
    parser = argparse.ArgumentParser(description='Validate tags in AI tool markdown files')
    parser.add_argument('--path', default='AI/003_Content (TheAIs)', 
                       help='Path to AI tools directory')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix common tag issues')
    parser.add_argument('--output', default='tag_validation_report.txt',
                       help='Output file for results')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = TagValidator(verbose=args.verbose)
    
    # Validate tags
    print(f"Validating tags in: {args.path}")
    results = validator.validate_directory(args.path)
    
    # Generate report
    report = validator.generate_report(results, args.output)
    
    # Print summary
    total_files = len(results)
    files_with_issues = sum(1 for r in results if r['has_issues'])
    
    print(f"\nValidation complete!")
    print(f"Files processed: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    
    if files_with_issues > 0:
        print(f"\nTag issues found. Check {args.output} for details.")
        return 1
    else:
        print("\nAll tags are valid!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
