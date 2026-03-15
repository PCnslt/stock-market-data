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

### Primary Data Sources

**1. Yahoo Finance (via yfinance library)**
- Real-time and historical stock prices
- Company fundamentals and financials
- Market movers and sector data
- Cryptocurrency prices

**2. Alternative Free APIs (2026)**

| API | Free Tier Limits | Key Features | Best For |
|-----|------------------|--------------|----------|
| **Alpha Vantage** | 5 calls/min, 500/day | 50+ technical indicators, real-time & historical | Technical analysis, indicators |
| **Financial Modeling Prep** | 250 requests/day | Deep fundamental data, financial statements | Fundamental analysis |
| **Finnhub** | 60 calls/min, 500k/month | Real-time via WebSockets, institutional data | Real-time trading, fundamentals |
| **EODHD** | 20 requests/day | 30+ years historical, fundamental data | Historical analysis, backtesting |
| **Marketstack** | 100 requests/month | Global coverage, 30k+ tickers | International markets |
| **Twelve Data** | 800 requests/day | 100+ technical indicators, global | Technical analysis, global data |
| **Polygon.io** | 5 calls/min | High-frequency, real-time US markets | Intraday trading |

### Alternative Data Sources for Enhanced Prediction

**3. SEC Filings & Regulatory Data**
- **EDGAR Database** (SEC.gov) - Free access to all filings
- **Form 8-K** - Major events (CEO changes, bankruptcies, acquisitions)
- **Form 10-K/10-Q** - Annual/quarterly financial reports
- **Form 4** - Insider trading activity
- **Form 13F** - Institutional holdings

**4. News & Social Media Sentiment**
- **News APIs**: NewsAPI.org, GDELT Project
- **Social Media**: Twitter/X API, Reddit API
- **Sentiment Analysis**: VADER, TextBlob, custom NLP models
- **Web Scraping**: BeautifulSoup, Scrapy for financial news sites

**5. Alternative Data Categories**
- **Credit Card Transaction Data** - Consumer spending patterns
- **Satellite & Geospatial Data** - Parking lot traffic, shipping activity
- **Supply Chain Data** - Shipping movements, logistics
- **Weather Data** - Impact on agriculture, energy, retail
- **App Usage & Web Traffic** - Digital engagement metrics
- **Employment Data** - Job postings, hiring trends

**6. Economic & Macro Data**
- **Federal Reserve Economic Data (FRED)** - 800,000+ economic time series
- **Bureau of Labor Statistics (BLS)** - Employment, inflation data
- **Bureau of Economic Analysis (BEA)** - GDP, trade data
- **World Bank Open Data** - Global economic indicators

### Data Collection Strategy

**Phase 1: Core Market Data** ✅
- Yahoo Finance (yfinance) - Basic prices and fundamentals

**Phase 2: Enhanced APIs** 🔄
- Alpha Vantage - Technical indicators
- Financial Modeling Prep - Deep fundamentals
- Multiple API integration for redundancy

**Phase 3: Alternative Data** 📋
- SEC filings scraping
- News sentiment analysis
- Social media monitoring

**Phase 4: Specialized Data** 📋
- Economic indicators
- Geospatial/satellite data
- Supply chain analytics

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

### Phase 1: Core Data Collection (Current) ✅
**Status:** ✅ **COMPLETE AND OPERATIONAL**
- **Data Sources:** Yahoo Finance (yfinance)
- **Automation:** GitHub Actions daily workflow
- **PR System:** Auto-merge enabled
- **Data Collected:**
  - Top Gainers/Losers/Most Active
  - Major US Market Indices
  - Basic company information

### Phase 2: Enhanced Data Sources & Fundamentals 🔄
**Status:** 🔄 **IN DEVELOPMENT**
**Primary Goal:** Diversify data sources and enhance fundamentals

**Data Source Expansion:**
1. **Alpha Vantage API** - 50+ technical indicators
2. **Financial Modeling Prep** - Deep fundamental data
3. **Multiple API Integration** - Redundancy and data validation

**Enhanced Data Collection:**
4. **Company Fundamentals** - PE ratios, market cap, dividend yields, financial statements
5. **Sector Performance** - All 11 GICS sectors with ETFs
6. **Extended Market Coverage** - Russell 2000, VIX, sector ETFs
7. **Cryptocurrency Markets** - Top 10 cryptos by market cap

### Phase 3: Alternative Data Integration 📋
**Status:** 📋 **PLANNED**
**Primary Goal:** Incorporate alternative data for predictive edge

**Alternative Data Sources:**
8. **SEC Filings** - EDGAR database scraping (8-K, 10-K, Form 4)
9. **News Sentiment** - Financial news analysis and scoring
10. **Social Media Monitoring** - Twitter/Reddit sentiment analysis
11. **Economic Indicators** - FRED, BLS, BEA data integration
12. **Options Market Data** - Most active options, unusual activity

### Phase 4: Advanced Analytics & Global Expansion 📋
**Status:** 📋 **PLANNED**
**Primary Goal:** Global coverage and sophisticated analytics

**Global Data:**
13. **International Markets** - FTSE, DAX, Nikkei, Hang Seng, Shanghai
14. **Commodities & Futures** - Gold, oil, agricultural, treasury yields
15. **Specialized Data** - Weather, geospatial, supply chain data

**Analytics Enhancement:**
16. **Technical Indicators** - Moving averages, RSI, MACD, Bollinger Bands
17. **Market Sentiment** - Fear & Greed index, put/call ratio
18. **IPO Tracking** - Recent IPOs and performance analysis

### Phase 5: Machine Learning & Predictive Models 📋
**Status:** 📋 **PLANNED**
**Primary Goal:** Build predictive trading models

**ML Integration:**
- **Stock Price Prediction** - LSTM, Random Forest, XGBoost models
- **Market Trend Analysis** - Time series forecasting
- **Anomaly Detection** - Unusual market activity identification
- **Portfolio Optimization** - Risk-adjusted return maximization
- **Feature Engineering** - Create predictive features from collected data
- **Backtesting Framework** - Historical performance validation

### Data Source Strategy
**Multi-Source Validation:** Use 3+ data sources for critical data points
**Redundancy:** If one API fails, fall back to alternatives
**Data Quality:** Implement validation and cleaning pipelines
**Cost Optimization:** Balance free tier limits across multiple APIs

## 🎯 Current Status
- **Phase 1:** ✅ Complete and operational
- **Phase 2:** 🔄 In development
- **Phases 3-5:** 📋 Planned

## 📄 License
MIT License - see LICENSE file for details.