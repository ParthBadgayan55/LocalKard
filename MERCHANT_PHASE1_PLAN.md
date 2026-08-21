# 🏪 LocalKard Phase 1 - Merchant Dashboard Plan

## Overview
Phase 1 focuses on **WhatsApp-Native Catalog & Reorder** with a web dashboard for shop owners to manage their business.

**Goal:** Prove merchant renewal and customer reorder behavior  
**Timeline:** Week 1-12  
**Investment:** $0-50/month (Bootstrapped)

---

## 🎯 Core Features for Phase 1 Merchant Dashboard

### 1. **Dashboard Home** 📊
**Priority:** HIGH  
**Purpose:** Quick overview of business performance

**Metrics to Display:**
- [ ] Today's Orders (count + trend)
- [ ] Today's Revenue (₹ amount + % change)
- [ ] Active Products (in stock)
- [ ] Pending Orders (need action)
- [ ] Total Customers (served this week)
- [ ] Reorder Reminders Sent (automated)

**Visual Elements:**
- Metric cards with icons
- Color-coded trends (green = up, red = down)
- Quick action buttons
- Recent activity feed

---

### 2. **Product Catalog Management** 🛍️
**Priority:** CRITICAL  
**Purpose:** Add, edit, manage products that customers can order

**Features:**

#### Add Product:
- [ ] Product Name *
- [ ] Category (dropdown: groceries, dairy, vegetables, pet-food, etc.)
- [ ] Price (₹) *
- [ ] Unit (kg, liter, piece, dozen) *
- [ ] Stock Status (In Stock / Out of Stock)
- [ ] Enable Reorder Reminder (Yes/No)
- [ ] Reorder Frequency (days: 3, 7, 15, 30)
- [ ] Product Image (optional for Phase 1)

#### View Products:
- [ ] List view with all products
- [ ] Search/filter by category
- [ ] Sort by name, price, stock status
- [ ] Quick toggle for stock status
- [ ] Bulk actions (mark out of stock, delete)

#### Edit Product:
- [ ] Click to edit any product
- [ ] Update price, stock, reorder settings
- [ ] Delete product (with confirmation)

**Data Structure:**
```json
{
  "id": "PROD001",
  "name": "Rice (Basmati)",
  "category": "groceries",
  "price": 120,
  "unit": "kg",
  "stock": true,
  "reorder_enabled": true,
  "reorder_frequency": 30,
  "created_at": "2026-08-21"
}
```

---

### 3. **Order Management** 📦
**Priority:** CRITICAL  
**Purpose:** View and manage customer orders

**Order Statuses:**
1. **Pending** → New order received
2. **Confirmed** → Merchant accepted
3. **Ready** → Ready for pickup/delivery
4. **Delivered** → Order complete
5. **Cancelled** → Order cancelled

**Features:**

#### Orders List:
- [ ] All orders with filters (Today, This Week, All)
- [ ] Status filters (Pending, Confirmed, Ready, etc.)
- [ ] Customer name + phone
- [ ] Order items + total amount
- [ ] Order date/time
- [ ] Delivery method (Pickup / Delivery)

#### Order Details:
- [ ] Full order breakdown
- [ ] Customer contact info
- [ ] Items ordered (quantity × price)
- [ ] Total amount
- [ ] Order notes (if any)
- [ ] Update status button
- [ ] Contact customer (WhatsApp link)

#### Quick Actions:
- [ ] Mark as Confirmed
- [ ] Mark as Ready
- [ ] Mark as Delivered
- [ ] Cancel Order
- [ ] Send WhatsApp message to customer

**Data Structure:**
```json
{
  "id": "ORD001",
  "customer_phone": "9988776655",
  "customer_name": "Amit Patel",
  "items": [
    {"product_id": "PROD001", "name": "Rice", "qty": 2, "price": 120},
    {"product_id": "PROD004", "name": "Milk", "qty": 3, "price": 60}
  ],
  "total": 420,
  "status": "pending",
  "created_at": "2026-08-21 10:30 AM",
  "delivery_method": "pickup"
}
```

---

### 4. **Shop Profile & Settings** ⚙️
**Priority:** MEDIUM  
**Purpose:** Manage shop information

**Features:**
- [ ] View Shop Details
  - Shop Name
  - Owner Name
  - Phone Number
  - Address (locality, pincode, full address)
  - GPS Location (latitude, longitude)
  - Operating Hours (optional)
  
- [ ] Edit Shop Profile
  - Update address
  - Update contact details
  - Update GPS location
  - Add shop description
  
- [ ] WhatsApp Integration
  - WhatsApp Business Number
  - Auto-reply settings (Phase 2)
  - Notification preferences

---

### 5. **Customer Database** 👥
**Priority:** MEDIUM  
**Purpose:** Track customers who have ordered

**Features:**
- [ ] Customer list with details
  - Name
  - Phone number
  - Total orders
  - Last order date
  - Total spent (₹)
  
- [ ] Customer Details View
  - Order history
  - Reorder patterns
  - Preferred products
  - Contact button (WhatsApp)

**Data Structure:**
```json
{
  "phone": "9988776655",
  "name": "Amit Patel",
  "total_orders": 12,
  "last_order": "2026-08-20",
  "total_spent": 5400,
  "reorder_items": ["Rice", "Milk", "Sugar"]
}
```

---

### 6. **Reorder Reminders** 🔔
**Priority:** HIGH  
**Purpose:** View automated reorder reminders sent to customers

**Features:**
- [ ] Reminders Dashboard
  - Total reminders sent today
  - Reminders scheduled (upcoming)
  - Conversion rate (% who reordered)
  
- [ ] Reminder List
  - Customer name + phone
  - Product reminded about
  - Date sent
  - Status (Sent, Delivered, Responded, Ignored)
  - Action taken (Reordered / Dismissed)

