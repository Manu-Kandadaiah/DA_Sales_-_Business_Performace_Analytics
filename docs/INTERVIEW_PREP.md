# Interview Preparation

## Part 1 — 2-Minute Project Explanation

I built an end-to-end personal portfolio project for a fictional company, Pi Systems Private Limited. I generated and cleaned about 8,000 synthetic sales transaction lines across 2025 and 2026, intentionally added data-quality issues, validated financial calculations, performed EDA with Pandas and NumPy, designed a normalized MySQL schema, wrote 35 SQL business queries, created Matplotlib charts, and built an Excel executive dashboard. I analyzed revenue, profit, margin, customers, products, regions, salespeople, discounts, returns, cancellations, delivery, Pareto concentration, and RFM-style segments. I then converted the findings into evidence-based recommendations and documented the project for GitHub.

## Part 2 & 3 — 30 Interview Questions with Answers

### 1. Explain this project in two minutes.
I built an end-to-end personal portfolio project for a fictional company, Pi Systems Private Limited. I generated and cleaned about 8,000 synthetic sales transaction lines across 2025 and 2026, intentionally added data-quality issues, validated financial calculations, performed EDA with Pandas and NumPy, designed a normalized MySQL schema, wrote 35 SQL business queries, created Matplotlib charts, and built an Excel executive dashboard. I analyzed revenue, profit, margin, customers, products, regions, salespeople, discounts, returns, cancellations, delivery, Pareto concentration, and RFM-style segments. I then converted the findings into evidence-based recommendations and documented the project for GitHub.

### 2. Why did you create synthetic data?
To demonstrate a realistic workflow without using confidential company or customer data. It also lets me deliberately include quality issues for cleaning practice.

### 3. How did you keep the data reproducible?
I used a fixed random seed so the generation process is deterministic.

### 4. What is the difference between Sales_Amount and Net_Sales_Amount?
Sales_Amount follows gross minus discount. Net_Sales_Amount adjusts reporting impact for cancelled and returned orders.

### 5. Why use Pandas?
It provides efficient tabular loading, cleaning, grouping, merging, reshaping, and time-series operations.

### 6. Where did NumPy add value?
Distribution statistics, percentiles, vectorized conditional fields with np.where/np.select, and array-based calculations.

### 7. How did you detect duplicates?
Using duplicated() and then drop_duplicates() for exact duplicate transaction rows.

### 8. How did you handle missing customer names?
I restored canonical details from the customer master using Customer_ID rather than guessing text.

### 9. How did you handle date errors?
I used controlled parsing for the known raw formats and validated that no dates remained invalid.

### 10. Why recalculate revenue and profit?
It prevents trusting potentially inconsistent raw derived fields and validates mathematical consistency.

### 11. What does groupby do?
It groups records by a business dimension and lets me aggregate measures such as revenue or profit.

### 12. What does merge do?
It combines related tables/DataFrames using common keys, such as salespeople with targets.

### 13. Why use pivot_table?
It creates matrix-style summaries such as category by region revenue, similar to Excel pivots.

### 14. When would you use loc vs iloc?
loc uses labels or boolean conditions; iloc uses integer positions.

### 15. What is MoM growth?
The percent change from the previous month: (current-previous)/previous × 100.

### 16. What is YoY growth?
The percent change versus the same annual period in the prior year; here 2026 versus 2025 total revenue.

### 17. What is AOV?
Average Order Value equals net revenue divided by number of distinct orders.

### 18. What is profit margin?
Profit divided by sales amount times 100; it shows profitability relative to revenue.

### 19. What is Pareto analysis?
It ranks contributors and calculates cumulative revenue share to see how concentrated revenue is among products/customers.

### 20. What is RFM?
Recency, Frequency, Monetary analysis segments customers based on how recently, how often, and how much they buy.

### 21. Why normalize the MySQL schema?
To reduce duplication, preserve data integrity, and separate customers, products, orders, items, payments, and shipping.

