import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import streamlit.components.v1 as components
import json
import os

# Import Payback-style backend
try:
    from payback_engine import (
        PaybackEngine,
        CentralCustomerDB,
        TransactionEngine,
        PointsEngine
    )
    PAYBACK_BACKEND_AVAILABLE = True
except ImportError:
    PAYBACK_BACKEND_AVAILABLE = False
    print("Warning: Payback backend not available")

# ============================================================================
# MERCHANT DASHBOARD INLINE CODE (No external imports needed)
# ============================================================================

# Data directory
DATA_DIR = 'merchant_data'

# World-Class Color Palette for Loyalty System
MD_COLORS = {
    'primary': '#6366F1',      # Indigo - Premium feel
    'success': '#10B981',      # Emerald - Growth/rewards
    'warning': '#F59E0B',      # Amber - Attention
    'danger': '#EF4444',       # Rose - Critical
    'info': '#3B82F6',         # Blue - Information
    'purple': '#8B5CF6',       # Purple - Premium tier
    'gold': '#F59E0B',         # Gold - Top tier
    'silver': '#94A3B8',       # Silver - Mid tier
    'bronze': '#CD7F32',       # Bronze - Entry tier
    'light_bg': '#F9FAFB',     # Almost white
    'card_bg': '#FFFFFF',      # Pure white
    'border': '#E5E7EB',       # Light border
    'text_dark': '#111827',    # Almost black
    'text_muted': '#6B7280'    # Gray
}

# Loyalty Tiers
LOYALTY_TIERS = {
    'bronze': {'name': 'Bronze', 'min_points': 0, 'multiplier': 1.0, 'color': MD_COLORS['bronze']},
    'silver': {'name': 'Silver', 'min_points': 500, 'multiplier': 1.25, 'color': MD_COLORS['silver']},
    'gold': {'name': 'Gold', 'min_points': 2000, 'multiplier': 1.5, 'color': MD_COLORS['gold']},
    'platinum': {'name': 'Platinum', 'min_points': 5000, 'multiplier': 2.0, 'color': MD_COLORS['purple']}
}

def md_ensure_dir(merchant_phone):
    merchant_dir = os.path.join(DATA_DIR, str(merchant_phone))
    os.makedirs(merchant_dir, exist_ok=True)
    return merchant_dir

def md_load_products(merchant_phone):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        products_file = os.path.join(merchant_dir, 'products.json')
        if os.path.exists(products_file):
            with open(products_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def md_save_products(merchant_phone, products):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        products_file = os.path.join(merchant_dir, 'products.json')
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)
        return True
    except:
        return False

def md_add_product(merchant_phone, product_data):
    products = md_load_products(merchant_phone)
    product_data['id'] = f"PROD{len(products)+1:03d}"
    product_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    products.append(product_data)
    md_save_products(merchant_phone, products)
    return product_data['id']

def md_delete_product(merchant_phone, product_id):
    products = md_load_products(merchant_phone)
    products = [p for p in products if p['id'] != product_id]
    md_save_products(merchant_phone, products)
    return True

