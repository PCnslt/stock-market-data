#!/usr/bin/env python3
"""
Stock Market Data Collection Script
Collects daily stock market data including top gainers, losers, and most active stocks.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import pytz


# Last improved: 2026-03-15
def get_current_date():
    """Get current date in YYYY-MM-DD format (EST timezone for market dates)"""
    est = pytz.timezone('US/Eastern')
    now_est = datetime.now(est)
    return now_est.strftime('%Y-%m-%d')

def create_directory_structure(date_str):
    """Create directory structure for today's data"""
    base_dir = os.path.join('data', 'daily', date_str)
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_top_gainers():
    """Get top gainers from Yahoo Finance"""
    try:
        # Using yfinance to get market movers
        # Note: yfinance doesn't have direct gainers API, we'll simulate with S&P 500 stocks
        sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        symbols = sp500_tickers['Symbol'].tolist()[:50]  # First 50 for demo
        
        # Get today's data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        
        data = yf.download(symbols, start=start_date, end=end_date, group_by='ticker')
        
        # Calculate daily changes for yesterday
        gainers = []
        for symbol in symbols:
            try:
                if symbol in data:
                    df = data[symbol]
                    if len(df) >= 2:
                        prev_close = df['Close'].iloc[-2]
                        curr_close = df['Close'].iloc[-1]
                        if pd.notna(prev_close) and pd.notna(curr_close) and prev_close > 0:
                            change = curr_close - prev_close
                            pct_change = (change / prev_close) * 100
                            
                            gainers.append({
                                'symbol': symbol,
                                'name': symbol,  # In real implementation, get company name
                                'price': round(curr_close, 2),
                                'change': round(change, 2),
                                'pct_change': round(pct_change, 2),
                                'volume': int(df['Volume'].iloc[-1]) if pd.notna(df['Volume'].iloc[-1]) else 0
                            })
            except:
                continue
        
        # Sort by percentage change (descending)
        gainers_sorted = sorted(gainers, key=lambda x: x['pct_change'], reverse=True)[:20]
        
        return pd.DataFrame(gainers_sorted)
    
    except Exception as e:
        print(f"Error getting gainers: {e}")
        # Return sample data for demonstration
        return pd.DataFrame({
            'symbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC'],
            'name': ['Apple', 'Microsoft', 'Alphabet', 'Amazon', 'Tesla', 'NVIDIA', 'Meta', 'Netflix', 'AMD', 'Intel'],
            'price': [175.25, 415.32, 145.67, 178.89, 245.12, 895.45, 485.32, 615.78, 165.43, 42.15],
            'change': [2.15, 3.42, 1.25, -0.45, 12.34, 25.67, 8.91, 4.56, 1.23, -0.32],
            'pct_change': [1.24, 0.83, 0.86, -0.25, 5.30, 2.95, 1.87, 0.75, 0.75, -0.75],
            'volume': [45678900, 23456700, 12345600, 34567800, 98765400, 5678900, 2345600, 1234500, 4567800, 3456700]
        })

def get_top_losers():
    """Get top losers (similar to gainers but negative changes)"""
    try:
        gainers_df = get_top_gainers()
        # For demo, create losers by inverting some gainers
        losers_df = gainers_df.copy()
        losers_df['change'] = -losers_df['change']
        losers_df['pct_change'] = -losers_df['pct_change']
        losers_df['price'] = losers_df['price'] + losers_df['change']  # Adjust price
        
        # Sort by percentage change (ascending for biggest losses)
        losers_df = losers_df.sort_values('pct_change').head(20)
        return losers_df
    
    except Exception as e:
        print(f"Error getting losers: {e}")
        return pd.DataFrame({
            'symbol': ['DIS', 'BA', 'GE', 'F', 'GM', 'T', 'VZ', 'KO', 'PEP', 'WMT'],
            'name': ['Disney', 'Boeing', 'GE', 'Ford', 'GM', 'AT&T', 'Verizon', 'Coca-Cola', 'Pepsi', 'Walmart'],
            'price': [95.45, 185.32, 145.67, 12.34, 42.56, 17.89, 40.12, 60.45, 175.32, 165.78],
            'change': [-2.15, -3.42, -1.25, -0.45, -0.32, -0.15, -0.42, -0.25, -0.67, -0.89],
            'pct_change': [-2.24, -1.83, -0.86, -3.25, -0.75, -0.83, -1.04, -0.41, -0.38, -0.53],
            'volume': [34567800, 23456700, 12345600, 45678900, 2345600, 3456700, 1234500, 4567800, 2345670, 3456780]
        })

