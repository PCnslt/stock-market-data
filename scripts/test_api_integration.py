#!/usr/bin/env python3
"""
Quick API integration test
"""

import os
import requests
import json
from datetime import datetime

def test_alpha_vantage():
    """Test Alpha Vantage API"""
    print("Testing Alpha Vantage API...")
    api_key = os.environ.get("ALPHA_VANTAGE_KEY", "")
    
    try:
        # Test with AAPL
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                print("✅ Alpha Vantage: Working")
                latest_date = list(data["Time Series (Daily)"].keys())[0]
                print(f"   Latest data: {latest_date}")
                return True
            else:
                print("⚠️ Alpha Vantage: No time series data")
                return False
        else:
            print(f"❌ Alpha Vantage: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Alpha Vantage Error: {e}")
        return False

def test_financial_modeling_prep():
    """Test Financial Modeling Prep API"""
    print("Testing Financial Modeling Prep API...")
    api_key = os.environ.get("FMP_KEY", "")
    
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/AAPL?apikey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                print("✅ Financial Modeling Prep: Working")
                print(f"   AAPL Price: ${data[0].get('price', 'N/A')}")
                return True
            else:
                print("⚠️ Financial Modeling Prep: No quote data")
                return False
        else:
            print(f"❌ Financial Modeling Prep: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Financial Modeling Prep Error: {e}")
        return False

def test_newsapi():
    """Test NewsAPI"""
    print("Testing NewsAPI...")
    api_key = os.environ.get("NEWSAPI_KEY", "")
    
    try:
        url = f"https://newsapi.org/v2/everything?q=Apple&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("✅ NewsAPI: Working")
                print(f"   Articles found: {data.get('totalResults', 0)}")
                return True
            else:
                print(f"⚠️ NewsAPI: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ NewsAPI: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ NewsAPI Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("=" * 60)
    print("API INTEGRATION TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {
        "alpha_vantage": test_alpha_vantage(),
        "financial_modeling_prep": test_financial_modeling_prep(),
        "newsapi": test_newsapi()
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    working = sum(results.values())
    total = len(results)
    
    print(f"Working APIs: {working}/{total}")
    
    if working == total:
        print("✅ All APIs working correctly!")
        print("\nReady for production data collection.")
    else:
        print("⚠️ Some APIs need attention.")
        print("\nCheck API keys and network connectivity.")
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)