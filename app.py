import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="LocalKard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Sleek, Futuristic Design
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

    /* Landing page container */
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        min-height: 100vh;
        text-align: center;
        padding: 2rem;
    }

    /* Logo/Brand */
    .brand {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
        letter-spacing: -2px;
    }

    .tagline {
        color: #a0a0c0;
        font-size: 1rem;
        font-weight: 300;
        margin-bottom: 0;
        letter-spacing: 1px;
    }

    /* Login cards */
    .login-cards {
        display: flex;
        gap: 3rem;
        margin-top: 2rem;
        flex-wrap: wrap;
        justify-content: center;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        width: 100%;
        max-width: 340px;
        height: 280px;
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

    /* Login form */
    .login-form-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 3rem;
        max-width: 450px;
        margin: 2rem auto;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .form-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: #ffffff;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    /* Back button */
    .back-link {
        color: #667eea;
        text-align: center;
        margin-top: 1.5rem;
        cursor: pointer;
        font-size: 0.95rem;
    }

    .back-link:hover {
        color: #764ba2;
        text-decoration: underline;
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

    /* Dataframes */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
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

# Sample data
MERCHANTS = {
    "9876543210": {
        "name": "Fresh Mart Grocery",
        "owner": "Rajesh Kumar",
        "password": "merchant123",
        "phone": "9876543210",
    },
    "9876543211": {
        "name": "Pet Paradise",
        "owner": "Priya Sharma",
        "password": "merchant123",
        "phone": "9876543211",
    }
}

CUSTOMERS = {
    "9988776655": {
        "name": "Amit Patel",
        "password": "customer123",
        "phone": "9988776655",
    },
    "9988776644": {
        "name": "Priya Shah",
        "password": "customer123",
        "phone": "9988776644",
    }
}

# Landing Page
def landing_page():
    # Single page layout - everything fits in viewport
    st.markdown("""
    <div style="display: flex; flex-direction: column; min-height: 100vh; justify-content: center; align-items: center; padding: 2rem;">
        <div style="text-align: center; margin-bottom: 3rem;">
            <div class="brand">LocalKard</div>
            <div class="tagline">The Unified Loyalty & Commerce Network</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login cards section - centered
    col1, col2, col3 = st.columns([1, 2.5, 1])

    with col2:
        c1, c2 = st.columns(2, gap="large")

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

# Merchant Login
def merchant_login_page():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">🏪 Merchant Login</div>', unsafe_allow_html=True)

        phone = st.text_input("Phone Number", placeholder="Enter your phone", key="merchant_phone")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="merchant_pass")

        if st.button("Login", key="merchant_login_btn"):
            if phone in MERCHANTS and MERCHANTS[phone]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = 'merchant'
                st.session_state.current_user = MERCHANTS[phone]
                st.session_state.page = 'merchant_dashboard'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('<div class="back-link">', unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_merchant"):
            st.session_state.page = 'landing'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Demo credentials
        st.info("Demo: 9876543210 / merchant123")

# Customer Login
def customer_login_page():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">👤 Customer Login</div>', unsafe_allow_html=True)

        phone = st.text_input("Phone Number", placeholder="Enter your phone", key="customer_phone")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="customer_pass")

        if st.button("Login", key="customer_login_btn"):
            if phone in CUSTOMERS and CUSTOMERS[phone]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = 'customer'
                st.session_state.current_user = CUSTOMERS[phone]
                st.session_state.page = 'customer_dashboard'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown('<div class="back-link">', unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_customer"):
            st.session_state.page = 'landing'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Demo credentials
        st.info("Demo: 9988776655 / customer123")

# Merchant Dashboard
def merchant_dashboard():
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

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Orders", "12", "+3")
    with col2:
        st.metric("Revenue", "₹4,250", "+15%")
    with col3:
        st.metric("Active Products", "24", "")
    with col4:
        st.metric("Pending Orders", "5", "")

    st.write("")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📦 Orders", "🛍️ Products", "📊 Analytics"])

    with tab1:
        st.subheader("Recent Orders")
        orders_data = {
            "Order ID": ["ORD001", "ORD002", "ORD003"],
            "Customer": ["Amit Patel", "Priya Shah", "Rahul Kumar"],
            "Amount": ["₹420", "₹217", "₹160"],
            "Status": ["Pending", "Confirmed", "Ready"]
        }
        st.dataframe(pd.DataFrame(orders_data), use_container_width=True)

    with tab2:
        st.subheader("Product Catalog")
        st.write("Manage your products here")

    with tab3:
        st.subheader("Sales Analytics")
        st.write("View your business insights")

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

# Router
if st.session_state.page == 'landing':
    landing_page()
elif st.session_state.page == 'merchant_login':
    merchant_login_page()
elif st.session_state.page == 'customer_login':
    customer_login_page()
elif st.session_state.page == 'merchant_dashboard':
    merchant_dashboard()
elif st.session_state.page == 'customer_dashboard':
    customer_dashboard()
