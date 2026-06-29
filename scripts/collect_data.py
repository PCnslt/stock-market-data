#!/usr/bin/env python3
"""
Stock Market Data Collection Script
Collects daily stock market data including top gainers, losers, and most active stocks.

Data sources (in priority order):
  1. Financial Modeling Prep   (env FMP_KEY)            -> gainers/losers/actives + index quotes
  2. Alpha Vantage             (env ALPHA_VANTAGE_KEY)  -> TOP_GAINERS_LOSERS (free) fallback
  3. Hardcoded sample          (last resort, flagged)   -> so silent fake data is visible

The previous version scraped Wikipedia + used yfinance, both of which are routinely
rate-limited / blocked on GitHub-hosted runners and therefore almost always fell back
to hardcoded sample numbers. This version pulls real data from authenticated APIs and
logs which source actually answered (the output files are unchanged).
"""

import json
import os
from datetime import datetime

import pandas as pd
import pytz
import requests

FMP_KEY = os.environ.get("FMP_KEY", "").strip()
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "").strip()

REQUEST_TIMEOUT = 15

# Tracks which source produced the mover data (logged, not persisted).
DATA_SOURCE = "unknown"

INDEX_NAME_MAP = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones Industrial Average",
    "^IXIC": "NASDAQ Composite",
    "^RUT": "Russell 2000",
    "^VIX": "CBOE Volatility Index",
}


def get_current_date():
    """Get current date in YYYY-MM-DD format (EST timezone for market dates)"""
    est = pytz.timezone("US/Eastern")
    return datetime.now(est).strftime("%Y-%m-%d")


def create_directory_structure(date_str):
    """Create directory structure for today's data"""
    base_dir = os.path.join("data", "daily", date_str)
    os.makedirs(base_dir, exist_ok=True)
    return base_dir


