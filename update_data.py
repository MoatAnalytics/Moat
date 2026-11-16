import json
import math
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# Output field -> key in Ticker.info
INFO_FIELDS = {
    "trailing_pe": "trailingPE",
    "forward_pe": "forwardPE",
    "free_cash_flow": "freeCashflow",
    "enterprise_value": "enterpriseValue",
    "dividend_yield": "dividendYield",
    "price_to_book": "priceToBook",
    "total_debt": "totalDebt",
    "total_revenue": "totalRevenue",
    "operating_margins": "operatingMargins",
    "profit_margins": "profitMargins",
    "return_on_assets": "returnOnAssets",
    "return_on_equity": "returnOnEquity",
    "website": "website",
    "market_cap": "marketCap",
    "fifty_two_week_high": "fiftyTwoWeekHigh",
    "fifty_two_week_low": "fiftyTwoWeekLow",
}

# Output field -> row label in the balance sheet
BALANCE_FIELDS = {
    "cash_and_equivalents": "Cash And Cash Equivalents",
    "short_term_investments": "Other Short Term Investments",
    "total_liabilities": "Total Liabilities Net Minority Interest",
}

PRICE_LOOKBACKS = {
    "adj_close_1m": 1,
    "adj_close_6m": 6,
    "adj_close_12m": 12,
    "adj_close_36m": 36,
}


def clean(value):
    """Convert numpy/NaN values into JSON-safe Python values."""
    if value is None:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def price_at(series, months):
    """Last adjusted close on or before `months` months before the latest date."""
    target = series.index[-1] - pd.DateOffset(months=months)
    earlier = series[:target]
    return clean(round(float(earlier.iloc[-1]), 2)) if len(earlier) else None


def fetch_fundamentals(symbol):
    """Fetch info + balance sheet for one ticker (run in a worker thread)."""
    out = {}
    t = yf.Ticker(symbol)
    try:
        info = t.info or {}
    except Exception:
        info = {}
    for field, key in INFO_FIELDS.items():
        out[field] = clean(info.get(key))

    try:
        bs = t.balance_sheet
    except Exception:
        bs = None
    for field, label in BALANCE_FIELDS.items():
        value = None
        if bs is not None and not bs.empty and label in bs.index:
            row = bs.loc[label].dropna()
            value = clean(row.iloc[0]) if len(row) else None
        out[field] = value
    return out


# One batched, multi-threaded price download (4y covers the 36m lookback)
prices = yf.download(
    tickers_list,
    period="4y",
    auto_adjust=False,   # keeps the "Adj Close" column
    group_by="ticker",
    threads=True,
    progress=False,
)

# Fundamentals fetched in parallel, one thread per ticker
with ThreadPoolExecutor(max_workers=8) as pool:
    fundamentals = dict(zip(tickers_list, pool.map(fetch_fundamentals, tickers_list)))

stocks_data = []
for symbol in tickers_list:
    if isinstance(prices.columns, pd.MultiIndex):
        adj = prices[symbol]["Adj Close"] if symbol in prices.columns.get_level_values(0) else pd.Series(dtype=float)
    else:
        adj = prices["Adj Close"]
    adj = adj.dropna()

    row = {"ticker": symbol}
    row["last_adj_close"] = clean(round(float(adj.iloc[-1]), 2)) if len(adj) else None
    for field, months in PRICE_LOOKBACKS.items():
        row[field] = price_at(adj, months) if len(adj) else None
    row.update(fundamentals[symbol])
    stocks_data.append(row)

output_data = {
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data,
}

with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json")
