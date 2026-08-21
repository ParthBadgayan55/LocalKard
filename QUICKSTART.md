# LocalKard Customer Portal - Quick Start Guide

## 🚀 Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 👤 Test the Customer Portal

### Option 1: Create New Account

1. Click **"Login as Customer"** on landing page
2. Click **"Create Customer Account"**
3. Fill in details:
   - **Name**: Your name
   - **Phone**: 10-digit number (e.g., 9876543210)
   - **Email**: Optional
   - **Password**: Min 8 chars, mixed case + number (e.g., Test@1234)
4. Click **"Create Account"**
5. Login with your credentials

### Option 2: Use Demo Account

**Demo Customer Account:**
- Phone: `demo`
- Password: `demo123`

**LocalKard Test Account:**
- Phone: `LocalKard`
- Password: `LocalKard@55`

---

## 🎯 Quick Feature Tour

### Dashboard (🏠)
- View your points balance and tier
- See redemption value in ₹
- Track progress to next tier
- View recent transactions

### Redeem Points (🎁)
1. Navigate to "Redeem Points"
2. Enter points to redeem (min 100)
3. Enter merchant phone (e.g., 9876543210)
4. Enter purchase amount
5. Click "Redeem Points"
6. Get redemption code to show merchant

### Transaction History (📜)
- View all your transactions
- Filter by type (All/Earned/Redeemed)
- Export to CSV

### Referrals (🔗)
- Get your unique referral code
- Share via WhatsApp
- Earn 50 points per referral

### Profile (👤)
- Edit name and email
- Change password
- Manage notification preferences

---

## 💡 Earning Points

To test the earning flow, you need to act as a **merchant**:

1. Open a new browser tab (or incognito window)
2. Go to merchant login
3. Login as merchant (phone: `demo`, password: `demo123`)
4. Navigate to **"Loyalty"** → **"Record Sale"**
5. Enter customer phone and purchase amount
6. Process the purchase
7. Go back to customer portal to see points credited!

**Earning Rate:** ₹100 = 5 points  
**Redemption Rate:** 100 points = ₹10

---

## 🏆 Tier System

| Tier | Minimum Points | Multiplier |
|------|---------------|------------|
| Bronze | 0 | 1.0x |
| Silver | 500 | 1.25x |
| Gold | 2,000 | 1.5x |
| Platinum | 5,000 | 2.0x |

---

## 🧪 Run Tests

```bash
python3 test_customer_portal.py
```

Should show:
```
✓ ALL TESTS PASSED!
```

---

## 📚 Full Documentation

- **CUSTOMER_PORTAL_GUIDE.md** - Complete feature guide
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **test_customer_portal.py** - Integration tests

---

## 🐛 Troubleshooting

### Can't login?
- Check phone format (10 digits)
- Try demo accounts first
- Verify password strength on signup

### No points showing?
- Points are earned through merchant transactions
- Login as merchant to record a sale
- Check transaction history to verify

### Redemption failed?
- Need minimum 100 points
- Check merchant phone is valid
- Ensure purchase amount ≥ discount value

---

## 🎨 Key Features

✅ Phone-based authentication  
✅ Secure password hashing (bcrypt)  
✅ Points balance dashboard  
✅ Tier progress tracking  
✅ Transaction history with filters  
✅ Points redemption with merchant  
✅ Referral system with WhatsApp  
✅ Profile management  
✅ Mobile-responsive design  
✅ Indian market optimized  

---

## 📱 Mobile Testing

1. Open app on mobile browser
2. All features are touch-friendly
3. Layout adapts to screen size
4. WhatsApp sharing opens native app

---

## 🔒 Security

- Passwords hashed with bcrypt (12 rounds)
- Phone validation (Indian format)
- Email validation
- Input sanitization
- Session management

---

## 🚀 Ready for Production!

All features are:
- ✓ Implemented
- ✓ Tested
- ✓ Documented
- ✓ Secure
- ✓ Mobile-ready

---

**Need help? Check the full documentation or run the test suite!**

*LocalKard - Empowering Local Commerce in India*
