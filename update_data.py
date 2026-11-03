import json
from datetime import datetime
import yfinance as yf

tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]
stocks_data = []

for ticker_symbol in tickers_list:
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. Get valuation info
    info = ticker.info
    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    
    # 2. Get Total Liabilities from the Balance Sheet
    total_liabilities = "N/A"
    try:
        bs = ticker.balance_sheet
        if not bs.empty:
            # Look for common row labels used by Yahoo Finance for Total Liabilities
            for label in ["Total Liabilities Net Minority Interest", "Total Liabilities"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0] # Most recent period
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        total_liabilities = float(val)
                        break
    except Exception as e:
        print(f"Could not fetch balance sheet for {ticker_symbol}: {e}")

    # 3. Get Free Cash Flow from the Cash Flow Statement
    free_cash_flow = "N/A"
    try:
        cf = ticker.cashflow
        if not cf.empty:
            for label in ["Free Cash Flow"]:
                if label in cf.index:
                    val = cf.loc[label].iloc[0] # Most recent period
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        free_cash_flow = float(val)
                        break
    except Exception as e:
        print(f"Could not fetch cash flow for {ticker_symbol}: {e}")

    stocks_data.append({
        "ticker": ticker_symbol,
        "trailing_pe": round(trailing_pe, 2) if trailing_pe is not None else "N/A",
        "forward_pe": round(forward_pe, 2) if forward_pe is not None else "N/A",
        "total_liabilities": total_liabilities,
        "free_cash_flow": free_cash_flow
    })

output_data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data
}

with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json with P/E, Liabilities, and FCF")
