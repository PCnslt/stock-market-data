#!/usr/bin/env python3
"""
Weekly Summary Script
Generates a weekly summary of stock market data for Saturday updates.
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import pytz
import glob

def get_week_dates():
    """Get dates for the past week (Monday to Friday)"""
    est = pytz.timezone('US/Eastern')
    today = datetime.now(est)
    
    # Find most recent Friday (or today if Friday)
    days_since_friday = (today.weekday() - 4) % 7
    last_friday = today - timedelta(days=days_since_friday)
    
    # Get Monday of that week
    last_monday = last_friday - timedelta(days=4)
    
    # Generate all weekdays
    week_dates = []
    current = last_monday
    while current <= last_friday:
        week_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    return week_dates

def load_weekly_data():
    """Load data from the past week"""
    week_dates = get_week_dates()
    all_gainers = []
    all_losers = []
    
    for date_str in week_dates:
        data_dir = os.path.join('..', 'data', 'daily', date_str)
        
        # Load gainers
        gainers_path = os.path.join(data_dir, 'gainers.csv')
        if os.path.exists(gainers_path):
            df = pd.read_csv(gainers_path)
            df['date'] = date_str
            all_gainers.append(df)
        
        # Load losers
        losers_path = os.path.join(data_dir, 'losers.csv')
        if os.path.exists(losers_path):
            df = pd.read_csv(losers_path)
            df['date'] = date_str
            all_losers.append(df)
    
    gainers_df = pd.concat(all_gainers, ignore_index=True) if all_gainers else pd.DataFrame()
    losers_df = pd.concat(all_losers, ignore_index=True) if all_losers else pd.DataFrame()
    
    return gainers_df, losers_df, week_dates

def analyze_weekly_performance(gainers_df, losers_df):
    """Analyze weekly performance"""
    analysis = {
        'summary': {},
        'top_performers': [],
        'consistent_gainers': [],
        'market_volatility': {}
    }
    
    if not gainers_df.empty:
        # Weekly summary
        analysis['summary']['total_days'] = gainers_df['date'].nunique()
        analysis['summary']['unique_stocks'] = gainers_df['symbol'].nunique()
        analysis['summary']['avg_daily_gainers'] = len(gainers_df) / analysis['summary']['total_days'] if analysis['summary']['total_days'] > 0 else 0
        
        # Top performers (highest average gain)
        stock_performance = gainers_df.groupby('symbol').agg({
            'pct_change': 'mean',
            'price': 'last',
            'name': 'first'
        }).reset_index()
        
        top_performers = stock_performance.nlargest(10, 'pct_change')
        analysis['top_performers'] = top_performers.to_dict('records')
        
        # Stocks that appeared multiple days
        stock_counts = gainers_df['symbol'].value_counts()
        consistent_stocks = stock_counts[stock_counts >= 2].index.tolist()
        if consistent_stocks:
            consistent_data = gainers_df[gainers_df['symbol'].isin(consistent_stocks)]
            analysis['consistent_gainers'] = consistent_data.groupby('symbol').agg({
                'pct_change': 'mean',
                'date': 'count',
                'name': 'first'
            }).rename(columns={'date': 'days_appeared'}).reset_index().to_dict('records')
    
    # Volatility analysis
    if not gainers_df.empty and not losers_df.empty:
        all_changes = pd.concat([gainers_df['pct_change'], losers_df['pct_change'].abs()])
        analysis['market_volatility'] = {
            'avg_change': round(all_changes.mean(), 2),
            'max_change': round(all_changes.max(), 2),
            'min_change': round(all_changes.min(), 2),
            'std_dev': round(all_changes.std(), 2)
        }
    
    return analysis

def generate_summary_report(analysis, week_dates):
    """Generate a markdown summary report"""
    report = f"""# Weekly Stock Market Summary

## Week of {week_dates[0]} to {week_dates[-1]}

### 📊 Weekly Overview
- **Trading Days**: {analysis['summary'].get('total_days', 0)}
- **Unique Stocks in Gainers**: {analysis['summary'].get('unique_stocks', 0)}
- **Average Daily Gainers**: {analysis['summary'].get('avg_daily_gainers', 0):.1f}

### 🏆 Top Performers of the Week
"""
    
    if analysis['top_performers']:
        for i, stock in enumerate(analysis['top_performers'][:5], 1):
            report += f"{i}. **{stock['symbol']}** ({stock['name']}): {stock['pct_change']:.2f}% average gain\n"
    else:
        report += "No data available for this week.\n"
    
    report += "\n### 🔄 Consistent Gainers\n"
    if analysis['consistent_gainers']:
        for stock in analysis['consistent_gainers'][:5]:
            report += f"- **{stock['symbol']}**: Appeared {stock['days_appeared']} days, {stock['pct_change']:.2f}% avg gain\n"
    else:
        report += "No stocks appeared multiple days this week.\n"
    
    if analysis['market_volatility']:
        vol = analysis['market_volatility']
        report += f"""
### 📈 Market Volatility
- **Average Daily Change**: {vol['avg_change']}%
- **Maximum Change**: {vol['max_change']}%
- **Minimum Change**: {vol['min_change']}%
- **Standard Deviation**: {vol['std_dev']}%

### 📅 Next Week Outlook
Based on this week's data, monitor the consistent gainers for potential continuation patterns.
"""
    
    return report

def save_weekly_summary(report, analysis):
    """Save weekly summary to file"""
    # Create weekly summary directory
    est = pytz.timezone('US/Eastern')
    today = datetime.now(est)
    week_end = today - timedelta(days=(today.weekday() - 4) % 7)  # Most recent Friday
    week_str = week_end.strftime('%Y-%m-%d')
    
    weekly_dir = os.path.join('..', 'data', 'weekly')
    os.makedirs(weekly_dir, exist_ok=True)
    
    # Save markdown report
    report_path = os.path.join(weekly_dir, f'summary_{week_str}.md')
    with open(report_path, 'w') as f:
        f.write(report)
    
    # Save analysis data
    data_path = os.path.join(weekly_dir, f'analysis_{week_str}.json')
    with open(data_path, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"Weekly summary saved to {report_path}")
    print(f"Analysis data saved to {data_path}")
    
    return report_path, data_path

def main():
    """Main function"""
    print("=" * 60)
    print("Weekly Stock Market Summary")
    print("=" * 60)
    
    # Load weekly data
    print("Loading data from the past week...")
    gainers_df, losers_df, week_dates = load_weekly_data()
    
    if gainers_df.empty:
        print("No data available for the past week.")
        # Create a placeholder report
        report = "# Weekly Stock Market Summary\n\nNo trading data available for the past week.\n"
        analysis = {'summary': {'total_days': 0, 'note': 'No data available'}}
    else:
        print(f"Loaded data for {len(week_dates)} days: {week_dates}")
        
        # Analyze data
        print("Analyzing weekly performance...")
        analysis = analyze_weekly_performance(gainers_df, losers_df)
        
        # Generate report
        print("Generating summary report...")
        report = generate_summary_report(analysis, week_dates)
    
    # Save summary
    report_path, data_path = save_weekly_summary(report, analysis)
    
    print("\n✅ Weekly summary completed!")
    print(f"Report: {report_path}")
    print(f"Data: {data_path}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()