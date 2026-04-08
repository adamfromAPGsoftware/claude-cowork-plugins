# Amex CSV Import

## Overview

The Amex import process parses American Express AU credit card statement CSV files and merges transactions into `finance/finance-data.json` alongside Airwallex transactions.

## Where to Put Files

Place Amex CSV statement files in:

```
finance/amex/
```

Any `.csv` file in this directory will be picked up by the import script. Filenames don't matter — name them however you like (e.g., `march-2026.csv`, `amex-statement-2026-03.csv`).

## Supported CSV Formats

Amex AU exports statements in two common formats. The import script auto-detects which format is in use.

### Format A — 3 Columns (Date, Description, Amount)

No header row. Most common from the Amex online portal "Download CSV" option.

```
01/03/2026,ANTHROPIC API,-500.00
02/03/2026,VERCEL INC,-29.00
05/03/2026,PAYMENT RECEIVED,1500.00
```

### Format B — 4 Columns (Date, Reference, Amount, Description)

Includes a header row. Sometimes exported by Amex business accounts or third-party tools.

```
Date,Reference,Amount,Description
01/03/2026,1234567890,-500.00,ANTHROPIC API
02/03/2026,9876543210,-29.00,VERCEL INC
05/03/2026,5555555555,1500.00,PAYMENT RECEIVED
```

### Date Format

All dates are DD/MM/YYYY (Australian format). The script converts them to YYYY-MM-DD internally.

### Amounts

- Negative amounts = debits (money spent)
- Positive amounts = credits (payments received, refunds)
- All amounts are in AUD (Amex AU statements are always in AUD)

## How Dedup Works

Each transaction gets a deterministic ID generated from its content:

```
amex_{sha256(date + amount + description)[:16]}
```

This means:
- Re-importing the same CSV file is safe — duplicates are skipped automatically
- Two transactions on the same date with the same amount and description will be treated as one (rare edge case)
- Changing the CSV content will generate new IDs

**Leave processed files in `finance/amex/`.** Re-importing is safe because of dedup, and keeping the originals provides an audit trail.

## Cross-Source Duplicate Detection

After importing Amex transactions, the script checks for potential duplicates between Amex and Airwallex. This catches cases where the same purchase appears in both sources (e.g., an Amex card linked to Airwallex).

Detection criteria:
- Amount within **$0.05** of each other (accounts for minor rounding/FX differences)
- Date within **3 days** of each other (accounts for settlement timing)

Potential duplicates are printed as warnings but **not automatically removed**. Review them manually and tag or remove as appropriate.

## Usage

Import all CSV files in `finance/amex/`:

```bash
python3 finance-plugin/scripts/import-amex.py
```

Import a specific file:

```bash
python3 finance-plugin/scripts/import-amex.py --file finance/amex/march-2026.csv
```

Or use the command:

```
/apg-finance:import-amex
```
