#!/usr/bin/env python3
"""
import-amex.py — Parse Amex AU CSV statement files and merge into finance-data.json.

Reads CSV files from finance/amex/ and imports transactions, deduplicating by
hash-based transaction IDs. After import, checks for potential cross-source
duplicates between Amex and Airwallex transactions.

Amex AU CSV formats handled:
  Format A: Date, Description, Amount
    01/03/2026,ANTHROPIC API,-500.00

  Format B: Date, Reference, Amount, Description (with header row)
    Date,Reference,Amount,Description
    01/03/2026,1234567890,-500.00,ANTHROPIC API

  Format C: Date, Date Processed, Description, Card Member, Account #, Amount, Flexible (with header row)
    Date,Date Processed,Description,Card Member,Account #,Amount,Flexible
    01/03/2026,02/03/2026,ANTHROPIC API,{YOUR_NAME_UPPER},-XXXXX,500.00,FS

Usage:
  python3 finance-plugin/scripts/import-amex.py
  python3 finance-plugin/scripts/import-amex.py --file finance/amex/march-2026.csv

Requires:
  pip install requests python-dotenv
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

FINANCE_DATA_PATH = Path("finance/finance-data.json")
AMEX_DIR = Path("finance/amex")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env at repo root (for consistency)."""
    repo_root = Path(__file__).parent.parent.parent
    load_dotenv(repo_root / ".env")


def load_existing_finance_data() -> dict:
    """Load existing finance-data.json or return empty scaffold."""
    if FINANCE_DATA_PATH.exists():
        with open(FINANCE_DATA_PATH) as f:
            return json.load(f)
    return {
        "last_sync": None,
        "airwallex_account_id": "",
        "sync_status": "synced",
        "balances": {
            "snapshot_date": None,
            "accounts": [],
        },
        "categories": [
            {"category_id": "software", "label": "Software & Subscriptions", "monthly_budget": None},
            {"category_id": "hosting", "label": "Hosting & Infrastructure", "monthly_budget": None},
            {"category_id": "contractors", "label": "Contractors & Freelancers", "monthly_budget": None},
            {"category_id": "travel", "label": "Travel & Transport", "monthly_budget": None},
            {"category_id": "meals", "label": "Meals & Entertainment", "monthly_budget": None},
            {"category_id": "office", "label": "Office & Equipment", "monthly_budget": None},
            {"category_id": "marketing", "label": "Marketing & Advertising", "monthly_budget": None},
            {"category_id": "professional", "label": "Professional Services", "monthly_budget": None},
            {"category_id": "other", "label": "Other", "monthly_budget": None},
        ],
        "transactions": [],
        "leak_flags": [],
    }


def existing_transaction_ids(data: dict) -> set:
    """Get set of transaction IDs already in finance-data.json."""
    return {t["transaction_id"] for t in data.get("transactions", [])}


def generate_transaction_id(date: str, amount: float, description: str) -> str:
    """Generate deterministic transaction ID for dedup: amex_{sha256(date+amount+description)[:16]}."""
    raw = f"{date}{amount}{description}"
    hash_hex = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"amex_{hash_hex}"


def parse_date(date_str: str) -> str:
    """Parse DD/MM/YYYY Australian date format to YYYY-MM-DD."""
    date_str = date_str.strip()
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        # Try ISO format in case it's already YYYY-MM-DD
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print(f"Warning: Could not parse date '{date_str}', skipping row.", file=sys.stderr)
            return ""


def normalize_merchant_name(raw_name: str) -> str:
    """Normalize merchant name for consistent categorization."""
    if not raw_name:
        return ""
    name = raw_name.strip()
    # Remove common gateway prefixes
    for prefix in ("STRIPE* ", "SQ *", "PAYPAL *", "PP*", "GOOGLE *", "AMZN *", "AWS *"):
        if name.upper().startswith(prefix):
            name = name[len(prefix):].strip()
    # Remove trailing reference numbers (e.g., "ANTHROPIC 1234567")
    parts = name.rsplit(" ", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) >= 6:
        name = parts[0]
    # Title case
    name = name.title()
    return name


def detect_csv_format(rows: list) -> str:
    """Detect whether CSV is Format A (3 cols), Format B (4 cols), or Format C (7 cols with header)."""
    if not rows:
        return "unknown"

    first_row = rows[0]
    header_lower = [cell.strip().lower() for cell in first_row]

    # Format C: 7-column Amex activity export with "date processed" column
    if len(first_row) >= 7 and "date processed" in header_lower:
        return "C"

    # Check for header row (Format B)
    if first_row[0].strip().lower() == "date":
        return "B"

    # Format A: 3 columns (Date, Description, Amount)
    if len(first_row) == 3:
        return "A"

    # Format B without header: 4 columns (Date, Reference, Amount, Description)
    if len(first_row) == 4:
        return "B"

    return "unknown"


