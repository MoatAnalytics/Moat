from datetime import datetime
import json
import pandas as pd
import yfinance as yf

tickers_list = [
    "NOW",
    "TDG",
    "VEEV",
    "CRM",
    "LR",
    "DUOL",
    "NFLX",
    "CRCT",
    "PYPL",
    "WKL.AS",
    "DASTY",
    "KNEBV.HE",
    "ALPM.PA",
    "FDS",
    "EBAY",
    "CPRT",
    "WMT",
    "NVDA",
    "PTON",
    "ASML",
    "HSIC",
    "IDXX",
    "ADSK",
    "V",
    "NEM",
    "TECN.SW",
    "IFCN.SW",
    "PHIA.AS",
    "EKTA-B.ST",
    "NOVO-B.CO",
    "TEL",
    "PLX",
    "KO",
    "AAPL",
    "GIVN.SW",
    "NOK",
    "ASSA-B.ST",
    "MICC",
    "SBUX",
    "XOM",
    "COST",
    "NKE",
    "TSLA",
    "OERL.SW",
    "CDNS",
    "ADYEN.AS",
    "AMS.MC",
    "MCD",
    "BA",
    "ZAL.DE",
    "SHOP",
    "SGPYY",
    "GAW.L",
    "WK",
    "MSCI",
    "TEMN.SW",
    "PLNT",
    "CSCO",
    "VRSK",
    "DE",
    "DIM.PA",
    "MTX.DE",
    "MC.PA",
    "SSNC",
    "DASH",
    "W",
    "QCOM",
    "BESI.AS",
    "INPOY",
    "DHR",
    "HD",
    "CAT",
    "PG",
    "DEO",
    "UHR.SW",
    "CFR.SW",
    "MGDDY",
    "OR.PA",
    "SY1.DE",
    "2UA.F",
    "RMV.L",
    "RR.L",
    "ITRK.L",
    "COLO-B.CO",
    "BATS.L",
    "SMIN",
    "ROR.L",
    "SPX.L",
    "AV",
    "SN.L",
    "BOY",
    "AI.PA",
    "DG.PA",
    "RI.PA",
    "SW.PA",
    "CPG.L",
    "EXPN",
    "FICO",
    "NEDAP.AS",
    "EDEN.PA",
]
stocks_data = []


def subtract_months(dt, months):
  year = dt.year - (months // 12)
  month = dt.month - (months % 12)
  if month <= 0:
    month += 12
    year -= 1
  days_in_month = [
      31,
      29
      if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
      else 28,
      31,
      30,
      31,
      30,
      31,
      31,
      30,
      31,
      30,
      31,
  ]
  day = min(dt.day, days_in_month[month - 1])
  return dt.replace(year=year, month=month, day=day)


# Calculate historical milestone dates relative to today
today = datetime.utcnow()
date_1m = subtract_months(today, 1)
date_6m = subtract_months(today, 6)
date_12m = subtract_months(today, 12)
date_36m = subtract_months(today, 36)

for ticker_symbol in tickers_list:
  print(f"Processing {ticker_symbol}...")
  ticker = yf.Ticker(ticker_symbol)

  # 1. Fetch info dictionary
  info = ticker.info

  trailing_pe = info.get("trailingPE")
  forward_pe = info.get("forwardPE")
  enterprise_value = info.get("enterpriseValue")
  dividend_yield = info.get("dividendYield")
  total_cash_fallback = info.get("totalCash")

  # Free Cash Flow (Current TTM)
  free_cash_flow = info.get("freeCashflow")
  if free_cash_flow is None:
    try:
      cf = ticker.cash_flow
      if not cf.empty and "Free Cash Flow" in cf.index:
        free_cash_flow = float(cf.loc["Free Cash Flow"].iloc[0])
      elif (
          not cf.empty
          and "Operating Cash Flow" in cf.index
          and "Capital Expenditure" in cf.index
      ):
        ocf = cf.loc["Operating Cash Flow"].iloc[0]
        capex = cf.loc["Capital Expenditure"].iloc[0]
        free_cash_flow = float(ocf + capex)
    except Exception:
      pass

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
        next_earnings = str(earnings_dates[0]).split()[0]
  except Exception as e:
    print(f"Could not fetch earnings date for {ticker_symbol}: {e}")

  # 3. Get Balance Sheet metrics
  cash_equivalents = "N/A"
  short_term_investments = "N/A"
  total_liabilities = "N/A"

  try:
    bs = ticker.balance_sheet
    if not bs.empty:
      for label in [
          "Cash And Cash Equivalents",
          "Cash Cash Equivalents And Short Term Investments",
      ]:
        if label in bs.index:
          val = bs.loc[label].iloc[0]
          if val is not None and not (
              isinstance(val, float) and str(val) == "nan"
          ):
            cash_equivalents = float(val)
            break
      if cash_equivalents == "N/A" and total_cash_fallback is not None:
        cash_equivalents = float(total_cash_fallback)

      for label in ["Other Short Term Investments", "Short Term Investments"]:
        if label in bs.index:
          val = bs.loc[label].iloc[0]
          if val is not None and not (
              isinstance(val, float) and str(val) == "nan"
          ):
            short_term_investments = float(val)
            break

      for label in [
          "Total Liabilities Net Minority Interest",
          "Total Liabilities",
      ]:
        if label in bs.index:
          val = bs.loc[label].iloc[0]
          if val is not None and not (
              isinstance(val, float) and str(val) == "nan"
          ):
            total_liabilities = float(val)
            break
  except Exception as e:
    print(f"Could not fetch balance sheet for {ticker_symbol}: {e}")

  # 4. Historical Prices (Last Adj Close & 1, 6, 12, 36 months ago)
  last_adj_close = "N/A"
  adj_close_1m = "N/A"
  adj_close_6m = "N/A"
  adj_close_12m = "N/A"
  adj_close_36m = "N/A"

  try:
    hist = ticker.history(period="4y")
    if not hist.empty and "Adj Close" in hist.columns:
      last_adj_close = float(hist["Adj Close"].iloc[-1])

      def get_price_at_date(target_dt):
        target_ts = pd.Timestamp(target_dt)
        if hist.index.tz is not None and target_ts.tz is None:
          target_ts = target_ts.tz_localize(hist.index.tz)
        sub_hist = hist[hist.index <= target_ts]
        if not sub_hist.empty:
          return float(sub_hist["Adj Close"].iloc[-1])
        return float(hist["Adj Close"].iloc[0])

      adj_close_1m = get_price_at_date(date_1m)
      adj_close_6m = get_price_at_date(date_6m)
      adj_close_12m = get_price_at_date(date_12m)
      adj_close_36m = get_price_at_date(date_36m)
  except Exception as e:
    print(f"Could not fetch historical prices for {ticker_symbol}: {e}")

  # Append all compiled metrics (forecasted FCF removed)
  stocks_data.append({
      "ticker": ticker_symbol,
      "trailing_pe": (
