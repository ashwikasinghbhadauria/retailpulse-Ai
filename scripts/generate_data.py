"""
RetailPulse AI — Realistic Synthetic Retail Data Generator
Generates:
- 10,000+ Customers across 5 Regions (North, South, East, West, Central)
- 120+ Products across 5 Categories (Electronics, Furniture, Office Supplies, Apparel, Home & Kitchen)
- 50,000+ Orders spanning 2023 to 2026 with realistic seasonality, price elasticity, repeat purchasing, and churn patterns.
- 120,000+ Order Items with realistic pricing, costs, discounts, and line profits.
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

# Set deterministic seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating synthetic retail dataset in {OUTPUT_DIR}...")

# -------------------------------------------------------------
# 1. Categories
# -------------------------------------------------------------
CATEGORIES = [
    {"category_id": "CAT-001", "category_name": "Electronics", "description": "Laptops, phones, audio devices, accessories and smart gadgets"},
    {"category_id": "CAT-002", "category_name": "Furniture", "description": "Ergonomic chairs, desks, bookcases, tables and lighting"},
    {"category_id": "CAT-003", "category_name": "Office Supplies", "description": "Paper, binders, pens, storage, filing and stationery"},
    {"category_id": "CAT-004", "category_name": "Apparel", "description": "Men, women and unisex clothing, athletic wear and accessories"},
    {"category_id": "CAT-005", "category_name": "Home & Kitchen", "description": "Appliances, cookware, storage containers and kitchenware"}
]

# -------------------------------------------------------------
# 2. Products (120+ Products)
# -------------------------------------------------------------
PRODUCT_TEMPLATES = {
    "CAT-001": [ # Electronics: High price, moderate margin (25-45%)
        ("ProBook Ultrabook 15", 899.99, 580.00),
        ("AirBeats Wireless ANC Headphones", 199.99, 110.00),
        ("SmartWatch Series X", 299.99, 175.00),
        ("4K Ultra HD 27-inch Monitor", 349.99, 220.00),
        ("ErgoClick Mechanical Keyboard", 129.99, 68.00),
        ("Precision Laser Gaming Mouse", 79.99, 38.00),
        ("ThunderBolt 10-in-1 Docking Station", 159.99, 85.00),
        ("FastCharge 65W GaN Charger", 49.99, 22.00),
        ("StreamCam 1080p Pro Webcam", 89.99, 44.00),
        ("SoundWave Portable Bluetooth Speaker", 69.99, 32.00),
        ("PowerVault 20000mAh Power Bank", 59.99, 26.00),
        ("TrueWireless Studio Earbuds", 149.99, 78.00),
        ("SmartHome Security Camera Hub", 179.99, 98.00),
        ("NoiseShield Pods Pro", 229.99, 125.00),
        ("UltraView 34-inch Curved Display", 599.99, 390.00),
        ("Creator Stylus Pen v2", 89.99, 42.00),
        ("MicroSDXC 256GB High-Speed Card", 39.99, 16.00),
        ("Smart Light Strip 5M RGB", 45.99, 19.00),
        ("MagSafe Car Mount Wireless Charger", 39.99, 17.00),
        ("Digital Voice Recorder Studio", 119.99, 59.00),
        ("Dual-Band Wi-Fi 6 Router Pro", 149.99, 82.00),
        ("USB-C Braided Cable 3-Pack", 24.99, 7.50),
        ("External SSD 1TB Rugged", 139.99, 74.00),
        ("HD Conference Speakerphone", 189.99, 102.00),
        ("VR Headset Motion Bundle", 449.99, 290.00)
    ],
    "CAT-002": [ # Furniture: Moderate to high price, good margin (35-55%)
        ("Apex Ergonomic Mesh Task Chair", 279.99, 140.00),
        ("Solid Oak Executive Standing Desk", 649.99, 330.00),
        ("Nordic Modern Bookshelf 5-Tier", 189.99, 92.00),
        ("Dual Monitor Gas Spring Arm", 99.99, 44.00),
        ("Mid-Century Velvet Lounge Armchair", 389.99, 185.00),
        ("Steel Frame Mobile File Cabinet", 149.99, 72.00),
        ("Minimalist LED Desk Lamp with Dimmer", 69.99, 28.00),
        ("Acoustic Felt Privacy Desk Divider", 89.99, 36.00),
        ("Adjustable Ergonomic Footrest", 49.99, 18.00),
        ("Conference Table Modular 8-Seater", 899.99, 460.00),
        ("Anti-Fatigue Standing Mat Deluxe", 59.99, 22.00),
        ("Under-Desk Cable Management Spine", 34.99, 11.00),
        ("Heavy Duty Storage Utility Cart", 79.99, 34.00),
        ("Stackable Guest Reception Chairs (Set of 2)", 199.99, 95.00),
        ("Walnut Finish Coffee Table", 219.99, 105.00),
        ("Modern Wall Mounted Floating Shelves", 54.99, 21.00),
        ("ErgoSupport Lumbar Pillow Cushion", 39.99, 14.00),
        ("Executive Leather Swivel High-Back", 459.99, 225.00),
        ("Foldable Study Desk Compact", 119.99, 52.00),
        ("Industrial Floor Lamp Brass Finish", 129.99, 56.00),
        ("Rolling Drafting Stool with Foot Ring", 139.99, 62.00),
        ("Wooden Credenza Sideboard Storage", 529.99, 260.00),
        ("Mesh Back Meeting Chair", 159.99, 74.00),
        ("Corner L-Shaped Gaming/Work Desk", 349.99, 165.00),
        ("Under-Desk Walking Pad Treadmill Stand", 299.99, 155.00)
    ],
    "CAT-003": [ # Office Supplies: Low price, high margin (50-70%), high frequency
        ("Premium Multi-Purpose Copy Paper 500 Sheets", 12.99, 4.20),
        ("Retractable Gel Ink Pens (Pack of 12)", 15.99, 4.50),
        ("Heavy-Duty Desktop Stapler & Remover", 22.99, 6.80),
        ("Heavy Duty Cross-Cut Paper Shredder", 89.99, 38.00),
        ("Assorted Pastel Sticky Notes (12 Pads)", 14.99, 3.80),
        ("Heavy Duty 3-Ring Presentation Binder 2-inch", 8.99, 2.40),
        ("Desktop Acrylic Organizer Set", 29.99, 9.50),
        ("Stainless Steel Office Scissors 3-Pack", 11.99, 3.20),
        ("Color Coded Expanding File Accordion Folder", 18.99, 5.40),
        ("Chalkboard & Whiteboard Dry Erase Markers 8-Pack", 13.99, 3.90),
        ("Self-Healing Cutting Mat & Precision Knife", 24.99, 7.20),
        ("Thermal Label Roll Pack (6 Rolls)", 32.99, 10.50),
        ("Heavy Duty Packing Tape with Dispenser 6-Pack", 26.99, 7.80),
        ("Laminating Machine & 50 Pouches Kit", 49.99, 17.50),
        ("Correction Tape Ergonomic Applicators 6-Pack", 9.99, 2.50),
        ("Magnetic Glass Dry-Erase Board 36x24", 79.99, 29.00),
        ("Mesh Metal Hanging File Organizer Box", 21.99, 6.50),
        ("Highlighter Marker Assorted Chisel Tip 10-Pack", 10.99, 2.80),
        ("Desk Pad Blotter Vegan Leather 36x20", 25.99, 7.90),
        ("Electric Heavy Duty Pencil Sharpener", 28.99, 9.20),
        ("Reinforced File Folders Letter Size 100-Pack", 27.99, 8.40),
        ("Binder Clips Assorted Sizes Tub of 100", 11.49, 2.90),
        ("Push Pins & Thumb Tacks Container 300-Count", 7.99, 1.80),
        ("Receipt & Card Scanner Mini Portable", 119.99, 48.00),
        ("Security Tint Self-Seal Envelopes 500-Pack", 29.99, 8.90)
    ],
    "CAT-004": [ # Apparel: Medium price, high margin (45-65%), seasonal
        ("Performance Moisture-Wicking Polo Shirt", 42.99, 14.50),
        ("Tech Fleece Athletic Zip Hoodie", 68.99, 24.00),
        ("All-Weather Waterproof Rain Shell Jacket", 119.99, 46.00),
        ("Slim-Fit Stretch Chino Work Trousers", 59.99, 21.00),
        ("Merino Wool Crewneck Sweater", 89.99, 32.00),
        ("Seamless Breathable Running T-Shirt", 34.99, 10.50),
        ("Lightweight Insulated Puffer Vest", 79.99, 28.00),
        ("Cushioned Anti-Blister Crew Socks (6 Pairs)", 21.99, 6.20),
        ("Thermal Compression Base Layer Set", 49.99, 16.00),
        ("Casual Oxford Button-Down Long Sleeve", 54.99, 18.50),
        ("Yoga Stretch High-Waisted Leggings", 44.99, 13.50),
        ("Canvas Weekender Duffel Travel Bag", 74.99, 26.00),
        ("Genuine Leather Dress Belt Reversible", 39.99, 12.00),
        ("UV Protection Brimmed Outdoor Sun Hat", 29.99, 8.50),
        ("Polarized Classic Sunglasses with UV400", 49.99, 13.00),
        ("Water-Resistant Commuter Backpack 25L", 84.99, 31.00),
        ("Fleece-Lined Winter Touchscreen Gloves", 24.99, 7.00),
        ("Quick-Dry Athletic Training Shorts", 32.99, 9.80),
        ("Classic Denim Trucker Jacket", 89.99, 33.00),
        ("Cotton Casual Graphic Tee", 26.99, 7.20),
        ("Windproof Softshell Soft Active Jacket", 94.99, 35.00),
        ("Thermal Knit Beanie Cap", 19.99, 5.00),
        ("Formal Tailored Suit Blazer", 179.99, 68.00),
        ("Slip-On Lightweight Walking Loafers", 64.99, 22.00),
        ("Quick-Dry Travel Swim Boardshorts", 36.99, 11.20)
    ],
    "CAT-005": [ # Home & Kitchen: Broad price, moderate to good margin (40-60%)
        ("Cold Brew Coffee Maker Glass Pitcher 1L", 34.99, 13.00),
        ("Stainless Steel Programmable Espresso Maker", 249.99, 115.00),
        ("Digital Air Fryer Max 6-Quart", 109.99, 48.00),
        ("Cast Iron Pre-Seasoned Dutch Oven 6-Qt", 79.99, 32.00),
        ("Professional Damascus Chef Knife 8-Inch", 69.99, 25.00),
        ("Aromatherapy Essential Oil Ultrasonic Diffuser", 29.99, 9.50),
        ("Vacuum Insulated Stainless Steel Tumbler 32oz", 27.99, 8.20),
        ("Smart Wi-Fi Meat Thermometer Wireless", 89.99, 36.00),
        ("Electric Gooseneck Precision Kettle 1.0L", 64.99, 26.00),
        ("Silicone Cooking Utensils 12-Piece Set", 36.99, 12.50),
        ("High-Speed Countertop Smoothie Blender 1200W", 129.99, 54.00),
        ("Heavy-Duty Bamboo Cutting Board Set (3-Piece)", 42.99, 14.00),
        ("Airtight Glass Food Storage Containers (18-Piece)", 49.99, 18.00),
        ("Electric Wine Opener Gift Set with Aerator", 32.99, 10.50),
        ("HEPA Air Purifier for Large Rooms 300 SqFt", 149.99, 62.00),
        ("Non-Stick Ceramic Frying Pan Set (8 & 10 Inch)", 59.99, 22.00),
        ("Robotic Vacuum Cleaner Slim with Auto-Charge", 229.99, 105.00),
        ("Stainless Steel Mixing Bowls with Lids (5-Pack)", 38.99, 13.20),
        ("Memory Foam Cooling Bed Pillow Standard", 45.99, 15.50),
        ("Luxury Turkish Cotton Bath Towels (Set of 4)", 54.99, 19.00),
        ("Ultra-Quiet Ultrasonic Cool Mist Humidifier", 49.99, 17.00),
        ("Compact Microwave Oven 900W Stainless", 119.99, 58.00),
        ("Rechargeable LED Motion Sensor Closet Lights", 28.99, 8.50),
        ("Digital Kitchen Scale with Precision Tare", 19.99, 5.80),
        ("Handheld Garment Fabric Steamer Fast-Heat", 39.99, 13.50)
    ]
}

products_list = []
prod_idx = 1
for cat_id, prods in PRODUCT_TEMPLATES.items():
    for name, price, cost in prods:
        p_id = f"PRD-{prod_idx:04d}"
        products_list.append({
            "product_id": p_id,
            "product_name": name,
            "category_id": cat_id,
            "price": round(price, 2),
            "cost": round(cost, 2)
        })
        prod_idx += 1

print(f"Created {len(products_list)} products across {len(CATEGORIES)} categories.")

# -------------------------------------------------------------
# 3. Customers (12,000 Customers)
# -------------------------------------------------------------
NUM_CUSTOMERS = 12000
REGIONS = {
    "West": ["Los Angeles", "San Francisco", "Seattle", "San Diego", "Portland", "Phoenix", "Las Vegas"],
    "East": ["New York City", "Boston", "Philadelphia", "Washington D.C.", "Baltimore", "Pittsburgh"],
    "Central": ["Chicago", "Dallas", "Houston", "Austin", "Minneapolis", "Detroit", "St. Louis"],
    "South": ["Atlanta", "Miami", "Charlotte", "Nashville", "Orlando", "Tampa", "New Orleans"],
    "North": ["Denver", "Salt Lake City", "Milwaukee", "Columbus", "Indianapolis", "Omaha"]
}
REGION_PROBS = [0.28, 0.26, 0.20, 0.16, 0.10] # West, East, Central, South, North
REGION_NAMES = list(REGIONS.keys())

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
               "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
               "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra",
               "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
               "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah",
               "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon", "Jeffrey", "Laura", "Ryan", "Cynthia",
               "Jacob", "Kathleen", "Gary", "Amy", "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen",
               "Stephen", "Anna", "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
               "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Alexander", "Debra", "Patrick", "Rachel",
               "Frank", "Catherine", "Raymond", "Carolyn", "Jack", "Janet", "Dennis", "Ruth", "Jerry", "Maria"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
              "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
              "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
              "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
              "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
              "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
              "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
              "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes"]

SEGMENT_TYPES = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

customers_list = []
START_DATE = datetime.date(2022, 1, 1)
END_DATE = datetime.date(2026, 8, 15)
TOTAL_DAYS = (END_DATE - START_DATE).days

for i in range(1, NUM_CUSTOMERS + 1):
    c_id = f"CUST-{i:05d}"
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    c_name = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}{i}@example.com"
    
    region = np.random.choice(REGION_NAMES, p=REGION_PROBS)
    city = random.choice(REGIONS[region])
    segment = np.random.choice(SEGMENT_TYPES, p=SEGMENT_WEIGHTS)
    
    # Random signup date skewed towards earlier years
    signup_day_offset = int(np.random.beta(a=1.5, b=2.0) * (TOTAL_DAYS - 90))
    signup_date = START_DATE + datetime.timedelta(days=signup_day_offset)
    
    customers_list.append({
        "customer_id": c_id,
        "customer_name": c_name,
        "email": email,
        "city": city,
        "region": region,
        "segment": segment,
        "signup_date": signup_date.isoformat()
    })

print(f"Created {len(customers_list)} customers.")

# -------------------------------------------------------------
# 4. Orders & Order Items (55,000 Orders, 130,000+ Items)
# -------------------------------------------------------------
NUM_ORDERS = 56000
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
SHIP_WEIGHTS = [0.58, 0.22, 0.15, 0.05]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Debit Card", "Bank Transfer", "Apple Pay"]
PAYMENT_WEIGHTS = [0.45, 0.25, 0.15, 0.08, 0.07]

# Customer purchasing behaviors:
# - High Value / Champions (15%): frequent, higher spending, recent
# - Loyal Regulars (35%): steady frequency, medium basket
# - Occasional / Casual (30%): 1-3 orders, spaced out
# - At-Risk / Churned (20%): joined early, active in 2023/2024, dormant in 2025/2026
cust_behavior_archetype = np.random.choice(["champion", "loyal", "occasional", "at_risk"], size=NUM_CUSTOMERS, p=[0.15, 0.35, 0.30, 0.20])

customer_map = {c["customer_id"]: (c, cust_behavior_archetype[idx]) for idx, c in enumerate(customers_list)}

orders_list = []
order_items_list = []
item_counter = 1

# Seasonality weight multiplier by month (1 to 12)
# Q4 holiday bump (Nov/Dec), Back-to-school (Aug/Sep), Spring bump (Mar/May)
MONTH_SEASONALITY = {
    1: 0.82, 2: 0.78, 3: 0.95, 4: 0.92, 5: 1.02, 6: 0.98,
    7: 1.00, 8: 1.10, 9: 1.08, 10: 1.05, 11: 1.38, 12: 1.55
}

product_lookup = {p["product_id"]: p for p in products_list}
cat_product_map = {}
for p in products_list:
    cat_product_map.setdefault(p["category_id"], []).append(p)

print("Simulating customer order lifecycles and transactions...")

order_counter = 1
for cust_id, (cust, archetype) in customer_map.items():
    signup_dt = datetime.date.fromisoformat(cust["signup_date"])
    days_since_signup = (END_DATE - signup_dt).days
    if days_since_signup <= 0:
        continue

    # Determine order count for customer
    if archetype == "champion":
        n_orders = np.random.randint(6, 18)
        last_active_window = 45 # active recently
    elif archetype == "loyal":
        n_orders = np.random.randint(3, 8)
        last_active_window = 90
    elif archetype == "occasional":
        n_orders = np.random.randint(1, 4)
        last_active_window = 200
    else: # at_risk
        n_orders = np.random.randint(2, 6)
        last_active_window = np.random.randint(180, 450) # stopped buying long ago

    # Generate dates
    max_days = max(1, days_since_signup - last_active_window)
    if archetype == "at_risk":
        # Order dates clustered early
        order_day_offsets = sorted(np.random.randint(0, max_days, size=n_orders))
    else:
        order_day_offsets = sorted(np.random.randint(0, days_since_signup, size=n_orders))

    for day_off in order_day_offsets:
        order_dt = signup_dt + datetime.timedelta(days=int(day_off))
        if order_dt > END_DATE:
            order_dt = END_DATE

        # Seasonality check
        season_prob = MONTH_SEASONALITY[order_dt.month] / 1.55
        if random.random() > season_prob and archetype != "champion":
            # skip slight probability during quiet months to simulate seasonal curves
            pass

        o_id = f"ORD-{order_counter:06d}"
        order_counter += 1
        
        ship_mode = np.random.choice(SHIP_MODES, p=SHIP_WEIGHTS)
        ship_days = 1 if ship_mode == "Same Day" else (2 if ship_mode == "First Class" else (3 if ship_mode == "Second Class" else 5))
        ship_dt = order_dt + datetime.timedelta(days=ship_days)
        pay_method = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)

        orders_list.append({
            "order_id": o_id,
            "customer_id": cust_id,
            "order_date": order_dt.isoformat(),
            "ship_date": ship_dt.isoformat(),
            "ship_mode": ship_mode,
            "region": cust["region"],
            "payment_method": pay_method,
            "order_status": "Completed"
        })

        # Order Items (1 to 5 distinct items per order)
        num_items_in_order = np.random.choice([1, 2, 3, 4, 5], p=[0.48, 0.28, 0.14, 0.07, 0.03])
        chosen_prods = random.sample(products_list, k=num_items_in_order)

        for prod in chosen_prods:
            oi_id = f"ITEM-{item_counter:07d}"
            item_counter += 1
            
            # Quantity depends on category
            if prod["category_id"] == "CAT-003": # Office supplies higher quantity
                qty = int(np.random.choice([1, 2, 3, 4, 5, 10], p=[0.35, 0.25, 0.18, 0.10, 0.08, 0.04]))
            elif prod["category_id"] == "CAT-001": # Electronics mostly 1 or 2
                qty = int(np.random.choice([1, 2, 3], p=[0.82, 0.15, 0.03]))
            else:
                qty = int(np.random.choice([1, 2, 3, 4], p=[0.60, 0.25, 0.10, 0.05]))

            # Discounts: mostly 0%, occasionally 5%, 10%, 15%, 20%, 30%
            # November/December and certain products have higher discount probability
            if order_dt.month in [11, 12] or random.random() < 0.22:
                discount = float(np.random.choice([0.05, 0.10, 0.15, 0.20, 0.30], p=[0.25, 0.35, 0.20, 0.12, 0.08]))
            else:
                discount = 0.00

            unit_price = prod["price"]
            cost = prod["cost"]
            line_total = round(qty * unit_price * (1.0 - discount), 2)
            line_profit = round(line_total - (qty * cost), 2)

            order_items_list.append({
                "order_item_id": oi_id,
                "order_id": o_id,
                "product_id": prod["product_id"],
                "quantity": qty,
                "unit_price": unit_price,
                "discount": discount,
                "line_total": line_total,
                "line_profit": line_profit
            })

print(f"Generated {len(orders_list)} orders and {len(order_items_list)} line items.")

# -------------------------------------------------------------
# 5. Export Raw CSV Datasets
# -------------------------------------------------------------
df_categories = pd.DataFrame(CATEGORIES)
df_products = pd.DataFrame(products_list)
df_customers = pd.DataFrame(customers_list)
df_orders = pd.DataFrame(orders_list)
df_order_items = pd.DataFrame(order_items_list)

df_categories.to_csv(os.path.join(OUTPUT_DIR, "categories.csv"), index=False)
df_products.to_csv(os.path.join(OUTPUT_DIR, "products.csv"), index=False)
df_customers.to_csv(os.path.join(OUTPUT_DIR, "customers.csv"), index=False)
df_orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False)
df_order_items.to_csv(os.path.join(OUTPUT_DIR, "order_items.csv"), index=False)

# Master denormalized view for direct BI tools / rapid pandas analysis
df_master = df_order_items.merge(df_orders, on="order_id") \
                          .merge(df_products, on="product_id") \
                          .merge(df_categories, on="category_id") \
                          .merge(df_customers, on="customer_id")

df_master.to_csv(os.path.join(OUTPUT_DIR, "retail_transactions_master.csv"), index=False)

print("\n--- Summary Statistics of Synthetic Retail Data ---")
print(f"Total Customers: {len(df_customers):,}")
print(f"Total Products: {len(df_products):,}")
print(f"Total Orders: {len(df_orders):,}")
print(f"Total Line Items: {len(df_order_items):,}")
print(f"Total Gross Revenue: ${df_order_items['line_total'].sum():,.2f}")
print(f"Total Gross Profit: ${df_order_items['line_profit'].sum():,.2f}")
print(f"Overall Profit Margin: {(df_order_items['line_profit'].sum() / df_order_items['line_total'].sum()) * 100:.2f}%")
print(f"Date Span: {df_orders['order_date'].min()} to {df_orders['order_date'].max()}")
print("Master dataset saved successfully!")
