#!/usr/bin/env python3
"""
Repository Update Script
Handles Git operations for daily updates.
"""

import os
import subprocess
import sys
from datetime import datetime
import pytz

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def get_git_status():
    """Check Git status"""
    returncode, stdout, stderr = run_command("git status --porcelain")
    return returncode == 0 and stdout.strip() != ""

def commit_changes(date_str):
    """Commit changes to Git"""
    commit_message = f"Update stock market data for {date_str}"
    
    commands = [
        "git add .",
        f'git commit -m "{commit_message}"',
        "git push origin main"
    ]
    
    for cmd in commands:
        returncode, stdout, stderr = run_command(cmd)
        if returncode != 0:
            print(f"Error executing: {cmd}")
            print(f"Stderr: {stderr}")
            return False
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("GitHub Repository Update")
    print("=" * 60)
    
    # Get current date
    est = pytz.timezone('US/Eastern')
    now_est = datetime.now(est)
    date_str = now_est.strftime('%Y-%m-%d')
    
    # Check if there are changes
    if not get_git_status():
        print("No changes to commit.")
        return
    
    print(f"Committing changes for {date_str}...")
    
    # Commit and push
    if commit_changes(date_str):
        print("✅ Changes committed and pushed successfully!")
    else:
        print("❌ Failed to commit changes.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()