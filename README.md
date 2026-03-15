# Stock Market Data Repository

A daily collection of stock market data including top gainers, losers, and most active stocks.

**Last updated:** 2026-03-15

## 📊 Data Collected Daily

### 1. Market Movers
**Top Gainers**
- Stocks with highest percentage gains for the day
- **Data Points:** Symbol, Name, Price, Change, % Change, Volume, Market Cap, PE Ratio, 52-Week Range

**Top Losers**
- Stocks with highest percentage losses for the day
- **Data Points:** Symbol, Name, Price, Change, % Change, Volume, Market Cap, PE Ratio, 52-Week Range

**Most Active**
- Stocks with highest trading volume
- **Data Points:** Symbol, Name, Price, Change, Volume, Market Cap, Average Volume

### 2. Market Indices & ETFs
**Major US Indices**
- S&P 500 (^GSPC): Price, Change, % Change, Volume
- Dow Jones Industrial Average (^DJI): Price, Change, % Change, Volume
- NASDAQ Composite (^IXIC): Price, Change, % Change, Volume
- Russell 2000 (^RUT): Small-cap performance
- VIX Volatility Index (^VIX): Market volatility

**Sector ETFs**
- Technology (XLK), Financials (XLF), Healthcare (XLV), Energy (XLE)
- Consumer Discretionary (XLY), Consumer Staples (XLP), Industrials (XLI)
- Materials (XLB), Real Estate (XLRE), Utilities (XLU), Communication (XLC)

### 3. Sector Performance
- Daily performance by sector (11 GICS sectors)
- Top gainers/losers within each sector
- Sector rotation trends

### 4. Cryptocurrency Markets
**Major Cryptos**
- Bitcoin (BTC-USD): Price, Change, % Change, Volume, Market Cap
- Ethereum (ETH-USD): Price, Change, % Change, Volume, Market Cap
- Top 10 cryptocurrencies by market cap

### 5. Options Market Data
**Most Active Options**
- Highest volume options contracts
- **Data Points:** Symbol, Strike, Expiry, Type (Call/Put), Volume, Open Interest, Last Price

**Unusual Options Activity**
- Large block trades
- Sweeps and unusual volume patterns

### 6. Futures & Commodities
**Commodities**
- Gold (GC=F), Silver (SI=F), Copper (HG=F)
- Crude Oil (CL=F), Natural Gas (NG=F)
- Agricultural commodities (Corn, Wheat, Soybeans)

**Interest Rates**
- 10-Year Treasury Yield (^TNX)
- 30-Year Treasury Yield (^TYX)
- Federal Funds Rate expectations

### 7. Global Markets
**Major International Indices**
- FTSE 100 (^FTSE) - UK
- DAX (^GDAXI) - Germany
- CAC 40 (^FCHI) - France
- Nikkei 225 (^N225) - Japan
- Hang Seng (^HSI) - Hong Kong
- Shanghai Composite (000001.SS) - China

### 8. Economic Indicators
**Daily Updates**
- US Dollar Index (DXY)
- Fear & Greed Index
- Put/Call Ratio
- Advance/Decline Ratio
- New Highs/New Lows

### 9. Company Fundamentals (Sample)
**For top 50 S&P 500 companies**
- Earnings dates and estimates
- Dividend yield and history
- Analyst ratings and price targets
- Institutional ownership
- Short interest data

### 10. Technical Indicators
**For major indices and top stocks**
- Moving averages (50-day, 200-day)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume profile

### 11. Market Sentiment
**Social & News Sentiment**
- Trending stock discussions
- News sentiment analysis
- Social media mentions volume
- Analyst upgrade/downgrade alerts

### 12. IPO & New Listings
**Recent IPOs**
- Performance since IPO
- Lockup expiration dates
- Analyst coverage initiation

## 📁 Enhanced Repository Structure

