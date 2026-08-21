# Complete Merchant Dashboard for LocalKard Phase 1
import streamlit as st
import pandas as pd
from datetime import datetime, date
from merchant_data import *

# Category options
CATEGORIES = ["Groceries", "Dairy", "Vegetables", "Fruits", "Bakery", "Pet Food", "Beverages", "Snacks", "Others"]
UNITS = ["kg", "liter", "piece", "dozen", "packet", "grams", "ml"]

def merchant_dashboard_main(merchant_data):
    """Main merchant dashboard"""
    merchant_phone = merchant_data['phone']

    # Sidebar Navigation
    st.sidebar.markdown(f"""
    <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 1rem;'>
        <div style='color: white; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;'>🏪 {merchant_data['name']}</div>
        <div style='color: rgba(255,255,255,0.9); font-size: 0.85rem;'>{merchant_data['owner']}</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "🛍️ Products", "💳 Points System", "📦 Orders", "👥 Customers", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = 'landing'
        st.rerun()

    # Main Content
    if menu == "🏠 Dashboard":
        dashboard_home(merchant_phone, merchant_data)
    elif menu == "🛍️ Products":
        product_management(merchant_phone)
    elif menu == "💳 Points System":
        points_system(merchant_phone)
    elif menu == "📦 Orders":
        order_management(merchant_phone)
    elif menu == "👥 Customers":
        customer_management(merchant_phone)
    elif menu == "📊 Analytics":
        analytics_page(merchant_phone)
    elif menu == "⚙️ Settings":
        settings_page(merchant_phone, merchant_data)

def dashboard_home(merchant_phone, merchant_data):
    """Dashboard home with metrics"""
    st.title("📊 Dashboard Overview")

    # Load data
    products = load_products(merchant_phone)
    orders = load_orders(merchant_phone)
    points_stats = get_points_stats(merchant_phone)
    customers = load_customers(merchant_phone)

    # Calculate metrics
    today = date.today().strftime("%Y-%m-%d")
    today_orders = [o for o in orders if o.get('created_at', '').startswith(today)]
    pending_orders = [o for o in orders if o.get('status') == 'pending']
    today_revenue = sum(o.get('total', 0) for o in today_orders)
    in_stock_products = len([p for p in products if p.get('stock', False)])

    # Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Orders", len(today_orders), "+3")
    with col2:
        st.metric("Today's Revenue", f"₹{today_revenue:,.0f}", "+15%")
    with col3:
        st.metric("Active Products", in_stock_products)
    with col4:
        st.metric("Pending Orders", len(pending_orders))

    # Metrics Row 2
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", len(products))
    with col2:
        st.metric("Total Customers", len(customers))
    with col3:
        st.metric("Points Disbursed", f"{points_stats['disbursed']:,.0f}")
    with col4:
        st.metric("Points Redeemed", f"{points_stats['redeemed']:,.0f}")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Recent Activity
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Recent Orders")
        if orders:
            recent_orders = sorted(orders, key=lambda x: x.get('created_at', ''), reverse=True)[:5]
            for order in recent_orders:
                status_color = {"pending": "orange", "confirmed": "blue", "ready": "green", "delivered": "gray"}
                st.markdown(f"""
                <div style='padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 0.5rem;'>
                    <div style='color: white; font-weight: 600;'>{order.get('id')} - {order.get('customer_name', 'N/A')}</div>
                    <div style='color: #a0a0c0; font-size: 0.85rem;'>₹{order.get('total', 0)} • <span style='color: {status_color.get(order.get('status', 'pending'), 'gray')}'>{order.get('status', 'pending').upper()}</span></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No orders yet")

    with col2:
        st.subheader("📈 Quick Stats")
        st.markdown(f"""
        <div style='padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px;'>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'>Total Orders: <span style='color: white; font-weight: 600;'>{len(orders)}</span></div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'>Average Order: <span style='color: white; font-weight: 600;'>₹{(sum(o.get('total', 0) for o in orders) / len(orders)) if orders else 0:,.0f}</span></div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'>Outstanding Points: <span style='color: white; font-weight: 600;'>{points_stats['outstanding']:,.0f}</span></div>
            <div style='color: #a0a0c0;'>Points Transactions: <span style='color: white; font-weight: 600;'>{points_stats['total_transactions']}</span></div>
        </div>
        """, unsafe_allow_html=True)

def product_management(merchant_phone):
    """Product catalog management"""
    st.title("🛍️ Product Management")

    tab1, tab2, tab3 = st.tabs(["📋 All Products", "➕ Add Product", "📊 Inventory"])

    products = load_products(merchant_phone)

    with tab1:
        st.subheader("Product Catalog")

        if products:
            # Search and filter
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                search = st.text_input("🔍 Search products", placeholder="Search by name...")
            with col2:
                category_filter = st.selectbox("Category", ["All"] + CATEGORIES)
            with col3:
                stock_filter = st.selectbox("Stock", ["All", "In Stock", "Out of Stock"])

            # Filter products
            filtered = products
            if search:
                filtered = [p for p in filtered if search.lower() in p.get('name', '').lower()]
            if category_filter != "All":
                filtered = [p for p in filtered if p.get('category') == category_filter]
            if stock_filter == "In Stock":
                filtered = [p for p in filtered if p.get('stock', False)]
            elif stock_filter == "Out of Stock":
                filtered = [p for p in filtered if not p.get('stock', False)]

            st.markdown(f"**{len(filtered)} products**")

            for product in filtered:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    stock_badge = "🟢 In Stock" if product.get('stock') else "🔴 Out of Stock"
                    st.markdown(f"""
                    **{product.get('name')}**
                    {product.get('category', 'N/A')} • {stock_badge}
                    """)

                with col2:
                    st.markdown(f"**₹{product.get('price', 0)}**/{product.get('unit', 'unit')}")

                with col3:
                    points_text = f"{product.get('points', 0)} pts" if product.get('points') else "Global rate"
                    st.markdown(f"💎 {points_text}")

                with col4:
                    if st.button("✏️", key=f"edit_{product.get('id')}", help="Edit"):
                        st.session_state[f'edit_product_{product.get("id")}'] = True
                    if st.button("🗑️", key=f"del_{product.get('id')}", help="Delete"):
                        delete_product(merchant_phone, product.get('id'))
                        st.success(f"Deleted {product.get('name')}")
                        st.rerun()

                # Edit form
                if st.session_state.get(f'edit_product_{product.get("id")}'):
                    with st.expander("✏️ Edit Product", expanded=True):
                        edit_product_form(merchant_phone, product)

                st.markdown("---")
        else:
            st.info("📦 No products yet. Add your first product!")

    with tab2:
        add_product_form(merchant_phone)

    with tab3:
        st.subheader("📊 Inventory Status")
        if products:
            in_stock = len([p for p in products if p.get('stock')])
            out_stock = len(products) - in_stock

            col1, col2 = st.columns(2)
            with col1:
                st.metric("In Stock", in_stock, f"{(in_stock/len(products)*100):.0f}%")
            with col2:
                st.metric("Out of Stock", out_stock)

            # Category breakdown
            st.subheader("By Category")
            df = pd.DataFrame(products)
            if not df.empty:
                category_counts = df['category'].value_counts()
                st.bar_chart(category_counts)

def add_product_form(merchant_phone):
    """Add new product form"""
    st.subheader("➕ Add New Product")

    with st.form("add_product_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Product Name *", placeholder="e.g., Rice (Basmati)")
            category = st.selectbox("Category *", CATEGORIES)
            price = st.number_input("Price (₹) *", min_value=0.0, step=1.0)

        with col2:
            unit = st.selectbox("Unit *", UNITS)
            stock = st.checkbox("In Stock", value=True)
            reorder_enabled = st.checkbox("Enable Reorder Reminders", value=True)

        if reorder_enabled:
            reorder_freq = st.select_slider("Reorder Frequency (days)", [3, 7, 15, 30], value=30)
        else:
            reorder_freq = 0

        # Points configuration
        st.markdown("**💎 Points Configuration**")
        use_custom_points = st.checkbox("Set custom points for this product")
        if use_custom_points:
            custom_points = st.number_input("Points per unit", min_value=0.0, step=0.5, value=5.0)
        else:
            custom_points = None
            st.info("Will use global points rate")

        submitted = st.form_submit_button("➕ Add Product", use_container_width=True)

        if submitted:
            if not name or not price:
                st.error("Please fill all required fields")
            else:
                product_data = {
                    "name": name,
                    "category": category,
                    "price": float(price),
                    "unit": unit,
                    "stock": stock,
                    "reorder_enabled": reorder_enabled,
                    "reorder_frequency": reorder_freq,
                    "points": float(custom_points) if custom_points else None
                }

                product_id = add_product(merchant_phone, product_data)
                st.success(f"✓ Product added successfully! ID: {product_id}")
                st.balloons()
                st.rerun()

def edit_product_form(merchant_phone, product):
    """Edit existing product"""
    with st.form(f"edit_form_{product['id']}"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Product Name", value=product.get('name', ''))
            category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(product.get('category', CATEGORIES[0])) if product.get('category') in CATEGORIES else 0)
            price = st.number_input("Price (₹)", value=float(product.get('price', 0)))

        with col2:
            unit = st.selectbox("Unit", UNITS, index=UNITS.index(product.get('unit', UNITS[0])) if product.get('unit') in UNITS else 0)
            stock = st.checkbox("In Stock", value=product.get('stock', True))

        # Points
        current_points = product.get('points')
        if current_points:
            custom_points = st.number_input("Points per unit", value=float(current_points))
        else:
            custom_points = st.number_input("Points per unit (leave 0 for global rate)", value=0.0)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                updated_data = {
                    "name": name,
                    "category": category,
                    "price": price,
                    "unit": unit,
                    "stock": stock,
                    "points": custom_points if custom_points > 0 else None
                }
                update_product(merchant_phone, product['id'], updated_data)
                st.success("✓ Product updated!")
                del st.session_state[f'edit_product_{product["id"]}']
                st.rerun()

        with col2:
            if st.form_submit_button("❌ Cancel"):
                del st.session_state[f'edit_product_{product["id"]}']
                st.rerun()

def points_system(merchant_phone):
    """Cashback points system configuration"""
    st.title("💳 Cashback Points System")

    config = load_points_config(merchant_phone)
    stats = get_points_stats(merchant_phone)

    # Points Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💎 Points Disbursed", f"{stats['disbursed']:,.0f}")
    with col2:
        st.metric("🎁 Points Redeemed", f"{stats['redeemed']:,.0f}")
    with col3:
        st.metric("📊 Outstanding", f"{stats['outstanding']:,.0f}")
    with col4:
        avg_points = stats['disbursed'] / len(load_orders(merchant_phone)) if load_orders(merchant_phone) else 0
        st.metric("📈 Avg/Order", f"{avg_points:.1f}")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "📊 Transactions", "📈 Analytics"])

    with tab1:
        st.subheader("Points Configuration")

        system_type = st.radio(
            "Points System Type",
            ["global", "product_specific"],
            format_func=lambda x: "🌍 Global Flat Rate" if x == "global" else "🎯 Product-Specific Points",
            index=0 if config['points_system'] == 'global' else 1,
            horizontal=True
        )

        if system_type == "global":
            st.markdown("### Global Points Rate")
            st.info("💡 Set one rate for all products. Points calculated automatically based on order amount.")

            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input("For every ₹", value=float(config['global_rate']['amount']), min_value=1.0, step=10.0)
            with col2:
                points = st.number_input("Customer earns (points)", value=float(config['global_rate']['points']), min_value=0.1, step=0.5)

            rate_per_rupee = points / amount
            st.success(f"**Current Rate:** ₹1 = {rate_per_rupee:.4f} points")

            # Example calculations
            st.markdown("### 📊 Example Calculations")
            test_amounts = [50, 100, 250, 500, 1000]
            examples = []
            for amt in test_amounts:
                pts = amt * rate_per_rupee
                examples.append({"Order Amount": f"₹{amt}", "Points Earned": f"{pts:.1f}"})
            st.table(pd.DataFrame(examples))

            if st.button("💾 Save Global Rate", use_container_width=True):
                config['points_system'] = 'global'
                config['global_rate'] = {
                    "amount": amount,
                    "points": points,
                    "rate_per_rupee": rate_per_rupee
                }
                save_points_config(merchant_phone, config)
                st.success("✓ Global rate saved!")
                st.balloons()
                st.rerun()

        else:
            st.markdown("### Product-Specific Points")
            st.info("💡 Set different points for each product. More control but requires managing each product.")

            products = load_products(merchant_phone)
            if products:
                st.markdown("Set points for each product:")

                for product in products:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{product.get('name')}** - ₹{product.get('price')}/{product.get('unit')}")
                    with col2:
                        current = product.get('points', 0)
                        st.text_input("Points", value=str(current), key=f"pts_{product['id']}", label_visibility="collapsed")
                    with col3:
                        if st.button("Save", key=f"save_pts_{product['id']}"):
                            new_points = float(st.session_state.get(f"pts_{product['id']}", 0))
                            product['points'] = new_points
                            update_product(merchant_phone, product['id'], product)
                            st.success("✓ Saved!")

                if st.button("💾 Enable Product-Specific Mode", use_container_width=True):
                    config['points_system'] = 'product_specific'
                    save_points_config(merchant_phone, config)
                    st.success("✓ Product-specific mode enabled!")
                    st.rerun()
            else:
                st.warning("Add products first to set product-specific points")

        # Redemption Settings
        st.markdown("---")
        st.markdown("### 💰 Redemption Settings")
        col1, col2 = st.columns(2)
        with col1:
            redeem_points = st.number_input("Points to redeem", value=float(config['redemption_rate']['points']), min_value=1.0)
        with col2:
            redeem_value = st.number_input("Worth ₹", value=float(config['redemption_rate']['value']), min_value=1.0)

        redeem_rate = redeem_value / redeem_points
        st.info(f"**Redemption Rate:** 1 point = ₹{redeem_rate:.2f}")

        if st.button("💾 Save Redemption Settings"):
            config['redemption_rate'] = {
                "points": redeem_points,
                "value": redeem_value,
                "rate": redeem_rate
            }
            save_points_config(merchant_phone, config)
            st.success("✓ Redemption settings saved!")
            st.rerun()

    with tab2:
        st.subheader("📊 Points Transactions")
        transactions = load_points_transactions(merchant_phone)

        if transactions:
            # Filter options
            trans_filter = st.selectbox("Filter", ["All", "Earned", "Redeemed"])

            filtered_trans = transactions
            if trans_filter == "Earned":
                filtered_trans = [t for t in transactions if t.get('type') == 'earned']
            elif trans_filter == "Redeemed":
                filtered_trans = [t for t in transactions if t.get('type') == 'redeemed']

            st.markdown(f"**{len(filtered_trans)} transactions**")

            for trans in reversed(filtered_trans[-20:]):  # Show latest 20
                type_icon = "💎" if trans.get('type') == 'earned' else "🎁"
                type_color = "green" if trans.get('type') == 'earned' else "orange"
                sign = "+" if trans.get('type') == 'earned' else "-"

                st.markdown(f"""
                <div style='padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 0.5rem;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <span style='color: {type_color}; font-size: 1.2rem;'>{type_icon}</span>
                            <span style='color: white; font-weight: 600; margin-left: 0.5rem;'>{trans.get('customer_phone', 'N/A')}</span>
                        </div>
                        <div style='color: {type_color}; font-weight: 700; font-size: 1.1rem;'>{sign}{trans.get('points', 0)} pts</div>
                    </div>
                    <div style='color: #a0a0c0; font-size: 0.85rem; margin-top: 0.5rem;'>
                        Order: {trans.get('order_id', 'N/A')} • {trans.get('date', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No points transactions yet")

    with tab3:
        st.subheader("📈 Points Analytics")

        if stats['total_transactions'] > 0:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Distribution")
                dist_data = pd.DataFrame({
                    'Type': ['Disbursed', 'Redeemed'],
                    'Points': [stats['disbursed'], stats['redeemed']]
                })
                st.bar_chart(dist_data.set_index('Type'))

            with col2:
                st.markdown("### Outstanding Liability")
                st.markdown(f"""
                <div style='padding: 2rem; background: rgba(103, 126, 234, 0.1); border-radius: 15px; text-align: center;'>
                    <div style='color: #a0a0c0; font-size: 0.9rem;'>Outstanding Points</div>
                    <div style='color: #667eea; font-size: 2.5rem; font-weight: 700;'>{stats['outstanding']:,.0f}</div>
                    <div style='color: #a0a0c0; font-size: 0.9rem;'>≈ ₹{(stats['outstanding'] * config['redemption_rate']['rate']):,.0f} value</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data yet. Points analytics will appear once you have transactions.")

def order_management(merchant_phone):
    """Order management system"""
    st.title("📦 Order Management")

    orders = load_orders(merchant_phone)

    # Tabs
    tab1, tab2 = st.tabs(["📋 All Orders", "➕ Create Test Order"])

    with tab1:
        st.subheader("Orders List")

        if orders:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.selectbox("Status", ["All", "Pending", "Confirmed", "Ready", "Delivered", "Cancelled"])
            with col2:
                date_filter = st.selectbox("Date", ["All Time", "Today", "This Week"])
            with col3:
                search = st.text_input("Search customer")

            # Apply filters
            filtered_orders = orders

            if status_filter != "All":
                filtered_orders = [o for o in filtered_orders if o.get('status', '').lower() == status_filter.lower()]

            if date_filter == "Today":
                today = date.today().strftime("%Y-%m-%d")
                filtered_orders = [o for o in filtered_orders if o.get('created_at', '').startswith(today)]

            if search:
                filtered_orders = [o for o in filtered_orders if search.lower() in o.get('customer_name', '').lower()]

            st.markdown(f"**{len(filtered_orders)} orders**")

            # Display orders
            for order in reversed(filtered_orders):
                status_colors = {
                    "pending": "#FF9800",
                    "confirmed": "#2196F3",
                    "ready": "#4CAF50",
                    "delivered": "#9E9E9E",
                    "cancelled": "#f44336"
                }

                status_color = status_colors.get(order.get('status', 'pending'), "#9E9E9E")

                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        st.markdown(f"### {order.get('id')}")
                        st.markdown(f"**{order.get('customer_name')}** • {order.get('customer_phone')}")
                        st.markdown(f"*{order.get('created_at', 'N/A')}*")

                    with col2:
                        st.markdown(f"**₹{order.get('total', 0):,.0f}**")
                        st.markdown(f"<span style='color: {status_color}; font-weight: 600;'>{order.get('status', 'pending').upper()}</span>", unsafe_allow_html=True)

                    with col3:
                        # Status update buttons
                        current_status = order.get('status', 'pending')

                        if current_status == 'pending':
                            if st.button("✓ Confirm", key=f"conf_{order['id']}"):
                                update_order_status(merchant_phone, order['id'], 'confirmed')
                                st.success("Order confirmed!")
                                st.rerun()
                        elif current_status == 'confirmed':
                            if st.button("📦 Ready", key=f"ready_{order['id']}"):
                                update_order_status(merchant_phone, order['id'], 'ready')
                                st.success("Order marked ready!")
                                st.rerun()
                        elif current_status == 'ready':
                            if st.button("✓ Delivered", key=f"del_{order['id']}"):
                                update_order_status(merchant_phone, order['id'], 'delivered')
                                # Add points transaction
                                points = calculate_points_earned(merchant_phone, order.get('total', 0))
                                add_points_transaction(merchant_phone, {
                                    'customer_phone': order.get('customer_phone'),
                                    'order_id': order['id'],
                                    'type': 'earned',
                                    'points': points
                                })
                                st.success(f"Order delivered! Customer earned {points} points")
                                st.rerun()

                    # Order details expander
                    with st.expander("View Details"):
                        st.markdown("**Items:**")
                        for item in order.get('items', []):
                            st.markdown(f"- {item.get('name')} × {item.get('qty')} = ₹{item.get('price', 0) * item.get('qty', 0)}")

                        st.markdown(f"**Total:** ₹{order.get('total', 0)}")
                        st.markdown(f"**Delivery:** {order.get('delivery_method', 'N/A')}")

                        # Contact customer
                        whatsapp_link = f"https://wa.me/91{order.get('customer_phone')}?text=Hello%20{order.get('customer_name')},%20regarding%20your%20order%20{order.get('id')}"
                        st.markdown(f"[💬 Contact on WhatsApp]({whatsapp_link})")

                    st.markdown("---")
        else:
            st.info("📦 No orders yet")

    with tab2:
        st.subheader("Create Test Order")
        st.info("💡 This is for testing. In production, orders come from customers via WhatsApp/Web.")

        with st.form("create_order_form"):
            col1, col2 = st.columns(2)

            with col1:
                cust_name = st.text_input("Customer Name *")
                cust_phone = st.text_input("Customer Phone *")

            with col2:
                delivery_method = st.selectbox("Delivery Method", ["Pickup", "Delivery"])

            # Product selection
            st.markdown("**Select Products:**")
            products = load_products(merchant_phone)

            if products:
                selected_items = []
                for product in products[:5]:  # Limit to first 5 for simplicity
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**{product.get('name')}** (₹{product.get('price')}/{product.get('unit')})")
                    with col2:
                        qty = st.number_input(f"Qty", min_value=0, key=f"qty_{product['id']}", label_visibility="collapsed")
                    with col3:
                        if qty > 0:
                            selected_items.append({
                                "product_id": product['id'],
                                "name": product['name'],
                                "qty": qty,
                                "price": product['price']
                            })
                            st.markdown(f"₹{qty * product['price']}")

                total = sum(item['qty'] * item['price'] for item in selected_items)
                st.markdown(f"### Total: ₹{total}")

                submitted = st.form_submit_button("Create Order")

                if submitted:
                    if not cust_name or not cust_phone:
                        st.error("Please fill customer details")
                    elif not selected_items:
                        st.error("Please select at least one product")
                    else:
                        order_data = {
                            "customer_name": cust_name,
                            "customer_phone": cust_phone,
                            "items": selected_items,
                            "total": total,
                            "status": "pending",
                            "delivery_method": delivery_method.lower()
                        }

                        order_id = add_order(merchant_phone, order_data)
                        st.success(f"✓ Order {order_id} created!")
                        st.balloons()
                        st.rerun()
            else:
                st.warning("Add products first to create orders")

def customer_management(merchant_phone):
    """Customer database"""
    st.title("👥 Customer Management")

    customers = load_customers(merchant_phone)
    orders = load_orders(merchant_phone)

    # Build customer data from orders
    customer_data = {}
    for order in orders:
        phone = order.get('customer_phone')
        if phone:
            if phone not in customer_data:
                customer_data[phone] = {
                    'name': order.get('customer_name'),
                    'phone': phone,
                    'orders': 0,
                    'total_spent': 0,
                    'last_order': order.get('created_at')
                }

            customer_data[phone]['orders'] += 1
            customer_data[phone]['total_spent'] += order.get('total', 0)

    if customer_data:
        st.markdown(f"**{len(customer_data)} customers**")

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Customers", len(customer_data))
        with col2:
            avg_orders = sum(c['orders'] for c in customer_data.values()) / len(customer_data)
            st.metric("Avg Orders/Customer", f"{avg_orders:.1f}")
        with col3:
            avg_spent = sum(c['total_spent'] for c in customer_data.values()) / len(customer_data)
            st.metric("Avg Spent/Customer", f"₹{avg_spent:,.0f}")

        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        # Customer list
        for cust_phone, cust in sorted(customer_data.items(), key=lambda x: x[1]['orders'], reverse=True):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

            with col1:
                st.markdown(f"**{cust['name']}**")
                st.markdown(f"{cust['phone']}")

            with col2:
                st.markdown(f"**{cust['orders']}** orders")

            with col3:
                st.markdown(f"**₹{cust['total_spent']:,.0f}** spent")

            with col4:
                whatsapp_link = f"https://wa.me/91{cust['phone']}"
                st.markdown(f"[💬 WhatsApp]({whatsapp_link})")

            st.markdown("---")
    else:
        st.info("👥 No customers yet. Customers appear after first order.")

def analytics_page(merchant_phone):
    """Analytics and reports"""
    st.title("📊 Analytics & Reports")

    products = load_products(merchant_phone)
    orders = load_orders(merchant_phone)
    points_stats = get_points_stats(merchant_phone)

    if not orders:
        st.info("📈 Analytics will appear once you have orders")
        return

    # Date range
    col1, col2 = st.columns([1, 3])
    with col1:
        date_range = st.selectbox("Period", ["Today", "This Week", "This Month", "All Time"])

    # Calculate metrics
    today = date.today().strftime("%Y-%m-%d")

    filtered_orders = orders
    if date_range == "Today":
        filtered_orders = [o for o in orders if o.get('created_at', '').startswith(today)]

    total_revenue = sum(o.get('total', 0) for o in filtered_orders)
    total_orders = len(filtered_orders)
    avg_order = total_revenue / total_orders if total_orders > 0 else 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Revenue", f"₹{total_revenue:,.0f}")
    with col2:
        st.metric("Orders", total_orders)
    with col3:
        st.metric("Avg Order Value", f"₹{avg_order:,.0f}")
    with col4:
        delivered = len([o for o in filtered_orders if o.get('status') == 'delivered'])
        fulfillment_rate = (delivered / total_orders * 100) if total_orders > 0 else 0
        st.metric("Fulfillment Rate", f"{fulfillment_rate:.0f}%")

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Products")
        product_sales = {}
        for order in filtered_orders:
            for item in order.get('items', []):
                pid = item.get('product_id')
                if pid not in product_sales:
                    product_sales[pid] = {'name': item.get('name'), 'qty': 0, 'revenue': 0}
                product_sales[pid]['qty'] += item.get('qty', 0)
                product_sales[pid]['revenue'] += item.get('price', 0) * item.get('qty', 0)

        if product_sales:
            top_products = sorted(product_sales.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
            chart_data = pd.DataFrame([
                {'Product': p[1]['name'], 'Revenue': p[1]['revenue']}
                for p in top_products
            ])
            st.bar_chart(chart_data.set_index('Product'))
        else:
            st.info("No product data yet")

    with col2:
        st.subheader("Order Status")
        status_counts = {}
        for order in filtered_orders:
            status = order.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        if status_counts:
            status_df = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
            st.bar_chart(status_df.set_index('Status'))
        else:
            st.info("No status data yet")

def settings_page(merchant_phone, merchant_data):
    """Settings and shop profile"""
    st.title("⚙️ Settings")

    tab1, tab2 = st.tabs(["🏪 Shop Profile", "🔐 Account"])

    with tab1:
        st.subheader("Shop Information")

        st.markdown(f"""
        <div style='padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 15px;'>
            <div style='color: white; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;'>{merchant_data.get('name')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Owner:</strong> {merchant_data.get('owner')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Phone:</strong> {merchant_data.get('phone')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Address:</strong> {merchant_data.get('address', 'N/A')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Locality:</strong> {merchant_data.get('locality', 'N/A')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Pincode:</strong> {merchant_data.get('pincode', 'N/A')}</div>
            <div style='color: #a0a0c0;'><strong>GPS:</strong> {merchant_data.get('latitude', 'N/A')}, {merchant_data.get('longitude', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 Contact support to update shop details")

    with tab2:
        st.subheader("Account Information")

        st.markdown(f"""
        <div style='padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 15px;'>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Account Type:</strong> Merchant</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Phone:</strong> {merchant_data.get('phone')}</div>
            <div style='color: #a0a0c0; margin-bottom: 0.5rem;'><strong>Status:</strong> <span style='color: #4CAF50;'>Active</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        if st.button("🔒 Change Password"):
            st.info("Password change coming soon!")

