CREATE DATABASE IF NOT EXISTS pi_sales_analytics;
USE pi_sales_analytics;

CREATE TABLE IF NOT EXISTS categories (
 category_id INT PRIMARY KEY, category_name VARCHAR(80) NOT NULL, subcategory_name VARCHAR(80) NOT NULL, UNIQUE KEY uq_cat_sub(category_name,subcategory_name));
CREATE TABLE IF NOT EXISTS customers (
 customer_id VARCHAR(10) PRIMARY KEY, customer_name VARCHAR(120) NOT NULL, customer_segment VARCHAR(40) NOT NULL, city VARCHAR(60), state VARCHAR(60), region VARCHAR(30), signup_date DATE, INDEX idx_customer_region(region), INDEX idx_customer_segment(customer_segment));
CREATE TABLE IF NOT EXISTS products (
 product_id VARCHAR(10) PRIMARY KEY, product_name VARCHAR(160) NOT NULL, category_id INT NOT NULL, brand VARCHAR(80), unit_cost DECIMAL(14,2) NOT NULL, unit_price DECIMAL(14,2) NOT NULL, CONSTRAINT fk_product_category FOREIGN KEY(category_id) REFERENCES categories(category_id), INDEX idx_product_category(category_id));
CREATE TABLE IF NOT EXISTS salespeople (
 salesperson_id VARCHAR(10) PRIMARY KEY, salesperson_name VARCHAR(120) NOT NULL, region VARCHAR(30) NOT NULL, joining_date DATE, target_2026 DECIMAL(16,2), INDEX idx_sp_region(region));
CREATE TABLE IF NOT EXISTS orders (
 order_id VARCHAR(20) PRIMARY KEY, order_date DATE NOT NULL, customer_id VARCHAR(10) NOT NULL, salesperson_id VARCHAR(10) NOT NULL, order_status VARCHAR(30) NOT NULL, CONSTRAINT fk_order_customer FOREIGN KEY(customer_id) REFERENCES customers(customer_id), CONSTRAINT fk_order_salesperson FOREIGN KEY(salesperson_id) REFERENCES salespeople(salesperson_id), INDEX idx_order_date(order_date), INDEX idx_order_status(order_status));
CREATE TABLE IF NOT EXISTS order_items (
 order_item_id INT PRIMARY KEY, order_id VARCHAR(20) NOT NULL, product_id VARCHAR(10) NOT NULL, quantity INT NOT NULL CHECK(quantity>=0), unit_price DECIMAL(14,2) NOT NULL CHECK(unit_price>=0), discount_percent DECIMAL(6,2) NOT NULL, discount_amount DECIMAL(16,2) NOT NULL, sales_amount DECIMAL(16,2) NOT NULL, cost_amount DECIMAL(16,2) NOT NULL, profit DECIMAL(16,2) NOT NULL, profit_margin DECIMAL(8,2), net_sales_amount DECIMAL(16,2) NOT NULL, net_profit DECIMAL(16,2) NOT NULL, net_quantity INT NOT NULL, CONSTRAINT fk_item_order FOREIGN KEY(order_id) REFERENCES orders(order_id), CONSTRAINT fk_item_product FOREIGN KEY(product_id) REFERENCES products(product_id), INDEX idx_item_order(order_id), INDEX idx_item_product(product_id));
CREATE TABLE IF NOT EXISTS payments (order_id VARCHAR(20) PRIMARY KEY, payment_method VARCHAR(40) NOT NULL, CONSTRAINT fk_payment_order FOREIGN KEY(order_id) REFERENCES orders(order_id), INDEX idx_payment_method(payment_method));
CREATE TABLE IF NOT EXISTS shipping (order_id VARCHAR(20) PRIMARY KEY, shipping_mode VARCHAR(30) NOT NULL, delivery_days INT NOT NULL, CONSTRAINT fk_shipping_order FOREIGN KEY(order_id) REFERENCES orders(order_id), INDEX idx_shipping_mode(shipping_mode));
