"""Generate reproducible synthetic sales data for Pi Systems Private Limited.

Fictional company and synthetic dataset created for portfolio demonstration.
The script generates 5,600 orders / exactly 8,000 transaction lines, then injects
controlled data-quality issues and 50 duplicate rows into the RAW file.
"""
from pathlib import Path
import random
import numpy as np
import pandas as pd

SEED = 42
BASE_DIR = Path(__file__).resolve().parents[1]


def choose_order_line_counts(rng: np.random.Generator, segments: list[str]) -> list[int]:
    counts = []
    for segment in segments:
        probs = [0.56, 0.31, 0.13] if segment in {"Corporate", "Enterprise"} else [0.70, 0.23, 0.07]
        counts.append(int(rng.choice([1, 2, 3], p=probs)))
    current = sum(counts)
    while current < 8000:
        i = int(rng.integers(0, len(counts)))
        if counts[i] < 3:
            counts[i] += 1
            current += 1
    while current > 8000:
        i = int(rng.integers(0, len(counts)))
        if counts[i] > 1:
            counts[i] -= 1
            current -= 1
    return counts


def main() -> None:
    np.random.seed(SEED)
    random.seed(SEED)
    rng = np.random.default_rng(SEED)

    products = pd.read_csv(BASE_DIR / "data/reference/products.csv")
    customers = pd.read_csv(BASE_DIR / "data/reference/customers.csv")
    salespeople = pd.read_csv(BASE_DIR / "data/reference/salespeople.csv")

    dates = pd.date_range("2025-01-01", "2026-12-31", freq="D")
    month_mult = {1:.85, 2:.88, 3:.98, 4:1.00, 5:1.04, 6:.98, 7:.95, 8:1.02, 9:1.08, 10:1.25, 11:1.35, 12:1.45}
    date_weights = np.array([
        month_mult[d.month] * (1.13 if d.year == 2026 else 1.0) * (1.06 if d.weekday() < 5 else 0.88)
        for d in dates
    ], dtype=float)
    date_weights /= date_weights.sum()

    customer_weights = customers["Customer_Segment"].map({
        "Consumer": 0.8, "Small Business": 1.1, "Corporate": 1.6, "Enterprise": 2.6
    }).to_numpy(dtype=float)
    customer_weights[:25] *= 2.5
    customer_weights /= customer_weights.sum()

    product_weights = rng.lognormal(0, 0.65, len(products))
    product_weights /= product_weights.sum()

    n_orders = 5600
    chosen_dates = rng.choice(dates, size=n_orders, p=date_weights)
    customer_indices = rng.choice(len(customers), size=n_orders, p=customer_weights)
    order_segments = customers.iloc[customer_indices]["Customer_Segment"].tolist()
    line_counts = choose_order_line_counts(rng, order_segments)

    records: list[dict] = []
    for order_idx in range(n_orders):
        order_id = f"ORD{order_idx + 1:06d}"
        order_date = pd.Timestamp(chosen_dates[order_idx])
        customer = customers.iloc[int(customer_indices[order_idx])]
        regional_sp = salespeople[salespeople["Region"].eq(customer["Region"])]
        salesperson = regional_sp.iloc[int(rng.integers(len(regional_sp)))]
        status = rng.choice(["Completed", "Shipped", "Processing", "Cancelled", "Returned"], p=[.72, .11, .05, .07, .05])
        payment = rng.choice(["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"], p=[.34, .24, .16, .18, .08])
        shipping = rng.choice(["Standard", "Express", "Same Day"], p=[.68, .25, .07])
        if status in {"Cancelled", "Processing"}:
            delivery_days = 0
        else:
            means = {"Standard": 5.1, "Express": 2.5, "Same Day": 1.1}
            stds = {"Standard": 1.4, "Express": .8, "Same Day": .25}
            delivery_days = max(1, int(round(rng.normal(means[shipping], stds[shipping]))))

        selected_products: set[int] = set()
        for _ in range(line_counts[order_idx]):
            probs = product_weights.copy()
            if customer["Customer_Segment"] in {"Corporate", "Enterprise"}:
                probs *= np.where(products["Category"].isin(["Computers", "Networking", "Office Equipment", "Software"]), 1.5, .85)
            elif customer["Customer_Segment"] == "Consumer":
                probs *= np.where(products["Category"].isin(["Electronics", "Mobile Accessories", "Audio", "Gaming", "Home Appliances"]), 1.35, .90)
            if order_date.month in {10, 11, 12}:
                probs *= np.where(products["Category"].isin(["Electronics", "Gaming", "Computers", "Mobile Accessories"]), 1.30, 1.0)
            probs /= probs.sum()
            pi = int(rng.choice(len(products), p=probs))
            for _try in range(10):
                if pi not in selected_products:
                    break
                pi = int(rng.choice(len(products), p=probs))
            selected_products.add(pi)
            product = products.iloc[pi]

            quantity_choices = {
                "Consumer": [1, 1, 1, 2, 2, 3],
                "Small Business": [1, 1, 2, 2, 3, 4, 5],
                "Corporate": [1, 2, 3, 4, 5, 6, 8],
                "Enterprise": [2, 3, 4, 6, 8, 10, 12],
            }[customer["Customer_Segment"]]
            quantity = int(rng.choice(quantity_choices))
            if product["Category"] in {"Software", "Office Supplies", "Mobile Accessories"} and customer["Customer_Segment"] in {"Corporate", "Enterprise"}:
                quantity += int(rng.integers(0, 5))

            base_discount = {"Consumer": 3.5, "Small Business": 5.5, "Corporate": 8.0, "Enterprise": 11.0}[customer["Customer_Segment"]]
            discount_pct = float(np.clip(rng.normal(base_discount, 4.2), 0, 28))
            if order_date.month in {10, 11}:
                discount_pct = min(30, discount_pct + rng.uniform(1, 5))
            if product["Category"] == "Software":
                discount_pct = min(30, discount_pct + rng.uniform(0, 3))
            discount_pct = round(discount_pct, 2)

            unit_price = float(product["Unit_Price"])
            unit_cost = float(product["Unit_Cost"])
            gross = round(quantity * unit_price, 2)
            discount_amount = round(gross * discount_pct / 100, 2)
            sales = round(gross - discount_amount, 2)
            cost = round(quantity * unit_cost, 2)
            profit = round(sales - cost, 2)
            margin = round(profit / sales * 100, 2) if sales else 0.0

            if status == "Cancelled":
                net_sales, net_profit, net_quantity = 0.0, 0.0, 0
            elif status == "Returned":
                net_sales, net_profit, net_quantity = -sales, round(-0.12 * sales, 2), -quantity
            else:
                net_sales, net_profit, net_quantity = sales, profit, quantity

            records.append({
                "Order_ID": order_id, "Order_Date": order_date.date().isoformat(),
                "Customer_ID": customer["Customer_ID"], "Customer_Name": customer["Customer_Name"],
                "Customer_Segment": customer["Customer_Segment"], "Product_ID": product["Product_ID"],
                "Product_Name": product["Product_Name"], "Category": product["Category"], "Subcategory": product["Subcategory"],
                "Brand": product["Brand"], "Region": customer["Region"], "State": customer["State"], "City": customer["City"],
                "Salesperson_ID": salesperson["Salesperson_ID"], "Salesperson_Name": salesperson["Salesperson_Name"],
                "Quantity": quantity, "Unit_Price": round(unit_price, 2), "Unit_Cost": round(unit_cost, 2),
                "Discount_Percent": discount_pct, "Gross_Sales": gross, "Discount_Amount": discount_amount,
                "Sales_Amount": sales, "Cost_Amount": cost, "Profit": profit, "Profit_Margin": margin,
                "Payment_Method": payment, "Order_Status": status, "Shipping_Mode": shipping, "Delivery_Days": delivery_days,
                "Net_Sales_Amount": net_sales, "Net_Profit": net_profit, "Net_Quantity": net_quantity,
            })

    df = pd.DataFrame(records)
    if len(df) != 8000:
        raise RuntimeError(f"Expected exactly 8,000 base rows, got {len(df):,}.")

    # Controlled RAW data-quality issues for cleaning practice.
    for col, frac in [("Customer_Name", .006), ("City", .004), ("Delivery_Days", .004), ("Salesperson_Name", .003)]:
        idx = rng.choice(df.index, size=max(1, int(len(df) * frac)), replace=False)
        df.loc[idx, col] = np.nan
    for col in ["Category", "Payment_Method", "Order_Status", "Shipping_Mode", "Region"]:
        idx = rng.choice(df.index, size=int(len(df) * .018), replace=False)
        for j in idx:
            value = str(df.at[j, col])
            mode = rng.choice(["lower", "upper", "spaces"])
            df.at[j, col] = value.lower() if mode == "lower" else value.upper() if mode == "upper" else f"  {value} "
    aliases = {"Office Equipment": "Office Equip.", "Mobile Accessories": "Mobile Accessory", "Home Appliances": "Home Appliance", "Office Supplies": "Office Supply"}
    for j in rng.choice(df.index, size=70, replace=False):
        value = str(df.at[j, "Category"]).strip().title()
        if value in aliases:
            df.at[j, "Category"] = aliases[value]
    for j in rng.choice(df.index, size=180, replace=False):
        d = pd.Timestamp(records[int(j)]["Order_Date"])
        df.at[j, "Order_Date"] = rng.choice([d.strftime("%d/%m/%Y"), d.strftime("%m-%d-%Y"), d.strftime("%Y/%m/%d")])
    for j in rng.choice(df.index, size=100, replace=False):
        if pd.notna(df.at[j, "Customer_Name"]):
            df.at[j, "Customer_Name"] = f" {df.at[j, 'Customer_Name']} "
    for j in rng.choice(df.index, size=80, replace=False):
        df.at[j, "Product_Name"] = f" {df.at[j, 'Product_Name']} "

    raw = pd.concat([df, df.sample(50, random_state=SEED)], ignore_index=True)
    output = BASE_DIR / "data/raw/01_raw_data.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(output, index=False)
    print(f"Generated {len(raw):,} raw rows ({len(df):,} base + 50 duplicates) at {output}")


if __name__ == "__main__":
    main()
