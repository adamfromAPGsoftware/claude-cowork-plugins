---
name: categorize
description: Auto-categorize uncategorized transactions by merchant name and MCC code
menu-code: CT
---

# Categorize Transactions

Auto-categorize uncategorized transactions using merchant name patterns and MCC codes.

## Process

1. **Load finance-data.json** — filter to transactions where `category_confidence == "UNSET"` or `category_id` is empty

2. **Load known patterns** — Read `_bmad/_memory/bmad-apg-fin-transaction-analyst-sidecar/patterns.md` for previously learned merchant → category mappings

3. **For each uncategorized transaction:**

   a. **Check known merchants:** If `merchant_name_normalized` matches a pattern in memory, apply that category with confidence `AUTO`
   
   b. **Check MCC code:** Map common MCC ranges to categories:
      - 5815-5818 (Digital goods, streaming) → software
      - 4816 (Computer network services) → hosting
      - 7372-7379 (Computer services) → software
      - 5811-5814 (Restaurants, eating places) → meals
      - 4111-4789 (Transportation) → travel
      - 5943-5999 (Stationery, office supplies) → office
      - 7311-7399 (Advertising, business services) → marketing
      - 8111-8999 (Professional services) → professional
   
   c. **Present uncertain matches:** If merchant name is ambiguous, show the user:
      ```
      Transaction: {date} | {merchant_name} | ${amount}
      Suggested: {category} (reason: {MCC/pattern match})
      Confirm? [y/n/other category]
      ```

4. **Save updates** to finance-data.json

5. **Update patterns.md** with any new confirmed merchant → category mappings for future auto-categorization

## Output

```
Categorization complete.
  Auto-categorized: {count}
  User-confirmed: {count}
  Still uncategorized: {count}
  
  New patterns learned: {count}
```

## Categories Reference

| ID | Label |
|----|-------|
| software | Software & Subscriptions |
| hosting | Hosting & Infrastructure |
| contractors | Contractors & Freelancers |
| travel | Travel & Transport |
| meals | Meals & Entertainment |
| office | Office & Equipment |
| marketing | Marketing & Advertising |
| professional | Professional Services |
| other | Other |
