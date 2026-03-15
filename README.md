# Stock Market Data Repository

A daily collection of stock market data including top gainers, losers, and most active stocks.

**Last updated:** 2026-03-15

## 📊 Data Collected Daily

### 1. Top Gainers
- Stocks with highest percentage gains for the day
- Includes: Symbol, Name, Price, Change, % Change, Volume

### 2. Top Losers  
- Stocks with highest percentage losses for the day
- Includes: Symbol, Name, Price, Change, % Change, Volume

### 3. Most Active
- Stocks with highest trading volume
- Includes: Symbol, Name, Price, Change, Volume

### 4. Market Indices
- S&P 500 (^GSPC)
- Dow Jones Industrial Average (^DJI)
- NASDAQ Composite (^IXIC)

## 📁 Repository Structure

```
stock-market-data/
├── data/
│   ├── daily/              # Daily snapshots
│   │   └── YYYY-MM-DD/     # Date folders
│   │       ├── gainers.csv
│   │       ├── losers.csv
│   │       ├── most_active.csv
│   │       └── indices.json
│   ├── historical/         # Historical time series
│   │   ├── stocks/         # Individual stock data
│   │   └── indices/        # Market indices data
│   └── processed/          # Aggregated/processed data
├── scripts/
│   ├── collect_data.py     # Data collection script
│   ├── update_repo.py      # Repository update script
│   └── requirements.txt    # Python dependencies
├── .github/
│   └── workflows/
│       └── daily-collection.yml  # GitHub Actions workflow
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

## 📄 License
MIT License - see LICENSE file for details.