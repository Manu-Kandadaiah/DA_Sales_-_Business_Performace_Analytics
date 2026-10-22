# Sales & Business Performance Analytics System

**Company:** Pi Systems Private Limited  
**Disclosure:** **Fictional company and synthetic dataset created for portfolio demonstration.**

## Project Overview
A complete Data Analyst portfolio project covering the workflow from intentionally imperfect raw sales data through cleaning, validation, exploratory analysis, SQL, advanced analytics, visualization, and an Excel executive dashboard. The project contains 8,000 cleaned transaction lines across 2025–2026.

## Business Problem
Management needs a reliable view of revenue, profitability, customers, products, regions, salespeople, discounts, order outcomes, and delivery performance from a two-year sales dataset.

## Objectives
- Build a realistic synthetic dataset and controlled data-quality issues.
- Clean and validate data with Python/Pandas.
- Analyze KPI, trend, product, customer, region, salesperson, discount, return/cancellation, and delivery performance.
- Model the data in normalized MySQL tables and answer business questions with 37 SQL queries.
- Present management KPIs in Microsoft Excel without Power BI/Tableau.

## Dataset
- Raw rows: 8,050
- Cleaned rows: 8,000
- Unique orders: 5,600
- Customers: 750
- Products: 150
- Salespeople: 25
- Date range: 2025-01-01 to 2026-12-31

## Tools & Technologies
Python 3.12+, Pandas, NumPy, Matplotlib, MySQL, SQL, Microsoft Excel, Jupyter, Git, GitHub.

## Project Architecture
```text
sales_business_analytics/
├── data/raw/01_raw_data.csv
├── data/processed/02_cleaned_sales_data.csv
├── data/reference/
├── notebooks/01_Data_Cleaning.ipynb
├── notebooks/02_EDA_Sales_Analysis.ipynb
├── python/
├── sql/
├── excel/Pi_Systems_Sales_Dashboard.xlsx
├── reports/charts/
├── reports/exports/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

## Data Cleaning
The raw file intentionally contains missing values, duplicate transaction rows, mixed capitalization, whitespace, minor category aliases, and several date formats. Cleaning uses master-data mappings, controlled date parsing, duplicate removal, status-aware missing-value handling, and complete recalculation of financial fields. See `reports/data_quality_report.md`.

## Exploratory Data Analysis
The analysis covers overall sales/profit/margin, monthly-quarterly-yearly trends, categories, subcategories, products, brands, regions, states/cities, customer segments, top customers, salespeople, payments, shipping, discounts, order status, and delivery time.

## SQL Analysis
`sql/03_SQL_Business_Analysis.sql` contains 37 business queries using joins, CTEs, CASE, COALESCE patterns, aggregates, RANK, DENSE_RANK, ROW_NUMBER, LAG, NTILE, and running totals.

## Excel Dashboard
The workbook contains Raw_Data, Cleaned_Data, Calculations, Pivot_Tables, Customer_Analysis, Product_Analysis, Regional_Analysis, Monthly_Analysis, and Dashboard sheets. KPI formulas, lookup examples, data validation, summary tables, and executive charts use a navy/gold/light corporate theme.

**Workbook build note:** the complete datasets are the CSV files in `data/raw/` (8,050 rows) and `data/processed/` (8,000 rows). To keep the generated `.xlsx` reliable in the available workbook engine, the Raw_Data and Cleaned_Data tabs contain clearly labelled previews (250 raw rows and 500 cleaned rows). Dashboard metrics and analytical summaries are calculated from the complete dataset before being written into the workbook. The `Pivot_Tables` tab contains pivot-style management summaries used as chart sources; native Excel PivotTable objects and slicers are not programmatically emitted by the workbook engine.

## Key Business Insights
See `reports/business_insights.md` for 15 dataset-derived insights and evidence-based recommendations.

## How to Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Optional: regenerate synthetic raw data first
python python/generate_data.py
python python/clean_data.py
python python/analysis.py
python python/generate_reports.py
```

## MySQL Setup
1. Create the schema: `mysql -u root -p < sql/schema.sql`
2. Set environment variables `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE=pi_sales_analytics`.
3. Run `python python/load_mysql.py`.
4. Execute `sql/03_SQL_Business_Analysis.sql`.

## Screenshots to Add to Portfolio
1. Excel Dashboard full-screen.
2. Monthly revenue chart.
3. Top products / top customers chart.
4. Data-cleaning notebook showing before/after quality checks.
5. SQL query plus result for monthly growth or salesperson ranking.
6. MySQL schema/ER view if you create one locally.

## Future Improvements
Add forecast models, cohort analysis, automated refresh jobs, richer Excel slicers/pivot charts, customer lifetime value modeling, and test coverage for pipeline functions.

## Skills Demonstrated
Python, Pandas, NumPy, data cleaning, EDA, business metrics, SQL, MySQL normalization, window functions, Excel dashboards, visualization, data quality validation, Git/GitHub documentation, and business communication.
