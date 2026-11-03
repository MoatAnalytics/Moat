import json
from datetime import datetime
import yfinance as.yf if needed, or just yfinance
import yfinance as yf

# Define the tickers you want to track
tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]

stocks_data = []

for ticker_symbol in tickers_list:
    ticker = yf.Ticker(ticker_symbol)
    # Get recent history to find current price and daily change
    hist = ticker.history(period="2d")
    
    if len(hist) >= 2:
        current_price = hist['Close'].iloc[-1]
        previous_close = hist['Close'].iloc[-2]
        change_val = current_price - previous_close
        change_pct = (change_val / previous_close) * 100
        
        sign = "+" if change_pct >= 0 else ""
        change_str = f"{sign}{change_pct:.2f}%"
    else:
        current_price = hist['Close'].iloc[-1] if len(hist) > 0 else 0.0
        change_str = "0.00%"

    stocks_data.append({
        "ticker": ticker_symbol,
        "price": round(float(current_price), 2),
        "change": change_str
    })

# Build the final dictionary with timestamp
output_data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data
}

# Save to data.json
with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json")