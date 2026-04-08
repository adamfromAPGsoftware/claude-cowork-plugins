---
name: query-tax
description: Answer freeform tax-specific queries with transaction-level evidence
menu-code: QT
---

# Query Tax

Answer freeform tax-related questions by querying finance-data.json and providing transaction-level evidence.

## Process

1. **Receive the user's question.** Examples:
   - "How much GST can I claim this quarter?"
   - "What's my total R&D spend?"
   - "Show me all overseas transactions"
   - "What did I spend on contractors in Q2?"
   - "Which transactions are missing GST classification?"

2. **Parse the query to determine:**
   - Time period (default: current FY if not specified)
   - Filter criteria (category, GST status, currency, receipt status, R&D flag, etc.)
   - Aggregation type (sum, count, list, group-by)

3. **Query finance-data.json** with the determined filters.

4. **Present results with transaction-level evidence:**
   - Always show the specific transactions that back up any totals
   - Include transaction ID, date, merchant, amount for each
   - Group logically based on the question

5. **Add tax context where relevant:**
   - GST queries: reference BAS quarter boundaries and 1/11th rule
   - FX queries: show both original currency and AUD amounts
   - R&D queries: note eligibility criteria and receipt coverage
   - Period queries: use Australian FY convention (Jul-Jun)

6. **Flag any data quality issues** that affect the answer:
   - Transactions with unconfirmed GST
   - Missing receipts in the result set
   - Uncategorized transactions that might be relevant

## Output

Structured answer with:
- Direct answer to the question (dollar amount, count, or list)
- Supporting transaction table
- Any caveats about data completeness
- Suggested follow-up actions if gaps exist
