import json
from datetime import datetime
import yfinance as yf

# Define the tickers you want to track
tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]

stocks_data = []

for ticker_symbol in tickers_list:
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetch the info dictionary containing fundamental metrics
    info = ticker.info
    
    # Extract Trailing P/E and Forward P/E safely
    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    
    stocks_data.append({
        "ticker": ticker_symbol,
        "trailing_pe": round(trailing_pe, 2) if trailing_pe is not None else "N/A",
        "forward_pe": round(forward_pe, 2) if forward_pe is not None else "N/A"
    })

# Build the final dictionary with timestamp
output_data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data
}

# Save to data.json
with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json with P/E ratios")
