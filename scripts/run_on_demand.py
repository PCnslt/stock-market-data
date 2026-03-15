#!/usr/bin/env python3
"""
On-demand stock market data collection
Run this script anytime to fetch and store current market data
"""

import os
import sys
import argparse
from datetime import datetime
import subprocess
import json

def run_pre_market():
    """Run pre-market data collection"""
    print("Running pre-market data collection...")
    try:
        result = subprocess.run(
            [sys.executable, "pre_market_collection.py"],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Pre-market collection successful")
            return True
        else:
            print(f"❌ Pre-market collection failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running pre-market collection: {e}")
        return False

def run_mid_day():
    """Run mid-day analysis"""
    print("Running mid-day analysis...")
    try:
        result = subprocess.run(
            [sys.executable, "mid_day_analysis.py"],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Mid-day analysis successful")
            return True
        else:
            print(f"❌ Mid-day analysis failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running mid-day analysis: {e}")
        return False

def run_end_of_day():
    """Run end-of-day data collection"""
    print("Running end-of-day data collection...")
    try:
        result = subprocess.run(
            [sys.executable, "collect_data.py"],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ End-of-day collection successful")
            return True
        else:
            print(f"❌ End-of-day collection failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running end-of-day collection: {e}")
        return False

def run_all():
    """Run all three collection types"""
    print("Running all data collection types...")
    results = {
        "pre_market": run_pre_market(),
        "mid_day": run_mid_day(),
        "end_of_day": run_end_of_day()
    }
    
    success_count = sum(results.values())
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"ON-DEMAND COLLECTION COMPLETE: {success_count}/{total} successful")
    print(f"{'='*60}")
    
    for collection_type, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {collection_type.replace('_', ' ').title()}")
    
    return all(results.values())

def create_summary_report():
    """Create a summary report of the on-demand run"""
    timestamp = datetime.now().isoformat()
    report = {
        "timestamp": timestamp,
        "run_type": "on_demand",
        "status": "completed",
        "data_collected": {
            "pre_market": os.path.exists("../data/pre_market"),
            "mid_day": os.path.exists("../data/mid_day"),
            "end_of_day": os.path.exists("../data/daily")
        }
    }
    
    # Save report
    report_dir = os.path.join(os.path.dirname(__file__), "..", "data", "on_demand")
    os.makedirs(report_dir, exist_ok=True)
    
    report_file = os.path.join(report_dir, f"report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Summary report saved to: {report_file}")
    return report_file

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="On-demand stock market data collection")
    parser.add_argument(
        "--type",
        choices=["pre_market", "mid_day", "end_of_day", "all"],
        default="all",
        help="Type of data to collect (default: all)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Don't create a summary report"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ON-DEMAND STOCK MARKET DATA COLLECTION")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Type: {args.type}")
    print("=" * 60)
    
    # Set environment variables from GitHub Secrets (if running locally)
    env_vars = ["ALPHA_VANTAGE_KEY", "FMP_KEY", "NEWSAPI_KEY"]
    for var in env_vars:
        if var not in os.environ:
            print(f"⚠️  Warning: {var} not set in environment")
    
    # Run the requested collection type
    success = False
    if args.type == "pre_market":
        success = run_pre_market()
    elif args.type == "mid_day":
        success = run_mid_day()
    elif args.type == "end_of_day":
        success = run_end_of_day()
    else:  # all
        success = run_all()
    
    # Create summary report unless disabled
    if not args.no_report and success:
        report_file = create_summary_report()
        print(f"\n📁 Data saved to appropriate directories")
        print(f"📄 Report: {report_file}")
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ON-DEMAND COLLECTION COMPLETED SUCCESSFULLY")
    else:
        print("❌ ON-DEMAND COLLECTION HAD ERRORS")
    print("=" * 60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()