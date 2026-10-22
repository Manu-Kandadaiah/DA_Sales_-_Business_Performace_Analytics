# Excel Dashboard Build Notes

The requested executive workbook is included as `excel/Pi_Systems_Sales_Dashboard.xlsx`.

- The full project data remains in `data/raw/01_raw_data.csv` (8,050 rows) and `data/processed/02_cleaned_sales_data.csv` (8,000 rows).
- The workbook's `Raw_Data` and `Cleaned_Data` sheets are labelled previews (250 and 500 rows respectively) because exporting both full-width datasets in one workbook exceeded the available workbook engine's reliable export size.
- KPI values, business summaries, top-product/customer views, regional/monthly analyses, and charts were generated from the complete cleaned dataset.
- The `Pivot_Tables` sheet contains pivot-style analytical summaries. Native PivotTable objects and slicers are not generated programmatically by the current workbook engine.
- Formula demonstrations include `SUMIFS`, `COUNTIFS`, `IFS`, `INDEX/MATCH`, and lookup logic, plus a region data-validation selector.

This limitation affects only how much row-level data is embedded in the `.xlsx`; it does not remove the complete CSV datasets or the Python/SQL analysis.
