import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import streamlit.components.v1 as components
import json
import os

# Import merchant modules at top level
try:
    import merchant_data
    import merchant_dashboard
    MERCHANT_MODULES_LOADED = True
except ImportError as e:
    MERCHANT_MODULES_LOADED = False
    print(f"Warning: Could not import merchant modules: {e}")

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
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

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
    """Main merchant dashboard - calls comprehensive dashboard module"""
    if MERCHANT_MODULES_LOADED:
        try:
            merchant_dashboard.merchant_dashboard_main(st.session_state.current_user)
            return
        except Exception as e:
            st.error(f"Error loading dashboard module: {e}")
            # Fall through to simple dashboard

    # Fallback simple dashboard
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-title">Welcome, {st.session_state.current_user['owner']}</div>
        <div class="dashboard-subtitle">{st.session_state.current_user['name']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout", key="merchant_logout"):
        st.session_state.logged_in = False
        st.session_state.page = 'landing'
        st.rerun()

    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Orders", "0", "")
    with col2:
        st.metric("Revenue", "₹0", "")
    with col3:
        st.metric("Active Products", "0", "")
    with col4:
        st.metric("Pending Orders", "0", "")

    st.write("")

    # Simple tabs
    tab1, tab2, tab3 = st.tabs(["📦 Orders", "🛍️ Products", "📊 Analytics"])

    with tab1:
        st.subheader("Recent Orders")
        st.info("📦 No orders yet. The complete dashboard will load shortly.")

    with tab2:
        st.subheader("Product Catalog")
        st.info("🛍️ Add your products here. Dashboard loading...")

    with tab3:
        st.subheader("Sales Analytics")
        st.info("📊 Analytics will appear here.")

    # Show what went wrong
    if not MERCHANT_MODULES_LOADED:
        with st.expander("🔧 Troubleshooting"):
            st.warning("Merchant dashboard modules couldn't load. The app is still deploying on Streamlit Cloud.")
            st.info("Please wait 1-2 minutes and refresh the page.")
            st.write("Files in directory:", [f for f in os.listdir('.') if f.endswith('.py')])

# Customer Dashboard
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
