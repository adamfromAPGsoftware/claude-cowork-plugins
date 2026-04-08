#!/usr/bin/env python3
"""
fetch-transactions.py — Pull transactions from Airwallex (READ-ONLY).

Fetches from TWO endpoints and merges:
  1. /api/v1/issuing/transactions — card spend with merchant name, MCC, city, country
  2. /api/v1/financial_transactions — wallet ledger for non-card items (transfers, fees, payouts)

Card transactions (issuing) are the primary source for spend analysis.
Financial transactions catch everything else (wire transfers, platform fees, conversions).

Usage:
  python3 finance-plugin/scripts/fetch-transactions.py --from-date 2026-03-01 --to-date 2026-04-01
  python3 finance-plugin/scripts/fetch-transactions.py  # defaults to last 90 days

Requires:
  pip install requests python-dotenv

SAFETY: This script ONLY uses GET endpoints (plus one POST for auth token).
        It NEVER calls payment, transfer, or any write endpoint.
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

FINANCE_DATA_PATH = Path("finance/finance-data.json")

API_BASES = {
    "demo": "https://api-demo.airwallex.com",
    "prod": "https://api.airwallex.com",
}

# Issuing endpoint max is ~200; financial_transactions supports larger pages
ISSUING_PAGE_SIZE = 200
FINANCIAL_PAGE_SIZE = 200


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env at repo root."""
    repo_root = Path(__file__).parent.parent.parent
    load_dotenv(repo_root / ".env")

    client_id = os.environ.get("AIRWALLEX_CLIENT_ID")
    api_key = os.environ.get("AIRWALLEX_API_KEY")
    environment = os.environ.get("AIRWALLEX_ENVIRONMENT", "demo")

    if not client_id:
        print("Error: AIRWALLEX_CLIENT_ID not set. Add it to .env at the repo root.", file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print("Error: AIRWALLEX_API_KEY not set. Add it to .env at the repo root.", file=sys.stderr)
        sys.exit(1)
    if environment not in API_BASES:
        print(f"Error: AIRWALLEX_ENVIRONMENT must be 'demo' or 'prod', got '{environment}'", file=sys.stderr)
        sys.exit(1)

    return client_id, api_key, environment


def authenticate(base_url: str, client_id: str, api_key: str) -> str:
    """
    Authenticate with Airwallex and return a Bearer token.
    This is the ONLY non-GET request in this script.
    """
    resp = requests.post(
        f"{base_url}/api/v1/authentication/login",
        headers={
            "x-client-id": client_id,
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if resp.status_code == 401:
        print("Error: Invalid Airwallex credentials. Check AIRWALLEX_CLIENT_ID and AIRWALLEX_API_KEY.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    token = resp.json().get("token")
    if not token:
        print("Error: No token in authentication response.", file=sys.stderr)
        sys.exit(1)
    return token


def api_get(base_url: str, token: str, path: str, params: dict = None) -> dict:
    """Make a GET request to Airwallex. GET only — no writes."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    resp = requests.get(f"{base_url}{path}", headers=headers, params=params or {}, timeout=30)
    if resp.status_code == 401:
        print("Error: Token expired or invalid.", file=sys.stderr)
        sys.exit(1)
    if resp.status_code == 429:
        print("Error: Airwallex rate limit hit. Wait a moment and retry.", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


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


# ─── Issuing Transaction Converter ───────────────────────────────────────────

def issuing_to_transaction(item: dict) -> dict:
    """Convert an issuing/transactions API item to our schema.

    Issuing transactions have rich merchant data:
      merchant.name, merchant.category_code (MCC), merchant.city, merchant.country
    """
    txn_id = item.get("transaction_id", "")
    merchant = item.get("merchant", {}) or {}

    # Amounts — always prefer billing (AUD) over transaction currency.
    # billing_amount can be 0 for AUTHORIZATION records — only fall back to
    # txn_amount if billing_amount is explicitly None/missing.
    billing_amount = item.get("billing_amount")
    txn_amount = item.get("transaction_amount", 0)
    billing_currency = item.get("billing_currency", "")
    txn_currency = item.get("transaction_currency", "")

    if billing_amount is not None and billing_amount != 0:
        # Have a real billing amount — use it (this is the AUD equivalent)
        amount = billing_amount
        currency = billing_currency or "AUD"
    elif billing_currency and billing_currency != txn_currency:
        # billing_amount is 0 but currencies differ — this is an AUTH hold
        # or uncleared transaction. Store in original currency with FX metadata
        # so the RBA rates script can convert it later.
        amount = txn_amount
        currency = txn_currency or "AUD"
    else:
        # Same currency or no billing info — use transaction amount
        amount = txn_amount
        currency = txn_currency or billing_currency or "AUD"

    # Issuing debits are spend (negative for our schema)
    txn_type = item.get("transaction_type", "")
    if txn_type in ("AUTHORIZATION", "CLEARING"):
        amount = -abs(amount)
        direction = "debit"
    elif txn_type in ("REFUND", "REVERSAL"):
        amount = abs(amount)
        direction = "credit"
    else:
        direction = "debit" if amount < 0 else "credit"

    # Dates
    txn_date = item.get("transaction_date", "")
    posted_date = item.get("posted_date", txn_date)
    date_str = txn_date[:10] if txn_date else ""
    posted_str = posted_date[:10] if posted_date else date_str

    # Merchant details
    merchant_name = merchant.get("name", "")
    mcc = merchant.get("category_code", "")
    merchant_city = merchant.get("city", "")
    merchant_country = merchant.get("country", "")

    # Card details
    card_id = item.get("card_id", "")
    masked_card = item.get("masked_card_number", "")
    card_last_four = masked_card[-4:] if masked_card else ""

    # Build description from merchant location
    description_parts = [merchant_name]
    if merchant_city:
        description_parts.append(merchant_city)
    if merchant_country and merchant_country != "AU":
        description_parts.append(merchant_country)
    description = ", ".join(p for p in description_parts if p)

    # FX data — always store original currency details and AUD equivalent
    fx = {"original_amount": None, "original_currency": None, "fx_rate": None, "fx_source": None}
    amount_aud = None

    if txn_currency and txn_currency != "AUD" and billing_amount and billing_currency == "AUD":
        # Foreign currency card spend with AUD billing — best case
        fx["original_amount"] = txn_amount
        fx["original_currency"] = txn_currency
        if txn_amount and txn_amount != 0:
            fx["fx_rate"] = round(abs(billing_amount / txn_amount), 6)
        fx["fx_source"] = "airwallex"
        amount_aud = -abs(billing_amount) if direction == "debit" else abs(billing_amount)
    elif txn_currency and txn_currency != "AUD":
        # Foreign currency but no AUD billing amount — needs RBA rate later
        fx["original_amount"] = txn_amount
        fx["original_currency"] = txn_currency
        fx["fx_source"] = None  # To be filled by convert-fx.py
        amount_aud = None  # To be filled by convert-fx.py
    elif currency == "AUD":
        # AUD transaction — amount is already in AUD
        amount_aud = amount

    # Auto-classify: card refunds vs expenses
    if txn_type in ("REFUND", "REVERSAL"):
        transaction_class = "refund"
    else:
        transaction_class = "expense"

    return {
        "transaction_id": f"issuing_{txn_id}",
        "airwallex_id": txn_id,
        "date": date_str,
        "posted_date": posted_str,
        "amount": amount,
        "amount_aud": amount_aud,
        "currency": currency,
        "direction": direction,
        "transaction_class": transaction_class,
        "account_source": "airwallex",
        "merchant_name": merchant_name,
        "merchant_name_normalized": normalize_merchant_name(merchant_name),
        "merchant_category_code": mcc,
        "merchant_city": merchant_city,
        "merchant_country": merchant_country,
        "category_id": "",
        "category_confidence": "UNSET",
        "description": description,
        "reference": item.get("retrieval_ref", ""),
        "source": "card_transaction",
        "card_id": card_id,
        "card_last_four": card_last_four,
        "card_nickname": item.get("card_nickname", ""),
        "transaction_type": txn_type,
        "fx": fx,
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


# ─── Financial Transaction Converter ─────────────────────────────────────────

def financial_to_transaction(item: dict) -> dict:
    """Convert a financial_transactions API item to our schema.

    Financial transactions are wallet-level ledger entries.
    They lack merchant detail but catch transfers, fees, and payouts.
    """
    airwallex_id = item.get("id", "")
    amount = item.get("amount", 0)
    currency = item.get("currency", "AUD")

    direction = "debit" if amount < 0 else "credit"

    created = item.get("created_at", "")
    settled = item.get("settled_at", created)
    date_str = created[:10] if created else ""
    posted_str = settled[:10] if settled else date_str

    description = item.get("description", "")
    source_type = item.get("source_type", "")
    txn_type = item.get("transaction_type", "")

    # FX data from financial transactions
    currency_pair = item.get("currency_pair", "")
    client_rate = item.get("client_rate", None)
    fx = {"original_amount": None, "original_currency": None, "fx_rate": None, "fx_source": None}
    amount_aud = None

    if currency == "AUD":
        # Already AUD
        amount_aud = amount
    elif currency_pair and client_rate:
        # Has Airwallex conversion rate
        fx["fx_rate"] = client_rate
        fx["fx_source"] = "airwallex"
        if len(currency_pair) == 6:
            fx["original_currency"] = currency_pair[:3]
        fx["original_amount"] = amount
        # client_rate is typically FROM/TO — calculate AUD equivalent
        # currency_pair "USDAUD" means 1 USD = client_rate AUD
        if currency_pair.endswith("AUD"):
            amount_aud = round(amount * client_rate, 2)
        elif currency_pair.startswith("AUD"):
            amount_aud = round(amount / client_rate, 2) if client_rate else None
        else:
            amount_aud = None  # Unusual pair — needs manual review
    else:
        # Non-AUD without rate — needs RBA conversion
        fx["original_amount"] = amount
        fx["original_currency"] = currency
        amount_aud = None  # To be filled by convert-fx.py

    # Auto-classify by source_type.
    # Complete mapping based on Airwallex API docs — all known source_types:
    #   PAYOUT, CONVERSION, DEPOSIT, ADJUSTMENT, FEE, PAYMENT_ATTEMPT,
    #   REFUND, DISPUTE, CHARGE, TRANSFER, YIELD, BATCH_PAYOUT,
    #   CARD_PURCHASE, CARD_REFUND, PURCHASE, REFUND_REVERSAL, REPAYMENT,
    #   PAYIN, BATCH_SETTLEMENT, PAYMENT_SETTLEMENT, DIRECT_DEBIT
    if source_type == "DEPOSIT":
        transaction_class = "income"
    elif source_type in ("PAYIN", "BATCH_SETTLEMENT", "PAYMENT_SETTLEMENT"):
        transaction_class = "income"
    elif source_type in ("REFUND_REVERSAL",):
        transaction_class = "income"  # reversed refund = money back
    elif source_type in ("CONVERSION", "PAYMENT_ATTEMPT", "TRANSFER"):
        transaction_class = "internal"
    elif source_type == "PAYOUT" and direction == "credit":
        transaction_class = "refund"
    elif source_type in ("PAYOUT", "BATCH_PAYOUT"):
        transaction_class = "expense"
    elif source_type in ("FEE",):
        transaction_class = "expense"
    elif source_type in ("DIRECT_DEBIT", "PURCHASE", "REPAYMENT"):
        transaction_class = "expense"
    elif source_type == "REFUND":
        transaction_class = "refund"
    elif source_type == "DISPUTE":
        # Dispute debit = chargeback (expense), dispute credit = won dispute (refund)
        transaction_class = "expense" if direction == "debit" else "refund"
    elif source_type == "CHARGE":
        transaction_class = "expense"
    elif source_type == "YIELD":
        transaction_class = "internal"
    elif source_type == "ADJUSTMENT":
        transaction_class = "expense" if direction == "debit" else "income"
    elif direction == "credit" and ("transfer" in (description or "").lower() or "internal" in (description or "").lower()):
        transaction_class = "internal"
    elif direction == "credit":
        transaction_class = "income"
    else:
        transaction_class = "expense"

    # Warn on unknown source_types so we catch new ones early
    known_source_types = {
        "PAYOUT", "CONVERSION", "DEPOSIT", "ADJUSTMENT", "FEE", "PAYMENT_ATTEMPT",
        "REFUND", "DISPUTE", "CHARGE", "TRANSFER", "YIELD", "BATCH_PAYOUT",
        "CARD_PURCHASE", "CARD_REFUND", "PURCHASE", "REFUND_REVERSAL", "REPAYMENT",
        "PAYIN", "BATCH_SETTLEMENT", "PAYMENT_SETTLEMENT", "DIRECT_DEBIT", "",
    }
    if source_type not in known_source_types:
        print(f"  WARNING: Unknown source_type '{source_type}' on {date_str} {amount} {currency} — classified as {transaction_class}", file=sys.stderr)

    return {
        "transaction_id": f"fin_{airwallex_id}",
        "airwallex_id": airwallex_id,
        "date": date_str,
        "posted_date": posted_str,
        "amount": amount,
        "amount_aud": amount_aud,
        "currency": currency,
        "direction": direction,
        "transaction_class": transaction_class,
        "account_source": "airwallex",
        "merchant_name": description,
        "merchant_name_normalized": normalize_merchant_name(description),
        "merchant_category_code": "",
        "merchant_city": "",
        "merchant_country": "",
        "category_id": "",
        "category_confidence": "UNSET",
        "description": description,
        "reference": item.get("batch_id", ""),
        "source": "financial_transaction",
        "source_type": source_type,
        "card_id": None,
        "card_last_four": None,
        "card_nickname": "",
        "transaction_type": txn_type,
        "fx": fx,
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


# ─── Payment Intent (PA) Converter ─────────────────────────────────────────────

def payment_intent_to_transaction(item: dict) -> dict:
    """Convert a pa/payment_intents API item to our schema.

    Payment intents represent payments received via Airwallex payment links.
    These are income transactions that don't appear in the financial_transactions endpoint.
    """
    intent_id = item.get("id", "")
    amount = item.get("captured_amount", 0) or item.get("amount", 0)
    currency = item.get("currency", "AUD")

    direction = "credit"

    created = item.get("created_at", "")
    updated = item.get("updated_at", created)
    date_str = created[:10] if created else ""
    posted_str = updated[:10] if updated else date_str

    customer = item.get("customer", {}) or {}
    customer_name = customer.get("name", "")
    merchant_order_id = item.get("merchant_order_id", "")
    method = item.get("method", "")

    description = f"{customer_name} - {merchant_order_id}" if customer_name else merchant_order_id

    # FX data
    fx = {"original_amount": None, "original_currency": None, "fx_rate": None, "fx_source": None}
    amount_aud = None

    if currency == "AUD":
        amount_aud = amount
    else:
        fx["original_amount"] = amount
        fx["original_currency"] = currency
        amount_aud = None  # To be filled by convert-fx.py

    return {
        "transaction_id": f"pa_{intent_id}",
        "airwallex_id": intent_id,
        "date": date_str,
        "posted_date": posted_str,
        "amount": amount,
        "amount_aud": amount_aud,
        "currency": currency,
        "direction": direction,
        "transaction_class": "income",
        "account_source": "airwallex",
        "merchant_name": description,
        "merchant_name_normalized": normalize_merchant_name(customer_name) if customer_name else "",
        "merchant_category_code": "",
        "merchant_city": "",
        "merchant_country": "",
        "category_id": "",
        "category_confidence": "UNSET",
        "description": description,
        "reference": merchant_order_id,
        "source": "payment_intent",
        "source_type": "PAYIN",
        "card_id": None,
        "card_last_four": None,
        "card_nickname": "",
        "transaction_type": "PAYMENT",
        "fx": fx,
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
        "notes": f"Payment method: {method}" if method else "",
        "gst_amount": None,
        "gst_status": "unknown",
    }


# ─── API Calls ────────────────────────────────────────────────────────────────

def fetch_issuing_transactions(base_url: str, token: str, from_date: str, to_date: str) -> list:
    """
    Fetch card issuing transactions with full merchant detail.
    Filters to CLEARING (settled) transactions for accurate spend data.
    GET only.
    """
    all_items = []
    page_num = 0

    while True:
        params = {
            "from_created_at": f"{from_date}T00:00:00Z",
            "to_created_at": f"{to_date}T23:59:59Z",
            "page_num": page_num,
            "page_size": ISSUING_PAGE_SIZE,
        }
        data = api_get(base_url, token, "/api/v1/issuing/transactions", params)
        items = data.get("items", [])
        all_items.extend(items)

        has_more = data.get("has_more", False)
        if not has_more or not items:
            break
        page_num += 1

    return all_items


def fetch_financial_transactions(base_url: str, token: str, from_date: str, to_date: str) -> list:
    """
    Fetch wallet-level financial transactions (transfers, fees, payouts).
    Excludes card-sourced items to avoid duplicates with issuing endpoint.
    GET only.
    """
    all_items = []
    page_num = 0

    # Source types that overlap with issuing - skip these
    card_source_types = {
        "CARD_PURCHASE", "CARD_REFUND",
        "ISSUING_AUTHORISATION_HOLD", "ISSUING_AUTHORISATION_RELEASE",
        "ISSUING_CAPTURE", "ISSUING_REFUND",
    }

    while True:
        params = {
            "from_created_at": f"{from_date}T00:00:00Z",
            "to_created_at": f"{to_date}T23:59:59Z",
            "page_num": page_num,
            "page_size": FINANCIAL_PAGE_SIZE,
        }
        data = api_get(base_url, token, "/api/v1/financial_transactions", params)
        items = data.get("items", [])

        # Filter out card-sourced transactions (already covered by issuing endpoint)
        for item in items:
            source_type = item.get("source_type", "")
            txn_type = item.get("transaction_type", "")
            if source_type not in card_source_types and txn_type not in card_source_types:
                all_items.append(item)

        has_more = data.get("has_more", False)
        if not has_more or not items:
            break
        page_num += 1

    return all_items


def fetch_payment_intents(base_url: str, token: str, from_date: str, to_date: str) -> list:
    """
    Fetch payment intents from Airwallex Payment Acceptance (PA).
    These are payments received via payment links that don't appear in
    the financial_transactions endpoint. Only returns SUCCEEDED payments.
    GET only.
    """
    all_items = []
    page_num = 0

    while True:
        params = {
            "from_created_at": f"{from_date}T00:00:00Z",
            "to_created_at": f"{to_date}T23:59:59Z",
            "page_num": page_num,
            "page_size": 200,
        }
        data = api_get(base_url, token, "/api/v1/pa/payment_intents", params)
        items = data.get("items", [])

        # Only include succeeded payments (actual income received)
        for item in items:
            if item.get("status") == "SUCCEEDED":
                all_items.append(item)

        has_more = data.get("has_more", False)
        if not has_more or not items:
            break
        page_num += 1

    return all_items


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Airwallex transactions (read-only).")
    parser.add_argument("--from-date", type=str, default=None,
                        help="Start date (YYYY-MM-DD). Default: 90 days ago.")
    parser.add_argument("--to-date", type=str, default=None,
                        help="End date (YYYY-MM-DD). Default: today.")
    parser.add_argument("--skip-issuing", action="store_true",
                        help="Skip issuing/card transactions (only fetch wallet ledger)")
    parser.add_argument("--skip-financial", action="store_true",
                        help="Skip financial/wallet transactions (only fetch card transactions)")
    parser.add_argument("--skip-payments", action="store_true",
                        help="Skip payment acceptance (PA) transactions")
    args = parser.parse_args()

    # Defaults
    today = datetime.now(timezone.utc)
    from_date = args.from_date or (today - timedelta(days=90)).strftime("%Y-%m-%d")
    to_date = args.to_date or today.strftime("%Y-%m-%d")

    # Load env and authenticate
    client_id, api_key, environment = load_env()
    base_url = API_BASES[environment]

    print(f"Environment: {environment}")
    print(f"Date range: {from_date} → {to_date}")
    print("Authenticating with Airwallex...")

    token = authenticate(base_url, client_id, api_key)
    print("Authenticated.\n")

    # Load existing data for dedup
    finance_data = load_existing_finance_data()
    existing_ids = existing_transaction_ids(finance_data)

    new_card = 0
    new_wallet = 0
    new_payments = 0
    skipped_count = 0

    # ── 1. Issuing transactions (card spend with merchant detail) ──
    if not args.skip_issuing:
        print("Fetching card transactions (issuing/transactions)...")
        raw_issuing = fetch_issuing_transactions(base_url, token, from_date, to_date)
        print(f"  Fetched {len(raw_issuing)} card transactions from Airwallex.")

        for item in raw_issuing:
            txn = issuing_to_transaction(item)
            if txn["transaction_id"] in existing_ids:
                skipped_count += 1
                continue
            finance_data["transactions"].append(txn)
            existing_ids.add(txn["transaction_id"])
            new_card += 1
    else:
        print("Skipping card transactions (--skip-issuing)")

    # ── 2. Financial transactions (wallet ledger, excluding card items) ──
    if not args.skip_financial:
        print("Fetching wallet transactions (financial_transactions)...")
        raw_financial = fetch_financial_transactions(base_url, token, from_date, to_date)
        print(f"  Fetched {len(raw_financial)} wallet transactions (card items excluded).")

        # Diagnostic: show all source_types returned by API
        source_type_counts = Counter()
        for item in raw_financial:
            source_type_counts[item.get("source_type", "UNKNOWN")] += 1
        if source_type_counts:
            print(f"  Source types found: {dict(source_type_counts)}")

        for item in raw_financial:
            txn = financial_to_transaction(item)
            if txn["transaction_id"] in existing_ids:
                skipped_count += 1
                continue
            finance_data["transactions"].append(txn)
            existing_ids.add(txn["transaction_id"])
            new_wallet += 1
    else:
        print("Skipping wallet transactions (--skip-financial)")

    # ── 3. Payment Acceptance (PA) — payment link income ──
    if not args.skip_payments:
        print("Fetching payment acceptance transactions (pa/payment_intents)...")
        raw_payments = fetch_payment_intents(base_url, token, from_date, to_date)
        print(f"  Fetched {len(raw_payments)} succeeded payment intents from Airwallex.")

        for item in raw_payments:
            txn = payment_intent_to_transaction(item)
            if txn["transaction_id"] in existing_ids:
                skipped_count += 1
                continue
            finance_data["transactions"].append(txn)
            existing_ids.add(txn["transaction_id"])
            new_payments += 1
    else:
        print("Skipping payment acceptance transactions (--skip-payments)")

    # Sort transactions by date (newest first)
    finance_data["transactions"].sort(key=lambda t: t.get("date", ""), reverse=True)

    # Update sync metadata
    finance_data["last_sync"] = today.isoformat()
    finance_data["sync_status"] = "synced"

    # Ensure output directory exists
    FINANCE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save
    with open(FINANCE_DATA_PATH, "w") as f:
        json.dump(finance_data, f, indent=2)

    total_new = new_card + new_wallet + new_payments
    print(f"\n{'─' * 50}")
    print(f"Done.")
    print(f"  New card transactions:     {new_card}")
    print(f"  New wallet transactions:   {new_wallet}")
    print(f"  New payment intents:       {new_payments}")
    print(f"  Skipped (duplicates):    {skipped_count}")
    print(f"  Total in finance-data.json: {len(finance_data['transactions'])}")
    print(f"  Saved to: {FINANCE_DATA_PATH}")

    # Summary of top merchants from this pull
    if total_new > 0:
        merchants = Counter()
        for txn in finance_data["transactions"]:
            if txn.get("date", "") >= from_date:
                name = txn.get("merchant_name_normalized") or txn.get("merchant_name") or "Unknown"
                merchants[name] += abs(txn.get("amount", 0))

        if merchants:
            print(f"\n  Top merchants ({from_date} → {to_date}):")
            for merchant, total in merchants.most_common(10):
                print(f"    {merchant}: ${total:,.2f}")

        # Count by source
        card_count = sum(1 for t in finance_data["transactions"] if t.get("source") == "card_transaction")
        wallet_count = sum(1 for t in finance_data["transactions"] if t.get("source") == "financial_transaction")
        uncat = sum(1 for t in finance_data["transactions"] if t.get("category_confidence") == "UNSET")
        print(f"\n  Breakdown: {card_count} card | {wallet_count} wallet | {uncat} uncategorized")


if __name__ == "__main__":
    main()