def parse_csv_file(filepath: Path) -> list:
    """Parse an Amex CSV file and return a list of raw transaction dicts."""
    transactions = []

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print(f"  Warning: {filepath.name} is empty, skipping.", file=sys.stderr)
        return []

    # Filter out empty rows
    rows = [r for r in rows if any(cell.strip() for cell in r)]

    fmt = detect_csv_format(rows)
    start_idx = 0

    if fmt in ("B", "C") and rows[0][0].strip().lower() == "date":
        start_idx = 1  # Skip header row

    for i, row in enumerate(rows[start_idx:], start=start_idx + 1):
        try:
            if fmt == "C" and len(row) >= 6:
                # Format C: Date, Date Processed, Description, Card Member, Account #, Amount, Flexible
                date_raw = row[0].strip()
                description = row[2].strip()
                amount_str = row[5].strip()
                reference = ""
            elif fmt == "A" and len(row) >= 3:
                date_raw = row[0].strip()
                description = row[1].strip()
                amount_str = row[2].strip()
                reference = ""
            elif fmt == "B" and len(row) >= 4:
                date_raw = row[0].strip()
                reference = row[1].strip()
                amount_str = row[2].strip()
                description = row[3].strip()
            elif fmt == "B" and len(row) == 3:
                # Format B without the reference column sometimes
                date_raw = row[0].strip()
                amount_str = row[1].strip()
                description = row[2].strip()
                reference = ""
            else:
                print(f"  Warning: {filepath.name} line {i} has unexpected format ({len(row)} columns), skipping.", file=sys.stderr)
                continue

            # Parse date
            date = parse_date(date_raw)
            if not date:
                continue

            # Parse amount
            amount_str = amount_str.replace(",", "").replace("$", "").strip()
            try:
                amount = float(amount_str)
            except ValueError:
                print(f"  Warning: {filepath.name} line {i} has invalid amount '{amount_str}', skipping.", file=sys.stderr)
                continue

            transactions.append({
                "date": date,
                "description": description,
                "amount": amount,
                "reference": reference,
            })

        except Exception as e:
            print(f"  Warning: {filepath.name} line {i} error: {e}, skipping.", file=sys.stderr)
            continue

    return transactions


def amex_to_transaction(raw: dict) -> dict:
    """Convert a parsed Amex CSV row to our finance-data.json transaction schema."""
    date = raw["date"]
    description = raw["description"]
    amount = raw["amount"]
    reference = raw["reference"]

    txn_id = generate_transaction_id(date, amount, description)

    # Amex AU: positive amounts are charges (expenses), negative are credits/payments
    direction = "debit" if amount > 0 else "credit"

    # Classify transaction type
    desc_upper = description.upper()
    if amount < 0 and "DIRECT DEBIT" in desc_upper:
        txn_class = "internal"  # Airwallex → Amex card payment
    elif amount < 0:
        txn_class = "refund"
    else:
        txn_class = "expense"

    return {
        "transaction_id": txn_id,
        "airwallex_id": None,
        "date": date,
        "posted_date": date,
        "amount": amount,
        "amount_aud": amount,
        "currency": "AUD",
        "direction": direction,
        "transaction_class": txn_class,
        "account_source": "amex",
        "merchant_name": description,
        "merchant_name_normalized": normalize_merchant_name(description),
        "merchant_category_code": "",
        "merchant_city": "",
        "merchant_country": "",
        "category_id": "",
        "category_confidence": "UNSET",
        "description": description,
        "reference": reference,
        "source": "amex_import",
        "source_type": "",
        "card_id": None,
        "card_last_four": None,
        "card_nickname": "",
        "transaction_type": "",
        "fx": {
            "original_amount": None,
            "original_currency": None,
            "fx_rate": None,
            "fx_source": None,
        },
        "reconciliation": {
            "status": "unmatched",
            "crm_entity_type": None,
            "crm_entity_id": None,
            "crm_document_id": None,
        },
        "receipt": {
            "attached": False,
            "file_path": None,
            "extracted_merchant": None,
            "extracted_amount": None,
            "extracted_date": None,
            "extracted_gst": None,
        },
        "tax": {
            "bas_period": None,
            "deductible": True,
            "r_and_d_eligible": False,
        },
        "tags": [],
        "notes": "",
        "gst_amount": None,
        "gst_status": "unknown",
    }


