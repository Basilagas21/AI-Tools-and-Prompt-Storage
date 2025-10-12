#!/usr/bin/env python3
"""
AI Tools Metadata Update Script

This script updates metadata in AI tool markdown files, including:
- Last verified dates
- Rating updates
- Status changes
- Pricing updates

Usage:
    python update_metadata.py [options]

Options:
    --path PATH          Path to AI tools directory (default: AI/003_Content\\(TheAIs\\))
    --update-dates       Update last_verified dates
    --update-ratings     Update ratings based on external data
    --update-status      Update tool status
    --dry-run            Show what would be updated without making changes
    --verbose            Enable verbose output
"""

import os
import re
import sys
import argparse
import yaml
from datetime import datetime
from typing import Dict, List, Optional
import logging

class MetadataUpdater:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_frontmatter(self, content: str) -> tuple[Dict, str, str]:
        """
        Extract YAML frontmatter from markdown content.
        Returns (frontmatter_dict, frontmatter_text, remaining_content)
        """
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
    
    def update_last_verified(self, frontmatter: Dict) -> Dict:
        """Update last_verified date to today"""
        frontmatter['last_verified'] = datetime.now().strftime('%Y-%m-%d')
        return frontmatter
    
    def update_rating(self, frontmatter: Dict, new_rating: float) -> Dict:
        """Update rating in frontmatter"""
        frontmatter['rating'] = new_rating
        return frontmatter
    
    def update_status(self, frontmatter: Dict, new_status: str) -> Dict:
        """Update status in frontmatter"""
        valid_statuses = ['active', 'deprecated', 'beta', 'discontinued']
        if new_status in valid_statuses:
            frontmatter['status'] = new_status
        else:
            self.logger.warning(f"Invalid status: {new_status}")
        return frontmatter
    
    def update_pricing(self, frontmatter: Dict, new_pricing: str) -> Dict:
        """Update pricing in frontmatter"""
        valid_pricing = ['free', 'freemium', 'paid']
        if new_pricing in valid_pricing:
            frontmatter['pricing'] = new_pricing
        else:
            self.logger.warning(f"Invalid pricing: {new_pricing}")
        return frontmatter
    
    def generate_frontmatter_yaml(self, frontmatter: Dict) -> str:
        """Generate YAML frontmatter from dictionary"""
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_content}---"
    
    def update_file_metadata(self, file_path: str, updates: Dict, dry_run: bool = False) -> bool:
        """
        Update metadata in a markdown file.
        Returns True if successful, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            frontmatter_dict, frontmatter_text, remaining_content = self.extract_frontmatter(content)
            
            if not frontmatter_dict:
                self.logger.warning(f"No frontmatter found in {file_path}")
                return False
            
            # Apply updates
            original_frontmatter = frontmatter_dict.copy()
            
            if 'update_dates' in updates and updates['update_dates']:
                frontmatter_dict = self.update_last_verified(frontmatter_dict)
            
            if 'rating' in updates and updates['rating']:
                frontmatter_dict = self.update_rating(frontmatter_dict, updates['rating'])
            
            if 'status' in updates and updates['status']:
                frontmatter_dict = self.update_status(frontmatter_dict, updates['status'])
            
            if 'pricing' in updates and updates['pricing']:
                frontmatter_dict = self.update_pricing(frontmatter_dict, updates['pricing'])
            
            # Check if changes were made
            if frontmatter_dict == original_frontmatter:
                if self.verbose:
                    self.logger.info(f"No changes needed for {file_path}")
                return True
            
            if dry_run:
                self.logger.info(f"Would update {file_path}")
                return True
            
            # Generate new content
            new_frontmatter = self.generate_frontmatter_yaml(frontmatter_dict)
            new_content = new_frontmatter + '\n' + remaining_content
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            self.logger.info(f"Updated metadata in {file_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error updating {file_path}: {e}")
            return False
    
    def update_directory_metadata(self, directory_path: str, updates: Dict, dry_run: bool = False) -> Dict:
        """
        Update metadata in all markdown files in a directory.
        Returns summary of updates.
        """
        results = {
            'total_files': 0,
            'updated_files': 0,
            'failed_files': 0,
            'skipped_files': 0
        }
        
        if not os.path.exists(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return results
        
        markdown_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        self.logger.info(f"Found {len(markdown_files)} markdown files")
        
        for file_path in markdown_files:
            results['total_files'] += 1
            
            try:
                success = self.update_file_metadata(file_path, updates, dry_run)
                if success:
                    results['updated_files'] += 1
                else:
                    results['skipped_files'] += 1
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                results['failed_files'] += 1
        
        return results
    
    def generate_update_report(self, results: Dict, updates: Dict) -> str:
        """Generate a report of the update process"""
        report_lines = []
        report_lines.append("AI Tools Metadata Update Report")
        report_lines.append("=" * 40)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        report_lines.append("UPDATE SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Total files processed: {results['total_files']}")
        report_lines.append(f"Files updated: {results['updated_files']}")
        report_lines.append(f"Files skipped: {results['skipped_files']}")
        report_lines.append(f"Files failed: {results['failed_files']}")
        report_lines.append("")
        
        report_lines.append("UPDATES APPLIED")
        report_lines.append("-" * 20)
        for key, value in updates.items():
            if value:
                report_lines.append(f"  {key}: {value}")
        
        return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description='Update metadata in AI tool markdown files')
    parser.add_argument('--path', default='AI/003_Content (TheAIs)', 
                       help='Path to AI tools directory')
    parser.add_argument('--update-dates', action='store_true',
                       help='Update last_verified dates')
    parser.add_argument('--update-ratings', action='store_true',
                       help='Update ratings based on external data')
    parser.add_argument('--update-status', action='store_true',
                       help='Update tool status')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize updater
    updater = MetadataUpdater(verbose=args.verbose)
    
    # Prepare updates
    updates = {
        'update_dates': args.update_dates,
        'rating': None,
        'status': None,
        'pricing': None
    }
    
    if args.update_ratings:
        # This would typically come from external data source
        updates['rating'] = 4.0  # Default rating
    
    if args.update_status:
        # This would typically come from external data source
        updates['status'] = 'active'  # Default status
    
    # Update metadata
    print(f"Updating metadata in: {args.path}")
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
    
    results = updater.update_directory_metadata(args.path, updates, args.dry_run)
    
    # Generate report
    report = updater.generate_update_report(results, updates)
    print("\n" + report)
    
    if results['failed_files'] > 0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())
