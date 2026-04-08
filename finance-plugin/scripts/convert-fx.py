#!/usr/bin/env python3
"""
convert-fx.py — Convert non-AUD transactions to AUD using RBA daily exchange rates.

Reads finance-data.json, finds transactions where amount_aud is null,
fetches the RBA daily exchange rate for the transaction date and currency,
calculates the AUD equivalent, and updates the record.

RBA rates are cached locally in finance/rba-rates.json to avoid re-fetching.

Usage:
  python3 finance-plugin/scripts/convert-fx.py
  python3 finance-plugin/scripts/convert-fx.py --dry-run   # Preview without saving

Requires:
  pip install requests

SAFETY: Read-only against RBA. Only writes to local finance-data.json and cache.
"""

import argparse
import csv
import io
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

FINANCE_DATA_PATH = Path("finance/finance-data.json")
RATES_CACHE_PATH = Path("finance/rba-rates.json")

# RBA publishes daily exchange rates as CSV
# These are "units of foreign currency per 1 AUD"
# e.g., USD rate of 0.65 means 1 AUD = 0.65 USD, so 1 USD = 1/0.65 AUD
RBA_CSV_URL = "https://www.rba.gov.au/statistics/tables/csv/f11.1-data.csv"

# RBA series IDs for currencies we need
# Format: FXRUSD = units of USD per 1 AUD
RBA_SERIES = {
    "USD": "FXRUSD",
    "EUR": "FXREUR",
    "GBP": "FXRUKPS",
    "JPY": "FXRJPY",
    "CAD": "FXRCAD",
    "NZD": "FXRNZD",
    "CNY": "FXRCNY",
    "SGD": "FXRSGD",
    "HKD": "FXRHKD",
    "KRW": "FXRKRW",
    "IDR": "FXRIDR",
    "THB": "FXRTHB",
    "INR": "FXRINR",
    "MYR": "FXRMYR",
    "TWD": "FXRTWD",
    "VND": "FXRVND",
    "ZAR": "FXRZAR",
    "CHF": "FXRSFR",
    "SEK": "FXRSEK",
    "DKK": "FXRDKK",
    "NOK": "FXRNOK",
    "PHP": "FXRPHP",
    "PKR": "FXRPKR",
}


# ─── RBA Rate Fetching ───────────────────────────────────────────────────────

def load_cached_rates() -> dict:
    """Load cached RBA rates from disk."""
    if RATES_CACHE_PATH.exists():
        with open(RATES_CACHE_PATH) as f:
            return json.load(f)
    return {"last_fetched": None, "rates": {}}


def save_cached_rates(cache: dict):
    """Save RBA rates cache to disk."""
    RATES_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RATES_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def fetch_rba_rates() -> dict:
    """
    Fetch daily exchange rates from RBA CSV feed.
    Returns dict: { "USD": { "2025-01-15": 0.6234, ... }, "EUR": { ... }, ... }
    Rates are "units of foreign currency per 1 AUD".
    """
    print("Fetching RBA daily exchange rates...")
    resp = requests.get(RBA_CSV_URL, timeout=60)
    resp.raise_for_status()

    # RBA CSV has metadata rows at the top, then a header row, then data
    lines = resp.text.splitlines()

    # Find the header row (starts with "Series ID")
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("Series ID"):
            header_idx = i
            break

    if header_idx is None:
        print("Error: Could not find header row in RBA CSV.", file=sys.stderr)
        sys.exit(1)

    # Parse the series ID row and the Title row (one above header)
    reader = csv.reader(io.StringIO("\n".join(lines[header_idx:])))
    series_row = next(reader)  # Series IDs

    # Build column index: which column has which series
    series_to_col = {}
    for col_idx, series_id in enumerate(series_row):
        series_id = series_id.strip()
        for currency, rba_id in RBA_SERIES.items():
            if series_id == rba_id:
                series_to_col[currency] = col_idx
                break

    # Skip the "units" row
    next(reader)

    # Parse data rows
    rates = defaultdict(dict)
    for row in reader:
        if not row or not row[0].strip():
            continue
        date_str = row[0].strip()
        try:
            # RBA dates are DD-Mon-YYYY (e.g., "02-Jan-2025")
            dt = datetime.strptime(date_str, "%d-%b-%Y")
            iso_date = dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

        for currency, col_idx in series_to_col.items():
            if col_idx < len(row):
                val = row[col_idx].strip()
                if val and val not in ("", "N/A", "n/a"):
                    try:
                        rate = float(val)
                        if rate > 0:
                            rates[currency][iso_date] = rate
                    except ValueError:
                        pass

    print(f"  Loaded rates for {len(rates)} currencies.")
    for cur, dates in sorted(rates.items()):
        date_range = sorted(dates.keys())
        if date_range:
            print(f"    {cur}: {date_range[0]} → {date_range[-1]} ({len(dates)} days)")

    return dict(rates)


def get_rate_for_date(rates, currency, date):
    """
    Get the RBA rate for a currency on a specific date.
    If no rate for that exact date (weekend/holiday), use the most recent prior rate.
    Returns the rate as "units of foreign currency per 1 AUD".
    """
    currency_rates = rates.get(currency, {})
    if not currency_rates:
        return None

    # Try exact date
    if date in currency_rates:
        return currency_rates[date]

    # Walk backwards up to 7 days to find the most recent rate
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None

    for days_back in range(1, 8):
        prev = (dt - timedelta(days=days_back)).strftime("%Y-%m-%d")
        if prev in currency_rates:
            return currency_rates[prev]

    return None


