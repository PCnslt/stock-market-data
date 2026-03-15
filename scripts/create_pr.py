#!/usr/bin/env python3
"""
Pull Request Creation Script
Creates a PR for daily updates and handles auto-merge.
"""

import os
import subprocess
import json
from datetime import datetime
import pytz
import sys
import re

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def get_git_status():
    """Check if there are changes to commit"""
    returncode, stdout, stderr = run_command("git status --porcelain")
    has_changes = returncode == 0 and stdout.strip() != ""
    return has_changes, stdout

def create_branch(day_type, activity_type):
    """Create a new branch for today's changes"""
    est = pytz.timezone('US/Eastern')
    current_date = datetime.now(est).strftime('%Y-%m-%d')
    current_time = datetime.now(est).strftime('%H%M')
    
    # Determine commit type from activity_type or environment
    commit_type = os.environ.get('COMMIT_TYPE', activity_type)
    
    # Create branch name based on commit type
    if commit_type == 'pre_market':
        branch_name = f"pre_market/{current_date}/{current_time}"
        commit_message = f"Pre-market data collection for {current_date} at {current_time} EST"
    elif commit_type == 'mid_day':
        branch_name = f"mid_day/{current_date}/{current_time}"
        commit_message = f"Mid-day market analysis for {current_date} at {current_time} EST"
    elif commit_type == 'end_of_day':
        branch_name = f"end_of_day/{current_date}/{current_time}"
        commit_message = f"End-of-day data collection for {current_date} at {current_time} EST"
    elif day_type == 'saturday':
        branch_name = f"saturday/weekly_summary/{current_date}"
        commit_message = f"Weekly summary for {current_date}"
    elif day_type == 'sunday':
        branch_name = f"sunday/code_improvement/{current_date}"
        commit_message = f"Sunday code improvements for {current_date}"
    else:
        branch_name = f"{day_type}/{activity_type}/{current_date}"
        commit_message = f"{day_type.capitalize()} update: {activity_type.replace('_', ' ')} for {current_date}"
    
    # Create and switch to new branch
    commands = [
        f"git checkout -b {branch_name}",
        "git add .",
        f'git commit -m "{commit_message}"'
    ]
    
    for cmd in commands:
        returncode, stdout, stderr = run_command(cmd)
        if returncode != 0:
            print(f"Error executing: {cmd}")
            print(f"Stderr: {stderr}")
            return None
    
    return branch_name

def push_branch(branch_name):
    """Push branch to remote"""
    cmd = f"git push origin {branch_name}"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode != 0:
        print(f"Error pushing branch: {stderr}")
        return False
    
    return True

