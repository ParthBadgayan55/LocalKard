import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="LocalKard Phase 1 Demo",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
    }
    .chat-message {
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 80%;
    }
    .chat-bot {
        background-color: #e8e8e8;
        margin-right: auto;
    }
    .chat-user {
        background-color: #dcf8c6;
        margin-left: auto;
        text-align: right;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1 {
        color: #2563eb;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_shop = None

# Sample data
SAMPLE_SHOPS = {
    "9876543210": {
        "name": "Fresh Mart Grocery",
        "owner": "Rajesh Kumar",
        "category": "grocery",
        "phone": "9876543210",
        "password": "password123",
        "address": "123 Main Street, Mumbai",
        "whatsapp": "9876543210",
        "products": [
            {"id": 1, "name": "Rice (Basmati)", "category": "groceries", "price": 120, "unit": "kg", "stock": True, "reorder": True, "frequency": 30},
            {"id": 2, "name": "Wheat Flour (Atta)", "category": "groceries", "price": 45, "unit": "kg", "stock": True, "reorder": True, "frequency": 30},
            {"id": 3, "name": "Sugar", "category": "groceries", "price": 42, "unit": "kg", "stock": True, "reorder": True, "frequency": 30},
            {"id": 4, "name": "Milk (Full Cream)", "category": "dairy", "price": 60, "unit": "liter", "stock": True, "reorder": True, "frequency": 7},
            {"id": 5, "name": "Bread", "category": "bakery", "price": 35, "unit": "piece", "stock": True, "reorder": True, "frequency": 3},
            {"id": 6, "name": "Tomatoes", "category": "vegetables", "price": 30, "unit": "kg", "stock": True, "reorder": False, "frequency": 0},
            {"id": 7, "name": "Onions", "category": "vegetables", "price": 25, "unit": "kg", "stock": True, "reorder": False, "frequency": 0},
            {"id": 8, "name": "Eggs", "category": "dairy", "price": 70, "unit": "dozen", "stock": True, "reorder": True, "frequency": 7},
        ],
        "orders": [
            {"id": "ORD001", "customer": "9988776655", "customer_name": "Amit Patel", "items": "Rice x2, Milk x3", "total": 420, "status": "pending", "date": "2026-08-21", "delivery": "pickup"},
            {"id": "ORD002", "customer": "9988776644", "customer_name": "Priya Shah", "items": "Bread x5, Sugar x1", "total": 217, "status": "confirmed", "date": "2026-08-20", "delivery": "delivery"},
            {"id": "ORD003", "customer": "9988776633", "customer_name": "Rahul Kumar", "items": "Wheat Flour x2, Eggs x1", "total": 160, "status": "ready", "date": "2026-08-20", "delivery": "pickup"},
        ]
    },
    "9876543211": {
        "name": "Pet Paradise",
        "owner": "Priya Sharma",
        "category": "pet-store",
        "phone": "9876543211",
        "password": "password123",
        "address": "456 Park Road, Mumbai",
        "whatsapp": "9876543211",
        "products": [
            {"id": 1, "name": "Dog Food (Premium)", "category": "pet-food", "price": 850, "unit": "3kg bag", "stock": True, "reorder": True, "frequency": 30},
            {"id": 2, "name": "Cat Food (Premium)", "category": "pet-food", "price": 650, "unit": "2kg bag", "stock": True, "reorder": True, "frequency": 30},
            {"id": 3, "name": "Dog Treats", "category": "pet-food", "price": 150, "unit": "pack", "stock": True, "reorder": True, "frequency": 15},
            {"id": 4, "name": "Cat Litter", "category": "other", "price": 350, "unit": "5kg bag", "stock": True, "reorder": True, "frequency": 20},
            {"id": 5, "name": "Pet Shampoo", "category": "other", "price": 250, "unit": "bottle", "stock": True, "reorder": False, "frequency": 0},
        ],
        "orders": [
            {"id": "PET001", "customer": "9988776622", "customer_name": "Neha Desai", "items": "Dog Food x1, Dog Treats x2", "total": 1150, "status": "delivered", "date": "2026-08-19", "delivery": "delivery"},
        ]
    }
}

# Header
st.title("🛍️ LocalKard Phase 1 - Interactive Demo")
st.markdown("**WhatsApp-Native Digital Catalog with Automated Reorder Reminders & Cross-Shop Discovery**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f6cd.png", width=80)
    st.header("🧭 Navigation")

    if not st.session_state.logged_in:
        page = st.radio(
            "Choose a page:",
            ["🏠 Overview", "🔐 Shop Login", "💬 WhatsApp Demo", "📚 Documentation"],
            label_visibility="collapsed"
        )
    else:
        st.success(f"✅ Logged in as **{st.session_state.current_shop['name']}**")
        page = st.radio(
            "Choose a page:",
            ["📊 Dashboard", "📦 Products", "🛒 Orders", "💬 WhatsApp Demo", "👤 Profile"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_shop = None
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("[📖 GitHub Repo](#) | [📄 Docs](#) | [🐛 Report Issue](#)")

    st.markdown("---")
    st.caption("Built with ❤️ for local businesses")

# Overview Page
if page == "🏠 Overview":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📊 System Overview")

    with col2:
        st.info("👈 Login to explore the shop dashboard!")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Shops", "2", "+2 this month")
    with col2:
        st.metric("Products", "13", "+13")
    with col3:
        st.metric("Orders Today", "4", "+4")
    with col4:
        st.metric("Active Reminders", "8", "+8")

    st.markdown("---")

    # Core Features
    st.subheader("✅ Phase 1 Core Features")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("💬 **WhatsApp Integration**", expanded=True):
            st.markdown("""
            - ✅ Business API webhook integration
            - ✅ Message parsing & routing
            - ✅ Catalog browsing via chat
            - ✅ Text-based ordering (`1x5, 2x3`)
            - ✅ Order confirmations
            - ✅ Interactive commands (CATALOG, NEARBY, HELP)
            """)

        with st.expander("🔔 **Automated Reorder Reminders**", expanded=True):
            st.markdown("""
            - ✅ Automatic reminder creation on order
            - ✅ Daily cron job (9 AM)
            - ✅ Frequency-based scheduling
            - ✅ One-tap reorder with YES
            - ✅ Smart dismissal
            - ✅ Customizable intervals per product
            """)

    with col2:
        with st.expander("🏪 **Shop Owner Dashboard**", expanded=True):
            st.markdown("""
            - ✅ Registration & JWT authentication
            - ✅ Product CRUD operations
            - ✅ Stock management
            - ✅ Order tracking & status updates
            - ✅ Profile settings
            - ✅ Responsive web interface
            """)

        with st.expander("🗺️ **Cross-Shop Discovery**", expanded=True):
            st.markdown("""
            - ✅ MongoDB geospatial queries (2dsphere)
            - ✅ Location-based search (5km radius)
            - ✅ Category filtering
            - ✅ Personalized recommendations
            - ✅ Network effect between shops
            - ✅ Automated suggestions while browsing
            """)

    st.markdown("---")

    # Tech Stack
    st.subheader("🛠️ Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Backend**
        - Node.js 16+
        - Express.js
        - MongoDB + Mongoose
        - node-cron
        """)

    with col2:
        st.markdown("""
        **Integration**
        - WhatsApp Business API
        - JWT Authentication
        - bcrypt (password hashing)
        - Axios (HTTP client)
        """)

    with col3:
        st.markdown("""
        **Frontend**
        - Vanilla HTML/CSS/JS
        - Responsive design
        - RESTful API
        - 10+ endpoints
        """)

    st.markdown("---")

    # Key Highlights
    st.success("""
    ### 🎯 Zero Payment Strategy

    ✅ **No payment gateway integration**
    ✅ **No KYC requirements**
    ✅ **Customers pay directly to shops** (cash/UPI)
    ✅ **Faster launch, zero regulatory burden**
    ✅ **Focus on core value:** Discovery + Reorders
    """)

    st.info("""
    ### 📈 By the Numbers

    **26 files created** | **13 JavaScript source files** | **5 database models**
    **10+ API endpoints** | **5 documentation files** | **Ready to deploy**
    """)

# Login Page
elif page == "🔐 Shop Login":
    st.header("🔐 Shop Owner Login")

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.form("login_form"):
            st.subheader("Login to Dashboard")

            phone = st.text_input("📱 Phone Number", value="9876543210", max_chars=10)
            password = st.text_input("🔒 Password", type="password", value="password123")

            submit = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit:
                if phone in SAMPLE_SHOPS and SAMPLE_SHOPS[phone]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_shop = SAMPLE_SHOPS[phone]
                    st.success(f"✅ Welcome back, {SAMPLE_SHOPS[phone]['owner']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

    with col2:
        st.info("""
        ### 🔑 Demo Credentials

        **Fresh Mart Grocery**
        - Phone: `9876543210`
        - Password: `password123`

        **Pet Paradise**
        - Phone: `9876543211`
        - Password: `password123`

        ---

        💡 **Tip:** In production, these would be registered through the shop registration form with proper authentication.
        """)

# Dashboard Page
elif page == "📊 Dashboard" and st.session_state.logged_in:
    shop = st.session_state.current_shop

    st.header(f"📊 {shop['name']} Dashboard")
    st.caption(f"👤 Owner: {shop['owner']} | 📂 Category: {shop['category']}")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Products", len(shop['products']))
    with col2:
        in_stock = sum(1 for p in shop['products'] if p['stock'])
        st.metric("In Stock", in_stock)
    with col3:
        pending = sum(1 for o in shop['orders'] if o['status'] == 'pending')
        st.metric("Pending Orders", pending)
    with col4:
        st.metric("Total Orders", len(shop['orders']))

    st.markdown("---")

    # Recent Orders
    st.subheader("📈 Recent Orders")

    if shop['orders']:
        df = pd.DataFrame(shop['orders'])

        # Style the dataframe
        def style_status(val):
            colors = {
                'pending': 'background-color: #fef3c7; color: #92400e',
                'confirmed': 'background-color: #dbeafe; color: #1e40af',
                'ready': 'background-color: #d1fae5; color: #065f46',
                'delivered': 'background-color: #e5e7eb; color: #374151'
            }
            return colors.get(val, '')

        styled_df = df.style.applymap(style_status, subset=['status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No orders yet. Share your WhatsApp catalog with customers!")

    st.markdown("---")

    # Quick Actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Add New Product", use_container_width=True):
            st.info("Navigate to Products tab to add items")

    with col2:
        if st.button("📱 WhatsApp Status", use_container_width=True):
            st.success("✅ WhatsApp Connected")

    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Coming in Phase 2!")

# Products Page
elif page == "📦 Products" and st.session_state.logged_in:
    shop = st.session_state.current_shop

    st.header(f"📦 Product Management - {shop['name']}")

    tab1, tab2 = st.tabs(["📋 Product List", "➕ Add Product"])

    with tab1:
        st.subheader("Your Products")

        # Group products by category
        categories = {}
        for product in shop['products']:
            cat = product['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)

        for category, products in categories.items():
            st.markdown(f"### {category.upper()}")

            for product in products:
                with st.expander(f"**{product['name']}** - ₹{product['price']}/{product['unit']}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Category:** {product['category']}")
                        st.write(f"**Stock:** {'✅ In Stock' if product['stock'] else '❌ Out of Stock'}")

                        if product['reorder']:
                            st.write(f"**Reorder:** 🔔 Enabled (every {product['frequency']} days)")
                        else:
                            st.write("**Reorder:** Disabled")

                    with col2:
                        if st.button(f"Toggle Stock", key=f"stock_{product['id']}_{shop['phone']}"):
                            st.success("✅ Stock status updated!")

                        if st.button(f"🗑️ Delete", key=f"delete_{product['id']}_{shop['phone']}", type="secondary"):
                            st.warning("⚠️ Product deleted!")

    with tab2:
        st.subheader("Add New Product")

        with st.form("add_product_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_name = st.text_input("Product Name*", placeholder="e.g., Tomatoes")
                new_category = st.selectbox("Category*",
                    ["groceries", "vegetables", "fruits", "dairy", "bakery", "pet-food", "medicines", "household", "other"])
                new_price = st.number_input("Price (₹)*", min_value=0.0, step=1.0, value=0.0)

            with col2:
                new_unit = st.text_input("Unit*", value="piece", placeholder="kg, liter, piece")
                new_reorder = st.checkbox("Enable Reorder Reminders", value=False)

                if new_reorder:
                    new_frequency = st.number_input("Reorder Frequency (days)", min_value=1, max_value=365, value=30)
                else:
                    new_frequency = 0

            new_description = st.text_area("Description (optional)", placeholder="Product details...")

            submit = st.form_submit_button("✅ Add Product", use_container_width=True)

            if submit:
                if new_name and new_price > 0:
                    st.success(f"✅ Added **{new_name}** to your catalog!")
                    st.balloons()
                else:
                    st.error("❌ Please fill all required fields")

# Orders Page
elif page == "🛒 Orders" and st.session_state.logged_in:
    shop = st.session_state.current_shop

    st.header(f"🛒 Order Management - {shop['name']}")

    # Filter
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_status = st.selectbox("Filter by Status:", ["All", "pending", "confirmed", "ready", "delivered"])

    st.markdown("---")

    if shop['orders']:
        filtered_orders = [o for o in shop['orders'] if filter_status == "All" or o['status'] == filter_status]

        if filtered_orders:
            for order in filtered_orders:
                with st.expander(f"**Order #{order['id']}** - ₹{order['total']} ({order['status'].upper()})"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(f"**Customer:** {order['customer_name']} ({order['customer']})")
                        st.write(f"**Items:** {order['items']}")
                        st.write(f"**Total:** ₹{order['total']}")
                        st.write(f"**Date:** {order['date']}")
                        st.write(f"**Delivery:** {order['delivery'].capitalize()}")

                        status_colors = {
                            'pending': '🟡',
                            'confirmed': '🔵',
                            'ready': '🟢',
                            'delivered': '⚪'
                        }
                        st.write(f"**Status:** {status_colors.get(order['status'], '')} {order['status'].upper()}")

                    with col2:
                        if order['status'] == 'pending':
                            if st.button("✅ Confirm", key=f"confirm_{order['id']}"):
                                st.success("Order confirmed! Customer notified via WhatsApp.")
                        elif order['status'] == 'confirmed':
                            if st.button("📦 Mark Ready", key=f"ready_{order['id']}"):
                                st.success("Order ready! Customer notified.")
                        elif order['status'] == 'ready':
                            if st.button("🚚 Mark Delivered", key=f"delivered_{order['id']}"):
                                st.success("Order delivered! ✅")
        else:
            st.info(f"No {filter_status} orders found.")
    else:
        st.info("📭 No orders yet. Customers can order via WhatsApp!")

# WhatsApp Demo Page
elif page == "💬 WhatsApp Demo":
    st.header("💬 WhatsApp Customer Experience")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📱 Customer's WhatsApp")

        # Chat container
        chat_container = st.container()

        with chat_container:
            # Welcome message
            st.markdown("""
            <div class="chat-message chat-bot">
            👋 Welcome to LocalKard!<br><br>
            Discover local shops and their products.<br><br>
            Commands:<br>
            • CATALOG - Browse shops<br>
            • NEARBY - Find shops near you<br>
            • HELP - Get help
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="chat-message chat-user">CATALOG</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="chat-message chat-bot">
            🏪 <b>Nearby LocalKard Shops</b><br><br>
            1. <b>Fresh Mart Grocery</b><br>
            &nbsp;&nbsp;&nbsp;grocery • Mumbai<br>
            &nbsp;&nbsp;&nbsp;🚚 Delivery available<br><br>
            2. <b>Pet Paradise</b><br>
            &nbsp;&nbsp;&nbsp;pet-store • Mumbai<br>
            &nbsp;&nbsp;&nbsp;🚚 Delivery available<br><br>
            Reply with shop number to view catalog.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="chat-message chat-user">SHOP 1</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="chat-message chat-bot">
            🛍️ <b>Fresh Mart Grocery - Product Catalog</b><br><br>
            <b>GROCERIES</b><br>
            1. Rice (Basmati) - ₹120/kg ✅<br>
            2. Wheat Flour - ₹45/kg ✅<br>
            3. Sugar - ₹42/kg ✅<br><br>
            <b>DAIRY</b><br>
            4. Milk - ₹60/liter ✅<br><br>
            <b>BAKERY</b><br>
            5. Bread - ₹35/piece ✅<br><br>
            To order, reply with product numbers and quantities.<br>
            Example: "1x5, 2x3"
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="chat-message chat-user">1x2, 4x3</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="chat-message chat-bot">
            ✅ <b>Order Confirmed!</b><br><br>
            Order ID: ORD123<br>
            Fresh Mart Grocery<br><br>
            <b>Items:</b><br>
            • Rice (Basmati) x2 - ₹240<br>
            • Milk x3 - ₹180<br><br>
            <b>Total: ₹420</b><br><br>
            You'll receive updates on your order status.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="padding: 20px; background: #fff3cd; border-radius: 10px; margin: 10px 0;"><b>⏰ 30 days later...</b></div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="chat-message chat-bot">
            Hi there! 🔔<br><br>
            Time to reorder <b>Rice (Basmati)</b> from <b>Fresh Mart Grocery</b>?<br><br>
            Reply YES to place the same order, or CATALOG to browse all products.
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="chat-message chat-user">YES</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="chat-message chat-bot">
            ✅ <b>Reorder Placed!</b><br><br>
            Same items ordered again.<br>
            Total: ₹420
            </div>
            """, unsafe_allow_html=True)

        # Input area
        st.markdown("---")
        user_input = st.text_input("💬 Type a message...", placeholder="e.g., CATALOG, NEARBY, 1x2")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📱 CATALOG", use_container_width=True):
                st.info("Browsing shops...")
        with col_b:
            if st.button("📍 NEARBY", use_container_width=True):
                st.info("Finding nearby shops...")
        with col_c:
            if st.button("❓ HELP", use_container_width=True):
                st.info("Commands: CATALOG, NEARBY, SHOP [n]")

    with col2:
        st.subheader("✨ Key Features Demonstrated")

        st.success("""
        ### 1️⃣ Catalog Browsing
        Customers browse products by category with simple commands.
        """)

        st.info("""
        ### 2️⃣ Text-Based Ordering
        Simple format: `1x5, 2x3`
        Order 5 of item 1, 3 of item 2
        """)

        st.warning("""
        ### 3️⃣ Reorder Reminders
        Automated reminders after set intervals:
        - Groceries: 30 days
        - Dairy: 7 days
        - Bread: 3 days
        """)

        st.success("""
        ### 4️⃣ Order Confirmation
        Instant confirmation with order details to both customer and shop.
        """)

        st.markdown("---")

        st.markdown("### 📊 Commands Available")

        commands = pd.DataFrame({
            "Command": ["CATALOG", "NEARBY", "SHOP [n]", "HELP", "1x5, 2x3", "YES"],
            "Description": [
                "Browse all shops",
                "Find shops near you",
                "View shop's catalog",
                "Show all commands",
                "Place order",
                "Reorder from reminder"
            ]
        })

        st.dataframe(commands, use_container_width=True, hide_index=True)

# Profile Page
elif page == "👤 Profile" and st.session_state.logged_in:
    shop = st.session_state.current_shop

    st.header(f"👤 Shop Profile - {shop['name']}")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Shop Name", value=shop['name'])
            st.text_input("Owner Name", value=shop['owner'])
            st.text_input("Phone", value=shop['phone'], disabled=True)

        with col2:
            st.selectbox("Category",
                ["grocery", "pharmacy", "pet-store", "general-store", "bakery", "other"],
                index=["grocery", "pharmacy", "pet-store", "general-store", "bakery", "other"].index(shop['category']))
            st.text_input("WhatsApp Number", value=shop['whatsapp'])
            st.text_input("Address", value=shop['address'])

        st.markdown("### Delivery Settings")

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Delivery Available", value=True)
        with col2:
            st.number_input("Delivery Radius (km)", value=5, min_value=1, max_value=20)

        if st.form_submit_button("💾 Update Profile", use_container_width=True):
            st.success("✅ Profile updated successfully!")

# Documentation Page
elif page == "📚 Documentation":
    st.header("📚 LocalKard Documentation")

    tabs = st.tabs(["📖 Overview", "🚀 Quick Start", "🔌 API", "💻 Tech Stack"])

    with tabs[0]:
        st.markdown("""
        ## What is LocalKard?

        LocalKard Phase 1 is a **WhatsApp-native digital catalog platform** that connects local shops with customers through:

        - 💬 Chat-based ordering
        - 🔔 Automated reorder reminders
        - 🗺️ Cross-shop discovery
        - 🚫 Zero payment complexity

        ### Key Benefits

        **For Shop Owners:**
        - ✅ Free web dashboard
        - ✅ Easy product management
        - ✅ Order tracking
        - ✅ No payment gateway needed
        - ✅ Reach more customers

        **For Customers:**
        - ✅ No app download
        - ✅ Order via familiar WhatsApp
        - ✅ Never forget to reorder
        - ✅ Discover nearby shops
        - ✅ Pay as usual (cash/UPI)
        """)

    with tabs[1]:
        st.markdown("""
        ## 🚀 Quick Start Guide

        ### Installation

        ```bash
        cd /home/ec2-user/localkard
        ./INSTALL.sh
        ```

        ### Configuration

        Create `.env` file:
        ```env
        MONGODB_URI=mongodb://localhost:27017/localkard
        JWT_SECRET=your_secret_key
        WHATSAPP_PHONE_NUMBER_ID=your_id
        WHATSAPP_ACCESS_TOKEN=your_token
        ```

        ### Seed Test Data

        ```bash
        npm run seed
        ```

        ### Start Server

        ```bash
        npm run dev
        # Opens on http://localhost:3000
        ```

        ### Test Login

        - Phone: 9876543210
        - Password: password123
        """)

    with tabs[2]:
        st.markdown("""
        ## 🔌 API Endpoints

        ### Shop Endpoints

        | Method | Endpoint | Description | Auth |
        |--------|----------|-------------|------|
        | POST | `/api/shop/register` | Register new shop | No |
        | POST | `/api/shop/login` | Authenticate shop | No |
        | GET | `/api/shop/profile` | Get shop details | Yes |
        | PUT | `/api/shop/profile` | Update shop | Yes |
        | POST | `/api/shop/products` | Add product | Yes |
        | GET | `/api/shop/products` | List products | Yes |
        | PUT | `/api/shop/products/:id` | Update product | Yes |
        | DELETE | `/api/shop/products/:id` | Delete product | Yes |
        | GET | `/api/shop/orders` | List orders | Yes |
        | PUT | `/api/shop/orders/:id` | Update order status | Yes |

        ### WhatsApp Webhook

        | Method | Endpoint | Description |
        |--------|----------|-------------|
        | GET | `/api/whatsapp/webhook` | Verification |
        | POST | `/api/whatsapp/webhook` | Message handler |
        """)

    with tabs[3]:
        st.markdown("""
        ## 💻 Technology Stack

        ### Backend
        - **Runtime:** Node.js 16+
        - **Framework:** Express.js
        - **Database:** MongoDB 5+
        - **ODM:** Mongoose
        - **Scheduling:** node-cron

        ### Authentication
        - **Tokens:** JWT
        - **Passwords:** bcrypt (10 rounds)

        ### Integration
        - **Messaging:** WhatsApp Business Cloud API
        - **HTTP Client:** Axios

        ### Frontend
        - **Dashboard:** Vanilla HTML/CSS/JavaScript
        - **Design:** Responsive, mobile-friendly

        ### Database Schema

        **5 Collections:**
        - `shops` - Shop profiles & locations
        - `products` - Catalog items
        - `customers` - User profiles
        - `orders` - Order history
        - `reorderreminders` - Scheduled reminders

        **Key Indexes:**
        - 2dsphere geospatial on shop coordinates
        - Compound index on customer + product
        - Status indexes for queries
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🛍️ **LocalKard Phase 1**")
    st.caption("Built for local businesses")

with col2:
    st.caption("**Tech Stack**")
    st.caption("Node.js • MongoDB • WhatsApp API")

with col3:
    st.caption("**Demo Version**")
    st.caption("Powered by Streamlit")
