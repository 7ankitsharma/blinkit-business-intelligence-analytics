import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# --- INITIALIZATION ---
fake = Faker('en_IN')
np.random.seed(42)

# Configuration
NUM_CUSTOMERS = 250000
NUM_PRODUCTS = 8000
NUM_STORES = 120
NUM_PARTNERS = 15000
NUM_ORDERS = 1000000  # Full 1M orders for production-grade scale
START_DATE = datetime(2023, 1, 1)

print("🚀 Starting Enterprise-Grade Blinkit Dataset Generation...")

# --- 1. CALENDAR TABLE ---
def generate_calendar():
    print("📅 Generating Calendar...")
    date_range = pd.date_range(start="2023-01-01", end="2023-12-31")
    df = pd.DataFrame({'date': date_range})
    df['day_name'] = df['date'].dt.day_name()
    df['week_number'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday']).astype(int)
    
    festivals = {
        '2023-01-14': 'Makar Sankranti', '2023-01-26': 'Republic Day',
        '2023-03-08': 'Holi', '2023-08-15': 'Independence Day',
        '2023-10-24': 'Dussehra', '2023-11-12': 'Diwali', '2023-12-25': 'Christmas'
    }
    df['festival'] = df['date'].dt.strftime('%Y-%m-%d').map(festivals).fillna('None')
    df['is_holiday'] = (df['is_weekend'] | (df['festival'] != 'None')).astype(int)
    return df

# --- 2. PRODUCT CATALOG (Indian Brands & Realistic Pricing) ---
def generate_products():
    print("🛒 Generating Product Catalog...")
    product_map = {
        "Dairy & Breakfast": {"Amul": ["Milk 500ml", "Butter 100g", "Masti Dahi", "Cheese Slices"], "Mother Dairy": ["Paneer 200g", "Toned Milk"]},
        "Snacks & Munchies": {"Lay's": ["Magic Masala", "Classic Salted"], "Haldiram": ["Bhujia Sev", "Aloo Bhujia"], "Cadbury": ["Dairy Milk Silk"]},
        "Staples & Kitchen": {"Aashirvaad": ["Atta 5kg"], "Tata": ["Salt 1kg", "Sampann Dal", "Tea Gold"], "Fortune": ["Sunflower Oil 1L"]},
        "Beverages": {"Coca Cola": ["Coke 500ml"], "Nescafe": ["Classic Coffee"], "Red Bull": ["Energy Drink"]},
        "Cleaning": {"Surf Excel": ["Easy Wash"], "Vim": ["Dishwash Gel"], "Dettol": ["Antiseptic"]}
    }
    
    data = []
    categories = list(product_map.keys())
    for i in range(NUM_PRODUCTS):
        cat = np.random.choice(categories)
        brand = np.random.choice(list(product_map[cat].keys()))
        p_name = np.random.choice(product_map[cat][brand])
        
        mrp = round(random.uniform(20, 1500), 2)
        selling_price = round(mrp * random.uniform(0.8, 0.98), 2)
        cost_price = round(selling_price * random.uniform(0.65, 0.85), 2)
        
        data.append([
            i + 1, f"SKU-{random.randint(10000, 99999)}", f"{brand} {p_name} {i}", 
            brand, cat, f"{cat} Sub", mrp, selling_price, cost_price, 
            random.choice(["100g", "500g", "1kg", "1L"]), brand, 
            random.choice([0.05, 0.12, 0.18]), round(random.uniform(3.5, 4.9), 1), 
            "2022-01-01", 0
        ])
    return pd.DataFrame(data, columns=['product_id', 'SKU', 'product_name', 'brand', 'category', 'subcategory', 'MRP', 'selling_price', 'cost_price', 'weight', 'supplier', 'GST_rate', 'rating', 'launch_date', 'discontinued_flag'])

# --- 3. INFRASTRUCTURE TABLES ---
def generate_base_entities():
    print("🏢 Generating Stores, Customers, Partners, and Coupons...")
    cities = ['Bangalore', 'Mumbai', 'Delhi', 'Gurgaon', 'Hyderabad']
    
    customers = pd.DataFrame([{
        'customer_id': i + 1,
        'signup_date': fake.date_between(start_date='-2y'),
        'gender': np.random.choice(['Male', 'Female'], p=[0.55, 0.45]),
        'age': random.randint(18, 65),
        'city': np.random.choice(cities),
        'membership_type': np.random.choice(['Normal', 'Plus', 'Premium'], p=[0.7, 0.2, 0.1]),
        'acquisition_channel': random.choice(['Instagram', 'Google Ads', 'Organic', 'Referral']),
        'customer_status': 'Active'
    } for i in range(NUM_CUSTOMERS)])

    stores = pd.DataFrame([{
        'store_id': i + 1, 'city': random.choice(cities), 'locality': f"Dark Store {i}",
        'opening_date': '2022-01-01', 'warehouse_capacity': random.choice([5000, 10000])
    } for i in range(NUM_STORES)])

    partners = pd.DataFrame([{
        'delivery_partner_id': i + 1, 'joining_date': fake.date_between(start_date='-1y'),
        'city': random.choice(cities), 'vehicle_type': random.choice(['Bike', 'EV', 'Scooter']),
        'employment_type': 'Gig', 'average_rating': round(random.uniform(4.0, 5.0), 1)
    } for i in range(NUM_PARTNERS)])
    
    coupons = pd.DataFrame([{
        'coupon_id': i + 1, 'coupon_code': f"SAVE{i+10}", 'discount_type': 'Percentage',
        'minimum_order': 299, 'maximum_discount': 100
    } for i in range(250)])

    return customers, stores, partners, coupons

# --- 4. CORE ENGINE (Orders, Items, Payments) ---
def generate_orders_and_related(customers, products, stores, partners, coupons):
    print(f"⏳ Building {NUM_ORDERS} Orders with Business Logic...")
    orders, items, payments = [], [], []
    item_id_counter = 1
    
    # Pre-calculating product indices for performance
    dairy_indices = products[products['category'] == 'Dairy & Breakfast'].index.values
    snack_indices = products[products['category'] == 'Snacks & Munchies'].index.values
    all_indices = products.index.values

    # FIX: Hour Probabilities sum exactly to 1.00
    # Night(0-6: 7h) @ 0.01 | Morn(7-11: 5h) @ 0.04 | Aft(12-17: 6h) @ 0.06 | Peak(18-21: 4h) @ 0.08 | Late(22-23: 2h) @ 0.025
    hour_probs = [0.01]*7 + [0.04]*5 + [0.06]*6 + [0.08]*4 + [0.025]*2

    for i in range(1, NUM_ORDERS + 1):
        o_date = START_DATE + timedelta(days=random.randint(0, 364))
        month = o_date.month
        
        # Select hour using the corrected probability list
        hour = np.random.choice(range(24), p=hour_probs)
        o_time = o_date.replace(hour=hour, minute=random.randint(0, 59))
        
        cust = customers.iloc[random.randint(0, NUM_CUSTOMERS-1)]
        city_stores = stores[stores['city'] == cust['city']]
        store_id = city_stores.sample(1)['store_id'].values[0] if not city_stores.empty else stores.sample(1)['store_id'].values[0]

        # Seasonality Logic
        if month in [5, 6, 7]: p_pool = np.concatenate([snack_indices, all_indices])
        elif month in [11, 12, 1]: p_pool = np.concatenate([dairy_indices, all_indices])
        else: p_pool = all_indices

        num_items = random.randint(1, 10)
        selected_p_indices = np.random.choice(p_pool, num_items)
        
        o_val = 0
        for p_idx in selected_p_indices:
            p = products.iloc[p_idx]
            qty = 1 if random.random() > 0.15 else 2
            total_item_price = p['selling_price'] * qty
            items.append([item_id_counter, i, p['product_id'], qty, p['selling_price'], 0, total_item_price, p['cost_price']*qty])
            o_val += total_item_price
            item_id_counter += 1

        # Pricing Math
        discount = round(o_val * 0.15, 2) if (random.random() > 0.8 or i < 500) else 0
        fees = 25 + 2 + 5 
        tip = random.choice([0, 0, 0, 10, 20])
        total_paid = (o_val - discount) + fees + tip
        
        # Delivery Physics
        dist = round(random.uniform(0.5, 6.0), 2)
        weather = np.random.choice(['Clear', 'Rainy', 'Foggy'], p=[0.85, 0.12, 0.03])
        traffic = np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.4, 0.3])
        
        actual_min = int(12 + (dist * 4) + (15 if weather == 'Rainy' else 0) + (8 if traffic == 'High' else 0) + random.randint(-2, 5))
        status = np.random.choice(['Delivered', 'Cancelled', 'Returned'], p=[0.94, 0.04, 0.02])
        
        orders.append([
            i, cust['customer_id'], store_id, random.randint(1, NUM_PARTNERS), i, random.randint(1, 250),
            o_time, o_time + timedelta(minutes=actual_min) if status == 'Delivered' else None,
            25 if dist < 3 else 35, actual_min if status == 'Delivered' else None, dist,
            status, None if status == 'Delivered' else "Address not found", weather, traffic,
            'Online', round(o_val, 2), 25, 2, 5, discount, round(total_paid, 2), tip, 
            round(random.uniform(3, 5), 1) if status == 'Delivered' else None,
            'Yes' if actual_min <= 25 else 'No', 'Android'
        ])
        
        payments.append([i, 'UPI' if random.random() > 0.4 else 'Card', 'Success' if status != 'Cancelled' else 'Failed', 'Razorpay', 15, 0, 0])

        if i % 200000 == 0: print(f"✅ {i} orders processed...")

    return pd.DataFrame(orders, columns=['order_id', 'customer_id', 'store_id', 'delivery_partner_id', 'payment_id', 'coupon_id', 'order_datetime', 'delivery_datetime', 'promised_delivery_minutes', 'actual_delivery_minutes', 'delivery_distance_km', 'order_status', 'cancellation_reason', 'weather', 'traffic_level', 'payment_method', 'order_value', 'delivery_fee', 'platform_fee', 'packaging_fee', 'discount', 'total_paid', 'tip_amount', 'customer_rating', 'sla_met', 'order_source']), \
           pd.DataFrame(items, columns=['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'item_discount', 'total_price', 'cost_price_at_sale']), \
           pd.DataFrame(payments, columns=['payment_id', 'payment_method', 'payment_status', 'gateway', 'payment_time_seconds', 'cashback', 'refund_amount'])

# --- EXECUTION FLOW ---
calendar_df = generate_calendar()
product_df = generate_products()
customer_df, store_df, partner_df, coupon_df = generate_base_entities()
order_df, order_items_df, payment_df = generate_orders_and_related(customer_df, product_df, store_df, partner_df, coupon_df)

# --- SAVE DATA ---
print("💾 Saving all 9 CSV files...")
files = {
    'calendar.csv': calendar_df, 'products.csv': product_df, 'customers.csv': customer_df,
    'stores.csv': store_df, 'delivery_partners.csv': partner_df, 'coupons.csv': coupon_df,
    'orders.csv': order_df, 'order_items.csv': order_items_df, 'payments.csv': payment_df
}
for name, df in files.items():
    df.to_csv(name, index=False)
    print(f"✔️ Saved {name}")

print("\n✨ Done! Your enterprise-grade dataset is ready for SQL and Power BI.")    