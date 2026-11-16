import json
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

# Define the tickers you want to track
tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# One batched, multi-threaded request for all tickers.
# period="5d" ensures we still get 2 trading days over weekends/holidays.
data = yf.download(
    tickers_list,
    period="5d",
    group_by="ticker",
    threads=True,
    progress=False,
)

stocks_data = []

for ticker_symbol in tickers_list:
    # Single-ticker downloads may come back with flat columns
    if isinstance(data.columns, pd.MultiIndex):
        close = data[ticker_symbol]["Close"] if ticker_symbol in data.columns.get_level_values(0) else pd.Series(dtype=float)
    else:
        close = data["Close"]
    close = close.dropna()

    if len(close) >= 2:
        current_price = close.iloc[-1]
        previous_close = close.iloc[-2]
        change_pct = (current_price - previous_close) / previous_close * 100
        sign = "+" if change_pct >= 0 else ""
        change_str = f"{sign}{change_pct:.2f}%"
    else:
        current_price = close.iloc[-1] if len(close) > 0 else 0.0
        change_str = "0.00%"

    stocks_data.append({
        "ticker": ticker_symbol,
        "price": round(float(current_price), 2),
        "change": change_str,
    })

# Build the final dictionary with timestamp
output_data = {
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data,
}

# Save to data.json
with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json")