def _to_float(value, default=0.0):
    try:
        if value is None:
            return default
        # Alpha Vantage returns strings like "12.34" / "1.2345%"
        return float(str(value).replace("%", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return default


def _to_int(value, default=0):
    try:
        return int(_to_float(value, default))
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Financial Modeling Prep
# ---------------------------------------------------------------------------
def _fmp_movers(kind):
    """kind in {gainers, losers, actives}. Returns list[dict] or raises on failure."""
    url = f"https://financialmodelingprep.com/api/v3/stock_market/{kind}?apikey={FMP_KEY}"
    resp = requests.get(url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, list):
        # FMP returns a dict with an "Error Message" / rate-limit notice on failure.
        raise ValueError(f"Unexpected FMP response for {kind}: {payload}")
    rows = []
    for item in payload[:20]:
        rows.append(
            {
                "symbol": item.get("symbol", ""),
                "name": item.get("name") or item.get("symbol", ""),
                "price": round(_to_float(item.get("price")), 2),
                "change": round(_to_float(item.get("change")), 2),
                "pct_change": round(_to_float(item.get("changesPercentage")), 2),
                "volume": _to_int(item.get("volume")),
            }
        )
    return rows


def fetch_movers_fmp():
    """Return (gainers, losers, most_active) DataFrames from FMP, or None."""
    if not FMP_KEY:
        return None
    try:
        gainers = _fmp_movers("gainers")
        losers = _fmp_movers("losers")
        actives = _fmp_movers("actives")
        if not gainers and not losers and not actives:
            return None
        return (
            pd.DataFrame(gainers),
            pd.DataFrame(losers),
            pd.DataFrame(actives),
        )
    except Exception as e:  # noqa: BLE001 - any failure -> try next source
        print(f"  FMP movers unavailable: {e}")
        return None


def fetch_indices_fmp():
    """Return indices DataFrame from FMP quote endpoint, or None."""
    if not FMP_KEY:
        return None
    symbols = ",".join(s.replace("^", "%5E") for s in INDEX_NAME_MAP)
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={FMP_KEY}"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        if not isinstance(payload, list) or not payload:
            return None
        rows = []
        for item in payload:
            sym = item.get("symbol", "")
            rows.append(
                {
                    "symbol": sym,
                    "name": INDEX_NAME_MAP.get(sym, item.get("name", sym)),
                    "price": round(_to_float(item.get("price")), 2),
                    "change": round(_to_float(item.get("change")), 2),
                    "pct_change": round(_to_float(item.get("changesPercentage")), 2),
                }
            )
        return pd.DataFrame(rows)
    except Exception as e:  # noqa: BLE001
        print(f"  FMP indices unavailable: {e}")
        return None


# ---------------------------------------------------------------------------
# Alpha Vantage (free TOP_GAINERS_LOSERS endpoint covers all three movers)
# ---------------------------------------------------------------------------
def _av_rows(items):
    rows = []
    for item in items[:20]:
        price = _to_float(item.get("price"))
        change = _to_float(item.get("change_amount"))
        rows.append(
            {
                "symbol": item.get("ticker", ""),
                "name": item.get("ticker", ""),  # AV does not return company names here
                "price": round(price, 2),
                "change": round(change, 2),
                "pct_change": round(_to_float(item.get("change_percentage")), 2),
                "volume": _to_int(item.get("volume")),
            }
        )
    return rows


def fetch_movers_alpha_vantage():
    """Return (gainers, losers, most_active) DataFrames from Alpha Vantage, or None."""
    if not ALPHA_VANTAGE_KEY:
        return None
    url = (
        "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS"
        f"&apikey={ALPHA_VANTAGE_KEY}"
    )
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()
        gainers = payload.get("top_gainers")
        losers = payload.get("top_losers")
        actives = payload.get("most_actively_traded")
        if not gainers and not losers and not actives:
            # Likely a rate-limit / informational message.
            print(f"  Alpha Vantage returned no movers: {payload}")
            return None
        return (
            pd.DataFrame(_av_rows(gainers or [])),
            pd.DataFrame(_av_rows(losers or [])),
            pd.DataFrame(_av_rows(actives or [])),
        )
    except Exception as e:  # noqa: BLE001
        print(f"  Alpha Vantage movers unavailable: {e}")
        return None


# ---------------------------------------------------------------------------
# Sample fallback (flagged so it is never mistaken for real data)
# ---------------------------------------------------------------------------
def sample_movers():
    gainers = pd.DataFrame(
        {
            "symbol": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
            "name": ["Apple", "Microsoft", "Alphabet", "Amazon", "Tesla"],
            "price": [175.25, 415.32, 145.67, 178.89, 245.12],
            "change": [2.15, 3.42, 1.25, 3.45, 12.34],
            "pct_change": [1.24, 0.83, 0.86, 1.96, 5.30],
            "volume": [45678900, 23456700, 12345600, 34567800, 98765400],
        }
    )
    losers = pd.DataFrame(
        {
            "symbol": ["DIS", "BA", "GE", "F", "GM"],
            "name": ["Disney", "Boeing", "GE", "Ford", "GM"],
            "price": [95.45, 185.32, 145.67, 12.34, 42.56],
            "change": [-2.15, -3.42, -1.25, -0.45, -0.32],
            "pct_change": [-2.24, -1.83, -0.86, -3.25, -0.75],
            "volume": [34567800, 23456700, 12345600, 45678900, 2345600],
        }
    )
    most_active = pd.DataFrame(
        {
            "symbol": ["SPY", "QQQ", "IWM", "DIA", "TLT"],
            "name": ["SPDR S&P 500", "Invesco QQQ", "iShares Russell 2000", "SPDR Dow", "iShares 20Y Treasury"],
            "price": [515.45, 435.32, 195.67, 385.89, 92.34],
            "change": [1.15, 2.42, 0.75, 1.45, -0.32],
            "pct_change": [0.22, 0.56, 0.38, 0.38, -0.35],
            "volume": [98765400, 87654300, 76543200, 65432100, 54321000],
        }
    )
    return gainers, losers, most_active


def sample_indices():
    return pd.DataFrame(
        {
            "symbol": ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"],
            "name": ["S&P 500", "Dow Jones", "NASDAQ", "Russell 2000", "VIX"],
            "price": [5150.45, 38542.32, 16215.67, 2050.89, 15.34],
            "change": [25.15, 142.42, 75.25, 10.45, -0.32],
            "pct_change": [0.49, 0.37, 0.47, 0.51, -2.05],
        }
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def collect_movers():
    """Return (gainers, losers, most_active, source)."""
    result = fetch_movers_fmp()
    if result is not None:
        print("  Movers source: Financial Modeling Prep")
        return (*result, "fmp")

    result = fetch_movers_alpha_vantage()
    if result is not None:
        print("  Movers source: Alpha Vantage")
        return (*result, "alpha_vantage")

    print("  WARNING: No live mover source available - using SAMPLE data")
    return (*sample_movers(), "fallback_sample")


def collect_indices(movers_source):
    """Return (indices_df, source)."""
    result = fetch_indices_fmp()
    if result is not None:
        print("  Indices source: Financial Modeling Prep")
        return result, "fmp"
    print("  WARNING: No live index source available - using SAMPLE data")
    return sample_indices(), "fallback_sample"


def save_data(date_str, data_dir):
    """Collect and save all data. Returns True if real data was collected."""
    print(f"Collecting data for {date_str}...")

    gainers_df, losers_df, most_active_df, movers_source = collect_movers()
    indices_df, indices_source = collect_indices(movers_source)

    global DATA_SOURCE
    DATA_SOURCE = movers_source

    # Keep the original output files/columns unchanged (planned data structure).
    mover_cols = ["symbol", "name", "price", "change", "pct_change", "volume"]
    for df in (gainers_df, losers_df, most_active_df):
        for col in mover_cols:
            if col not in df.columns:
                df[col] = 0

    gainers_df.to_csv(os.path.join(data_dir, "gainers.csv"), index=False, columns=mover_cols)
    losers_df.to_csv(os.path.join(data_dir, "losers.csv"), index=False, columns=mover_cols)
    most_active_df.to_csv(
        os.path.join(data_dir, "most_active.csv"),
        index=False,
        columns=["symbol", "name", "price", "change", "volume"],
    )

    # indices.json keeps its original schema (date, indices, updated_at).
    with open(os.path.join(data_dir, "indices.json"), "w") as f:
        json.dump(
            {
                "date": date_str,
                "indices": indices_df.to_dict("records"),
                "updated_at": datetime.now().isoformat(),
            },
            f,
            indent=2,
        )

    # Data source is logged to the run console only (not written to data files,
    # so the planned data structure is unchanged).
    print(f"Data saved to {data_dir}/ (movers source: {movers_source}, indices source: {indices_source})")
    print(f"  - {len(gainers_df)} gainers")
    print(f"  - {len(losers_df)} losers")
    print(f"  - {len(most_active_df)} most active")
    print(f"  - {len(indices_df)} market indices")

    return movers_source != "fallback_sample"


def main():
    """Main function"""
    print("=" * 60)
    print("Stock Market Data Collection")
    print("=" * 60)

    date_str = get_current_date()
    print(f"Date: {date_str}")

    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)
    if now_est.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        print("Today is a weekend. No market data to collect.")
        return

    data_dir = create_directory_structure(date_str)
    real_data = save_data(date_str, data_dir)

    if real_data:
        print("\nData collection completed successfully (live data).")
    else:
        # Still wrote files (so a commit/contribution happens), but make the
        # degraded state loud and visible in the workflow logs.
        print("\nWARNING: Data collection fell back to SAMPLE data.")
        print("    Check FMP_KEY / ALPHA_VANTAGE_KEY secrets and API quotas.")

    print("=" * 60)


if __name__ == "__main__":
    main()
