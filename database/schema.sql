-- ========================================================
-- RetailPulse AI — Production Normalized Database Schema (3NF)
-- Compatible with PostgreSQL and SQLite
-- ========================================================

-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    segment VARCHAR(50) NOT NULL DEFAULT 'Consumer',
    signup_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    cost NUMERIC(10, 2) NOT NULL CHECK (cost >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    ship_mode VARCHAR(50) DEFAULT 'Standard Class',
    region VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    order_status VARCHAR(50) DEFAULT 'Completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    discount NUMERIC(5, 2) NOT NULL DEFAULT 0.00 CHECK (discount >= 0.00 AND discount <= 1.00),
    line_total NUMERIC(12, 2) NOT NULL,
    line_profit NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE RESTRICT
);

-- Indexes for Optimal Analytical Query Performance
CREATE INDEX IF NOT EXISTS idx_customers_region ON customers(region);
CREATE INDEX IF NOT EXISTS idx_customers_signup ON customers(signup_date);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
