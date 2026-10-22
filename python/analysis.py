"""Business analysis using Pandas and NumPy."""
from pathlib import Path
import numpy as np
import pandas as pd
BASE_DIR=Path(__file__).resolve().parents[1]

def main():
    df=pd.read_csv(BASE_DIR/"data/processed/02_cleaned_sales_data.csv",parse_dates=["Order_Date"])
    orders=df[df.Order_Flag.eq(1)]
    revenue=df.Net_Sales_Amount.sum(); profit=df.Net_Profit.sum(); n_orders=df.Order_Flag.sum()
    print("Total revenue:",revenue); print("Total profit:",profit); print("Average order value:",revenue/n_orders); print("Profit margin %:",profit/revenue*100)
    # NumPy examples with business meaning
    rev=df.Net_Sales_Amount.to_numpy(); print("Mean line revenue:",np.mean(rev)); print("Median:",np.median(rev)); print("Std dev:",np.std(rev)); print("95th percentile:",np.percentile(rev,95))
    df["Margin_Flag"]=np.where(df.Profit_Margin<10,"Low Margin","Normal")
    df["Discount_Band"]=np.select([df.Discount_Percent<=5,df.Discount_Percent<=10,df.Discount_Percent<=20],["0-5%","5-10%","10-20%"],default="20%+")
    print(df.groupby("Category").agg(Revenue=("Net_Sales_Amount","sum"),Profit=("Net_Profit","sum")).sort_values("Revenue",ascending=False))
    print(orders["Order_Status"].value_counts(normalize=True).mul(100))
    # loc/iloc examples
    print(df.loc[df.Region.eq("South"),["Order_ID","Region","Net_Sales_Amount"]].head())
    print(df.iloc[:5,:8])
if __name__=="__main__": main()
