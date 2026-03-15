#!/usr/bin/env python3
"""
Setup directory structure for triple daily data collection
"""

import os
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """Create the complete directory structure for triple daily data"""
    
    base_dirs = [
        "data/pre_market",
        "data/mid_day", 
        "data/daily",
        "data/historical/stocks",
        "data/historical/indices",
        "data/historical/sectors",
        "data/historical/crypto",
        "data/processed",
        "data/validation",
        "docs/improvements",
        "logs"
    ]
    
    print("Creating directory structure...")
    
    for dir_path in base_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {dir_path}")
    
    # Create .gitkeep files in empty directories
    gitkeep_dirs = [
        "data/pre_market",
        "data/mid_day",
        "data/historical/stocks",
        "data/historical/indices", 
        "data/historical/sectors",
        "data/historical/crypto",
        "data/processed",
        "data/validation",
        "docs/improvements",
        "logs"
    ]
    
    for dir_path in gitkeep_dirs:
        gitkeep_file = Path(dir_path) / ".gitkeep"
        gitkeep_file.touch(exist_ok=True)
        print(f"  ✓ Added .gitkeep to: {dir_path}")
    
    print("\n✅ Directory structure created successfully!")
    
    # Create README for data structure
    readme_content = """# Data Directory Structure

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
"""
    
    readme_path = Path("data/README.md")
    readme_path.write_text(readme_content)
    print(f"  ✓ Created: {readme_path}")
    
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("TRIPLE DAILY DATA COLLECTION - DIRECTORY SETUP")
    print("=" * 60)
    
    try:
        success = create_directory_structure()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ SETUP COMPLETE")
            print("\nDirectory structure is ready for triple daily data collection.")
            print("\nNext steps:")
            print("1. Ensure GitHub Actions workflow is configured")
            print("2. Test data collection scripts")
            print("3. Verify auto-merge functionality")
            print("4. Monitor first day of triple collection")
        else:
            print("❌ SETUP FAILED")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)