- [ ] Manual Send
  - Send custom reminder to specific customer
  - Select products to remind about

**Data Structure:**
```json
{
  "id": "REM001",
  "customer_phone": "9988776655",
  "product": "Rice (Basmati)",
  "frequency": 30,
  "last_order_date": "2026-07-21",
  "reminder_date": "2026-08-21",
  "status": "sent",
  "response": "reordered"
}
```

---

### 7. **Analytics & Reports** 📈
**Priority:** MEDIUM  
**Purpose:** Basic business insights

**Metrics:**
- [ ] Sales Overview
  - Today / This Week / This Month
  - Revenue trend chart
  - Order count trend
  
- [ ] Product Performance
  - Top 5 selling products
  - Out of stock items
  - Products with low orders
  
- [ ] Customer Insights
  - New vs Returning customers
  - Reorder rate
  - Average order value
  
- [ ] Reorder Performance
  - Reminders sent vs orders received
  - Best performing reorder products
  - Reminder conversion rate

---

## 📱 Navigation Structure

```
Merchant Dashboard
├── 🏠 Home (Dashboard Overview)
├── 🛍️ Products (Catalog Management)
│   ├── All Products
│   ├── Add New Product
│   └── Out of Stock
├── 📦 Orders
│   ├── All Orders
│   ├── Pending (needs attention)
│   ├── Confirmed
│   ├── Ready
│   └── Delivered
├── 👥 Customers
│   ├── All Customers
│   └── Customer Details
├── 🔔 Reminders
│   ├── Sent Today
│   ├── Scheduled
│   └── Send Manual Reminder
├── 📊 Analytics
│   ├── Sales Report
│   ├── Product Performance
│   └── Customer Insights
├── ⚙️ Settings
│   ├── Shop Profile
│   ├── WhatsApp Settings
│   └── Account Settings
└── 🚪 Logout
```

---

## 🎨 UI/UX Design Principles

### Visual Design:
- Clean, modern interface
- Mobile-responsive (works on phone)
- Fast loading
- Minimal clicks to key actions
- Color-coded status (green/yellow/red)

### Key Colors:
- **Primary:** Purple gradient (#667eea to #764ba2)
- **Success:** Green (#4CAF50)
- **Warning:** Orange (#FF9800)
- **Danger:** Red (#f44336)
- **Info:** Blue (#2196F3)

### Layout:
- Sidebar navigation (collapsible on mobile)
- Top bar: Shop name + notifications + logout
- Main content area
- Action buttons always visible

---

## 🔐 Access Control

**Merchant Can:**
- ✅ View/manage own products only
- ✅ View/manage orders for their shop only
- ✅ View customers who ordered from them
- ✅ Send reminders to their customers
- ✅ View their own analytics

**Merchant Cannot:**
- ❌ View other merchants' data
- ❌ Access customer passwords
- ❌ Delete their account (contact admin)

---

## 📊 Data Requirements

### Persistent Storage Needed:
1. **Products Database** (per merchant)
2. **Orders Database** (per merchant)
3. **Customers Database** (per merchant)
4. **Reorder Reminders Database**
5. **Shop Settings**

### File Structure:
```
/data
  /merchants
    /{merchant_phone}
      /products.json
      /orders.json
      /customers.json
      /reminders.json
      /settings.json
```

---

## 🚀 Implementation Phases

### Week 1-2: Core Dashboard
- [ ] Dashboard home with metrics
- [ ] Navigation structure
- [ ] Basic layout and styling

### Week 3-4: Product Management
- [ ] Add product form
- [ ] Product list view
- [ ] Edit/delete products
- [ ] Stock status management

### Week 5-6: Order Management
- [ ] Orders list with filters
- [ ] Order details view
- [ ] Status update functionality
- [ ] Customer contact integration

### Week 7-8: Reorder System
- [ ] Reorder reminders dashboard
- [ ] View sent reminders
- [ ] Manual reminder sending
- [ ] Conversion tracking

### Week 9-10: Customer & Analytics
- [ ] Customer database
- [ ] Basic analytics
- [ ] Sales reports
- [ ] Product performance

### Week 11-12: Polish & Testing
- [ ] Mobile optimization
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] User testing with 3-5 merchants

---

## ✅ Success Metrics

**For Merchants:**
- Time to add product: < 2 minutes
- Time to process order: < 30 seconds
- Dashboard load time: < 3 seconds
- Mobile usability: Works on any phone

**Business Metrics:**
- Merchants can manage 20+ products easily
- Process 10+ orders per day efficiently
- Send reorder reminders automatically
- 80%+ merchant satisfaction with dashboard

---

## 🔄 Phase 2 Features (Future)

*Not in Phase 1, but planned:*
- Payment integration
- Inventory tracking
- WhatsApp auto-replies
- Customer app integration
- Loyalty points management
- Advanced analytics
- Multi-user access
- Delivery tracking

---

## 💡 Key Insights from Business Plan

**Phase 1 Goal:**
> Prove merchant renewal behavior (60%+ willing to pay after trial)

**Success Criteria:**
- Dashboard is easy to use
- Saves merchant time
- Increases orders via reorder reminders
- Provides valuable insights
- Works reliably every day

**Zero Payment Complexity:**
- No payment gateway needed
- Orders tracked for learning
- Focus on product discovery & reorder
- Cash/UPI handled outside system

---

## 📝 Next Steps

1. ✅ Review this plan
2. ✅ Confirm feature priorities
3. ✅ Start with Dashboard Home
4. ✅ Build Product Management next
5. ✅ Iterate based on feedback

---

**Ready to build? Let's start with the Dashboard Home!** 🚀
