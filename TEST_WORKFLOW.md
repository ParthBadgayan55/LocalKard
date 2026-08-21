# 🧪 LocalKard Complete System Test Workflow

**Date:** 2026-08-21  
**Tester:** Master Agent (QA Mode)  
**Environment:** https://localkard-demo.streamlit.app/  
**Objective:** End-to-end testing of all features

---

## 📋 TEST PLAN

### **Phase 1: Landing Page & Navigation**
- [ ] Landing page loads correctly
- [ ] Hero section visible and appealing
- [ ] CTA buttons work (Merchant Login, Customer Portal, Sign Up)
- [ ] Color scheme correct (not purple/dark theme)
- [ ] All text readable
- [ ] Mobile responsive

### **Phase 2: Merchant Journey**

#### **2A: Merchant Signup**
- [ ] Navigate to merchant signup
- [ ] Form fields visible and labeled
- [ ] Shop name input working
- [ ] Owner name input working
- [ ] Phone number validation (10 digits, 6-9 start)
- [ ] Password requirements shown
- [ ] Password strength validation
- [ ] Signup button works
- [ ] Success message displayed
- [ ] Redirect to dashboard

#### **2B: Merchant Login**
- [ ] Navigate to merchant login
- [ ] Phone/username field working
- [ ] Password field working (masked)
- [ ] Login button works
- [ ] Error handling for wrong credentials
- [ ] Success redirect to dashboard

#### **2C: Merchant Dashboard - Home**
- [ ] Dashboard loads without errors
- [ ] Sidebar navigation visible
- [ ] 4 nav options visible (Home, Loyalty, Customers, Analytics)
- [ ] Logout button visible
- [ ] Shop name displayed in header
- [ ] KPI cards visible (4 primary metrics)
- [ ] Numbers formatted correctly
- [ ] Tier distribution showing
- [ ] Colors appropriate (not all purple)
- [ ] Text readable on all backgrounds

#### **2D: Merchant Dashboard - Loyalty Section**
- [ ] Navigate to Loyalty
- [ ] 4 tabs visible: Record Sale, Points Rules, Rewards & Tiers, Program Analytics
- [ ] Tab 1: Record Sale
  - [ ] Customer phone input visible
  - [ ] Customer name input (optional)
  - [ ] Purchase amount input
  - [ ] Description input (optional)
  - [ ] "Process Purchase" button visible and working
  - [ ] "Check Balance" button working
  - [ ] Form validation working
  - [ ] Success message with confetti
  - [ ] Points breakdown displayed
  - [ ] Transaction ID shown
  - [ ] No errors in console

- [ ] Tab 2: Redeem Points (NEW)
  - [ ] Customer phone lookup input
  - [ ] "Lookup" button working
  - [ ] Customer info card displays (name, ID, balance, tier)
  - [ ] Purchase amount input
  - [ ] Points to redeem input
  - [ ] Discount preview shows in real-time
  - [ ] "Confirm Redemption" button working
  - [ ] Validation for insufficient balance
  - [ ] Success message displayed
  - [ ] Redemption history visible below
  - [ ] Transaction cards formatted correctly

- [ ] Tab 3: Points Rules
  - [ ] Earning rate inputs working
  - [ ] Redemption rate inputs working
  - [ ] Bonus points inputs working
  - [ ] Live rate calculations showing
  - [ ] Example table visible
  - [ ] Save button working
  - [ ] Success confirmation

- [ ] Tab 4: Rewards & Tiers
  - [ ] 4 tier cards visible
  - [ ] Tier colors correct (Bronze, Silver, Gold, Platinum)
  - [ ] Multipliers displayed (1x, 1.25x, 1.5x, 2x)
  - [ ] Requirements shown
  - [ ] Benefits listed

- [ ] Tab 5: Program Analytics
  - [ ] Metrics displayed
  - [ ] Points liability calculated
  - [ ] Redemption rate shown
  - [ ] ROI displayed

#### **2E: Merchant Dashboard - Customers**
- [ ] Navigate to Customers
- [ ] Customer list visible
- [ ] Customer cards formatted correctly
- [ ] Tier badges color-coded
- [ ] Points balance prominent
- [ ] "Add Customer" section working
- [ ] Form fields functioning
- [ ] Add button working
- [ ] New customer appears in list
- [ ] Transaction history expandable (if PaybackEngine integrated)