def convert_to_aud(amount: float, rate: float) -> float:
    """
    Convert a foreign currency amount to AUD.
    RBA rate is "units of foreign currency per 1 AUD".
    So AUD = foreign_amount / rate.
    """
    if rate <= 0:
        return None
    return round(amount / rate, 2)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Convert non-AUD transactions to AUD using RBA rates.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview conversions without saving.")
    parser.add_argument("--force-refresh", action="store_true",
                        help="Re-fetch RBA rates even if cache exists.")
    args = parser.parse_args()

    # Load finance data
    if not FINANCE_DATA_PATH.exists():
        print("Error: finance-data.json not found. Run fetch-transactions.py first.", file=sys.stderr)
        sys.exit(1)

    with open(FINANCE_DATA_PATH) as f:
        data = json.load(f)

    # Find transactions needing conversion
    needs_conversion = [
        t for t in data["transactions"]
        if t.get("amount_aud") is None and (t.get("currency") or "AUD") != "AUD"
    ]

    if not needs_conversion:
        print("All transactions already have amount_aud. Nothing to convert.")
        return

    # Also add amount_aud to AUD transactions that are missing it
    aud_missing = [
        t for t in data["transactions"]
        if t.get("amount_aud") is None and (t.get("currency") or "AUD") == "AUD"
    ]
    for t in aud_missing:
        t["amount_aud"] = t["amount"]

    currencies_needed = set(t.get("currency", "") for t in needs_conversion)
    print(f"Transactions needing FX conversion: {len(needs_conversion)}")
    print(f"Currencies: {sorted(currencies_needed)}")
    print(f"AUD transactions backfilled with amount_aud: {len(aud_missing)}")

    # Load or fetch RBA rates
    cache = load_cached_rates()
    if args.force_refresh or not cache.get("rates"):
        rates = fetch_rba_rates()
        cache["rates"] = rates
        cache["last_fetched"] = datetime.utcnow().isoformat() + "Z"
        save_cached_rates(cache)
        print(f"  Cached to {RATES_CACHE_PATH}")
    else:
        rates = cache["rates"]
        print(f"Using cached rates from {cache.get('last_fetched', 'unknown')}")
        # Check if we have all needed currencies
        missing_currencies = currencies_needed - set(rates.keys())
        if missing_currencies:
            print(f"  Warning: No RBA rates for: {sorted(missing_currencies)}")
            print(f"  Re-fetching to check...")
            rates = fetch_rba_rates()
            cache["rates"] = rates
            cache["last_fetched"] = datetime.utcnow().isoformat() + "Z"
            save_cached_rates(cache)

    # Convert
    converted = 0
    failed = 0
    already_has_airwallex = 0

    for txn in needs_conversion:
        currency = txn.get("currency", "")
        date = txn.get("date", "")
        amount = txn.get("amount", 0)
        fx = txn.get("fx") or {}

        # Skip if already has an Airwallex-sourced AUD amount
        if fx.get("fx_source") == "airwallex" and txn.get("amount_aud") is not None:
            already_has_airwallex += 1
            continue

        # Try to get RBA rate
        rate = get_rate_for_date(rates, currency, date)
        if rate is None:
            failed += 1
            if not args.dry_run:
                # Leave amount_aud as None — flag for manual review
                pass
            continue

        aud_amount = convert_to_aud(amount, rate)
        if aud_amount is None:
            failed += 1
            continue

        if args.dry_run:
            desc = (txn.get("description") or txn.get("merchant_name") or "")[:40]
            print(f"  {date} {currency} {amount:>12,.2f} → AUD {aud_amount:>12,.2f} (rate: {rate}) {desc}")
        else:
            txn["amount_aud"] = aud_amount
            txn["fx"] = txn.get("fx") or {}
            txn["fx"]["fx_rate"] = rate
            txn["fx"]["fx_source"] = "rba"
            txn["fx"]["original_amount"] = amount
            txn["fx"]["original_currency"] = currency

        converted += 1

    print(f"\n{'─' * 50}")
    print(f"Converted: {converted}")
    print(f"Already had Airwallex rate: {already_has_airwallex}")
    print(f"Failed (no RBA rate available): {failed}")

    if failed > 0:
        # Show which ones failed
        failed_txns = [
            t for t in needs_conversion
            if t.get("amount_aud") is None and (t.get("currency") or "AUD") != "AUD"
        ]
        by_cur = defaultdict(int)
        for t in failed_txns:
            by_cur[t.get("currency", "")] += 1
        print(f"  Failed by currency: {dict(by_cur)}")

    if not args.dry_run and converted > 0:
        with open(FINANCE_DATA_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nSaved {FINANCE_DATA_PATH}")

    # Summary
    total = len(data["transactions"])
    has_aud = sum(1 for t in data["transactions"] if t.get("amount_aud") is not None)
    missing_aud = total - has_aud
    print(f"\nCoverage: {has_aud}/{total} transactions have amount_aud ({100*has_aud/total:.0f}%)")
    if missing_aud:
        print(f"  {missing_aud} still missing — may need manual rate entry")


if __name__ == "__main__":
    main()
