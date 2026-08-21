# All merchant functionality inline - no imports needed

import json
import os
from datetime import datetime, date

# Data directory
DATA_DIR = 'merchant_data'

# Light color palette
COLORS = {
    'primary': '#2E86DE',
    'success': '#10AC84',
    'warning': '#FF9F43',
    'danger': '#EE5A6F',
    'info': '#54A0FF',
    'light_bg': '#F8F9FA',
    'card_bg': '#FFFFFF',
    'border': '#E1E8ED',
    'text_dark': '#2C3E50',
    'text_muted': '#636E72'
}

CATEGORIES = ["Groceries", "Dairy", "Vegetables", "Fruits", "Bakery", "Pet Food", "Beverages", "Snacks", "Others"]
UNITS = ["kg", "liter", "piece", "dozen", "packet", "grams", "ml"]

def ensure_merchant_dir(merchant_phone):
    merchant_dir = os.path.join(DATA_DIR, str(merchant_phone))
    os.makedirs(merchant_dir, exist_ok=True)
    return merchant_dir

def load_products(merchant_phone):
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        products_file = os.path.join(merchant_dir, 'products.json')
        if os.path.exists(products_file):
            with open(products_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_products(merchant_phone, products):
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        products_file = os.path.join(merchant_dir, 'products.json')
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)
        return True
    except:
        return False

def add_product(merchant_phone, product_data):
    products = load_products(merchant_phone)
    product_data['id'] = f"PROD{len(products)+1:03d}"
    product_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    products.append(product_data)
    save_products(merchant_phone, products)
    return product_data['id']

def delete_product(merchant_phone, product_id):
    products = load_products(merchant_phone)
    products = [p for p in products if p['id'] != product_id]
    save_products(merchant_phone, products)
    return True

def load_orders(merchant_phone):
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        orders_file = os.path.join(merchant_dir, 'orders.json')
        if os.path.exists(orders_file):
            with open(orders_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_points_stats(merchant_phone):
    return {
        'disbursed': 0,
        'redeemed': 0,
        'outstanding': 0,
        'total_transactions': 0
    }

def load_customers(merchant_phone):
    return []

