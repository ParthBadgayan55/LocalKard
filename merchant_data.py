# Merchant Data Management Functions

import json
import os
from datetime import datetime

# Data directory structure
DATA_DIR = 'merchant_data'

def ensure_merchant_dir(merchant_phone):
    """Create merchant data directory if it doesn't exist"""
    merchant_dir = os.path.join(DATA_DIR, str(merchant_phone))
    os.makedirs(merchant_dir, exist_ok=True)
    return merchant_dir

# Product Management
def load_products(merchant_phone):
    """Load merchant products"""
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
    """Save merchant products"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        products_file = os.path.join(merchant_dir, 'products.json')
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving products: {e}")
        return False

def add_product(merchant_phone, product_data):
    """Add a new product"""
    products = load_products(merchant_phone)
    product_data['id'] = f"PROD{len(products)+1:03d}"
    product_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    products.append(product_data)
    save_products(merchant_phone, products)
    return product_data['id']

def update_product(merchant_phone, product_id, product_data):
    """Update existing product"""
    products = load_products(merchant_phone)
    for i, p in enumerate(products):
        if p['id'] == product_id:
            product_data['id'] = product_id
            product_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            products[i] = product_data
            save_products(merchant_phone, products)
            return True
    return False

def delete_product(merchant_phone, product_id):
    """Delete a product"""
    products = load_products(merchant_phone)
    products = [p for p in products if p['id'] != product_id]
    save_products(merchant_phone, products)
    return True

# Order Management
def load_orders(merchant_phone):
    """Load merchant orders"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        orders_file = os.path.join(merchant_dir, 'orders.json')
        if os.path.exists(orders_file):
            with open(orders_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_orders(merchant_phone, orders):
    """Save merchant orders"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        orders_file = os.path.join(merchant_dir, 'orders.json')
        with open(orders_file, 'w') as f:
            json.dump(orders, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving orders: {e}")
        return False

def add_order(merchant_phone, order_data):
    """Add a new order"""
    orders = load_orders(merchant_phone)
    order_data['id'] = f"ORD{len(orders)+1:04d}"
    order_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orders.append(order_data)
    save_orders(merchant_phone, orders)
    return order_data['id']

def update_order_status(merchant_phone, order_id, status):
    """Update order status"""
    orders = load_orders(merchant_phone)
    for order in orders:
        if order['id'] == order_id:
            order['status'] = status
            order['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_orders(merchant_phone, orders)
            return True
    return False

# Points Configuration
def load_points_config(merchant_phone):
    """Load points configuration"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        config_file = os.path.join(merchant_dir, 'points_config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
    except:
        pass
    # Default configuration
    return {
        "points_system": "global",
        "global_rate": {
            "amount": 100,
            "points": 5,
            "rate_per_rupee": 0.05
        },
        "product_specific": {},
        "redemption_rate": {
            "points": 100,
            "value": 10,
            "rate": 0.1
        },
        "enabled": True
    }

def save_points_config(merchant_phone, config):
    """Save points configuration"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        config_file = os.path.join(merchant_dir, 'points_config.json')
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving points config: {e}")
        return False

# Points Transactions
def load_points_transactions(merchant_phone):
    """Load points transactions"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        trans_file = os.path.join(merchant_dir, 'points_transactions.json')
        if os.path.exists(trans_file):
            with open(trans_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_points_transactions(merchant_phone, transactions):
    """Save points transactions"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        trans_file = os.path.join(merchant_dir, 'points_transactions.json')
        with open(trans_file, 'w') as f:
            json.dump(transactions, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving points transactions: {e}")
        return False

def add_points_transaction(merchant_phone, transaction_data):
    """Add a points transaction"""
    transactions = load_points_transactions(merchant_phone)
    transaction_data['id'] = f"PT{len(transactions)+1:05d}"
    transaction_data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions.append(transaction_data)
    save_points_transactions(merchant_phone, transactions)
    return transaction_data['id']

def calculate_points_earned(merchant_phone, order_amount, product_ids=None):
    """Calculate points earned for an order"""
    config = load_points_config(merchant_phone)

    if not config['enabled']:
        return 0

    if config['points_system'] == 'global':
        # Global rate calculation
        rate = config['global_rate']['rate_per_rupee']
        points = order_amount * rate
        return round(points, 2)
    else:
        # Product-specific (would need product details)
        # For now, fallback to global
        rate = config['global_rate']['rate_per_rupee']
        points = order_amount * rate
        return round(points, 2)

def get_points_stats(merchant_phone):
    """Get points statistics"""
    transactions = load_points_transactions(merchant_phone)

    total_disbursed = sum(t['points'] for t in transactions if t['type'] == 'earned')
    total_redeemed = sum(t['points'] for t in transactions if t['type'] == 'redeemed')
    outstanding = total_disbursed - total_redeemed

    return {
        'disbursed': total_disbursed,
        'redeemed': total_redeemed,
        'outstanding': outstanding,
        'total_transactions': len(transactions)
    }

# Customer Management
def load_customers(merchant_phone):
    """Load merchant customers"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        customers_file = os.path.join(merchant_dir, 'customers.json')
        if os.path.exists(customers_file):
            with open(customers_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_customers(merchant_phone, customers):
    """Save merchant customers"""
    try:
        merchant_dir = ensure_merchant_dir(merchant_phone)
        customers_file = os.path.join(merchant_dir, 'customers.json')
        with open(customers_file, 'w') as f:
            json.dump(customers, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving customers: {e}")
        return False