```
stock-market-data/
├── data/
│   ├── daily/                    # Daily snapshots
│   │   └── YYYY-MM-DD/          # Date folders
│   │       ├── gainers.csv      # Top gainers with fundamentals
│   │       ├── losers.csv       # Top losers with fundamentals
│   │       ├── most_active.csv  # Most active stocks
│   │       ├── indices.json     # Market indices
│   │       ├── sectors.csv      # Sector performance
│   │       ├── crypto.csv       # Cryptocurrency data
│   │       ├── options.csv      # Options activity
│   │       ├── futures.json     # Commodities & futures
│   │       ├── global.csv       # Global markets
│   │       ├── economic.json    # Economic indicators
│   │       ├── fundamentals/    # Company fundamentals
│   │       ├── technical/       # Technical indicators
│   │       └── sentiment/       # Market sentiment data
│   ├── historical/              # Historical time series
│   │   ├── stocks/              # Individual stock data
│   │   ├── indices/             # Market indices data
│   │   ├── sectors/             # Sector performance history
│   │   └── crypto/              # Cryptocurrency history
│   └── processed/               # Aggregated/processed data
├── scripts/
│   ├── collect_data.py          # Main data collection script
│   ├── collect_fundamentals.py  # Company fundamentals
│   ├── collect_technical.py     # Technical indicators
│   ├── collect_sentiment.py     # Market sentiment
│   ├── update_repo.py           # Repository update script
│   └── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── daily-collection.yml # GitHub Actions workflow
└── .gitignore
```

## 🚀 Setup

### Prerequisites
- Python 3.8+
- Git
- GitHub account

### Installation
```bash
git clone https://github.com/PCnslt/stock-market-data.git
cd stock-market-data
pip install -r scripts/requirements.txt
```

## 🔧 Usage

### Manual Data Collection
```bash
cd scripts
python collect_data.py
```

### Automated Daily Collection
The repository uses GitHub Actions to automatically collect data daily at 9:00 PM UTC.

## 📈 Data Sources
- Yahoo Finance (via yfinance library)
- Real-time market data

## 📅 Update Schedule

### Daily Workflow
- **Weekdays (Mon-Fri)**: Stock market data collection via Pull Requests
- **Saturdays**: Weekly summary and analysis via Pull Requests
- **Sundays**: Code improvements and maintenance via Pull Requests
- **Schedule**: Daily at 21:00 UTC (4:00 PM EST, 1:00 PM PST)

### PR Automation
- Automated Pull Request creation for daily updates
- Different activity types for each day of the week
- Manual review and merge required (auto-merge can be configured)

## 🤝 Contributing
This repository is automatically maintained. For issues or suggestions, please open an issue.

## 🗺️ Implementation Roadmap

### Phase 1: Core Data Collection (Current)
✅ **Completed**
- Basic market movers (gainers, losers, most active)
- Major market indices
- Daily automation via GitHub Actions
- PR workflow with auto-merge

### Phase 2: Enhanced Fundamentals (Next)
**Additional Data Points:**
1. **Company Fundamentals** - PE ratios, market cap, dividend yields
2. **Sector Performance** - All 11 GICS sectors
3. **Extended Market Indices** - Russell 2000, VIX, sector ETFs
4. **Cryptocurrency Markets** - Top 10 cryptos by market cap

### Phase 3: Advanced Analytics
**Technical & Sentiment:**
5. **Technical Indicators** - Moving averages, RSI, MACD
6. **Options Market Data** - Most active options, unusual activity
7. **Market Sentiment** - News analysis, social media trends
8. **Economic Indicators** - Fear & Greed index, put/call ratio

### Phase 4: Global Expansion
**International Markets:**
9. **Global Indices** - FTSE, DAX, Nikkei, Hang Seng, Shanghai
10. **Commodities & Futures** - Gold, oil, treasury yields
11. **Company Fundamentals** - Top 50 S&P 500 companies
12. **IPO Tracking** - Recent IPOs and performance

### Phase 5: Machine Learning Integration
**Predictive Analytics:**
- Stock price prediction models
- Market trend analysis
- Anomaly detection
- Portfolio optimization

## 🎯 Current Status
- **Phase 1:** ✅ Complete and operational
- **Phase 2:** 🔄 In development
- **Phases 3-5:** 📋 Planned

## 📄 License
MIT License - see LICENSE file for details.