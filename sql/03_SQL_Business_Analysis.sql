USE pi_sales_analytics;
-- 1 Total net revenue
SELECT ROUND(SUM(net_sales_amount),2) AS total_revenue FROM order_items;
-- 2 Total net profit
SELECT ROUND(SUM(net_profit),2) AS total_profit FROM order_items;
-- 3 Average order value
SELECT ROUND(SUM(oi.net_sales_amount)/COUNT(DISTINCT oi.order_id),2) AS avg_order_value FROM order_items oi;
-- 4 Monthly revenue
SELECT DATE_FORMAT(o.order_date,'%Y-%m') month, ROUND(SUM(oi.net_sales_amount),2) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY month ORDER BY month;
-- 5 Monthly profit
SELECT DATE_FORMAT(o.order_date,'%Y-%m') month, ROUND(SUM(oi.net_profit),2) profit FROM orders o JOIN order_items oi USING(order_id) GROUP BY month ORDER BY month;
-- 6 Yearly revenue
SELECT YEAR(o.order_date) year, ROUND(SUM(oi.net_sales_amount),2) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY year ORDER BY year;
-- 7 Top products
SELECT p.product_name, ROUND(SUM(oi.net_sales_amount),2) revenue FROM order_items oi JOIN products p USING(product_id) GROUP BY p.product_id,p.product_name ORDER BY revenue DESC LIMIT 10;
-- 8 Top customers
SELECT c.customer_name, ROUND(SUM(oi.net_sales_amount),2) revenue FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.customer_id,c.customer_name ORDER BY revenue DESC LIMIT 10;
-- 9 Revenue by category
SELECT c.category_name, ROUND(SUM(oi.net_sales_amount),2) revenue FROM order_items oi JOIN products p USING(product_id) JOIN categories c USING(category_id) GROUP BY c.category_name ORDER BY revenue DESC;
-- 10 Profit by category
SELECT c.category_name, ROUND(SUM(oi.net_profit),2) profit FROM order_items oi JOIN products p USING(product_id) JOIN categories c USING(category_id) GROUP BY c.category_name ORDER BY profit DESC;
-- 11 Revenue by region
SELECT c.region, ROUND(SUM(oi.net_sales_amount),2) revenue FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.region ORDER BY revenue DESC;
-- 12 Profit by region
SELECT c.region, ROUND(SUM(oi.net_profit),2) profit FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.region ORDER BY profit DESC;
-- 13 Salesperson performance vs 2026 target
SELECT s.salesperson_name,s.region,s.target_2026,ROUND(SUM(oi.net_sales_amount),2) revenue,ROUND(SUM(oi.net_sales_amount)/NULLIF(s.target_2026,0)*100,1) target_achievement_pct FROM orders o JOIN salespeople s USING(salesperson_id) JOIN order_items oi USING(order_id) WHERE YEAR(o.order_date)=2026 GROUP BY s.salesperson_id,s.salesperson_name,s.region,s.target_2026 ORDER BY revenue DESC;
-- 14 Customer segment performance
SELECT c.customer_segment,ROUND(SUM(oi.net_sales_amount),2) revenue,ROUND(SUM(oi.net_profit),2) profit FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.customer_segment ORDER BY revenue DESC;
-- 15 Cancelled orders
SELECT COUNT(*) cancelled_orders,ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM orders),2) cancellation_rate_pct FROM orders WHERE order_status='Cancelled';
-- 16 Returned orders
SELECT COUNT(*) returned_orders,ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM orders),2) return_rate_pct FROM orders WHERE order_status='Returned';
-- 17 Average delivery time
SELECT ROUND(AVG(NULLIF(delivery_days,0)),2) avg_delivery_days FROM shipping;
-- 18 Payment method analysis
SELECT payment_method,COUNT(*) orders,ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),2) share_pct FROM payments GROUP BY payment_method ORDER BY orders DESC;
-- 19 Low-performing products
SELECT p.product_name,ROUND(SUM(oi.net_sales_amount),2) revenue FROM order_items oi JOIN products p USING(product_id) GROUP BY p.product_id,p.product_name HAVING revenue < (SELECT AVG(product_revenue) FROM (SELECT SUM(net_sales_amount) product_revenue FROM order_items GROUP BY product_id) x) ORDER BY revenue ASC LIMIT 20;
-- 20 High-profit products
SELECT p.product_name,ROUND(SUM(oi.net_profit),2) profit FROM order_items oi JOIN products p USING(product_id) GROUP BY p.product_id,p.product_name ORDER BY profit DESC LIMIT 10;
-- 21 High-revenue low-profit products
WITH x AS (SELECT p.product_id,p.product_name,SUM(oi.net_sales_amount) revenue,SUM(oi.net_profit) profit FROM order_items oi JOIN products p USING(product_id) GROUP BY p.product_id,p.product_name), y AS (SELECT *, profit/NULLIF(revenue,0)*100 margin, NTILE(4) OVER(ORDER BY revenue DESC) revenue_quartile FROM x) SELECT product_id,product_name,revenue,profit,margin FROM y WHERE revenue_quartile=1 ORDER BY margin ASC LIMIT 10;
-- 22 Discount analysis
SELECT CASE WHEN discount_percent<=5 THEN '0-5%' WHEN discount_percent<=10 THEN '5-10%' WHEN discount_percent<=20 THEN '10-20%' ELSE '20%+' END discount_band,ROUND(SUM(net_sales_amount),2) revenue,ROUND(SUM(net_profit),2) profit,ROUND(SUM(net_profit)/NULLIF(SUM(net_sales_amount),0)*100,2) margin_pct FROM order_items GROUP BY discount_band ORDER BY MIN(discount_percent);
-- 23 Month-over-month growth
WITH m AS (SELECT DATE_FORMAT(o.order_date,'%Y-%m') month,SUM(oi.net_sales_amount) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY month), x AS (SELECT month,revenue,LAG(revenue) OVER(ORDER BY month) prev_revenue FROM m) SELECT month,ROUND(revenue,2) revenue,ROUND((revenue-prev_revenue)/NULLIF(prev_revenue,0)*100,2) mom_growth_pct FROM x;
-- 24 Year-over-year growth
WITH y AS (SELECT YEAR(o.order_date) year,SUM(oi.net_sales_amount) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY year), x AS (SELECT year,revenue,LAG(revenue) OVER(ORDER BY year) prev_revenue FROM y) SELECT year,ROUND(revenue,2),ROUND((revenue-prev_revenue)/NULLIF(prev_revenue,0)*100,2) yoy_growth_pct FROM x;
-- 25 Running revenue total
WITH m AS (SELECT DATE_FORMAT(o.order_date,'%Y-%m') month,SUM(oi.net_sales_amount) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY month) SELECT month,ROUND(revenue,2) monthly_revenue,ROUND(SUM(revenue) OVER(ORDER BY month),2) running_revenue FROM m;
-- 26 Product ranking
WITH p AS (SELECT product_id,SUM(net_sales_amount) revenue FROM order_items GROUP BY product_id) SELECT pr.product_name,ROUND(p.revenue,2) revenue,RANK() OVER(ORDER BY p.revenue DESC) revenue_rank FROM p JOIN products pr USING(product_id) ORDER BY revenue_rank;
-- 27 Customer ranking
WITH c AS (SELECT o.customer_id,SUM(oi.net_sales_amount) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY o.customer_id) SELECT cu.customer_name,ROUND(c.revenue,2) revenue,DENSE_RANK() OVER(ORDER BY c.revenue DESC) customer_rank FROM c JOIN customers cu USING(customer_id) ORDER BY customer_rank;
-- 28 Regional ranking
WITH r AS (SELECT c.region,SUM(oi.net_sales_amount) revenue FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.region) SELECT region,ROUND(revenue,2) revenue,ROW_NUMBER() OVER(ORDER BY revenue DESC) regional_rank FROM r;
-- 29 Top 20% customers
WITH c AS (SELECT o.customer_id,SUM(oi.net_sales_amount) revenue FROM orders o JOIN order_items oi USING(order_id) GROUP BY o.customer_id), r AS (SELECT *,NTILE(5) OVER(ORDER BY revenue DESC) quintile FROM c) SELECT cu.customer_name,ROUND(r.revenue,2) revenue FROM r JOIN customers cu USING(customer_id) WHERE quintile=1 ORDER BY revenue DESC;
-- 30 Products contributing to major revenue share
WITH p AS (SELECT product_id,SUM(net_sales_amount) revenue FROM order_items GROUP BY product_id), x AS (SELECT product_id,revenue,SUM(revenue) OVER(ORDER BY revenue DESC) cumulative_revenue,SUM(revenue) OVER() total_revenue FROM p) SELECT pr.product_name,ROUND(x.revenue,2) revenue,ROUND(x.cumulative_revenue/x.total_revenue*100,2) cumulative_share_pct FROM x JOIN products pr USING(product_id) WHERE x.cumulative_revenue/x.total_revenue<=0.85 ORDER BY revenue DESC;
-- 31 Best states
SELECT c.state,ROUND(SUM(oi.net_sales_amount),2) revenue,ROUND(SUM(oi.net_profit),2) profit FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.state ORDER BY revenue DESC LIMIT 10;
-- 32 Best cities
SELECT c.city,c.state,ROUND(SUM(oi.net_sales_amount),2) revenue FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY c.city,c.state ORDER BY revenue DESC LIMIT 10;
-- 33 Shipping mode performance
SELECT s.shipping_mode,COUNT(*) orders,ROUND(AVG(NULLIF(s.delivery_days,0)),2) avg_delivery_days FROM shipping s GROUP BY s.shipping_mode ORDER BY orders DESC;
-- 34 Order status by region
SELECT c.region,o.order_status,COUNT(*) orders FROM orders o JOIN customers c USING(customer_id) GROUP BY c.region,o.order_status ORDER BY c.region,orders DESC;
-- 35 Brand performance
SELECT p.brand,ROUND(SUM(oi.net_sales_amount),2) revenue,ROUND(SUM(oi.net_profit),2) profit FROM order_items oi JOIN products p USING(product_id) GROUP BY p.brand ORDER BY revenue DESC;

-- 36 Customer sales coverage using LEFT JOIN and COALESCE
SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(ROUND(SUM(oi.net_sales_amount), 2), 0) AS revenue
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY revenue DESC;

-- 37 Product price range by category using MIN and MAX
SELECT
    ca.category_name,
    ROUND(MIN(p.unit_price), 2) AS min_unit_price,
    ROUND(MAX(p.unit_price), 2) AS max_unit_price,
    COUNT(DISTINCT p.product_id) AS product_count
FROM categories ca
JOIN products p ON p.category_id = ca.category_id
GROUP BY ca.category_name
ORDER BY ca.category_name;
