import json
from datetime import datetime
import yfinance as yf

tickers_list = ["AAPL", "MSFT", "GOOGL", "AMZN"]
stocks_data = []

for ticker_symbol in tickers_list:
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. Fetch info dictionary for metrics like EV, Dividend Yield, and Officers
    info = ticker.info
    
    enterprise_value = info.get("enterpriseValue")
    dividend_yield = info.get("dividendYield") # Usually a decimal like 0.0055 for 0.55%
    total_cash_fallback = info.get("totalCash")
    
    # Extract CEO Name from company officers
    ceo_name = "N/A"
    for officer in info.get("companyOfficers", []):
        title = officer.get("title", "").lower()
        if "ceo" in title or "chief executive officer" in title:
            ceo_name = officer.get("name", "N/A")
            break

    # 2. Get Next Earnings Date from calendar
    next_earnings = "N/A"
    try:
        cal = ticker.calendar
        if cal and "Earnings Date" in cal:
            earnings_dates = cal["Earnings Date"]
            if earnings_dates and len(earnings_dates) > 0:
                next_earnings = str(earnings_dates[0]).split()[0] # Keep date string only
    except Exception as e:
        print(f"Could not fetch earnings date for {ticker_symbol}: {e}")

    # 3. Get Balance Sheet metrics (Cash, Short-Term Investments, Liabilities)
    cash_equivalents = "N/A"
    short_term_investments = "N/A"
    total_liabilities = "N/A"
    
    try:
        bs = ticker.balance_sheet
        if not bs.empty:
            # Cash & Cash Equivalents
            for label in ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        cash_equivalents = float(val)
                        break
            if cash_equivalents == "N/A" and total_cash_fallback is not None:
                cash_equivalents = float(total_cash_fallback)
                
            # Short-Term Investments
            for label in ["Other Short Term Investments", "Short Term Investments"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        short_term_investments = float(val)
                        break
                        
            # Total Liabilities (from previous step, kept for completeness)
            for label in ["Total Liabilities Net Minority Interest", "Total Liabilities"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        total_liabilities = float(val)
                        break
    except Exception as e:
        print(f"Could not fetch balance sheet for {ticker_symbol}: {e}")

    # Append all compiled metrics
    stocks_data.append({
        "ticker": ticker_symbol,
        "ceo": ceo_name,
        "next_earnings": next_earnings,
        "enterprise_value": enterprise_value,
        "dividend_yield": round(dividend_yield * 100, 2) if dividend_yield is not None else "N/A",
        "cash_and_equivalents": cash_equivalents,
        "short_term_investments": short_term_investments,
        "total_liabilities": total_liabilities
    })

output_data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data
}

with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json with new financial fields.")
