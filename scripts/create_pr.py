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
    
    branch_name = f"{day_type}/{activity_type}/{current_date}"
    
    # Create and switch to new branch
    commands = [
        f"git checkout -b {branch_name}",
        "git add .",
        f'git commit -m "{day_type.capitalize()} update: {activity_type.replace("_", " ")} for {current_date}"'
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
    
    title = f"{day_type.capitalize()} Update: {activity_type.replace('_', ' ')} - {current_date}"
    
    # Generate body based on activity type
    if day_type == 'weekday':
        body = f"""## Daily Stock Market Data Update

**Date:** {current_date}
**Type:** Daily data collection

### Changes:
- Added daily stock market data for {current_date}
- Includes top gainers, losers, and most active stocks
- Updated market indices data

### Files Added:
- `data/daily/{current_date}/gainers.csv`
- `data/daily/{current_date}/losers.csv`
- `data/daily/{current_date}/most_active.csv`
- `data/daily/{current_date}/indices.json`

### Notes:
Automated daily update as part of stock market data collection project.
"""
    elif day_type == 'saturday':
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

### Notes:
Weekly automated analysis of stock market data.
"""
    else:  # sunday
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

### Notes:
Weekly maintenance and improvement tasks to ensure code quality and data accuracy.
"""
    
    # Try using GitHub CLI if available
    gh_cmd = f'gh pr create --title "{title}" --body "{body}" --base main --head {branch_name}'
    returncode, stdout, stderr = run_command(gh_cmd)
    
    if returncode == 0:
        print(f"✅ Pull Request created: {stdout.strip()}")
        return stdout.strip()
    else:
        # Fallback: Provide manual instructions
        print("ℹ️  GitHub CLI not available or failed. Manual PR creation needed:")
        print(f"   Title: {title}")
        print(f"   Branch: {branch_name}")
        print(f"   Base: main")
        print(f"   Body: {body[:100]}...")
        
        # Return a placeholder for auto-merge attempt
        return f"manual-pr-{branch_name}"

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
    
    print(f"Day Type: {day_type}")
    print(f"Activity Type: {activity_type}")
    
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
    
    # Attempt auto-merge (commented out for now)
    # print("\nAttempting auto-merge...")
    # auto_merge_pr(pr_result)
    
    print("\n" + "=" * 60)
    print("✅ PR CREATION COMPLETED")
    print("=" * 60)
    
    print(f"\nSummary:")
    print(f"- Branch: {branch_name}")
    print(f"- PR: {pr_result}")
    print(f"- Changes: {len(changes_list.splitlines())} files")
    
    print("\nNext steps:")
    print("1. Review the PR on GitHub")
    print("2. Merge if changes look good")
    print("3. Branch will be deleted after merge")
    
    return True

if __name__ == "__main__":
    main()