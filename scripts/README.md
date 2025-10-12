# Scripts Directory

This directory contains utility scripts for maintaining and managing the AI Tools collection.

## Available Scripts

### 1. `check_urls.py`
Validates URLs in AI tool markdown files to ensure they are still active and accessible.

**Features:**
- Checks for broken links, redirects, and accessibility issues
- Generates comprehensive validation reports
- Supports rate limiting and error handling
- Can suggest fixes for common URL issues

**Usage:**
```bash
python check_urls.py --path "AI/003_Content (TheAIs)" --output url_report.txt
```

### 2. `update_metadata.py`
Updates metadata in AI tool markdown files, including dates, ratings, and status.

**Features:**
- Updates last_verified dates
- Updates ratings and status information
- Supports dry-run mode for testing
- Generates update reports

**Usage:**
```bash
python update_metadata.py --update-dates --dry-run
```

### 3. `tag_validator.py`
Validates and ensures consistency of tags across AI tool markdown files.

**Features:**
- Checks for standardized tag formats
- Identifies missing required tags
- Finds inconsistent tag usage
- Detects orphaned tags

**Usage:**
```bash
python tag_validator.py --path "AI/003_Content (TheAIs)" --output tag_report.txt
```

## Installation

### Prerequisites
- Python 3.7 or higher
- Required packages (install with pip):

```bash
pip install requests pyyaml cryptography
```

### Setup
1. Clone or download the repository
2. Navigate to the scripts directory
3. Install required dependencies
4. Run scripts as needed

## Usage Examples

### Check all URLs
```bash
python check_urls.py --verbose --output url_validation_report.txt
```

### Update metadata for all tools
```bash
python update_metadata.py --update-dates --verbose
```

### Validate tags with fixes
```bash
python tag_validator.py --fix --verbose --output tag_report.txt
```

### Dry run updates
```bash
python update_metadata.py --update-dates --dry-run --verbose
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - For AI-powered validation (if implemented)
- `ANTHROPIC_API_KEY` - For Claude-based validation (if implemented)

### Customization
- Modify `standard_categories` in `tag_validator.py` to add new tag categories
- Adjust timeout values in `check_urls.py` for different network conditions
- Update validation rules in scripts as needed

## Output Files

### URL Validation Report
- Lists all checked URLs
- Shows status codes and response times
- Identifies broken links and redirects
- Provides suggestions for fixes

### Metadata Update Report
- Shows which files were updated
- Lists changes made
- Provides summary statistics

### Tag Validation Report
- Shows tag usage statistics
- Identifies files with tag issues
- Lists orphaned and unused tags
- Provides suggestions for fixes

## Best Practices

### Regular Maintenance
- Run URL validation monthly
- Update metadata quarterly
- Validate tags after major changes

### Automation
- Set up cron jobs for regular validation
- Integrate with CI/CD pipelines
- Use dry-run mode for testing

### Error Handling
- Always review reports before making changes
- Test scripts on small subsets first
- Keep backups of original files

## Troubleshooting

### Common Issues
1. **Permission errors**: Ensure write permissions for output files
2. **Network timeouts**: Increase timeout values in `check_urls.py`
3. **YAML parsing errors**: Check frontmatter format in markdown files
4. **Missing dependencies**: Install required Python packages

### Debug Mode
Use `--verbose` flag for detailed logging and debugging information.

## Contributing

When adding new scripts:
1. Follow the existing code style
2. Add comprehensive documentation
3. Include error handling
4. Test with sample data
5. Update this README

## License

These scripts are part of the AI Tools collection and follow the same license terms.
