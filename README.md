# Stock Market Data Repository

## Project Structure

```
stock-market-data/
├── data/
│   ├── pre_market/          # Pre-market data (8:00 AM UTC)
│   ├── mid_day/            # Mid-day analysis (1:00 PM UTC)
│   ├── daily/              # End-of-day data (9:00 PM UTC)
│   ├── historical/         # Long-term historical data
│   ├── processed/          # Aggregated and processed data
│   └── validation/         # Data quality reports
├── scripts/
│   ├── pre_market_collection.py
│   ├── mid_day_analysis.py
│   ├── collect_data.py
│   ├── create_pr.py
│   └── requirements.txt
└── .github/workflows/
    └── triple_daily_collection.yml
```

## Data Collection Schedule

| Time (UTC) | Collection Type | Description |
|------------|-----------------|-------------|
| 08:00 | Pre-market | Data before US market open |
| 13:00 | Mid-day | Morning session analysis |
| 21:00 | End-of-day | Complete market data |

**Note:** Collections run automatically on weekdays (Monday-Friday).

## On-Demand Collection

You can run data collection anytime:

```bash
# From the scripts directory
cd scripts

# Run all collection types
python run_on_demand.py

# Run specific type
python run_on_demand.py --type pre_market
python run_on_demand.py --type mid_day
python run_on_demand.py --type end_of_day
```

### GitHub Actions Manual Trigger:
1. Go to **Actions** → **Triple Daily Market Data Collection**
2. Click **Run workflow**
3. Select collection type
4. Click **Run workflow**

The on-demand script will fetch current market data and store it immediately.

## Available Data

### Pre-market Data
- Market movers before opening
- Futures and global market performance
- Economic calendar events
- News sentiment analysis

### Mid-day Analysis
- Morning session performance
- Sector rotation trends
- Volatility indicators
- Trading insights

### End-of-day Data
- Daily top gainers and losers
- Most active stocks
- Market indices performance
- Complete market summary

## How to Use This Repository

### Accessing Data
All data is organized by date in the respective directories:
- `data/pre_market/YYYY-MM-DD/`
- `data/mid_day/YYYY-MM-DD/`
- `data/daily/YYYY-MM-DD/`

### File Formats
- **JSON**: Configuration and structured data
- **CSV**: Tabular data for analysis
- **Markdown**: Documentation and summaries

### Automation
This repository uses automated workflows to:
- Collect data three times daily
- Create pull requests for each collection
- Auto-merge changes after validation
- Maintain data quality and consistency

## Data Quality

All collected data undergoes validation checks to ensure:
- Completeness of required fields
- Consistency across time periods
- Accuracy of calculations
- Proper formatting and structure

## Contributing

This repository is maintained through automated processes. Manual contributions should follow the established data structure and validation standards.

## License

This project contains financial market data collected from public sources. Use of this data is subject to the terms of the original data providers.