# 💳 LocalKard Cashback Points System - Detailed Specification

## Overview
Amazon Seller Central-style cashback points system where merchants control how customers earn loyalty points.

---

## 🎯 Core Concept

**Two Configuration Methods:**

### Method 1: Global Flat Rate (Simple)
- Merchant sets: **"For every ₹100 spent, customer gets 5 points"**
- System auto-calculates proportionally:
  - ₹100 = 5 points
  - ₹50 = 2.5 points
  - ₹1 = 0.05 points
  - ₹1,250 = 62.5 points

**Formula:** `Points = (Order Amount ÷ 100) × 5`

### Method 2: Product-Specific Points (Advanced)
- Different points for each product
- Example:
  - Rice (₹120/kg) = 10 points
  - Milk (₹60/liter) = 3 points
  - Sugar (₹42/kg) = 2 points

**Formula:** `Points = Sum of (Qty × Product Points)`

---

## 📋 Merchant Configuration Interface

### Points Settings Dashboard

```
┌─────────────────────────────────────────────┐
│  💳 Cashback Points Configuration          │
├─────────────────────────────────────────────┤
│                                             │
│  Points System: ⦿ Global Rate              │
│                 ○ Product-Specific          │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Global Points Rate                  │   │
│  │                                     │   │
│  │ For every ₹ [100] spent             │   │
│  │ Customer earns [5] points           │   │
│  │                                     │   │
│  │ Current Rate: ₹1 = 0.05 points    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [ Save Settings ]                          │
│                                             │
└─────────────────────────────────────────────┘
```

### Product-Specific Points (Advanced)

```
┌─────────────────────────────────────────────┐
│  Product Catalog - Points Configuration     │
├─────────────────────────────────────────────┤
│                                             │
│  Product Name      Price    Points/Unit     │
│  ────────────────────────────────────────   │
│  Rice (Basmati)    ₹120     [10] pts       │
│  Milk              ₹60      [3] pts        │
│  Sugar             ₹42      [2] pts        │
│  Bread             ₹35      [2] pts        │
│                                             │
│  [ Save All ]  [ Reset to Global Rate ]     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📊 Points Analytics Dashboard

### Merchant View

```
┌─────────────────────────────────────────────┐
│  💎 Points Overview                         │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────┐       │
│  │ Points       │  │ Points       │       │
│  │ Disbursed    │  │ Redeemed     │       │
│  │              │  │              │       │
│  │  12,450      │  │   3,200      │       │
│  │  +340 today  │  │   -150 today │       │
│  └──────────────┘  └──────────────┘       │
│                                             │
│  ┌──────────────┐  ┌──────────────┐       │
│  │ Outstanding  │  │ Avg Points/  │       │
│  │ Points       │  │ Order        │       │
│  │              │  │              │       │
│  │  9,250       │  │   45         │       │
│  └──────────────┘  └──────────────┘       │
│                                             │
├─────────────────────────────────────────────┤
│  Recent Points Transactions                 │
│  ───────────────────────────────────────   │
│  Customer         Type       Points  Date   │
│  Amit Patel       Earned     +42    Today  │
│  Priya Shah       Redeemed   -50    Today  │
│  Rahul Kumar      Earned     +35    Today  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 💾 Data Structure

### Points Configuration

```json
{
  "merchant_phone": "9876543210",
  "points_system": "global",  // or "product_specific"
  "global_rate": {
    "amount": 100,
    "points": 5,
    "rate_per_rupee": 0.05
  },
  "product_specific": {
    "PROD001": 10,
    "PROD002": 3,
    "PROD003": 2
  },
  "redemption_rate": {
    "points": 100,
    "value": 10,  // 100 points = ₹10
    "rate": 0.1    // 1 point = ₹0.10
  },
  "enabled": true,
  "created_at": "2026-08-21"
}
```

### Points Transaction

```json
{
  "id": "PT001",
  "merchant_phone": "9876543210",
  "customer_phone": "9988776655",
  "order_id": "ORD001",
  "type": "earned",  // or "redeemed"
  "points": 42,
  "calculation": {
    "order_amount": 840,
    "rate": 0.05,
    "formula": "840 × 0.05 = 42"
  },
  "date": "2026-08-21",
  "status": "credited"
}
```

