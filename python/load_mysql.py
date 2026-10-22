"""Load the cleaned portfolio dataset into the normalized MySQL schema."""
from pathlib import Path
import os
import pandas as pd
import mysql.connector
BASE_DIR=Path(__file__).resolve().parents[1]

def connect():
    return mysql.connector.connect(host=os.getenv("MYSQL_HOST","localhost"),user=os.getenv("MYSQL_USER","root"),password=os.getenv("MYSQL_PASSWORD",""),database=os.getenv("MYSQL_DATABASE","pi_sales_analytics"))

def executemany(cur,sql,rows,batch=1000):
    rows=list(rows)
    for i in range(0,len(rows),batch): cur.executemany(sql,rows[i:i+batch])

def main():
    df=pd.read_csv(BASE_DIR/"data/processed/02_cleaned_sales_data.csv")
    customers=pd.read_csv(BASE_DIR/"data/reference/customers.csv"); products=pd.read_csv(BASE_DIR/"data/reference/products.csv"); salespeople=pd.read_csv(BASE_DIR/"data/reference/salespeople.csv")
    cn=connect(); cur=cn.cursor()
    cats=products[["Category","Subcategory"]].drop_duplicates().reset_index(drop=True); cats["category_id"]=range(1,len(cats)+1)
    executemany(cur,"INSERT INTO categories(category_id,category_name,subcategory_name) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE category_name=VALUES(category_name)",cats[["category_id","Category","Subcategory"]].itertuples(index=False,name=None))
    executemany(cur,"INSERT INTO customers(customer_id,customer_name,customer_segment,city,state,region,signup_date) VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE customer_name=VALUES(customer_name)",customers.itertuples(index=False,name=None))
    p=products.merge(cats,on=["Category","Subcategory"])
    executemany(cur,"INSERT INTO products(product_id,product_name,category_id,brand,unit_cost,unit_price) VALUES(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE unit_price=VALUES(unit_price)",p[["Product_ID","Product_Name","category_id","Brand","Unit_Cost","Unit_Price"]].itertuples(index=False,name=None))
    executemany(cur,"INSERT INTO salespeople(salesperson_id,salesperson_name,region,joining_date,target_2026) VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE target_2026=VALUES(target_2026)",salespeople.itertuples(index=False,name=None))
    orders=df.sort_values("Order_Date").drop_duplicates("Order_ID")
    executemany(cur,"INSERT INTO orders(order_id,order_date,customer_id,salesperson_id,order_status) VALUES(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE order_status=VALUES(order_status)",orders[["Order_ID","Order_Date","Customer_ID","Salesperson_ID","Order_Status"]].itertuples(index=False,name=None))
    item_rows=[]
    for i,r in df.reset_index(drop=True).iterrows(): item_rows.append((i+1,r.Order_ID,r.Product_ID,int(r.Quantity),r.Unit_Price,r.Discount_Percent,r.Discount_Amount,r.Sales_Amount,r.Cost_Amount,r.Profit,r.Profit_Margin,r.Net_Sales_Amount,r.Net_Profit,int(r.Net_Quantity)))
    executemany(cur,"INSERT INTO order_items(order_item_id,order_id,product_id,quantity,unit_price,discount_percent,discount_amount,sales_amount,cost_amount,profit,profit_margin,net_sales_amount,net_profit,net_quantity) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",item_rows)
    executemany(cur,"INSERT INTO payments(order_id,payment_method) VALUES(%s,%s) ON DUPLICATE KEY UPDATE payment_method=VALUES(payment_method)",orders[["Order_ID","Payment_Method"]].itertuples(index=False,name=None))
    executemany(cur,"INSERT INTO shipping(order_id,shipping_mode,delivery_days) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE delivery_days=VALUES(delivery_days)",orders[["Order_ID","Shipping_Mode","Delivery_Days"]].itertuples(index=False,name=None))
    cn.commit(); cur.close(); cn.close(); print("MySQL load complete")
if __name__=="__main__": main()
