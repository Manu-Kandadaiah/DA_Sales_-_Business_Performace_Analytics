# Data Quality Report

**Company:** Pi Systems Private Limited  
**Project:** Sales & Business Performance Analytics System  
**Disclosure:** Fictional company and synthetic dataset created for portfolio demonstration.

## Summary
- Raw records: 8,050
- Cleaned records: 8,000
- Columns after cleaning: 37
- Missing values before cleaning: 138
- Missing values after cleaning: 0
- Duplicate rows before cleaning: 50
- Duplicate rows after cleaning: 0

## Cleaning actions
1. Trimmed leading/trailing whitespace in text fields.
2. Parsed four controlled date formats into ISO-compatible datetimes.
3. Restored canonical customer, product, category, geography, and salesperson values from reference master tables.
4. Standardized order status, payment method, and shipping mode capitalization.
5. Filled missing delivery days with status-aware or shipping-mode median values.
6. Removed exact duplicate transaction rows.
7. Recalculated gross sales, discount, sales amount, cost, profit, profit margin, net sales, net profit, and net quantity from source components.
8. Added Year, Month, Quarter, Order_Month, and Order_Flag fields for analysis.

## Outliers investigated
High-value order lines were reviewed through IQR/percentile summaries. They are retained because enterprise and corporate orders intentionally use higher quantities and are valid business scenarios rather than data-entry errors.

## Validation checks
```json
{
  "clean_rows": 8000,
  "raw_rows": 8050,
  "raw_duplicates": 50,
  "clean_duplicates": 0,
  "missing_before_total": 138,
  "missing_after_total": 0,
  "negative_quantity": 0,
  "negative_price": 0,
  "revenue_formula_mismatches": 0,
  "profit_formula_mismatches": 0,
  "invalid_dates": 0,
  "invalid_product_ids": 0,
  "invalid_customer_ids": 0,
  "invalid_salesperson_ids": 0
}
```
