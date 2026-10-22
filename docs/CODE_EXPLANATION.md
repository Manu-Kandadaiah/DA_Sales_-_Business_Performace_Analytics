# Code Explanation Guide

## groupby()
**What:** Groups rows by one or more keys. **Why:** Aggregate business metrics. **Project:** Revenue by category/region/product. **Example:** `df.groupby("Category").Net_Sales_Amount.sum()`.

## merge()
Combines DataFrames using keys. Used to attach salesperson targets and master-data attributes. Example: `actual.merge(targets, on="Salesperson_ID")`.

## pivot_table()
Creates cross-tab analytical summaries. Used for category-by-region revenue. Example: `pd.pivot_table(df,index="Category",columns="Region",values="Net_Sales_Amount",aggfunc="sum")`.

## apply()
Runs a function over rows/columns when vectorized logic is not convenient. Use sparingly because vectorized operations are faster.

## map()
Maps a Series through a dictionary/lookup Series. Used to restore canonical customer/product details from IDs.

## lambda
Small anonymous function, e.g. shipping delivery averages excluding zero-day non-delivered orders.

## loc
Label/condition-based selection: `df.loc[df.Region.eq("South"), ["Order_ID","Net_Sales_Amount"]]`.

## iloc
Position-based selection: `df.iloc[:5, :8]`.

## datetime
`pd.to_datetime()` enables year/month/quarter extraction, sorting, resampling, and date-difference calculations.

## rolling()
Calculates moving metrics such as a 3-month average: `monthly.Revenue.rolling(3).mean()`.

## ranking
`rank()` or SQL `RANK()` orders customers/products while preserving ties.

## SQL JOIN
Connects normalized tables, for example orders → customers → order_items.

## CTE
A named temporary query (`WITH ...`) that makes multi-step SQL analysis readable, used for growth and Pareto queries.

## Window Functions
Calculate rankings, LAG values, running totals, and percentiles without collapsing rows.

## Excel Pivot Tables
Summarize data by dimensions such as category, region, or month. The workbook includes a Pivot_Tables summary sheet containing the same management aggregations and chart sources.

## XLOOKUP
Finds a related value by key, e.g. customer segment from a Customer_ID.

## SUMIFS
Sums revenue under one or more conditions such as a selected region.