### 22. What is a primary key?
A unique identifier for a row, such as order_id or customer_id.

### 23. What is a foreign key?
A constraint linking a child table to a valid parent key, protecting referential integrity.

### 24. Why use indexes?
Indexes speed common filters and joins on columns like dates, status, region-related keys, and foreign keys.

### 25. What is a CTE?
A named temporary result defined with WITH, useful for readable multi-step queries.

### 26. What is LAG?
A window function that returns a previous row's value, useful for MoM and YoY growth.

### 27. Difference between RANK and DENSE_RANK?
RANK leaves gaps after ties; DENSE_RANK does not.

### 28. Why an Excel dashboard?
It is widely used in analyst/MIS roles and demonstrates business reporting without relying on BI tools.

### 29. How did you validate data quality?
I checked negatives, dates, key membership, duplicates, missing values, and revenue/profit formula consistency.

### 30. What would you improve next?
Automated tests, live database refresh, Excel slicers/pivot charts, forecasting, cohort analysis, and a more formal CLV model.

## Part 4 — 20 Dashboard/Business Questions

1. Which KPI would you show management first and why?
2. Why can revenue grow while profit margin falls?
3. Which category contributes the most revenue and is that enough to prioritize it?
4. How would you investigate a high-revenue low-margin product?
5. Which region deserves more attention and what evidence would you use?
6. How would you identify high-value customers?
7. What does the top-20%-customer revenue share tell you?
8. How do returns affect revenue and profit reporting?
9. How would you investigate cancellation rate?
10. What does AOV tell the business?
11. What is the risk of using only average values?
12. How do discounts affect margin in this dataset?
13. Which shipping mode is most used and how would you assess service quality?
14. How would you evaluate salesperson performance fairly?
15. Why compare target achievement and profit rather than revenue alone?
16. What seasonality is visible and how could operations respond?
17. How would you explain a sudden monthly decline?
18. Which product inventory should be prioritized?
19. What customer segment should receive retention campaigns?
20. Which dashboard filters would be most useful to a sales manager?

## Part 5 — 15 SQL Questions

1. Write total revenue using SUM.
2. Find top 10 products by revenue.
3. Explain INNER JOIN vs LEFT JOIN in this schema.
4. Calculate monthly revenue.
5. Find cancelled-order rate.
6. Find salespeople below target.
7. Use CASE to create discount bands.
8. Use LAG for MoM growth.
9. Use a CTE for yearly revenue.
10. Create a running revenue total.
11. Rank customers by revenue.
12. Explain ROW_NUMBER vs RANK.
13. Find products with revenue above average.
14. Find top 20% customers with NTILE.
15. How would an index on order_date help?

## Part 6 — 15 Pandas Questions

1. What does read_csv parse_dates do?
2. How did you use isnull?
3. How did you use duplicated/drop_duplicates?
4. Explain value_counts in quality checks.
5. What does nunique show?
6. How was groupby used?
7. How was agg used?
8. Why use merge?
9. Give a pivot_table example.
10. When do you use sort_values?
11. How did you use fillna or status-aware imputation?
12. Why prefer vectorized calculations over apply?
13. Explain map in master-data restoration.
14. How did datetime operations create Month/Quarter?
15. What does rolling(3).mean() show?

## Part 7 — 15 Excel Questions

1. How is the Excel dashboard structured?
2. What is a Pivot Table?
3. What does SUMIFS do?
4. What does COUNTIFS do?
5. When would you use XLOOKUP?
6. When would INDEX/MATCH be useful?
7. How do Excel Tables improve analysis?
8. How would you add a slicer to a Pivot Table?
9. How do you format currency and percentages?
10. How do KPI cards help management?
11. What conditional formatting is useful for targets?
12. How would you calculate profit margin in Excel?
13. How would you make a monthly trend chart?
14. How would you refresh a dashboard with new data?
15. How would you audit an Excel formula error?