def md_load_orders(merchant_phone):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        orders_file = os.path.join(merchant_dir, 'orders.json')
        if os.path.exists(orders_file):
            with open(orders_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def md_get_points_stats(merchant_phone):
    return {
        'disbursed': 0,
        'redeemed': 0,
        'outstanding': 0,
        'total_transactions': 0
    }

def md_load_customers(merchant_phone):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        customers_file = os.path.join(merchant_dir, 'customers.json')
        if os.path.exists(customers_file):
            with open(customers_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def md_save_customers(merchant_phone, customers):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        customers_file = os.path.join(merchant_dir, 'customers.json')
        with open(customers_file, 'w') as f:
            json.dump(customers, f, indent=2)
        return True
    except:
        return False

def md_add_customer(merchant_phone, customer_data):
    customers = md_load_customers(merchant_phone)
    customer_data['id'] = f"CUST{len(customers)+1:05d}"
    customer_data['joined_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_data['points_balance'] = 0
    customer_data['tier'] = 'bronze'
    customer_data['lifetime_points'] = 0
    customers.append(customer_data)
    md_save_customers(merchant_phone, customers)
    return customer_data['id']

def md_load_loyalty_config(merchant_phone):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        config_file = os.path.join(merchant_dir, 'loyalty_config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return {
        'earning_rate': {'amount': 100, 'points': 5},
        'redemption_rate': {'points': 100, 'value': 10},
        'tier_benefits': True,
        'expiry_enabled': False,
        'expiry_days': 365,
        'referral_bonus': 50,
        'birthday_bonus': 100
    }

def md_save_loyalty_config(merchant_phone, config):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        config_file = os.path.join(merchant_dir, 'loyalty_config.json')
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

def md_load_transactions(merchant_phone):
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        trans_file = os.path.join(merchant_dir, 'transactions.json')
        if os.path.exists(trans_file):
            with open(trans_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def md_save_transaction(merchant_phone, transaction):
    transactions = md_load_transactions(merchant_phone)
    transaction['id'] = f"TXN{len(transactions)+1:06d}"
    transaction['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions.append(transaction)
    try:
        merchant_dir = md_ensure_dir(merchant_phone)
        trans_file = os.path.join(merchant_dir, 'transactions.json')
        with open(trans_file, 'w') as f:
            json.dump(transactions, f, indent=2)
        return True
    except:
        return False

def md_get_customer_tier(lifetime_points):
    """Determine customer tier based on lifetime points"""
    for tier_key in reversed(['platinum', 'gold', 'silver', 'bronze']):
        tier = LOYALTY_TIERS[tier_key]
        if lifetime_points >= tier['min_points']:
            return tier_key
    return 'bronze'

# ============================================================================

# Page config
st.set_page_config(
    page_title="LocalKard - The Unified Loyalty & Commerce Network",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - World-Class Design
st.markdown("""
<style>
    /* Hide Streamlit branding but keep sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Keep header visible for sidebar toggle */
    header {visibility: visible !important;}

    /* Style the sidebar collapse button to be more visible */
    button[kind="header"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    button[kind="header"]:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: scale(1.05) !important;
    }

    /* Ensure sidebar toggle is always visible when collapsed */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        border-radius: 0 12px 12px 0 !important;
        padding: 1.5rem 0.7rem !important;
        cursor: pointer !important;
        box-shadow: 3px 0 15px rgba(99, 102, 241, 0.5) !important;
        z-index: 999999 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="collapsedControl"]:hover {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        transform: translateY(-50%) translateX(5px) !important;
        box-shadow: 5px 0 20px rgba(99, 102, 241, 0.7) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }

    /* Style the sidebar toggle icon */
    [data-testid="collapsedControl"] svg {
        fill: white !important;
        width: 28px !important;
        height: 28px !important;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)) !important;
    }

    /* Ensure sidebar close button is visible */
    [data-testid="stSidebar"] button[kind="header"] {
        visibility: visible !important;
        display: flex !important;
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        margin: 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] button[kind="header"]:hover {
        background: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
        transform: scale(1.1) !important;
    }

    [data-testid="stSidebar"] button[kind="header"] svg {
        fill: #EF4444 !important;
        width: 20px !important;
        height: 20px !important;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 0;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Logo/Brand */
    .brand {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -2px;
    }

    .tagline {
        color: #a0a0c0;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    }

    /* Coming Soon Badge */
    .coming-soon-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5);
        color: #667eea;
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
        }
    }

    /* Swipe to Login */
    .swipe-container {
        margin-top: 1rem;
        margin-bottom: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .swipe-text {
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .swipe-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .swipe-arrow {
        color: #667eea;
        font-size: 1.5rem;
        animation: swipeLeft 2s ease-in-out infinite;
        display: inline-block;
    }

    .swipe-arrow:nth-child(2) {
        animation-delay: 0.2s;
    }

    .swipe-arrow:nth-child(3) {
        animation-delay: 0.4s;
    }

    .swipe-arrow.right {
        animation-delay: 0s;
    }

    .swipe-arrow.right:nth-child(5) {
        animation-delay: 0.2s;
    }

    .swipe-arrow.right:nth-child(6) {
        animation-delay: 0.4s;
    }

    @keyframes swipeLeft {
        0%, 100% {
            opacity: 0.3;
            transform: translateX(-10px);
        }
        50% {
            opacity: 1;
            transform: translateX(10px);
        }
    }

    .swipe-line {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        border-radius: 2px;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 0.5;
        }
        50% {
            opacity: 1;
        }
    }

    /* Login cards */
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        width: 100%;
        max-width: 300px;
        height: 260px;
        margin: 0 auto;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .login-card:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 12px 48px 0 rgba(102, 126, 234, 0.3);
    }

    .card-icon {
        font-size: 3rem;
        margin-bottom: 1.2rem;
    }

    .card-title {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .card-description {
        color: #a0a0c0;
        font-size: 0.9rem;
        line-height: 1.5;
        text-align: center;
    }

    /* About Us Section */
    .about-section {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 3rem auto 2rem auto;
        max-width: 900px;
    }

    .about-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .about-content {
        color: #b0b0d0;
        font-size: 1rem;
        line-height: 1.8;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .feature-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }

    .feature-item {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }

    .feature-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #a0a0c0;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* Footer */
    .footer {
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
    }

    .footer-content {
        color: #808090;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .footer-brand {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .copyright {
        color: #606070;
        font-size: 0.85rem;
        margin-top: 1rem;
    }

    /* Login form */
    .login-form-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.18) 100%);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 3rem 2.5rem;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 20px 60px 0 rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.3);
    }

    .form-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2.5rem;
        text-align: center;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(255, 255, 255, 0.3);
    }

    /* Section headers in forms */
    .section-header {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
        letter-spacing: 0.5px !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 1) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 1rem 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.4) !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2), 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        background: rgba(255, 255, 255, 1) !important;
        outline: none !important;
    }

    /* Show labels */
    .stTextInput > label {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.6rem !important;
        letter-spacing: 0.3px !important;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(0, 0, 0, 0.8) !important;
        display: block !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 1) !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 12px !important;
        color: #000000 !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15) !important;
        padding: 0.9rem 1rem !important;
        font-size: 0.95rem !important;
    }

    .stNumberInput > label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(0, 0, 0, 0.8) !important;
        margin-bottom: 0.6rem !important;
    }

    /* Checkbox */
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6) !important;
    }

    /* Info/Success/Error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }

    /* Back button styling */
    div[data-testid="column"]:nth-child(2) .stButton:last-of-type > button {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #a0a0c0;
    }

    div[data-testid="column"]:nth-child(2) .stButton:last-of-type > button:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.3);
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: none;
    }

    /* Labels */
    .stTextInput > label {
        color: #a0a0c0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* Dashboard styles */
    .dashboard-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .dashboard-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .dashboard-subtitle {
        color: #a0a0c0;
        font-size: 1.1rem;
    }

    /* Metrics */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
    }

    .stMetric label {
        color: #a0a0c0 !important;
        font-size: 0.9rem !important;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Data file paths
MERCHANTS_FILE = 'merchants_data.json'
CUSTOMERS_FILE = 'customers_data.json'

# Load or initialize merchant data
def load_merchants():
    if os.path.exists(MERCHANTS_FILE):
        try:
            with open(MERCHANTS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_MERCHANTS

def save_merchants(merchants):
    try:
        with open(MERCHANTS_FILE, 'w') as f:
            json.dump(merchants, f, indent=2)
    except Exception as e:
        st.error(f"Error saving merchant data: {e}")

# Load or initialize customer data
def load_customers():
    if os.path.exists(CUSTOMERS_FILE):
        try:
            with open(CUSTOMERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CUSTOMERS

def save_customers(customers):
    try:
        with open(CUSTOMERS_FILE, 'w') as f:
            json.dump(customers, f, indent=2)
    except Exception as e:
        st.error(f"Error saving customer data: {e}")

# Default sample data
DEFAULT_MERCHANTS = {
    "LocalKard": {
        "name": "LocalKard Demo Store",
        "owner": "LocalKard Admin",
        "password": "LocalKard@55",
        "phone": "LocalKard",
        "address": "MG Road, Bangalore",
        "locality": "MG Road",
        "pincode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    },
    "9876543210": {
        "name": "Fresh Mart Grocery",
        "owner": "Rajesh Kumar",
        "password": "merchant123",
        "phone": "9876543210",
        "address": "123 Main Street, Mumbai",
        "locality": "Andheri West",
        "pincode": "400053",
        "latitude": 19.1136,
        "longitude": 72.8697,
    },
    "9876543211": {
        "name": "Pet Paradise",
        "owner": "Priya Sharma",
        "password": "merchant123",
        "phone": "9876543211",
        "address": "456 Park Road, Mumbai",
        "locality": "Bandra",
        "pincode": "400050",
        "latitude": 19.0596,
        "longitude": 72.8295,
    },
    "demo": {
        "name": "Demo Shop - Current Location",
        "owner": "Demo Merchant",
        "password": "demo123",
        "phone": "demo",
        "address": "Current GPS Location",
        "locality": "Your Area",
        "pincode": "000000",
        "latitude": 19.0760,
        "longitude": 72.8777,
    },
    "demoshop3": {
        "name": "Demo Shop 3",
        "owner": "Demo Owner 3",
        "password": "demoshop3",
        "phone": "demoshop3",
        "address": "456 Demo Street, Mumbai",
        "locality": "Powai",
        "pincode": "400076",
        "latitude": 19.1197,
        "longitude": 72.9078,
    }
}

# Load data at startup
MERCHANTS = load_merchants()

DEFAULT_CUSTOMERS = {
    "LocalKard": {
        "name": "LocalKard Demo User",
        "password": "LocalKard@55",
        "phone": "LocalKard",
    },
    "9988776655": {
        "name": "Amit Patel",
        "password": "customer123",
        "phone": "9988776655",
    },
    "9988776644": {
        "name": "Priya Shah",
        "password": "customer123",
        "phone": "9988776644",
    },
    "demo": {
        "name": "Demo Customer",
        "password": "demo123",
        "phone": "demo",
    }
}

# Load data at startup
CUSTOMERS = load_customers()

# Landing Page
def landing_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem 2rem 2rem;">
        <div class="coming-soon-badge">🚀 Coming Soon</div>
        <div class="brand">LocalKard</div>
        <div class="tagline">The Unified Loyalty & Commerce Network</div>
    </div>
    """, unsafe_allow_html=True)

    # Login Cards
    col1, col2, col3 = st.columns([0.5, 3, 0.5])

    with col2:
        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:
            st.markdown("""
            <div class="login-card">
                <div class="card-icon">🏪</div>
                <div class="card-title">Merchant</div>
                <div class="card-description">Manage your store, products, and orders</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Login as Merchant", key="merchant_btn", use_container_width=True):
                st.session_state.page = 'merchant_login'
                st.rerun()

        with c2:
            st.markdown("""
            <div class="login-card">
                <div class="card-icon">👤</div>
                <div class="card-title">Customer</div>
                <div class="card-description">Browse shops and place orders</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Login as Customer", key="customer_btn", use_container_width=True):
                st.session_state.page = 'customer_login'
                st.rerun()

        with c3:
            st.markdown("""
            <div class="login-card">
                <div class="card-icon">🔍</div>
                <div class="card-title">Discover</div>
                <div class="card-description">Browse all shops in the network</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Discover Shops", key="discover_btn", use_container_width=True):
                st.session_state.page = 'discover'
                st.rerun()

    # About Us Section - Header and description
    st.markdown("""
    <div class="about-section">
        <div class="about-title">About LocalKard</div>
        <div class="about-content">
            LocalKard is revolutionizing local commerce in India's Tier 2 and Tier 3 towns.
            We're building a unified loyalty and commerce network that connects neighborhood shops
            with their customers through WhatsApp, enabling seamless ordering, automated reorder
            reminders, and cross-shop loyalty rewards.
        </div>
        <div class="about-content">
            Our vision is to empower local retailers with digital tools while preserving the
            personal relationships that make local commerce special. From your corner grocery
            store to your favorite pet shop, LocalKard brings them all together in one network.
        </div>
    """, unsafe_allow_html=True)

    # Feature list - separate for proper rendering
    st.markdown("""
        <div class="feature-list">
            <div class="feature-item">
                <div class="feature-icon">📱</div>
                <div class="feature-title">WhatsApp Native</div>
                <div class="feature-description">Order from local shops via WhatsApp - no app download needed</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🔔</div>
                <div class="feature-title">Smart Reminders</div>
                <div class="feature-description">Never run out - get automatic reorder reminders</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🏪</div>
                <div class="feature-title">Shop Discovery</div>
                <div class="feature-description">Discover nearby shops and explore new products</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">💳</div>
                <div class="feature-title">Unified Loyalty</div>
                <div class="feature-description">Earn and redeem points across all participating shops</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">LocalKard</div>
        <div class="footer-content">
            Empowering local commerce in Tier 2 & Tier 3 India
        </div>
        <div class="copyright">
            © 2026 LocalKard. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Merchant Login
def merchant_login_page():
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1, 1.2])

    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Merchant Portal</div>', unsafe_allow_html=True)

        phone = st.text_input("Username / Phone Number", placeholder="Enter username or phone", key="merchant_phone")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="merchant_pass")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("Sign In", key="merchant_login_btn", use_container_width=True):
            # Reload merchants to get latest data
            current_merchants = load_merchants()
            if phone in current_merchants and current_merchants[phone]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = 'merchant'
                st.session_state.current_user = current_merchants[phone]
                st.session_state.page = 'merchant_dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Back", key="back_merchant", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Signup link
        st.markdown("""
        <div style='text-align: center; margin-top: 1.5rem;'>
            <span style='color: #a0a0c0; font-size: 0.9rem;'>Don't have an account? </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create Merchant Account", key="merchant_signup_link", use_container_width=True):
            st.session_state.page = 'merchant_signup'
            st.rerun()

# Customer Login
def customer_login_page():
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1, 1.2])

    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Customer Portal</div>', unsafe_allow_html=True)

        phone = st.text_input("Username / Phone Number", placeholder="Enter username or phone", key="customer_phone")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="customer_pass")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("Sign In", key="customer_login_btn", use_container_width=True):
            # Reload customers to get latest data
            current_customers = load_customers()
            if phone in current_customers and current_customers[phone]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = 'customer'
                st.session_state.current_user = current_customers[phone]
                st.session_state.page = 'customer_dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Back", key="back_customer", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Signup link
        st.markdown("""
        <div style='text-align: center; margin-top: 1.5rem;'>
            <span style='color: #a0a0c0; font-size: 0.9rem;'>Don't have an account? </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create Customer Account", key="customer_signup_link", use_container_width=True):
            st.session_state.page = 'customer_signup'
            st.rerun()

# Merchant Dashboard
def merchant_dashboard():
    """World-Class Loyalty Management System"""
    merchant_data = st.session_state.current_user
    merchant_phone = merchant_data['phone']

    # Premium CSS
    st.markdown(f"""
    <style>
        .main {{ background: linear-gradient(135deg, {MD_COLORS['light_bg']} 0%, #F3F4F6 100%); }}
        .premium-card {{
            background: {MD_COLORS['card_bg']};
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid {MD_COLORS['border']};
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        .stat-card {{
            background: linear-gradient(135deg, {MD_COLORS['primary']} 0%, {MD_COLORS['purple']} 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
        }}
        .tier-badge {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            display: inline-block;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Top Navigation Bar
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {MD_COLORS['primary']} 0%, {MD_COLORS['purple']} 100%);
                padding: 1.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);'>
        <div style='color: white; font-size: 1.6rem; font-weight: 800;'>
            💎 {merchant_data['name']} Loyalty Hub
        </div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.3rem;'>
            {merchant_data['owner']} • Powering Customer Loyalty
        </div>
    </div>
    """, unsafe_allow_html=True)

    # MAIN NAVIGATION BUTTONS (Always visible alternative to sidebar)
    st.markdown(f"""
    <div style='background: white; padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;
                border: 2px solid {MD_COLORS['primary']}; box-shadow: 0 4px 12px rgba(99,102,241,0.3);'>
        <div style='color: {MD_COLORS['primary']}; font-size: 1.1rem; font-weight: 700; text-align: center; margin-bottom: 1rem;'>
            📱 NAVIGATION MENU - Click a button to navigate
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        if st.button("🏠 HOME", key="nav_home_btn", use_container_width=True, type="primary"):
            st.session_state.merchant_menu = "🏠 Home"
            st.rerun()
    with col2:
        if st.button("💎 LOYALTY", key="nav_loyalty_btn", use_container_width=True, type="primary"):
            st.session_state.merchant_menu = "💎 Loyalty"
            st.rerun()
    with col3:
        if st.button("👥 CUSTOMERS", key="nav_customers_btn", use_container_width=True, type="primary"):
            st.session_state.merchant_menu = "👥 Customers"
            st.rerun()
    with col4:
        if st.button("📊 ANALYTICS", key="nav_analytics_btn", use_container_width=True, type="primary"):
            st.session_state.merchant_menu = "📊 Analytics"
            st.rerun()
    with col5:
        if st.button("🚪 Logout", key="nav_logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

    # Add VERY PROMINENT sidebar toggle button
    st.markdown("""
    <style>
    /* Force toggle button visibility */
    .custom-sidebar-toggle {
        position: fixed !important;
        top: 50% !important;
        left: 0 !important;
        transform: translateY(-50%) !important;
        z-index: 9999999 !important;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        border: 3px solid white !important;
        border-left: none !important;
        border-radius: 0 20px 20px 0 !important;
        padding: 2rem 1rem !important;
        font-size: 2rem !important;
        cursor: pointer !important;
        box-shadow: 5px 0 30px rgba(99, 102, 241, 0.8) !important;
        transition: all 0.3s ease !important;
        font-weight: 900 !important;
        animation: pulse 2s infinite !important;
    }

    .custom-sidebar-toggle:hover {
        padding-right: 1.5rem !important;
        box-shadow: 8px 0 40px rgba(99, 102, 241, 1) !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 5px 0 30px rgba(99, 102, 241, 0.8); }
        50% { box-shadow: 5px 0 40px rgba(99, 102, 241, 1); }
    }

    /* Also add top button */
    .custom-menu-button {
        position: fixed !important;
        top: 1rem !important;
        left: 1rem !important;
        z-index: 9999999 !important;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.2rem !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.6) !important;
        transition: all 0.3s ease !important;
        font-weight: 700 !important;
    }

    .custom-menu-button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 30px rgba(99, 102, 241, 0.9) !important;
    }
    </style>

    <script>
    function toggleSidebar() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        const collapseBtn = window.parent.document.querySelector('[data-testid="collapsedControl"]');

        if (sidebar) {
            const currentState = sidebar.getAttribute('aria-expanded');

            if (currentState === 'false' || !currentState) {
                // Sidebar is collapsed, open it
                if (collapseBtn) {
                    collapseBtn.click();
                } else {
                    sidebar.style.display = 'block';
                    sidebar.setAttribute('aria-expanded', 'true');
                }
            } else {
                // Sidebar is open, close it
                const closeBtn = sidebar.querySelector('button[kind="header"]');
                if (closeBtn) {
                    closeBtn.click();
                } else {
                    sidebar.style.display = 'none';
                    sidebar.setAttribute('aria-expanded', 'false');
                }
            }
        }
    }

    // Auto-add buttons after page load
    setTimeout(function() {
        if (!document.querySelector('.custom-sidebar-toggle')) {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'custom-sidebar-toggle';
            toggleBtn.innerHTML = '☰';
            toggleBtn.onclick = toggleSidebar;
            document.body.appendChild(toggleBtn);
        }

        if (!document.querySelector('.custom-menu-button')) {
            const menuBtn = document.createElement('button');
            menuBtn.className = 'custom-menu-button';
            menuBtn.innerHTML = '☰ MENU';
            menuBtn.onclick = toggleSidebar;
            document.body.appendChild(menuBtn);
        }
    }, 1000);
    </script>
    """, unsafe_allow_html=True)

    # Prominent Navigation Toggle + Logout
    st.markdown("""
    <div style='background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
                padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem;
                box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);'>
        <div style='color: white; font-size: 1.3rem; font-weight: 700; text-align: center;'>
            ⬅️ USE THE LEFT SIDEBAR TO NAVIGATE ➡️
        </div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.9rem; text-align: center; margin-top: 0.5rem;'>
            Click the purple button on the LEFT EDGE to open/close sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown(f"""
    <div style='padding: 1.5rem; background: linear-gradient(135deg, {MD_COLORS['primary']} 0%, {MD_COLORS['purple']} 100%);
                border-radius: 12px; margin-bottom: 1.5rem;'>
        <div style='color: white; font-size: 1.1rem; font-weight: 700;'>🎯 Loyalty Dashboard</div>
        <div style='color: rgba(255,255,255,0.85); font-size: 0.75rem; margin-top: 0.3rem;'>World-Class System</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar collapse tip
    st.sidebar.markdown("""
    <div style='background: rgba(99, 102, 241, 0.1); border-left: 3px solid #6366F1;
                padding: 0.8rem; border-radius: 6px; margin-bottom: 1rem;'>
        <div style='font-size: 0.75rem; color: #6366F1; font-weight: 600;'>
            💡 TIP: Click the [×] icon at the top or use the arrow button on the left edge to collapse this sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Check if menu selection from main area buttons
    if 'merchant_menu' not in st.session_state:
        st.session_state.merchant_menu = "🏠 Home"

    menu = st.sidebar.radio("Navigation", ["🏠 Home", "💎 Loyalty", "👥 Customers", "📊 Analytics"],
                           key="sidebar_menu",
                           index=["🏠 Home", "💎 Loyalty", "👥 Customers", "📊 Analytics"].index(st.session_state.merchant_menu) if st.session_state.merchant_menu in ["🏠 Home", "💎 Loyalty", "👥 Customers", "📊 Analytics"] else 0,
                           label_visibility="visible")

    # Load data
    customers = md_load_customers(merchant_phone)
    loyalty_config = md_load_loyalty_config(merchant_phone)
    transactions = md_load_transactions(merchant_phone)

    # Calculate KPIs
    total_customers = len(customers)
    active_customers = len([c for c in customers if c.get('points_balance', 0) > 0])
    total_points_issued = sum(c.get('lifetime_points', 0) for c in customers)
    total_points_redeemed = total_points_issued - sum(c.get('points_balance', 0) for c in customers)
    outstanding_liability = sum(c.get('points_balance', 0) for c in customers)
    redemption_rate = (total_points_redeemed / total_points_issued * 100) if total_points_issued > 0 else 0

    if menu == "🏠 Home":
        st.markdown(f"<h1 style='color: {MD_COLORS['text_dark']}; font-size: 2.5rem; font-weight: 800; margin-bottom: 2rem;'>📊 Loyalty Overview</h1>", unsafe_allow_html=True)

        # Row 1 - Primary KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='stat-card'>
                <div style='font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.5rem;'>TOTAL CUSTOMERS</div>
                <div style='font-size: 2.5rem; font-weight: 800;'>{total_customers}</div>
                <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;'>Enrolled in program</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, {MD_COLORS['success']} 0%, {MD_COLORS['info']} 100%);'>
                <div style='font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.5rem;'>ACTIVE CUSTOMERS</div>
                <div style='font-size: 2.5rem; font-weight: 800;'>{active_customers}</div>
                <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;'>With points balance</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, {MD_COLORS['gold']} 0%, {MD_COLORS['warning']} 100%);'>
                <div style='font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.5rem;'>POINTS ISSUED</div>
                <div style='font-size: 2.5rem; font-weight: 800;'>{total_points_issued:,.0f}</div>
                <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;'>Lifetime rewards</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, {MD_COLORS['danger']} 0%, {MD_COLORS['warning']} 100%);'>
                <div style='font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.5rem;'>OUTSTANDING</div>
                <div style='font-size: 2.5rem; font-weight: 800;'>{outstanding_liability:,.0f}</div>
                <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;'>Points liability</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

        # Row 2 - Secondary KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_points = total_points_issued / total_customers if total_customers > 0 else 0
            st.metric("Avg Points/Customer", f"{avg_points:,.0f}", "Lifetime")
        with col2:
            st.metric("Redemption Rate", f"{redemption_rate:.1f}%", "All time")
        with col3:
            engagement_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
            st.metric("Engagement Rate", f"{engagement_rate:.0f}%", "Active users")
        with col4:
            st.metric("Total Transactions", len(transactions), "All time")

        st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

        # Tier Distribution
        st.markdown(f"<h2 style='color: {MD_COLORS['text_dark']}; font-weight: 700; margin-bottom: 1.5rem;'>🏆 Customer Tiers</h2>", unsafe_allow_html=True)

        tier_counts = {'bronze': 0, 'silver': 0, 'gold': 0, 'platinum': 0}
        for customer in customers:
            tier = customer.get('tier', 'bronze')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        col1, col2, col3, col4 = st.columns(4)
        for idx, (tier_key, tier_info) in enumerate(LOYALTY_TIERS.items()):
            with [col1, col2, col3, col4][idx]:
                count = tier_counts.get(tier_key, 0)
                pct = (count / total_customers * 100) if total_customers > 0 else 0
                st.markdown(f"""
                <div class='premium-card' style='text-align: center;'>
                    <div class='tier-badge' style='background: {tier_info["color"]}; color: white;'>
                        {tier_info["name"].upper()}
                    </div>
                    <div style='font-size: 2rem; font-weight: 800; color: {MD_COLORS['text_dark']}; margin: 1rem 0;'>
                        {count}
                    </div>
                    <div style='color: {MD_COLORS['text_muted']}; font-size: 0.85rem;'>
                        {pct:.0f}% of customers
                    </div>
                    <div style='color: {MD_COLORS['text_muted']}; font-size: 0.75rem; margin-top: 0.5rem;'>
                        {tier_info["multiplier"]}x points
                    </div>
                </div>
                """, unsafe_allow_html=True)

    elif menu == "💎 Loyalty":
        st.markdown(f"<h1 style='color: {MD_COLORS['text_dark']}; font-size: 2.5rem; font-weight: 800; margin-bottom: 2rem;'>💎 Loyalty Program Management</h1>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["💳 Record Sale", "⚙️ Points Rules", "🎁 Rewards & Tiers", "📊 Program Analytics"])

        with tab1:
            st.markdown("### 💳 Record Customer Purchase")
            st.markdown("Process a customer purchase and award points using the Payback-style engine")

            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

            if PAYBACK_BACKEND_AVAILABLE:
                with st.form("record_purchase_form"):
                    st.markdown("#### Customer & Purchase Details")

                    col1, col2 = st.columns(2)
                    with col1:
                        customer_phone = st.text_input("Customer Phone Number *", placeholder="9876543210", help="10-digit phone number")
                        customer_name = st.text_input("Customer Name", placeholder="John Doe (optional for existing customers)")

                    with col2:
                        purchase_amount = st.number_input("Purchase Amount (₹) *", min_value=1.0, step=10.0, value=100.0)
                        description = st.text_input("Description", placeholder="Purchase description (optional)", value="")

                    customer_email = st.text_input("Customer Email", placeholder="john@example.com (optional)")

                    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        submit_btn = st.form_submit_button("🎯 Process Purchase & Award Points", use_container_width=True, type="primary")
                    with col2:
                        if st.form_submit_button("🔍 Check Customer Balance", use_container_width=True):
                            if customer_phone and len(customer_phone) == 10:
                                try:
                                    engine = PaybackEngine(merchant_id=merchant_phone)
                                    summary = engine.get_customer_summary(customer_phone)
                                    if summary['success']:
                                        cust = summary['customer']
                                        st.success(f"**{cust['name']}** ({cust['localkard_id']})")
                                        st.info(f"💎 Points Balance: **{cust['points_balance']:,.1f}** (Tier: **{cust['tier'].upper()}**)")
                                        st.info(f"💰 Redemption Value: **₹{summary['redemption_value']:.2f}**")
                                    else:
                                        st.warning(f"Customer not found. Will be created on first purchase.")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                            else:
                                st.error("Please enter a valid 10-digit phone number")

                if submit_btn:
                    if customer_phone and len(customer_phone) == 10 and purchase_amount > 0:
                        try:
                            # Initialize Payback Engine
                            engine = PaybackEngine(merchant_id=merchant_phone)

                            # Process the purchase
                            with st.spinner("Processing transaction..."):
                                result = engine.process_purchase(
                                    customer_phone=customer_phone,
                                    amount=purchase_amount,
                                    description=description or f"Purchase of ₹{purchase_amount}",
                                    metadata={
                                        'customer_name': customer_name if customer_name else None,
                                        'customer_email': customer_email if customer_email else None
                                    }
                                )

                            if result['success']:
                                # Success message with confetti
                                st.balloons()

                                # Transaction summary card
                                st.markdown(f"""
                                <div class='premium-card' style='background: linear-gradient(135deg, {MD_COLORS['success']} 0%, {MD_COLORS['info']} 100%); color: white; padding: 2rem;'>
                                    <h2 style='color: white; margin: 0 0 1rem 0;'>✅ Transaction Successful!</h2>
                                    <div style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
                                        <strong>Transaction ID:</strong> {result['transaction_id']}
                                    </div>
                                    <div style='font-size: 1.1rem; margin-bottom: 0.5rem;'>
                                        <strong>Customer:</strong> {result['customer_name']} ({result['localkard_id']})
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                # Points breakdown
                                st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("💎 Points Earned", f"{result['points_earned']:.1f}",
                                             help="Total points awarded for this purchase")
                                with col2:
                                    st.metric("📊 New Balance", f"{result['new_balance']:.1f}",
                                             help="Customer's total points balance")
                                with col3:
                                    tier_badge = result['customer_tier'].upper()
                                    tier_color = LOYALTY_TIERS[result['customer_tier']]['color']
                                    st.markdown(f"""
                                    <div style='text-align: center;'>
                                        <div style='font-size: 0.75rem; color: {MD_COLORS['text_muted']};'>TIER</div>
                                        <div class='tier-badge' style='background: {tier_color}; color: white; margin-top: 0.5rem;'>
                                            {tier_badge}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                with col4:
                                    multiplier = LOYALTY_TIERS[result['customer_tier']]['multiplier']
                                    st.metric("⚡ Multiplier", f"{multiplier}x",
                                             help="Current tier earning multiplier")

                                # Tier upgrade notification
                                if result.get('tier_upgraded'):
                                    st.success("🎉 **CONGRATULATIONS!** Customer upgraded to a new tier!")

                                # Points breakdown details
                                if 'points_breakdown' in result:
                                    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
                                    st.markdown("### 📋 Points Calculation Breakdown")

                                    breakdown = result['points_breakdown']
                                    st.markdown(f"""
                                    <div class='premium-card'>
                                        <table style='width: 100%; border-collapse: collapse;'>
                                            <tr style='border-bottom: 2px solid {MD_COLORS["border"]}'>
                                                <th style='text-align: left; padding: 0.8rem; color: {MD_COLORS["text_dark"]};'>Component</th>
                                                <th style='text-align: right; padding: 0.8rem; color: {MD_COLORS["text_dark"]};'>Points</th>
                                            </tr>
                                            <tr style='border-bottom: 1px solid {MD_COLORS["border"]}'>
                                                <td style='padding: 0.8rem; color: {MD_COLORS["text_muted"]};'>Base Points (₹{purchase_amount} × rate)</td>
                                                <td style='padding: 0.8rem; text-align: right; font-weight: 600;'>{breakdown.get('base_points', 0):.1f}</td>
                                            </tr>
                                            <tr style='border-bottom: 1px solid {MD_COLORS["border"]}'>
                                                <td style='padding: 0.8rem; color: {MD_COLORS["text_muted"]};'>Tier Bonus ({multiplier}x multiplier)</td>
                                                <td style='padding: 0.8rem; text-align: right; font-weight: 600; color: {MD_COLORS["success"]};'>+{breakdown.get('tier_bonus', 0):.1f}</td>
                                            </tr>
                                            <tr style='border-bottom: 1px solid {MD_COLORS["border"]}'>
                                                <td style='padding: 0.8rem; color: {MD_COLORS["text_muted"]};'>Campaign Bonus</td>
                                                <td style='padding: 0.8rem; text-align: right; font-weight: 600; color: {MD_COLORS["success"]};'>+{breakdown.get('campaign_bonus', 0):.1f}</td>
                                            </tr>
                                            <tr>
                                                <td style='padding: 0.8rem; font-weight: 700; color: {MD_COLORS["text_dark"]};'>TOTAL POINTS</td>
                                                <td style='padding: 0.8rem; text-align: right; font-size: 1.3rem; font-weight: 800; color: {MD_COLORS["primary"]};'>{result['points_earned']:.1f}</td>
                                            </tr>
                                        </table>
                                    </div>
                                    """, unsafe_allow_html=True)

                                # Fraud detection alerts
                                if 'fraud_alerts' in result and result['fraud_alerts']:
                                    st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
                                    st.warning("⚠️ **Fraud Alerts:**")
                                    for alert in result['fraud_alerts']:
                                        st.warning(f"• {alert}")

                            else:
                                st.error(f"❌ Transaction failed: {result.get('message', 'Unknown error')}")
                                if 'fraud_alerts' in result:
                                    for alert in result['fraud_alerts']:
                                        st.error(f"🛡️ {alert}")

                        except Exception as e:
                            st.error(f"❌ Error processing transaction: {str(e)}")
                            st.exception(e)
                    else:
                        st.error("Please fill in all required fields: Customer Phone (10 digits) and Purchase Amount")

            else:
                st.error("⚠️ Payback backend not available. Make sure payback_engine.py is present.")
                st.info("The Payback-style backend provides:\n- Central customer database\n- Transaction audit trail\n- Complex points calculation\n- Fraud detection\n- Settlement tracking")

        with tab2:
            st.markdown("### Points Earning Rules")

            col1, col2 = st.columns(2)
            with col1:
                earning_amount = st.number_input("For every ₹ spent", value=float(loyalty_config['earning_rate']['amount']), min_value=1.0, step=10.0)
            with col2:
                earning_points = st.number_input("Customer earns (points)", value=float(loyalty_config['earning_rate']['points']), min_value=0.1, step=0.5)

            rate = earning_points / earning_amount
            st.success(f"**Earning Rate:** ₹1 = {rate:.4f} points")

            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

            st.markdown("### Points Redemption Rules")
            col1, col2 = st.columns(2)
            with col1:
                redeem_points = st.number_input("Points to redeem", value=float(loyalty_config['redemption_rate']['points']), min_value=1.0, step=10.0)
            with col2:
                redeem_value = st.number_input("Worth ₹", value=float(loyalty_config['redemption_rate']['value']), min_value=1.0, step=1.0)

            redeem_rate = redeem_value / redeem_points
            st.success(f"**Redemption Rate:** 1 point = ₹{redeem_rate:.2f}")

            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

            st.markdown("### Bonus Points")
            col1, col2 = st.columns(2)
            with col1:
                referral_bonus = st.number_input("Referral Bonus", value=loyalty_config.get('referral_bonus', 50), min_value=0, step=10, help="Points for referring a friend")
            with col2:
                birthday_bonus = st.number_input("Birthday Bonus", value=loyalty_config.get('birthday_bonus', 100), min_value=0, step=10, help="Birthday gift points")

            st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

            if st.button("💾 Save Configuration", use_container_width=True):
                new_config = {
                    'earning_rate': {'amount': earning_amount, 'points': earning_points},
                    'redemption_rate': {'points': redeem_points, 'value': redeem_value},
                    'referral_bonus': referral_bonus,
                    'birthday_bonus': birthday_bonus,
                    'tier_benefits': True
                }
                md_save_loyalty_config(merchant_phone, new_config)
                st.success("✓ Configuration saved successfully!")
                st.balloons()

        with tab2:
            st.markdown("### 🏆 Loyalty Tiers & Benefits")

            for tier_key, tier_info in LOYALTY_TIERS.items():
                st.markdown(f"""
                <div class='premium-card' style='margin-bottom: 1rem; border-left: 4px solid {tier_info["color"]};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <span class='tier-badge' style='background: {tier_info["color"]}; color: white;'>
                                {tier_info["name"].upper()}
                            </span>
                            <div style='color: {MD_COLORS['text_dark']}; font-size: 1.1rem; font-weight: 700; margin-top: 0.8rem;'>
                                Minimum {tier_info["min_points"]:,} lifetime points
                            </div>
                            <div style='color: {MD_COLORS['text_muted']}; font-size: 0.9rem; margin-top: 0.3rem;'>
                                Earn {tier_info["multiplier"]}x points on every purchase
                            </div>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 2.5rem; font-weight: 800; color: {tier_info["color"]};'>
                                {tier_info["multiplier"]}x
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab3:
            st.markdown("### Program Performance")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Points Liability", f"₹{outstanding_liability * redeem_rate:,.0f}", help="Total value of outstanding points")
            with col2:
                st.metric("Redemption Rate", f"{redemption_rate:.1f}%")
            with col3:
                roi = ((total_points_redeemed * redeem_rate) / (total_points_issued * redeem_rate) * 100) if total_points_issued > 0 else 0
                st.metric("Program ROI", f"{roi:.0f}%")

    elif menu == "👥 Customers":
        st.markdown(f"<h1 style='color: {MD_COLORS['text_dark']}; font-size: 2.5rem; font-weight: 800; margin-bottom: 2rem;'>👥 Customer Loyalty Management</h1>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📋 All Customers", "➕ Add Customer"])

        with tab1:
            if customers:
                st.markdown(f"**{len(customers)} customers enrolled**")

                for customer in customers:
                    tier = customer.get('tier', 'bronze')
                    tier_info = LOYALTY_TIERS[tier]

                    st.markdown(f"""
                    <div class='premium-card' style='margin-bottom: 1rem;'>
                        <div style='display: flex; justify-content: space-between; align-items: start;'>
                            <div style='flex: 2;'>
                                <div style='color: {MD_COLORS['text_dark']}; font-size: 1.2rem; font-weight: 700;'>
                                    {customer.get('name', 'N/A')}
                                </div>
                                <div style='color: {MD_COLORS['text_muted']}; font-size: 0.9rem; margin-top: 0.3rem;'>
                                    📱 {customer.get('phone', 'N/A')} • ID: {customer.get('id', 'N/A')}
                                </div>
                                <div style='margin-top: 0.8rem;'>
                                    <span class='tier-badge' style='background: {tier_info["color"]}; color: white;'>
                                        {tier_info["name"].upper()}
                                    </span>
                                </div>
                            </div>
                            <div style='text-align: right;'>
                                <div style='color: {MD_COLORS['primary']}; font-size: 2rem; font-weight: 800;'>
                                    {customer.get('points_balance', 0):,.0f}
                                </div>
                                <div style='color: {MD_COLORS['text_muted']}; font-size: 0.75rem;'>points balance</div>
                                <div style='color: {MD_COLORS['text_muted']}; font-size: 0.75rem; margin-top: 0.3rem;'>
                                    {customer.get('lifetime_points', 0):,.0f} lifetime
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Add transaction history if Payback backend available
                    if PAYBACK_BACKEND_AVAILABLE:
                        with st.expander(f"📜 View Transaction History - {customer.get('name', 'N/A')}"):
                            try:
                                txn_engine = TransactionEngine()
                                # Try to find LocalKard ID
                                customer_phone_num = customer.get('phone', '')
                                if customer_phone_num:
                                    customer_db = CentralCustomerDB()
                                    central_customer = customer_db.get_customer_by_phone(customer_phone_num)

                                    if central_customer:
                                        localkard_id = central_customer['localkard_id']
                                        txns = txn_engine.get_customer_transactions(localkard_id, limit=10)

                                        if txns:
                                            st.markdown(f"**LocalKard ID:** {localkard_id}")
                                            st.markdown("---")

                                            for txn in txns:
                                                txn_type = txn.get('type', 'unknown')
                                                txn_color = MD_COLORS['success'] if txn_type == 'earn' else MD_COLORS['danger'] if txn_type == 'redeem' else MD_COLORS['info']
                                                points_sign = "+" if txn_type == 'earn' else "-"

                                                st.markdown(f"""
                                                <div style='padding: 1rem; background: white; border-left: 4px solid {txn_color}; margin-bottom: 0.8rem; border-radius: 8px;'>
                                                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                                                        <div>
                                                            <div style='font-weight: 600; color: {MD_COLORS["text_dark"]};'>{txn.get('description', 'Transaction')}</div>
                                                            <div style='font-size: 0.75rem; color: {MD_COLORS["text_muted"]}; margin-top: 0.3rem;'>
                                                                {txn.get('timestamp', 'N/A')} • {txn.get('transaction_id', 'N/A')}
                                                            </div>
                                                        </div>
                                                        <div style='text-align: right;'>
                                                            <div style='font-size: 1.3rem; font-weight: 700; color: {txn_color};'>
                                                                {points_sign}{txn.get('points', 0):.1f}
                                                            </div>
                                                            <div style='font-size: 0.75rem; color: {MD_COLORS["text_muted"]};'>
                                                                ₹{txn.get('amount', 0):.0f}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                """, unsafe_allow_html=True)
                                        else:
                                            st.info("No transactions yet for this customer")
                                    else:
                                        st.info("Customer not yet registered in central database. Record a purchase to register them.")
                            except Exception as e:
                                st.error(f"Could not load transaction history: {str(e)}")

            else:
                st.info("👥 No customers yet. Add your first customer to start building loyalty!")

        with tab2:
            st.markdown("### Add New Customer")

            with st.form("add_customer"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Customer Name *")
                    phone = st.text_input("Phone Number *")
                with col2:
                    email = st.text_input("Email (optional)")
                    initial_points = st.number_input("Initial Points Bonus", min_value=0, value=0, step=10)

                if st.form_submit_button("➕ Add Customer", use_container_width=True):
                    if name and phone:
                        customer_data = {
                            'name': name,
                            'phone': phone,
                            'email': email,
                            'points_balance': initial_points,
                            'lifetime_points': initial_points,
                            'tier': md_get_customer_tier(initial_points)
                        }
                        customer_id = md_add_customer(merchant_phone, customer_data)
                        st.success(f"✓ Customer {name} added! ID: {customer_id}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Please fill required fields")

    elif menu == "📊 Analytics":
        st.markdown(f"<h1 style='color: {MD_COLORS['text_dark']}; font-size: 2.5rem; font-weight: 800; margin-bottom: 2rem;'>📊 Loyalty Analytics</h1>", unsafe_allow_html=True)

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Customer Lifetime Value", f"₹{(total_points_issued * 0.1):,.0f}", help="Estimated CLV based on points")
        with col2:
            st.metric("Avg Points/Customer", f"{(total_points_issued / total_customers) if total_customers > 0 else 0:,.0f}")
        with col3:
            st.metric("Active Rate", f"{(active_customers / total_customers * 100) if total_customers > 0 else 0:.0f}%")
        with col4:
            st.metric("Program Health", "Excellent" if redemption_rate < 50 else "Good")

        st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

        # Charts
        if customers:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Tier Distribution")
                tier_data = pd.DataFrame(list(tier_counts.items()), columns=['Tier', 'Count'])
                st.bar_chart(tier_data.set_index('Tier'))

            with col2:
                st.markdown("### Points Distribution")
                st.info("Points analytics will be enhanced as more data is collected")

        else:
            st.info("📊 Analytics will populate as you add customers and transactions")
def customer_dashboard():
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-title">Welcome, {st.session_state.current_user['name']}</div>
        <div class="dashboard-subtitle">Discover local shops</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout", key="customer_logout"):
        st.session_state.logged_in = False
        st.session_state.page = 'landing'
        st.rerun()

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your Orders", "8", "")
    with col2:
        st.metric("Loyalty Points", "450", "+50")
    with col3:
        st.metric("Nearby Shops", "12", "")

    st.write("")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏪 Browse Shops", "📦 My Orders", "💳 Loyalty"])

    with tab1:
        st.subheader("Nearby Shops")
        shops_data = {
            "Shop": ["Fresh Mart Grocery", "Pet Paradise"],
            "Category": ["Grocery", "Pet Store"],
            "Distance": ["0.5 km", "1.2 km"],
            "Rating": ["⭐ 4.5", "⭐ 4.8"]
        }
        st.dataframe(pd.DataFrame(shops_data), use_container_width=True)

    with tab2:
        st.subheader("Your Orders")
        st.write("View your order history")

    with tab3:
        st.subheader("Loyalty Rewards")
        st.write("Track your points and rewards")

# Merchant Signup
def merchant_signup_page():
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown('<div class="login-form-container" style="max-width: 520px;">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Merchant Signup</div>', unsafe_allow_html=True)

        # Basic Info
        shop_name = st.text_input("Shop Name *", placeholder="Enter your shop name", key="signup_shop_name")
        owner_name = st.text_input("Owner Name *", placeholder="Enter your name", key="signup_owner_name")
        phone = st.text_input("Phone Number *", placeholder="Enter your phone", key="signup_phone")

        # Address Info
        st.markdown('<div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6); background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📍 Shop Location</div>', unsafe_allow_html=True)

        col_addr1, col_addr2 = st.columns(2)
        with col_addr1:
            locality = st.text_input("Locality *", placeholder="e.g., Andheri West", key="signup_locality")
        with col_addr2:
            pincode = st.text_input("Pincode *", placeholder="e.g., 400053", key="signup_pincode")

        address = st.text_input("Full Address *", placeholder="Street address", key="signup_address")

        # Geo-location
        st.markdown('<div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6); background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🗺️ Geo-Location *</div>', unsafe_allow_html=True)

        use_current = st.checkbox("📍 Use Current Location (GPS) - Recommended", key="use_current_location", value=True)

        # Initialize session state for location
        if 'gps_latitude' not in st.session_state:
            st.session_state.gps_latitude = None
        if 'gps_longitude' not in st.session_state:
            st.session_state.gps_longitude = None

        if use_current:
            # GPS Location Component
            location_html = """
            <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;

                            // Send to Streamlit
                            window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                value: {lat: lat, lon: lon}
                            }, '*');

                            document.getElementById('location-status').innerHTML =
                                '<div style="color: #4CAF50; padding: 10px; background: rgba(76, 175, 80, 0.1); border-radius: 8px; margin-top: 10px;">✓ Location detected: ' +
                                lat.toFixed(6) + ', ' + lon.toFixed(6) + '</div>';
                        },
                        function(error) {
                            let errorMsg = 'Unable to get location. ';
                            if (error.code === 1) errorMsg += 'Permission denied.';
                            else if (error.code === 2) errorMsg += 'Position unavailable.';
                            else if (error.code === 3) errorMsg += 'Timeout.';

                            document.getElementById('location-status').innerHTML =
                                '<div style="color: #f44336; padding: 10px; background: rgba(244, 67, 54, 0.1); border-radius: 8px; margin-top: 10px;">✗ ' +
                                errorMsg + '</div>';
                        },
                        {
                            enableHighAccuracy: true,
                            timeout: 5000,
                            maximumAge: 0
                        }
                    );
                } else {
                    document.getElementById('location-status').innerHTML =
                        '<div style="color: #f44336; padding: 10px; background: rgba(244, 67, 54, 0.1); border-radius: 8px; margin-top: 10px;">✗ Geolocation not supported</div>';
                }
            }

            // Auto-trigger on load
            window.onload = getLocation;
            </script>
            <div style="padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);">
                <div style="color: #667eea; font-weight: 600; margin-bottom: 10px;">📍 Fetching your GPS location...</div>
                <div style="color: #a0a0c0; font-size: 0.9rem;">Please allow location access when prompted</div>
                <div id="location-status"></div>
                <button onclick="getLocation()" style="margin-top: 10px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
                    🔄 Refresh Location
                </button>
            </div>
            """

            components.html(location_html, height=200)

            latitude = st.session_state.gps_latitude if st.session_state.gps_latitude else 19.0760
            longitude = st.session_state.gps_longitude if st.session_state.gps_longitude else 72.8777

        else:
            col_geo1, col_geo2 = st.columns(2)
            with col_geo1:
                latitude = st.number_input("Latitude", value=19.0760, format="%.6f", key="signup_latitude")
            with col_geo2:
                longitude = st.number_input("Longitude", value=72.8777, format="%.6f", key="signup_longitude")

        # Password
        st.markdown('<div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6); background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🔒 Security</div>', unsafe_allow_html=True)
        password = st.text_input("Password *", type="password", placeholder="Min 6 characters", key="signup_password")
        confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password", key="signup_confirm_password")

        st.markdown('<div style="color: #a0a0c0; font-size: 0.85rem; margin-top: 0.5rem; text-align: center;">* Required fields</div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("Create Account", key="merchant_signup_btn", use_container_width=True):
            # Validate all required fields
            if not shop_name:
                st.error("❌ Shop Name is required")
            elif not owner_name:
                st.error("❌ Owner Name is required")
            elif not phone:
                st.error("❌ Phone Number is required")
            elif not locality:
                st.error("❌ Locality is required")
            elif not pincode:
                st.error("❌ Pincode is required")
            elif not address:
                st.error("❌ Full Address is required")
            elif not latitude or not longitude:
                st.error("❌ GPS Location is required. Please enable 'Use Current Location' or enter coordinates manually")
            elif not password:
                st.error("❌ Password is required")
            elif not confirm_password:
                st.error("❌ Please confirm your password")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            else:
                # Load current merchants
                current_merchants = load_merchants()

                if phone in current_merchants:
                    st.error("❌ Account already exists with this phone number")
                else:
                    # Add new merchant with complete location data
                    current_merchants[phone] = {
                        "name": shop_name,
                        "owner": owner_name,
                        "password": password,
                        "phone": phone,
                        "address": address,
                        "locality": locality,
                        "pincode": pincode,
                        "latitude": float(latitude),
                        "longitude": float(longitude),
                    }

                    # Save to file
                    save_merchants(current_merchants)

                    st.success("✓ Account created successfully!")
                    st.info(f"📱 Login with: **{phone}**")
                    st.balloons()
                    st.session_state.page = 'merchant_login'
                    st.rerun()

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Back to Login", key="back_to_merchant_login", use_container_width=True):
            st.session_state.page = 'merchant_login'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Customer Signup
def customer_signup_page():
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 1, 1.2])

    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Customer Signup</div>', unsafe_allow_html=True)

        name = st.text_input("Full Name", placeholder="Enter your name", key="signup_name")
        phone = st.text_input("Phone Number", placeholder="Enter your phone", key="signup_customer_phone")
        password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_customer_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="signup_customer_confirm_password")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("Create Account", key="customer_signup_btn", use_container_width=True):
            if not all([name, phone, password, confirm_password]):
                st.error("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Load current customers
                current_customers = load_customers()

                if phone in current_customers:
                    st.error("Account already exists")
                else:
                    # Add new customer
                    current_customers[phone] = {
                        "name": name,
                        "password": password,
                        "phone": phone,
                    }

                    # Save to file
                    save_customers(current_customers)

                    st.success("Account created successfully!")
                    st.info(f"📱 Login with: **{phone}**")
                    st.session_state.page = 'customer_login'
                    st.rerun()

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Back to Login", key="back_to_customer_login", use_container_width=True):
            st.session_state.page = 'customer_login'
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Discover Shops
def discover_page():
    import math

    # Function to calculate distance between two coordinates (Haversine formula)
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        distance = R * c
        return distance

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Discover Shops</div>
        <div class="dashboard-subtitle">Find merchants near you in the LocalKard network</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Home", key="back_from_discover"):
        st.session_state.page = 'landing'
        st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Location controls
    col1, col2, col3 = st.columns([0.5, 3, 0.5])

    with col2:
        st.markdown('<div class="about-section" style="padding: 1.5rem;">', unsafe_allow_html=True)

        st.markdown('<div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;">📍 Your Location</div>', unsafe_allow_html=True)

        use_live = st.checkbox("📍 Use Current Location (GPS)", value=False, key="use_live_location")

        # Initialize session state
        if 'discover_gps_lat' not in st.session_state:
            st.session_state.discover_gps_lat = None
        if 'discover_gps_lon' not in st.session_state:
            st.session_state.discover_gps_lon = None

        if use_live:
            # GPS Component for Discover
            discover_location_html = """
            <script>
            function getDiscoverLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;

                            window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                value: {lat: lat, lon: lon}
                            }, '*');

                            document.getElementById('discover-status').innerHTML =
                                '<div style="color: #4CAF50; padding: 10px; background: rgba(76, 175, 80, 0.1); border-radius: 8px; margin-top: 10px;">✓ Your location: ' +
                                lat.toFixed(6) + ', ' + lon.toFixed(6) + '</div>';
                        },
                        function(error) {
                            let errorMsg = 'Unable to get location. ';
                            if (error.code === 1) errorMsg += 'Permission denied - please enable location.';
                            else if (error.code === 2) errorMsg += 'Position unavailable.';
                            else if (error.code === 3) errorMsg += 'Timeout.';

                            document.getElementById('discover-status').innerHTML =
                                '<div style="color: #f44336; padding: 10px; background: rgba(244, 67, 54, 0.1); border-radius: 8px; margin-top: 10px;">✗ ' +
                                errorMsg + '</div>';
                        },
                        {enableHighAccuracy: true, timeout: 5000, maximumAge: 0}
                    );
                } else {
                    document.getElementById('discover-status').innerHTML =
                        '<div style="color: #f44336;">✗ Geolocation not supported</div>';
                }
            }
            window.onload = getDiscoverLocation;
            </script>
            <div style="padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);">
                <div style="color: #667eea; font-weight: 600;">📍 Getting your GPS location...</div>
                <div id="discover-status" style="margin-top: 10px;"></div>
                <button onclick="getDiscoverLocation()" style="margin-top: 10px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
                    🔄 Refresh
                </button>
            </div>
            """

            components.html(discover_location_html, height=180)

            user_lat = st.session_state.discover_gps_lat if st.session_state.discover_gps_lat else 19.0760
            user_lon = st.session_state.discover_gps_lon if st.session_state.discover_gps_lon else 72.8777

        else:
            col_loc1, col_loc2 = st.columns(2)
            with col_loc1:
                user_lat = st.number_input("Latitude", value=19.0760, format="%.6f", key="discover_lat")
            with col_loc2:
                user_lon = st.number_input("Longitude", value=72.8777, format="%.6f", key="discover_lon")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Distance slider
        st.markdown('<div style="color: #ffffff; font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;">🎯 Distance Range</div>', unsafe_allow_html=True)

        # Slider with logarithmic-style options
        distance_options = {
            "20 meters": 0.02,
            "50 meters": 0.05,
            "100 meters": 0.1,
            "500 meters": 0.5,
            "1 km": 1,
            "5 km": 5,
            "10 km": 10,
            "25 km": 25,
            "50 km": 50,
            "100 km": 100
        }

        selected_distance_label = st.select_slider(
            "Filter shops within",
            options=list(distance_options.keys()),
            value="10 km",
            key="distance_slider"
        )

        max_distance = distance_options[selected_distance_label]

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Calculate distances and filter merchants
    current_merchants = load_merchants()
    merchant_distances = []
    for phone, merchant in current_merchants.items():
        if 'latitude' in merchant and 'longitude' in merchant:
            distance = calculate_distance(user_lat, user_lon, merchant['latitude'], merchant['longitude'])
            if distance <= max_distance:
                merchant_distances.append((phone, merchant, distance))

    # Sort by distance
    merchant_distances.sort(key=lambda x: x[2])

    # Display filtered merchants
    col1, col2, col3 = st.columns([0.5, 3, 0.5])

    with col2:
        if not merchant_distances:
            st.markdown("""
            <div class="about-section" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <div style="color: #a0a0c0; font-size: 1.1rem;">No shops found within {max_distance} km</div>
                <div style="color: #808090; font-size: 0.9rem; margin-top: 0.5rem;">Try increasing the distance range</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color: #a0a0c0; font-size: 0.9rem; margin-bottom: 1rem; text-align: center;">Found {len(merchant_distances)} shop(s) within {selected_distance_label}</div>', unsafe_allow_html=True)

            for phone, merchant, distance in merchant_distances:
                # Format distance
                if distance < 1:
                    distance_str = f"{distance * 1000:.0f}m"
                else:
                    distance_str = f"{distance:.1f}km"

                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <div style="color: #ffffff; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">
                                🏪 {merchant['name']}
                            </div>
                            <div style="color: #a0a0c0; font-size: 0.95rem; margin-bottom: 0.3rem;">
                                👤 {merchant['owner']}
                            </div>
                            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.3rem;">
                                📞 {phone}
                            </div>
                            <div style="color: #a0a0c0; font-size: 0.85rem;">
                                📍 {merchant.get('locality', 'N/A')} - {merchant.get('pincode', 'N/A')}
                            </div>
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; align-items: flex-end;">
                            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                                📍 {distance_str}
                            </div>
                            <div style="background: rgba(102, 234, 144, 0.2); border: 1px solid rgba(102, 234, 144, 0.5); color: #66ea90; padding: 0.4rem 1rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">
                                Active
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Router
if st.session_state.page == 'landing':
    landing_page()
elif st.session_state.page == 'merchant_login':
    merchant_login_page()
elif st.session_state.page == 'customer_login':
    customer_login_page()
elif st.session_state.page == 'merchant_signup':
    merchant_signup_page()
elif st.session_state.page == 'customer_signup':
    customer_signup_page()
elif st.session_state.page == 'discover':
    discover_page()
elif st.session_state.page == 'merchant_dashboard':
    merchant_dashboard()
elif st.session_state.page == 'customer_dashboard':
    customer_dashboard()
