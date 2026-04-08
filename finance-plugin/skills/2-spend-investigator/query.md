---
name: query
description: Freeform financial query — ask anything about where money is going
menu-code: QR
---

# Financial Query

Answer freeform questions about the financial data.

## Process

1. **Load finance-data.json** — Read all transactions

2. **Understand the question** — Parse what the user wants to know:
   - "How much did I spend on X?" → filter by merchant/category, sum amounts
   - "What's my biggest expense?" → sort by amount, show top items
   - "Show me all transactions over $500" → filter by amount threshold
   - "What subscriptions do I have?" → find recurring merchant patterns
   - "Compare March vs February" → period comparison
   - "What's from Anthropic?" → merchant-specific breakdown

3. **Answer with evidence:**
   - Always cite specific transaction IDs and amounts
   - Show calculations (e.g., "3 transactions: $500 + $500 + $500 = $1,500")
   - If the answer requires inference, state assumptions explicitly

4. **Present in the clearest format:**
   - Single number → direct answer with supporting transactions
   - List → table with transaction details
   - Comparison → side-by-side table with differences

## Principles

- Every answer includes at least one transaction ID as evidence
- If the question can't be answered from the data, say what's missing
- Offer follow-up: "Would you like me to dig deeper into any of these?"
- If the question touches uncategorized transactions, note that categorization might change the answer

## Example

User: "How much am I spending on AI?"

```
AI-Related Spend (All Time):

| Date       | Merchant   | Amount | Category | Txn ID   |
|------------|------------|--------|----------|----------|
| 2026-03-01 | Anthropic  | $500   | Software | txn_042  |
| 2026-03-01 | OpenAI     | $120   | Software | txn_043  |
| 2026-02-01 | Anthropic  | $500   | Software | txn_028  |
| 2026-02-01 | OpenAI     | $120   | Software | txn_029  |

Total: $1,240 ($620/month average)
Trend: Stable at ~$620/mo since Feb 2026
```
