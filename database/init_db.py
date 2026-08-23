"""
Database Initialization and Seeding Script for RetailPulse AI.
Loads schema and bulk-inserts generated CSV data into the configured database (PostgreSQL or SQLite).
"""

import os
import sys
import time
import pandas as pd
from sqlalchemy import text

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.database import engine, Base
from backend.app.models.retail import Category, Customer, Product, Order, OrderItem

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

def init_database():
    start_time = time.time()
    print("Connecting to database and creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # Read CSVs
    print(f"Loading raw datasets from {DATA_DIR}...")
    df_categories = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))
    df_customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    df_products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    df_orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
    df_order_items = pd.read_csv(os.path.join(DATA_DIR, "order_items.csv"))

    print("Populating database...")
    with engine.begin() as connection:
        df_categories.to_sql("categories", con=connection, if_exists="append", index=False)
        print(f" - Inserted {len(df_categories):,} categories")

        df_products.to_sql("products", con=connection, if_exists="append", index=False)
        print(f" - Inserted {len(df_products):,} products")

        df_customers.to_sql("customers", con=connection, if_exists="append", index=False, chunksize=2000)
        print(f" - Inserted {len(df_customers):,} customers")

        df_orders.to_sql("orders", con=connection, if_exists="append", index=False, chunksize=5000)
        print(f" - Inserted {len(df_orders):,} orders")

        df_order_items.to_sql("order_items", con=connection, if_exists="append", index=False, chunksize=10000)
        print(f" - Inserted {len(df_order_items):,} order items")

    duration = time.time() - start_time
    print(f"\nDatabase initialized and seeded in {duration:.2f} seconds.")

if __name__ == "__main__":
    init_database()