def check_cross_source_duplicates(finance_data: dict, new_txn_ids: set):
    """Check for potential duplicates between Amex and Airwallex transactions."""
    amex_txns = [t for t in finance_data["transactions"] if t.get("account_source") == "amex" and t["transaction_id"] in new_txn_ids]
    airwallex_txns = [t for t in finance_data["transactions"] if t.get("account_source") == "airwallex"]

    if not amex_txns or not airwallex_txns:
        return []

    potential_dupes = []

    for amex in amex_txns:
        amex_amount = abs(amex.get("amount", 0))
        amex_date = amex.get("date", "")
        if not amex_date:
            continue

        try:
            amex_dt = datetime.strptime(amex_date, "%Y-%m-%d")
        except ValueError:
            continue

        for aw in airwallex_txns:
            aw_amount = abs(aw.get("amount", 0))
            aw_date = aw.get("date", "")
            if not aw_date:
                continue

            try:
                aw_dt = datetime.strptime(aw_date, "%Y-%m-%d")
            except ValueError:
                continue

            # Same amount within $0.05 and date within 3 days
            amount_match = abs(amex_amount - aw_amount) <= 0.05
            date_match = abs((amex_dt - aw_dt).days) <= 3

            if amount_match and date_match:
                potential_dupes.append({
                    "amex_id": amex["transaction_id"],
                    "amex_desc": amex.get("description", ""),
                    "amex_amount": amex.get("amount", 0),
                    "amex_date": amex_date,
                    "airwallex_id": aw["transaction_id"],
                    "airwallex_desc": aw.get("description", ""),
                    "airwallex_amount": aw.get("amount", 0),
                    "airwallex_date": aw_date,
                })

    return potential_dupes


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Import Amex AU CSV statements into finance-data.json.")
    parser.add_argument("--file", type=str, default=None,
                        help="Specific CSV file to import. Default: all .csv files in finance/amex/.")
    args = parser.parse_args()

    # Load env for consistency with other scripts
    load_env()

    # Determine which files to process
    if args.file:
        csv_files = [Path(args.file)]
        if not csv_files[0].exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        if not AMEX_DIR.exists():
            print(f"Error: Amex directory not found: {AMEX_DIR}", file=sys.stderr)
            print(f"Create it and place CSV statement files there.", file=sys.stderr)
            sys.exit(1)

        csv_files = sorted(AMEX_DIR.glob("*.csv"))
        if not csv_files:
            print(f"No CSV files found in {AMEX_DIR}/", file=sys.stderr)
            sys.exit(1)

    print(f"Found {len(csv_files)} CSV file(s) to process.")

    # Load existing data for dedup
    finance_data = load_existing_finance_data()
    existing_ids = existing_transaction_ids(finance_data)

    new_count = 0
    skipped_count = 0
    new_txn_ids = set()
    total_parsed = 0

    for csv_file in csv_files:
        print(f"\nProcessing: {csv_file.name}")
        raw_transactions = parse_csv_file(csv_file)
        total_parsed += len(raw_transactions)
        print(f"  Parsed {len(raw_transactions)} rows.")

        file_new = 0
        file_skipped = 0

        for raw in raw_transactions:
            txn = amex_to_transaction(raw)

            if txn["transaction_id"] in existing_ids:
                file_skipped += 1
                skipped_count += 1
                continue

            finance_data["transactions"].append(txn)
            existing_ids.add(txn["transaction_id"])
            new_txn_ids.add(txn["transaction_id"])
            file_new += 1
            new_count += 1

        print(f"  New: {file_new} | Skipped (duplicates): {file_skipped}")

    # Sort transactions by date (newest first)
    finance_data["transactions"].sort(key=lambda t: t.get("date", ""), reverse=True)

    # Ensure output directory exists
    FINANCE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save
    with open(FINANCE_DATA_PATH, "w") as f:
        json.dump(finance_data, f, indent=2)

    print(f"\n{'─' * 50}")
    print(f"Done.")
    print(f"  Total rows parsed:       {total_parsed}")
    print(f"  New transactions:        {new_count}")
    print(f"  Skipped (duplicates):    {skipped_count}")
    print(f"  Total in finance-data.json: {len(finance_data['transactions'])}")
    print(f"  Saved to: {FINANCE_DATA_PATH}")

    # Check for potential cross-source duplicates
    if new_txn_ids:
        dupes = check_cross_source_duplicates(finance_data, new_txn_ids)
        if dupes:
            print(f"\n{'─' * 50}")
            print(f"POTENTIAL CROSS-SOURCE DUPLICATES ({len(dupes)} found):")
            print(f"These Amex transactions may already exist as Airwallex transactions.\n")
            for d in dupes:
                print(f"  Amex:      {d['amex_date']}  ${d['amex_amount']:>10.2f}  {d['amex_desc']}")
                print(f"  Airwallex: {d['airwallex_date']}  ${d['airwallex_amount']:>10.2f}  {d['airwallex_desc']}")
                print(f"  IDs: {d['amex_id']} <-> {d['airwallex_id']}")
                print()
        else:
            print(f"\n  No cross-source duplicates detected.")


if __name__ == "__main__":
    main()
