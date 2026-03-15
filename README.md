# Stock Market Data Repository

This repository runs three times daily using GitHub Actions, automatically collecting and storing comprehensive stock market data for analysis and prediction.

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

## Data Structure

```
data/
├── pre_market/YYYY-MM-DD/
│   ├── pre_market_movers.json
│   │   ├── gainers[]           # Pre-market gainers with price, change, volume
│   │   ├── losers[]            # Pre-market losers with price, change, volume
│   │   └── most_active[]       # Most active pre-market stocks
│   ├── futures.json
│   │   ├── equity_futures[]    # S&P, Nasdaq, Dow futures
│   │   ├── commodity_futures[] # Oil, gold, commodities
│   │   └── bond_futures[]      # Treasury yields, bond futures
│   ├── global_markets.json
│   │   ├── asia[]              # Asian market performance
│   │   ├── europe[]            # European market performance
│   │   └── americas[]          # Americas market performance
│   ├── economic_calendar.json
│   │   ├── date                # Event date
│   │   ├── events[]            # Economic events with time, importance
│   │   └── impact_analysis     # Market impact assessment
│   └── news_sentiment.json
│       ├── overall_sentiment   # Bullish/neutral/bearish
│       ├── positive_news[]     # Positive market news
│       └── negative_news[]     # Negative market news
├── mid_day/YYYY-MM-DD/
│   ├── morning_performance.json
│   │   ├── session_summary     # Morning session analysis
│   │   ├── top_performers[]    # Best performing stocks
│   │   └── sector_performance  # Sector-wise performance
│   ├── volatility_analysis.json
│   │   ├── vix_data            # Volatility index data
│   │   ├── option_activity     # Options market analysis
│   │   └── market_breadth      # Advance/decline ratios
│   ├── sector_rotation.json
│   │   ├── sector_changes[]    # Sector performance changes
│   │   ├── money_flow          # Institutional money flow
│   │   └── rotation_patterns   # Sector rotation analysis
│   ├── technical_indicators.json
│   │   ├── moving_averages     # MA crossovers, support/resistance
│   │   ├── momentum_indicators # RSI, MACD, stochastic
│   │   └── volume_analysis     # Volume patterns, accumulation
│   ├── news_sentiment_update.json
│   │   ├── breaking_news[]     # Mid-day news updates
│   │   ├── sentiment_trend     # Sentiment direction
│   │   └── market_reaction     # News impact analysis
│   └── trading_insights.json
│       ├── intraday_patterns   # Trading patterns identified
│       ├── institutional_flow  # Large trade analysis
│       └── market_microstructure # Order flow analysis
└── daily/YYYY-MM-DD/
    ├── market_summary.json
    │   ├── indices[]           # Major indices performance
    │   ├── volume_leaders[]    # Highest volume stocks
    │   └── market_breadth      # Overall market health
    ├── top_gainers.json
    │   ├── gainers[]           # Daily top gainers (price, % change)
    │   ├── breakout_stocks[]   # Technical breakout candidates
    │   └── momentum_analysis   # Momentum characteristics
    ├── top_losers.json
    │   ├── losers[]            # Daily top losers
    │   ├── oversold_stocks[]   # Potential bounce candidates
    │   └── weakness_analysis   # Sector/stock weakness patterns
    ├── sector_analysis.json
    │   ├── sector_performance[] # All sectors ranked
    │   ├── industry_leaders[]   # Top industries
    │   └── rotation_summary    # Daily rotation summary
    ├── technical_summary.json
    │   ├── key_levels          # Support/resistance levels
    │   ├── trend_analysis      # Market trend assessment
    │   └── pattern_recognition # Chart patterns identified
    └── prediction_features.json
        ├── feature_engineering # ML-ready features
        ├── target_variables    # Prediction targets (next day gainers)
        └── model_inputs        # Prepared data for ML models
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