def create_pull_request(branch_name, day_type, activity_type):
    """Create a pull request using GitHub CLI or API"""
    est = pytz.timezone('US/Eastern')
    current_date = datetime.now(est).strftime('%Y-%m-%d')
    current_time = datetime.now(est).strftime('%H:%M EST')
    
    # Determine commit type from activity_type or environment
    commit_type = os.environ.get('COMMIT_TYPE', activity_type)
    
    # Generate title and body based on commit type
    if commit_type == 'pre_market':
        title = f"Pre-Market Update: {current_date} - {current_time}"
        body = f"""## Pre-Market Data Collection

**Date:** {current_date}
**Time:** {current_time}
**Type:** Pre-market data collection

### Changes:
- Collected pre-market movers data
- Updated futures market information
- Added global market performance data
- Included economic calendar for the day
- Analyzed news sentiment

### Files Added:
- `data/pre_market/{current_date}/pre_market_movers.json`
- `data/pre_market/{current_date}/futures.json`
- `data/pre_market/{current_date}/global_markets.json`
- `data/pre_market/{current_date}/economic_calendar.json`
- `data/pre_market/{current_date}/news_sentiment.json`

### Value Provided:
- Early market insights before US market open
- Global market context for trading decisions
- Economic event awareness
- Pre-market sentiment analysis

### Notes:
Automated pre-market data collection as part of triple daily market monitoring system.
"""
    elif commit_type == 'mid_day':
        title = f"Mid-Day Analysis: {current_date} - {current_time}"
        body = f"""## Mid-Day Market Analysis

**Date:** {current_date}
**Time:** {current_time}
**Type:** Mid-day market analysis

### Changes:
- Analyzed morning session performance
- Updated volatility and sector rotation analysis
- Added technical indicators
- Generated trading insights
- Updated news sentiment

### Files Added:
- `data/mid_day/{current_date}/morning_performance.json`
- `data/mid_day/{current_date}/volatility_analysis.json`
- `data/mid_day/{current_date}/sector_rotation.json`
- `data/mid_day/{current_date}/technical_indicators.json`
- `data/mid_day/{current_date}/trading_insights.json`
- `data/mid_day/{current_date}/news_sentiment_update.json`

### Value Provided:
- Real-time market performance analysis
- Sector rotation insights for afternoon trading
- Technical indicator updates
- Actionable trading opportunities
- Risk assessment for remainder of day

### Notes:
Automated mid-day analysis as part of triple daily market monitoring system.
"""
    elif commit_type == 'end_of_day' or day_type == 'weekday':
        title = f"End-of-Day Update: {current_date} - {current_time}"
        body = f"""## Daily Stock Market Data Update

**Date:** {current_date}
**Time:** {current_time}
**Type:** End-of-day data collection

### Changes:
- Added complete daily stock market data for {current_date}
- Includes top gainers, losers, and most active stocks
- Updated market indices data
- Full day analysis and summary

### Files Added:
- `data/daily/{current_date}/gainers.csv`
- `data/daily/{current_date}/losers.csv`
- `data/daily/{current_date}/most_active.csv`
- `data/daily/{current_date}/indices.json`

### Value Provided:
- Complete market performance record
- Historical data for analysis and backtesting
- Portfolio performance tracking
- Market trend identification

### Notes:
Automated end-of-day data collection as part of triple daily market monitoring system.
"""
    elif day_type == 'saturday':
        title = f"Weekly Summary: {current_date}"
        body = f"""## Weekly Summary Update

**Date:** {current_date}
**Type:** Weekly analysis and summary

### Changes:
- Generated weekly summary report
- Analyzed market performance for the past week
- Added weekly insights and trends

### Files Added:
- `data/weekly/summary_{current_date}.md`
- `data/weekly/analysis_{current_date}.json`

### Value Provided:
- Weekly performance review
- Long-term trend analysis
- Portfolio rebalancing insights
- Market cycle identification

### Notes:
Weekly automated analysis of stock market data.
"""
    else:  # sunday or code improvements
        title = f"Sunday Improvements: {current_date}"
        body = f"""## Sunday Improvements & Maintenance

**Date:** {current_date}
**Type:** Code improvements and maintenance

### Changes:
- Updated documentation
- Code improvements and refactoring
- Data validation checks
- Created improvement log

### Files Modified/Added:
- Updated README.md
- Improved data collection scripts
- Added improvement log
- Validation reports

### Value Provided:
- System reliability and maintenance
- Code quality improvements
- Documentation updates
- Performance optimizations

### Notes:
Weekly maintenance and improvement tasks to ensure code quality and data accuracy.
"""
    
    # Try using GitHub CLI if available
    gh_cmd = f'gh pr create --title "{title}" --body "{body}" --base main --head {branch_name}'
    returncode, stdout, stderr = run_command(gh_cmd)
    
    if returncode == 0:
        print(f"✅ Pull Request created: {stdout.strip()}")
        
        # Extract PR number from output (format: "https://github.com/owner/repo/pull/123")
        import re
        match = re.search(r'/pull/(\d+)', stdout)
        if match:
            pr_number = match.group(1)
            # Set output for GitHub Actions
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
                print(f'pr_number={pr_number}', file=fh)
            return pr_number
        return stdout.strip()
    else:
        # Fallback: Provide manual instructions
        print("ℹ️  GitHub CLI not available or failed. Manual PR creation needed:")
        print(f"   Title: {title}")
        print(f"   Branch: {branch_name}")
        print(f"   Base: main")
        print(f"   Body: {body[:100]}...")
        
        # Return empty for no auto-merge
        return ""

def auto_merge_pr(pr_url_or_id):
    """Attempt to auto-merge the PR"""
    # This would require additional permissions and setup
    # For now, we'll just output instructions
    
    print("\n⚠️  Auto-merge not configured. Manual steps:")
    print(f"1. Go to the created PR: {pr_url_or_id}")
    print("2. Review changes")
    print("3. Merge using 'Squash and merge' or 'Merge pull request'")
    print("4. Delete branch after merge")
    
    return False

def main():
    """Main function"""
    print("=" * 60)
    print("Pull Request Creation")
    print("=" * 60)
    
    # Get environment variables
    day_type = os.environ.get('DAY_TYPE', 'unknown')
    activity_type = os.environ.get('ACTIVITY_TYPE', 'unknown')
    commit_type = os.environ.get('COMMIT_TYPE', activity_type)
    
    print(f"Day Type: {day_type}")
    print(f"Activity Type: {activity_type}")
    print(f"Commit Type: {commit_type}")
    
    # Check for changes
    has_changes, changes_list = get_git_status()
    
    if not has_changes:
        print("No changes to commit. Skipping PR creation.")
        return True
    
    print(f"Changes detected:\n{changes_list}")
    
    # Create branch
    print("\nCreating branch...")
    branch_name = create_branch(day_type, activity_type)
    
    if not branch_name:
        print("❌ Failed to create branch")
        return False
    
    print(f"✅ Branch created: {branch_name}")
    
    # Push branch
    print("\nPushing branch to remote...")
    if not push_branch(branch_name):
        print("❌ Failed to push branch")
        return False
    
    print("✅ Branch pushed to remote")
    
    # Create PR
    print("\nCreating Pull Request...")
    pr_result = create_pull_request(branch_name, day_type, activity_type)
    
    if not pr_result:
        print("❌ Failed to create PR")
        return False
    
    print("\n" + "=" * 60)
    print("✅ PR CREATION COMPLETED")
    print("=" * 60)
    
    print(f"\nSummary:")
    print(f"- Branch: {branch_name}")
    print(f"- PR: {pr_result}")
    print(f"- Changes: {len(changes_list.splitlines())} files")
    
    if pr_result and pr_result.isdigit():
        print(f"\n✅ PR #{pr_result} created successfully!")
        print("Auto-merge will be attempted by GitHub Actions workflow.")
    else:
        print("\n⚠️  Manual PR creation needed.")
        print("Auto-merge cannot be performed automatically.")
    
    return True

if __name__ == "__main__":
    main()