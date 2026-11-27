from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import random
import threading
import time
import yfinance as yf

tickers_list = [
    "NOW","TDG","VEEV","CRM","LSS.PA"]

# Remove duplicates while keeping order
tickers_list = list(dict.fromkeys(t.strip() for t in tickers_list if t.strip()))

FX_PAIRS_TO_EUR = ["USD", "GBP", "DKK", "NOK", "SEK", "CHF"]

# --- Rate-limit settings ---------------------------------------------------
MAX_WORKERS = 3            # few parallel workers
MIN_REQUEST_INTERVAL = 0.6 # min seconds between ANY two Yahoo requests (global)
MAX_RETRIES = 5            # retries per request when rate limited
BACKOFF_BASE = 30          # seconds; doubles each retry (30, 60, 120, ...)
PASS_COOLDOWN = 300        # seconds to wait before re-trying failed tickers
MAX_PASSES = 3             # full passes over tickers that failed


class RateLimitExhausted(Exception):
    pass


_lock = threading.Lock()
_next_slot = 0.0  # earliest time the next request may be sent


def _is_rate_limit(exc):
    name = type(exc).__name__
    msg = str(exc).lower()
    return (
        "ratelimit" in name.lower()
        or "too many requests" in msg
        or "429" in msg
        or "rate limit" in msg
    )


def call_with_retry(fn):
    """Run a yfinance call through a global throttle; back off on rate limits."""
    global _next_slot
    for attempt in range(MAX_RETRIES + 1):
        with _lock:
            now = time.monotonic()
            wait = max(0.0, _next_slot - now)
            _next_slot = max(now, _next_slot) + MIN_REQUEST_INTERVAL + random.uniform(0, 0.3)
        if wait:
            time.sleep(wait)
        try:
            return fn()
        except Exception as e:
            if not _is_rate_limit(e):
                raise
            if attempt == MAX_RETRIES:
                raise RateLimitExhausted(str(e))
            delay = BACKOFF_BASE * (2 ** attempt) + random.uniform(0, 5)
            print(f"Rate limited, pausing all workers for {delay:.0f}s...")
            with _lock:
                _next_slot = max(_next_slot, time.monotonic() + delay)


def get_latest_price(symbol):
    """Fetch only the latest price for a symbol using minimal data."""
    ticker = yf.Ticker(symbol)

    # Primary: 5-day daily history (avoids weekend/holiday empty 1d frames)
    try:
        hist = call_with_retry(lambda: ticker.history(period="5d", auto_adjust=True))
        if hist is not None and not hist.empty and "Close" in hist.columns:
            closes = hist["Close"].dropna()
            if not closes.empty:
                return float(closes.iloc[-1])
    except RateLimitExhausted:
        raise
    except Exception as e:
        print(f"History fallback for {symbol}: {e}")

    # Secondary fallback: fast_info.last_price
    try:
        last_price = call_with_retry(lambda: ticker.fast_info.get("last_price"))
        if last_price is not None and not (isinstance(last_price, float) and str(last_price) == "nan"):
            return float(last_price)
    except RateLimitExhausted:
        raise
    except Exception:
        pass

    return None


def fetch_fx_to_eur(ccy):
    """Return how many EUR equal 1 unit of `ccy` (e.g. USD/EUR)."""
    # Try direct pair first (e.g., USDEUR=X)
    direct = get_latest_price(f"{ccy}EUR=X")
    if direct is not None and direct > 0:
        return round(direct, 6)

    # Standard Yahoo convention is EURXXX=X (units of ccy per 1 EUR) -> invert
    inverse = get_latest_price(f"EUR{ccy}=X")
    if inverse is not None and inverse > 0:
        return round(1.0 / inverse, 6)

    return "N/A"


def fetch_ticker_price(ticker_symbol):
    print(f"Processing {ticker_symbol}...")
    price = get_latest_price(ticker_symbol)
    return {
        "ticker": ticker_symbol,
        "price": price if price is not None else "N/A",
    }


def run_pass(items, worker_fn):
    results, failed = {}, []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(worker_fn, item): item for item in items}
        for fut in as_completed(futures):
            item = futures[fut]
            try:
                results[item] = fut.result()
            except Exception as e:
                print(f"Failed {item}: {e}")
                failed.append(item)
    return results, failed


def run_with_retries(items, worker_fn, label="items"):
    all_results = {}
    pending = list(items)
    for n in range(1, MAX_PASSES + 1):
        res, pending = run_pass(pending, worker_fn)
        all_results.update(res)
        if not pending:
            break
        if n < MAX_PASSES:
            print(f"{len(pending)} {label} failed; cooling down {PASS_COOLDOWN}s before retry...")
            time.sleep(PASS_COOLDOWN)

    if pending:
        print(f"WARNING: still failed after {MAX_PASSES} passes ({label}): {pending}")

    return all_results


if __name__ == "__main__":
    # 1. Fetch stock prices
    stock_results = run_with_retries(tickers_list, fetch_ticker_price, label="tickers")
    stocks_data = [stock_results[t] for t in tickers_list if t in stock_results]

    # 2. Fetch FX rates (XXX/EUR)
    fx_results = run_with_retries(
        FX_PAIRS_TO_EUR,
        lambda ccy: {"pair": f"{ccy}/EUR", "rate": fetch_fx_to_eur(ccy)},
        label="FX pairs",
    )
    fx_data = {
        f"{ccy}/EUR": fx_results[ccy]["rate"]
        for ccy in FX_PAIRS_TO_EUR
        if ccy in fx_results
    }

    output_data = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "fx_rates": fx_data,
        "stocks": stocks_data,
    }

    with open("prices.json", "w") as f:
        json.dump(output_data, f, indent=4)

    print("Successfully wrote latest prices and FX rates to prices.json.")