### Customer Points Balance

```json
{
  "customer_phone": "9988776655",
  "merchants": {
    "9876543210": {
      "total_earned": 450,
      "total_redeemed": 100,
      "balance": 350,
      "last_transaction": "2026-08-21"
    }
  }
}
```

---

## 🔄 Points Flow

### When Customer Places Order

1. **Order Created** → Calculate points earned
2. **Order Confirmed by Merchant** → Points pending
3. **Order Delivered** → Points credited to customer
4. **Customer Notification** → "You earned 42 points!"

### When Customer Redeems Points

1. **Customer has 350 points** (350 × ₹0.10 = ₹35 value)
2. **New order for ₹150**
3. **Customer chooses to redeem** 100 points (₹10 off)
4. **Final amount** = ₹150 - ₹10 = ₹140
5. **Balance** = 350 - 100 = 250 points

---

## 🎨 UI Components Needed

### 1. Points Settings Page
- Radio buttons: Global / Product-Specific
- Input fields for rate configuration
- Save button
- Preview calculator

### 2. Product Management (Enhanced)
- Points column in product table
- Points input field in add/edit form
- Bulk update points option

### 3. Order Details (Enhanced)
- Points earned badge
- Points calculation breakdown
- Redemption section (if customer redeemed)

### 4. Points Dashboard Tab
- 4 metric cards (Disbursed, Redeemed, Outstanding, Avg)
- Transaction history table
- Export option

### 5. Customer View (Enhanced)
- Points balance per customer
- Points transaction history
- Redemption history

---

## 📐 Calculation Examples

### Example 1: Global Rate
**Settings:** ₹100 = 5 points (0.05 per rupee)

**Order 1:**
- Amount: ₹420
- Points: 420 × 0.05 = **21 points**

**Order 2:**
- Amount: ₹1,250
- Points: 1,250 × 0.05 = **62.5 points**

### Example 2: Product-Specific
**Settings:**
- Rice (₹120/kg) = 10 points/unit
- Milk (₹60/liter) = 3 points/unit

**Order:**
- 2 kg Rice = 2 × 10 = 20 points
- 3 liters Milk = 3 × 3 = 9 points
- **Total: 29 points**

### Example 3: Redemption
**Customer Balance:** 500 points (= ₹50 value at 0.1 rate)

**New Order:** ₹200
- Customer redeems 200 points (₹20 off)
- Final amount: ₹200 - ₹20 = **₹180**
- New balance: 500 - 200 = **300 points**
- Points earned on ₹180: 180 × 0.05 = **9 points**
- Final balance: 300 + 9 = **309 points**

---

## 🚀 Implementation Priority

### Phase 1A (MVP):
1. ✅ Global rate configuration
2. ✅ Points calculation on orders
3. ✅ Points earned tracking
4. ✅ Basic points dashboard

### Phase 1B (Enhanced):
5. ✅ Product-specific points
6. ✅ Points redemption system
7. ✅ Transaction history
8. ✅ Customer points balance

### Phase 2:
9. ⏳ Points expiry rules
10. ⏳ Bonus points campaigns
11. ⏳ Referral points
12. ⏳ Tier-based multipliers

---

## 🎯 Success Metrics

**For Merchants:**
- Easy setup (< 5 minutes)
- Clear visibility on points liability
- Understand ROI of points program

**For Customers:**
- Know points earned instantly
- Easy to redeem
- Motivates repeat purchases

**Business:**
- 15%+ increase in repeat orders
- 30%+ customers redeem points
- Merchants see value in loyalty

---

## 💡 Key Features (Amazon Seller Central Style)

✅ **Flexible Configuration** - Global or product-level  
✅ **Auto-Calculation** - No manual math  
✅ **Real-time Tracking** - See points disbursed/redeemed  
✅ **Customer Balance** - Track per-customer points  
✅ **Redemption Flow** - Let customers use points  
✅ **Analytics** - Understand program performance  
✅ **Customizable Rates** - Change anytime  

---

Ready to implement! 🚀