#### **2F: Merchant Dashboard - Analytics**
- [ ] Navigate to Analytics
- [ ] 4 metric cards visible
- [ ] CLV calculated
- [ ] Average points shown
- [ ] Active rate percentage
- [ ] Program health status
- [ ] Tier distribution chart visible
- [ ] Data accurate

### **Phase 3: Customer Journey**

#### **3A: Customer Portal Access**
- [ ] Navigate to Customer Portal (from landing)
- [ ] Login page loads
- [ ] Registration option visible
- [ ] Clean, mobile-friendly design

#### **3B: Customer Registration**
- [ ] Phone number input (10 digits)
- [ ] Name input
- [ ] Email input (optional)
- [ ] Password input
- [ ] Password confirmation
- [ ] Validation working
- [ ] "Register" button working
- [ ] Success message
- [ ] Automatic login or redirect

#### **3C: Customer Login**
- [ ] Phone number input
- [ ] Password input
- [ ] "Login" button working
- [ ] Error handling for wrong credentials
- [ ] Remember me option (if implemented)
- [ ] Success redirect to dashboard

#### **3D: Customer Dashboard - Home**
- [ ] Dashboard loads without errors
- [ ] Points balance displayed LARGE
- [ ] Tier badge visible and colored
- [ ] Progress bar to next tier
- [ ] Redemption value in ₹ shown
- [ ] Recent transactions visible
- [ ] LocalKard ID displayed
- [ ] Navigation menu working

#### **3E: Customer Dashboard - Transactions**
- [ ] Transaction history page loads
- [ ] Filter options visible (All/Earned/Redeemed)
- [ ] Transactions displayed in timeline
- [ ] Each transaction shows:
  - [ ] Date and time
  - [ ] Type (earn/redeem)
  - [ ] Points amount
  - [ ] ₹ value
  - [ ] Merchant name
  - [ ] Transaction ID
- [ ] Color coding (green for earn, red for redeem)
- [ ] Export button working (if implemented)

#### **3F: Customer Dashboard - Redeem**
- [ ] Redemption page loads
- [ ] Current balance shown
- [ ] Available ₹ value shown
- [ ] Merchant selection (if multi-merchant)
- [ ] Points input field
- [ ] Real-time ₹ calculation
- [ ] "Redeem" button working
- [ ] Confirmation dialog
- [ ] Success message
- [ ] Balance updated
- [ ] Redemption code/QR displayed

#### **3G: Customer Dashboard - Referrals**
- [ ] Referral page loads
- [ ] Unique referral code displayed
- [ ] WhatsApp share button working
- [ ] Referral count shown
- [ ] Bonus points earned displayed
- [ ] Instructions clear

#### **3H: Customer Dashboard - Profile**
- [ ] Profile page loads
- [ ] Name editable
- [ ] Email editable
- [ ] Phone number displayed (non-editable)
- [ ] Change password option
- [ ] Notification preferences
- [ ] Save button working
- [ ] Success confirmation

### **Phase 4: Integration Tests**

#### **4A: Points Flow**
- [ ] Merchant records sale for new customer
- [ ] Customer created automatically
- [ ] Points calculated correctly
- [ ] Tier multiplier applied
- [ ] Transaction recorded
- [ ] Customer can see points immediately
- [ ] Balance updates in real-time

#### **4B: Redemption Flow**
- [ ] Customer has points balance
- [ ] Merchant initiates redemption
- [ ] Customer phone lookup works
- [ ] Balance verified
- [ ] Redemption processed
- [ ] Points deducted
- [ ] Transaction recorded
- [ ] Both sides see updated balance

#### **4C: Tier Upgrade Flow**
- [ ] Customer accumulates points
- [ ] Reaches tier threshold (500, 2000, 5000)
- [ ] Tier automatically upgraded
- [ ] Multiplier changes
- [ ] Notification sent (if WhatsApp active)
- [ ] Badge color changes
- [ ] Progress bar updates

#### **4D: Referral Flow** (if implemented)
- [ ] Customer A generates referral code
- [ ] Customer B uses code to register
- [ ] Customer A receives bonus points
- [ ] Both customers notified
- [ ] Referral count incremented

#### **4E: WhatsApp Notifications** (mock mode)
- [ ] Points earned notification queued
- [ ] Redemption notification queued
- [ ] Tier upgrade notification queued
- [ ] Check console logs for mock messages
- [ ] No errors in notification queue

