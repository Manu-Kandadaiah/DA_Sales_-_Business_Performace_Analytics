"""Clean and validate the raw synthetic sales dataset."""
from pathlib import Path
import numpy as np
import pandas as pd
BASE_DIR=Path(__file__).resolve().parents[1]

def parse_date(value):
    if pd.isna(value): return pd.NaT
    s=str(value).strip()
    for fmt in ("%Y-%m-%d","%d/%m/%Y","%m-%d-%Y","%Y/%m/%d"):
        try: return pd.to_datetime(s,format=fmt)
        except ValueError: pass
    return pd.to_datetime(s,errors="coerce",dayfirst=True)

def main():
    df=pd.read_csv(BASE_DIR/"data/raw/01_raw_data.csv")
    customers=pd.read_csv(BASE_DIR/"data/reference/customers.csv").set_index("Customer_ID")
    products=pd.read_csv(BASE_DIR/"data/reference/products.csv").set_index("Product_ID")
    salespeople=pd.read_csv(BASE_DIR/"data/reference/salespeople.csv").set_index("Salesperson_ID")
    print("Shape before:",df.shape); print(df.head()); print(df.info()); print(df.describe(include="all")); print(df.isnull().sum()); print("Duplicates:",df.duplicated().sum()); print(df.nunique())
    df=df.drop_duplicates().copy()
    for c in df.select_dtypes(include="object").columns: df[c]=df[c].astype(str).str.strip().replace({"nan":np.nan})
    df["Order_Date"]=df["Order_Date"].map(parse_date)
    for col in ["Customer_Name","Customer_Segment","City","State","Region"]: df[col]=df["Customer_ID"].map(customers[col])
    for col in ["Product_Name","Category","Subcategory","Brand","Unit_Cost","Unit_Price"]: df[col]=df["Product_ID"].map(products[col])
    df["Salesperson_Name"]=df["Salesperson_ID"].map(salespeople["Salesperson_Name"])
    maps={"Payment_Method":{"upi":"UPI","credit card":"Credit Card","debit card":"Debit Card","net banking":"Net Banking","cash on delivery":"Cash on Delivery"},
          "Order_Status":{"completed":"Completed","shipped":"Shipped","processing":"Processing","cancelled":"Cancelled","returned":"Returned"},
          "Shipping_Mode":{"standard":"Standard","express":"Express","same day":"Same Day"}}
    for col,m in maps.items(): df[col]=df[col].astype(str).str.strip().str.lower().map(m)
    med=df[df.Delivery_Days.notna()].groupby("Shipping_Mode").Delivery_Days.median().to_dict()
    for i,r in df[df.Delivery_Days.isna()].iterrows(): df.at[i,"Delivery_Days"]=0 if r.Order_Status in ["Cancelled","Processing"] else med.get(r.Shipping_Mode,4)
    df["Delivery_Days"]=df.Delivery_Days.astype(int)
    df["Gross_Sales"]=(df.Quantity*df.Unit_Price).round(2); df["Discount_Amount"]=(df.Gross_Sales*df.Discount_Percent/100).round(2)
    df["Sales_Amount"]=(df.Gross_Sales-df.Discount_Amount).round(2); df["Cost_Amount"]=(df.Quantity*df.Unit_Cost).round(2); df["Profit"]=(df.Sales_Amount-df.Cost_Amount).round(2)
    df["Profit_Margin"]=np.where(df.Sales_Amount!=0,(df.Profit/df.Sales_Amount*100).round(2),0)
    df["Net_Sales_Amount"]=np.select([df.Order_Status.eq("Cancelled"),df.Order_Status.eq("Returned")],[0,-df.Sales_Amount],default=df.Sales_Amount).round(2)
    df["Net_Profit"]=np.select([df.Order_Status.eq("Cancelled"),df.Order_Status.eq("Returned")],[0,-.12*df.Sales_Amount],default=df.Profit).round(2)
    df["Net_Quantity"]=np.select([df.Order_Status.eq("Cancelled"),df.Order_Status.eq("Returned")],[0,-df.Quantity],default=df.Quantity).astype(int)
    df["Year"]=df.Order_Date.dt.year.astype(int); df["Month"]=df.Order_Date.dt.month_name().str[:3]; df["Quarter"]="Q"+df.Order_Date.dt.quarter.astype(str); df["Order_Month"]=df.Order_Date.dt.to_period("M").astype(str)
    df=df.sort_values(["Order_Date","Order_ID","Product_ID"]).reset_index(drop=True); df["Order_Flag"]=(~df.Order_ID.duplicated()).astype(int)
    assert not (df.Quantity<0).any(); assert not (df.Unit_Price<0).any(); assert np.allclose(df.Sales_Amount,df.Gross_Sales-df.Discount_Amount,atol=.02); assert np.allclose(df.Profit,df.Sales_Amount-df.Cost_Amount,atol=.02)
    out=BASE_DIR/"data/processed/02_cleaned_sales_data.csv"; out.parent.mkdir(parents=True,exist_ok=True); df.to_csv(out,index=False,date_format="%Y-%m-%d")
    print("Shape after:",df.shape,"Missing:",int(df.isna().sum().sum()),"Duplicates:",int(df.duplicated().sum()))
if __name__=="__main__": main()
