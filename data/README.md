# Data Directory Structure

This repository follows a structured approach to stock market data collection.

## Main Data Directories

### 1. `data/pre_market/`
Pre-market data collected at 8:00 AM UTC (3:00 AM EST)
- Futures market data
- Global market performance
- Economic calendar
- News sentiment
- Pre-market movers

### 2. `data/mid_day/`
Mid-day analysis collected at 1:00 PM UTC (8:00 AM EST)
- Morning session performance
- Sector rotation analysis
- Volatility indicators
- Technical analysis
- Trading insights

### 3. `data/daily/`
End-of-day data collected at 9:00 PM UTC (4:00 PM EST)
- Complete market data
- Top gainers/losers/active
- Market indices
- Full day analysis

### 4. `data/historical/`
Long-term historical data storage
- `stocks/`: Individual stock time series
- `indices/`: Market index historical data
- `sectors/`: Sector performance history
- `crypto/`: Cryptocurrency historical data

### 5. `data/processed/`
Aggregated and processed data
- Feature engineered datasets
- Model training data
- Analysis results

### 6. `data/validation/`
Data quality and validation reports
- Data integrity checks
- Validation reports
- Quality metrics

## File Naming Convention

All data files follow this pattern:
```
{data_type}/{YYYY-MM-DD}/{filename}.{ext}
```

Examples:
- `data/pre_market/2026-03-15/futures.json`
- `data/mid_day/2026-03-15/technical_indicators.json`
- `data/daily/2026-03-15/gainers.csv`

## Data Collection Schedule

| Time (UTC) | Time (EST) | Type | Description |
|------------|------------|------|-------------|
| 08:00 | 03:00 | Pre-market | Before US market open |
| 13:00 | 08:00 | Mid-day | Morning session analysis |
| 21:00 | 16:00 | End-of-day | After market close |

## Notes
- Weekend data collection follows different schedule
- All times are in UTC (Coordinated Universal Time)
- Data is automatically collected via GitHub Actions
- PRs are auto-merged after successful collection
