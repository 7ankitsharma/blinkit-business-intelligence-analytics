-- USE blinkit_analysis;

-- CREATE TABLE customers (
--     customer_id INT PRIMARY KEY,
--     signup_date DATE NOT NULL,
--     gender VARCHAR(10),
--     age TINYINT,
--     city VARCHAR(50),
--     membership_type VARCHAR(20),
--     acquisition_channel VARCHAR(50),
--     customer_status VARCHAR(20)
-- );
-- SHOW TABLES;
-- CREATE TABLE products (
--     product_id INT PRIMARY KEY,
--     SKU VARCHAR(30) NOT NULL,
--     product_name VARCHAR(150) NOT NULL,
--     brand VARCHAR(50),
--     category VARCHAR(50),
--     subcategory VARCHAR(50),
--     MRP DECIMAL(10,2),
--     selling_price DECIMAL(10,2),
--     cost_price DECIMAL(10,2),
--     weight VARCHAR(20),
--     supplier VARCHAR(100),
--     GST_rate DECIMAL(4,2),
--     rating DECIMAL(2,1),
--     launch_date DATE,
--     discontinued_flag BOOLEAN
-- );
-- CREATE TABLE stores (
--     store_id INT PRIMARY KEY,
--     city VARCHAR(50),
--     locality VARCHAR(100),
--     warehouse_capacity INT
-- );
-- CREATE TABLE delivery_partners (
--     delivery_partner_id INT PRIMARY KEY,
--     joining_date DATE,
--     city VARCHAR(50),
--     vehicle_type VARCHAR(20),
--     employment_type VARCHAR(20),
--     average_rating DECIMAL(2,1)
-- );
-- CREATE TABLE coupons (
--     coupon_id INT PRIMARY KEY,
--     coupon_code VARCHAR(30),
--     discount_type VARCHAR(20),
--     discount_value DECIMAL(10,2),
--     minimum_order_value DECIMAL(10,2),
--     expiry_date DATE,
--     is_active BOOLEAN
-- );
-- CREATE TABLE calendar (
--     date DATE PRIMARY KEY,
--     day_name VARCHAR(20),
--     week_number INT,
--     month INT,
--     quarter INT,
--     year INT,
--     is_weekend BOOLEAN,
--     festival VARCHAR(50),
--     is_holiday BOOLEAN
-- );
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT,
    payment_method VARCHAR(30),
    payment_status VARCHAR(20),
    payment_datetime DATETIME,
    gateway VARCHAR(30),
    transaction_amount DECIMAL(10,2)
);
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    store_id INT,
    delivery_partner_id INT,
    payment_id INT,
    coupon_id INT,
    order_datetime DATETIME,
    delivery_datetime DATETIME,
    promised_delivery_minutes INT,
    actual_delivery_minutes INT,
    delivery_distance_km DECIMAL(5,2),
    order_status VARCHAR(20),
    weather VARCHAR(20),
    traffic_level VARCHAR(20),
    order_value DECIMAL(10,2),
    delivery_fee DECIMAL(10,2),
    platform_fee DECIMAL(10,2),
    packaging_fee DECIMAL(10,2),
    discount DECIMAL(10,2),
    total_paid DECIMAL(10,2),
    tip_amount DECIMAL(10,2),
    order_source VARCHAR(20),
    customer_rating DECIMAL(2,1),
    cancellation_reason VARCHAR(100)
);
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    item_discount DECIMAL(10,2),
    total_price DECIMAL(10,2),
    cost_price_at_sale DECIMAL(10,2),
    profit DECIMAL(10,2),
    profit_margin DECIMAL(5,2)
);
show tables ;