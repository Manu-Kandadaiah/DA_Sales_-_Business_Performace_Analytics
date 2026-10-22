"""Generate analytical CSV exports and Matplotlib charts from the cleaned dataset."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
EXPORT_DIR = BASE_DIR / "reports/exports"
CHART_DIR = BASE_DIR / "reports/charts"


def save_bar(df, x, y, title, xlabel, ylabel, filename, horizontal=False):
    fig, ax = plt.subplots(figsize=(9, 5))
    if horizontal:
        ax.barh(df[x].astype(str), df[y])
        ax.invert_yaxis()
    else:
        ax.bar(df[x].astype(str), df[y])
        ax.tick_params(axis="x", rotation=35)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=160)
    plt.close(fig)


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(BASE_DIR / "data/processed/02_cleaned_sales_data.csv", parse_dates=["Order_Date"])
    salespeople = pd.read_csv(BASE_DIR / "data/reference/salespeople.csv")
    orders = df[df["Order_Flag"].eq(1)].copy()

    total_revenue = df["Net_Sales_Amount"].sum()
    total_profit = df["Net_Profit"].sum()
    total_orders = int(df["Order_Flag"].sum())
    total_qty = int(df["Net_Quantity"].sum())
    kpis = pd.DataFrame({
        "Metric": ["Total Revenue", "Total Profit", "Profit Margin %", "Total Orders", "Net Quantity Sold", "Average Order Value", "Return Rate %", "Cancellation Rate %", "Average Delivery Days"],
        "Value": [
            total_revenue,
            total_profit,
            total_profit / total_revenue * 100,
            total_orders,
            total_qty,
            total_revenue / total_orders,
            orders["Order_Status"].eq("Returned").mean() * 100,
            orders["Order_Status"].eq("Cancelled").mean() * 100,
            orders.loc[orders["Delivery_Days"] > 0, "Delivery_Days"].mean(),
        ],
    })
    kpis.to_csv(EXPORT_DIR / "kpis.csv", index=False)

    monthly = df.groupby("Order_Month", as_index=False).agg(Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"))
    monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change() * 100
    monthly.to_csv(EXPORT_DIR / "monthly_analysis.csv", index=False)

    quarterly = df.groupby(["Year", "Quarter"], as_index=False).agg(Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"))
    quarterly.to_csv(EXPORT_DIR / "quarterly_analysis.csv", index=False)

    yearly = df.groupby("Year", as_index=False).agg(Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"))
    yearly["YoY_Growth_%"] = yearly["Revenue"].pct_change() * 100
    yearly.to_csv(EXPORT_DIR / "yearly_analysis.csv", index=False)

    def performance_summary(keys):
        out = df.groupby(keys, as_index=False).agg(Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"))
        out["Profit_Margin_%"] = np.where(out["Revenue"] != 0, out["Profit"] / out["Revenue"] * 100, 0)
        return out.sort_values("Revenue", ascending=False)

    category = performance_summary(["Category"])
    category.to_csv(EXPORT_DIR / "category_analysis.csv", index=False)
    brand = performance_summary(["Brand"])
    brand.to_csv(EXPORT_DIR / "brand_analysis.csv", index=False)
    region = performance_summary(["Region"])
    region.to_csv(EXPORT_DIR / "regional_analysis.csv", index=False)
    state = performance_summary(["State"])
    state.to_csv(EXPORT_DIR / "state_analysis.csv", index=False)
    city = performance_summary(["State", "City"])
    city.to_csv(EXPORT_DIR / "city_analysis.csv", index=False)
    segment = performance_summary(["Customer_Segment"])
    segment.to_csv(EXPORT_DIR / "segment_analysis.csv", index=False)

    product = df.groupby(["Product_ID", "Product_Name", "Category"], as_index=False).agg(
        Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"), Quantity=("Net_Quantity", "sum")
    )
    product["Profit_Margin_%"] = np.where(product["Revenue"] != 0, product["Profit"] / product["Revenue"] * 100, 0)
    product = product.sort_values("Revenue", ascending=False)
    product.to_csv(EXPORT_DIR / "product_analysis.csv", index=False)

    customer = df.groupby(["Customer_ID", "Customer_Name", "Customer_Segment"], as_index=False).agg(
        Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"), Orders=("Order_Flag", "sum")
    )
    customer["Avg_Order_Value"] = np.where(customer["Orders"] > 0, customer["Revenue"] / customer["Orders"], 0)
    customer = customer.sort_values("Revenue", ascending=False)
    customer.to_csv(EXPORT_DIR / "customer_analysis.csv", index=False)

    payment = orders.groupby("Payment_Method", as_index=False).agg(Orders=("Order_ID", "count")).sort_values("Orders", ascending=False)
    payment.to_csv(EXPORT_DIR / "payment_analysis.csv", index=False)
    shipping = orders.groupby("Shipping_Mode", as_index=False).agg(
        Orders=("Order_ID", "count"),
        Avg_Delivery_Days=("Delivery_Days", lambda s: s[s > 0].mean()),
    ).sort_values("Orders", ascending=False)
    shipping.to_csv(EXPORT_DIR / "shipping_analysis.csv", index=False)
    status = orders.groupby("Order_Status", as_index=False).agg(Orders=("Order_ID", "count"))
    status["Order_Share_%"] = status["Orders"] / status["Orders"].sum() * 100
    status.to_csv(EXPORT_DIR / "order_status_analysis.csv", index=False)

    discount_band = pd.cut(df["Discount_Percent"], bins=[-0.001, 5, 10, 20, np.inf], labels=["0-5%", "5-10%", "10-20%", "20%+"])
    discount = df.assign(Discount_Band=discount_band).groupby("Discount_Band", observed=False, as_index=False).agg(
        Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum")
    )
    discount["Profit_Margin_%"] = np.where(discount["Revenue"] != 0, discount["Profit"] / discount["Revenue"] * 100, 0)
    discount.to_csv(EXPORT_DIR / "discount_analysis.csv", index=False)

    sales_2026 = df[df["Year"].eq(2026)].groupby("Salesperson_ID", as_index=False).agg(Revenue=("Net_Sales_Amount", "sum"), Profit=("Net_Profit", "sum"))
    salesperson = salespeople.merge(sales_2026, on="Salesperson_ID", how="left").fillna({"Revenue": 0, "Profit": 0})
    salesperson["Target_Achievement_%"] = np.where(salesperson["Target_2026"] != 0, salesperson["Revenue"] / salesperson["Target_2026"] * 100, 0)
    salesperson = salesperson[["Salesperson_ID", "Salesperson_Name", "Region", "Revenue", "Profit", "Target_2026", "Target_Achievement_%"]].sort_values("Revenue", ascending=False)
    salesperson.to_csv(EXPORT_DIR / "salesperson_analysis.csv", index=False)

    # Pareto analysis.
    cust_p = customer[["Customer_ID", "Customer_Name", "Revenue"]].copy()
    cust_p["Cumulative_Revenue"] = cust_p["Revenue"].cumsum()
    cust_p["Cumulative_Share_%"] = cust_p["Cumulative_Revenue"] / cust_p["Revenue"].sum() * 100
    cust_p.to_csv(EXPORT_DIR / "customer_pareto.csv", index=False)
    prod_p = product[["Product_ID", "Product_Name", "Revenue"]].copy()
    prod_p["Cumulative_Revenue"] = prod_p["Revenue"].cumsum()
    prod_p["Cumulative_Share_%"] = prod_p["Cumulative_Revenue"] / prod_p["Revenue"].sum() * 100
    prod_p.to_csv(EXPORT_DIR / "product_pareto.csv", index=False)

    # RFM-style customer analysis using latest date in the synthetic period.
    as_of = df["Order_Date"].max() + pd.Timedelta(days=1)
    completed = df[~df["Order_Status"].isin(["Cancelled", "Returned"])]
    rfm = completed.groupby(["Customer_ID", "Customer_Name"], as_index=False).agg(
        Last_Purchase=("Order_Date", "max"), Frequency=("Order_Flag", "sum"), Monetary=("Net_Sales_Amount", "sum")
    )
    rfm["Recency_Days"] = (as_of - rfm["Last_Purchase"]).dt.days
    rfm["R_Score"] = pd.qcut(rfm["Recency_Days"].rank(method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["RFM_Total"] = rfm[["R_Score", "F_Score", "M_Score"]].sum(axis=1)
    rfm["RFM_Segment"] = np.select(
        [rfm["RFM_Total"] >= 10, (rfm["R_Score"] <= 2) & (rfm["F_Score"] >= 3), rfm["RFM_Total"] <= 5],
        ["High Value", "At Risk", "Low Value"],
        default="Regular",
    )
    rfm.to_csv(EXPORT_DIR / "rfm_customer_analysis.csv", index=False)

    # Matplotlib visualizations.
    fig, ax = plt.subplots(figsize=(10, 5)); ax.plot(monthly["Order_Month"], monthly["Revenue"], marker="o"); ax.set_title("Monthly Revenue Trend"); ax.set_xlabel("Month"); ax.set_ylabel("Net Revenue (INR)"); ax.tick_params(axis="x", rotation=60); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(CHART_DIR / "01_monthly_revenue.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5)); ax.plot(monthly["Order_Month"], monthly["Profit"], marker="o"); ax.set_title("Monthly Profit Trend"); ax.set_xlabel("Month"); ax.set_ylabel("Net Profit (INR)"); ax.tick_params(axis="x", rotation=60); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(CHART_DIR / "02_monthly_profit.png", dpi=160); plt.close(fig)
    save_bar(category, "Category", "Revenue", "Revenue by Category", "Category", "Net Revenue (INR)", "03_revenue_category.png")
    save_bar(category, "Category", "Profit", "Profit by Category", "Category", "Net Profit (INR)", "04_profit_category.png")
    save_bar(region, "Region", "Revenue", "Revenue by Region", "Region", "Net Revenue (INR)", "05_revenue_region.png")
    save_bar(region, "Region", "Profit", "Profit by Region", "Region", "Net Profit (INR)", "06_profit_region.png")
    save_bar(product.head(10), "Product_Name", "Revenue", "Top 10 Products by Revenue", "Product", "Net Revenue (INR)", "07_top_products.png", True)
    save_bar(customer.head(10), "Customer_Name", "Revenue", "Top 10 Customers by Revenue", "Customer", "Net Revenue (INR)", "08_top_customers.png", True)
    save_bar(salesperson.head(15), "Salesperson_Name", "Target_Achievement_%", "2026 Salesperson Target Achievement", "Salesperson", "Target Achievement %", "09_salesperson_performance.png")
    save_bar(segment, "Customer_Segment", "Revenue", "Customer Segment Revenue", "Segment", "Net Revenue (INR)", "10_customer_segment_revenue.png")
    sample = df.sample(min(2500, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(9, 5)); ax.scatter(sample["Discount_Percent"], sample["Profit_Margin"], alpha=.35, s=14); ax.set_title("Discount vs Profit Margin"); ax.set_xlabel("Discount %"); ax.set_ylabel("Profit Margin %"); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(CHART_DIR / "11_discount_vs_profit.png", dpi=160); plt.close(fig)
    save_bar(status, "Order_Status", "Orders", "Order Status Distribution", "Status", "Orders", "12_order_status_distribution.png")
    save_bar(payment, "Payment_Method", "Orders", "Payment Method Distribution", "Payment Method", "Orders", "13_payment_method_distribution.png")
    fig, ax = plt.subplots(figsize=(9, 5)); ax.hist(orders.loc[orders["Delivery_Days"] > 0, "Delivery_Days"], bins=range(1, 12)); ax.set_title("Delivery Time Distribution"); ax.set_xlabel("Delivery Days"); ax.set_ylabel("Orders"); ax.grid(axis="y", alpha=.2); fig.tight_layout(); fig.savefig(CHART_DIR / "14_delivery_time_distribution.png", dpi=160); plt.close(fig)

    print(f"Generated analytical exports in {EXPORT_DIR}")
    print(f"Generated charts in {CHART_DIR}")


if __name__ == "__main__":
    main()