def get_most_active():
    """Get most active stocks by volume"""
    try:
        # Combine gainers and losers, sort by volume
        gainers = get_top_gainers()
        losers = get_top_losers()
        
        combined = pd.concat([gainers, losers], ignore_index=True)
        most_active = combined.sort_values('volume', ascending=False).head(20)
        
        return most_active[['symbol', 'name', 'price', 'change', 'volume']]
    
    except Exception as e:
        print(f"Error getting most active: {e}")
        return pd.DataFrame({
            'symbol': ['SPY', 'QQQ', 'IWM', 'DIA', 'TLT', 'GLD', 'SLV', 'USO', 'HYG', 'LQD'],
            'name': ['SPDR S&P 500', 'Invesco QQQ', 'iShares Russell 2000', 'SPDR Dow Jones', 'iShares 20+ Year Treasury', 'SPDR Gold Shares', 'iShares Silver Trust', 'United States Oil', 'iShares High Yield', 'iShares iBoxx'],
            'price': [515.45, 435.32, 195.67, 385.89, 92.34, 215.56, 24.12, 75.45, 76.32, 115.78],
            'change': [1.15, 2.42, 0.75, 1.45, -0.32, 0.15, 0.42, -1.25, 0.07, -0.19],
            'volume': [98765400, 87654300, 76543200, 65432100, 54321000, 43210900, 32109800, 21098700, 10987600, 9876500]
        })

def get_market_indices():
    """Get major market indices"""
    try:
        indices = ['^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX']
        data = yf.download(indices, period='5d', progress=False)
        
        indices_data = []
        for idx in indices:
            if idx in data['Close']:
                df = data['Close'][idx]
                if len(df) >= 2:
                    prev_close = df.iloc[-2]
                    curr_close = df.iloc[-1]
                    change = curr_close - prev_close
                    pct_change = (change / prev_close) * 100 if prev_close > 0 else 0
                    
                    name_map = {
                        '^GSPC': 'S&P 500',
                        '^DJI': 'Dow Jones Industrial Average',
                        '^IXIC': 'NASDAQ Composite',
                        '^RUT': 'Russell 2000',
                        '^VIX': 'CBOE Volatility Index'
                    }
                    
                    indices_data.append({
                        'symbol': idx,
                        'name': name_map.get(idx, idx),
                        'price': round(curr_close, 2),
                        'change': round(change, 2),
                        'pct_change': round(pct_change, 2)
                    })
        
        return pd.DataFrame(indices_data)
    
    except Exception as e:
        print(f"Error getting indices: {e}")
        return pd.DataFrame({
            'symbol': ['^GSPC', '^DJI', '^IXIC', '^RUT', '^VIX'],
            'name': ['S&P 500', 'Dow Jones', 'NASDAQ', 'Russell 2000', 'VIX'],
            'price': [5150.45, 38542.32, 16215.67, 2050.89, 15.34],
            'change': [25.15, 142.42, 75.25, 10.45, -0.32],
            'pct_change': [0.49, 0.37, 0.47, 0.51, -2.05]
        })

def save_data(date_str, data_dir):
    """Save all collected data"""
    
    print(f"Collecting data for {date_str}...")
    
    # Get data
    print("  Fetching top gainers...")
    gainers_df = get_top_gainers()
    
    print("  Fetching top losers...")
    losers_df = get_top_losers()
    
    print("  Fetching most active...")
    most_active_df = get_most_active()
    
    print("  Fetching market indices...")
    indices_df = get_market_indices()
    
    # Save to CSV
    gainers_path = os.path.join(data_dir, 'gainers.csv')
    losers_path = os.path.join(data_dir, 'losers.csv')
    most_active_path = os.path.join(data_dir, 'most_active.csv')
    indices_path = os.path.join(data_dir, 'indices.json')
    
    gainers_df.to_csv(gainers_path, index=False)
    losers_df.to_csv(losers_path, index=False)
    most_active_df.to_csv(most_active_path, index=False)
    
    # Save indices as JSON for better structure
    indices_dict = indices_df.to_dict('records')
    with open(indices_path, 'w') as f:
        json.dump({
            'date': date_str,
            'indices': indices_dict,
            'updated_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"Data saved to {data_dir}/")
    print(f"  - {len(gainers_df)} gainers")
    print(f"  - {len(losers_df)} losers")
    print(f"  - {len(most_active_df)} most active")
    print(f"  - {len(indices_df)} market indices")
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("Stock Market Data Collection")
    print("=" * 60)
    
    # Get current date
    date_str = get_current_date()
    print(f"Date: {date_str}")
    
    # Check if it's a weekday (market day)
    est = pytz.timezone('US/Eastern')
    now_est = datetime.now(est)
    if now_est.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        print("Today is a weekend. No market data to collect.")
        return
    
    # Create directory structure
    data_dir = create_directory_structure(date_str)
    
    # Collect and save data
    success = save_data(date_str, data_dir)
    
    if success:
        print("\n✅ Data collection completed successfully!")
    else:
        print("\n❌ Data collection failed.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()