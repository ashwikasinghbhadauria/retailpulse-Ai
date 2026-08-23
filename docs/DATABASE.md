# RetailPulse AI — Database Schema & ER Design

This document details the normalized relational database architecture (3NF), tables, integrity constraints, and query indexes.

---

## Entity-Relationship (ER) Schema

```
+--------------------+        +--------------------+
|     categories     |        |     customers      |
|--------------------|        |--------------------|
| PK category_id     |<---+   | PK customer_id     |<---+
|    category_name   |    |   |    customer_name   |    |
|    description     |    |   |    email           |    |
|    created_at      |    |   |    city            |    |
+--------------------+    |   |    region          |    |
                          |   |    segment         |    |
                          |   |    signup_date     |    |
                          |   |    created_at      |    |
                          |   +--------------------+    |
+--------------------+    |                             |
|      products      |    |                             |
|--------------------|    |                             |
| PK product_id      |    |   +--------------------+    |
|    product_name    |    |   |       orders       |    |
| FK category_id     |----+   |--------------------|    |
|    price           |        | PK order_id        |    |
|    cost            |        | FK customer_id     |----+
|    created_at      |        |    order_date      |
+--------------------+        |    ship_date       |
         ^                    |    ship_mode       |
         |                    |    region          |
         |                    |    payment_method  |
         |                    |    order_status    |
         |                    |    created_at      |
         |                    +--------------------+
         |                              ^
         +--------------------+         |
                              |         |
                     +--------------------+
                     |    order_items     |
                     |--------------------|
                     | PK order_item_id   |
                     | FK order_id        |----+
                     | FK product_id      |
                     |    quantity        |
                     |    unit_price      |
                     |    discount        |
                     |    line_total      |
                     |    line_profit     |
                     |    created_at      |
                     +--------------------+
```

---

## Table Definitions

### 1. `categories`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | VARCHAR(50) | PRIMARY KEY | Unique category identifier |
| `category_name` | VARCHAR(100) | NOT NULL, UNIQUE | Category name |
| `description` | TEXT | NULLABLE | Category description |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

### 2. `customers`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | VARCHAR(50) | PRIMARY KEY | Unique customer identifier |
| `customer_name` | VARCHAR(100) | NOT NULL | Customer full name |
| `email` | VARCHAR(150) | UNIQUE | Customer email address |
| `city` | VARCHAR(100) | NOT NULL | Customer city location |
| `region` | VARCHAR(50) | NOT NULL | Territory (West, East, Central, South, North) |
| `segment` | VARCHAR(50) | NOT NULL | Consumer, Corporate, Home Office |
| `signup_date` | DATE | NOT NULL | Account creation date |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

### 3. `products`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | VARCHAR(50) | PRIMARY KEY | Unique SKU identifier |
| `product_name` | VARCHAR(200) | NOT NULL | Product name |
| `category_id` | VARCHAR(50) | NOT NULL, FK -> `categories` | Category link |
| `price` | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | List price |
| `cost` | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | Unit COGS |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

### 4. `orders`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(50) | PRIMARY KEY | Unique order number |
| `customer_id` | VARCHAR(50) | NOT NULL, FK -> `customers` | Customer reference |
| `order_date` | DATE | NOT NULL | Date order was placed |
| `ship_date` | DATE | NULLABLE | Date order was shipped |
| `ship_mode` | VARCHAR(50) | DEFAULT 'Standard Class' | Shipping tier |
| `region` | VARCHAR(50) | NOT NULL | Destination sales territory |
| `payment_method`| VARCHAR(50) | NOT NULL | Payment provider |
| `order_status` | VARCHAR(50) | DEFAULT 'Completed' | Fulfillment status |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

### 5. `order_items`
| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `order_item_id`| VARCHAR(50) | PRIMARY KEY | Unique line item identifier |
| `order_id` | VARCHAR(50) | NOT NULL, FK -> `orders` | Order parent reference |
| `product_id` | VARCHAR(50) | NOT NULL, FK -> `products` | Product reference |
| `quantity` | INTEGER | NOT NULL, CHECK > 0 | Units purchased |
| `unit_price` | NUMERIC(10,2)| NOT NULL, CHECK >= 0 | Sale unit price |
| `discount` | NUMERIC(5,2) | DEFAULT 0.00, 0.0 to 1.0 | Promotional discount rate |
| `line_total` | NUMERIC(12,2)| NOT NULL | `quantity * unit_price * (1 - discount)` |
| `line_profit` | NUMERIC(12,2)| NOT NULL | `line_total - (quantity * cost)` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

---

## Performance Indexing Strategy

- `idx_customers_region` on `customers(region)`
- `idx_customers_signup` on `customers(signup_date)`
- `idx_products_category` on `products(category_id)`
- `idx_orders_customer` on `orders(customer_id)`
- `idx_orders_date` on `orders(order_date)`
- `idx_orders_region` on `orders(region)`
- `idx_order_items_order` on `order_items(order_id)`
- `idx_order_items_product` on `order_items(product_id)`