### **Phase 5: Security & Validation Tests**

#### **5A: Input Validation**
- [ ] Phone: Rejects <10 digits
- [ ] Phone: Rejects starting with 0-5
- [ ] Email: Rejects invalid format
- [ ] Password: Enforces minimum 8 chars
- [ ] Password: Requires uppercase
- [ ] Password: Requires number
- [ ] Amount: Rejects negative
- [ ] Points: Rejects negative

#### **5B: Access Control**
- [ ] Can't access merchant dashboard without login
- [ ] Can't access customer portal without login
- [ ] Logout works correctly
- [ ] Session timeout (if implemented)

#### **5C: Data Integrity**
- [ ] Points can't go negative
- [ ] Can't redeem more than balance
- [ ] Transaction IDs are unique
- [ ] LocalKard IDs are unique
- [ ] Dates formatted correctly
- [ ] No data loss on page refresh

### **Phase 6: UI/UX Tests**

#### **6A: Color Palette**
- [ ] No purple/dark theme (should be light)
- [ ] Text readable on all backgrounds
- [ ] High contrast ratios
- [ ] Consistent color usage
- [ ] Tier colors distinct (Bronze, Silver, Gold, Platinum)
- [ ] Success = Green
- [ ] Warning = Orange
- [ ] Error = Red
- [ ] Primary = Indigo/Blue

#### **6B: Typography**
- [ ] All text readable (no black on dark)
- [ ] Font sizes appropriate
- [ ] Headers distinguishable
- [ ] Labels clear
- [ ] Numbers prominent

#### **6C: Layout**
- [ ] No overlapping elements
- [ ] Spacing consistent
- [ ] Cards aligned
- [ ] Forms organized
- [ ] Buttons accessible

#### **6D: Mobile Responsiveness**
- [ ] Works on mobile screen sizes
- [ ] Navigation accessible
- [ ] Forms usable
- [ ] Buttons tappable (48px min)
- [ ] Text not cut off
- [ ] Horizontal scroll not needed

#### **6E: Loading States**
- [ ] Loading indicators shown
- [ ] No blank screens
- [ ] Error messages helpful
- [ ] Success messages clear
- [ ] Animations smooth

### **Phase 7: Error Handling**

#### **7A: Network Errors**
- [ ] Handles backend unavailable
- [ ] Shows user-friendly messages
- [ ] Doesn't crash app
- [ ] Retry option available

#### **7B: Data Errors**
- [ ] Handles corrupted data gracefully
- [ ] Validates JSON structure
- [ ] Fallbacks to defaults
- [ ] Logs errors appropriately

#### **7C: User Errors**
- [ ] Clear error messages
- [ ] Highlights invalid fields
- [ ] Suggests corrections
- [ ] Doesn't lose entered data

### **Phase 8: Performance Tests**

- [ ] Page load < 3 seconds
- [ ] Form submission < 1 second
- [ ] No console errors
- [ ] No memory leaks
- [ ] Images optimized
- [ ] Smooth animations

---

## 🐛 BUG TRACKING

### **Critical Bugs** 🔴
*(App-breaking issues)*

None found yet - will update during testing.

### **High Priority Bugs** 🟠
*(Feature not working as expected)*

None found yet - will update during testing.

### **Medium Priority Bugs** 🟡
*(Minor issues, workarounds available)*

None found yet - will update during testing.

### **Low Priority Bugs** 🟢
*(Cosmetic issues)*

None found yet - will update during testing.

---

## 💡 IMPROVEMENT SUGGESTIONS

### **Quick Wins** (< 1 hour each)

None yet - will populate after testing.

### **UX Enhancements** (1-2 hours each)

None yet - will populate after testing.

### **Feature Additions** (1 day each)

None yet - will populate after testing.

### **Long-term Improvements** (1 week+)

None yet - will populate after testing.

---

## ✅ TEST EXECUTION

**Tester:** Master Agent  
**Start Time:** [Will be filled]  
**End Time:** [Will be filled]  
**Total Tests:** 200+  
**Tests Passed:** [Will be filled]  
**Tests Failed:** [Will be filled]  
**Critical Issues:** [Will be filled]  
**Bugs Fixed:** [Will be filled]

---

**Status:** 🔄 Testing in progress...
