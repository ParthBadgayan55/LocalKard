# 🎯 LocalKard Technical Backlog

**Generated:** 2026-08-21  
**Total Items:** 18  
**Priority Breakdown:** Critical: 2 | High: 6 | Medium: 7 | Low: 3

---

## 🔴 CRITICAL (Do Immediately)

### 1. No database backup strategy

- **File:** `central_data/`, `merchant_data/`
- **Type:** data-loss-risk
- **Description:** All data stored in JSON files with no backup or recovery mechanism
- **Impact:** Complete data loss if files corrupted or accidentally deleted
- **Effort:** medium
- **Action:** Implement automated backup to cloud storage (S3/Firebase) or add database migration

---

### 2. No authentication security

- **File:** `app.py` (login sections)
- **Type:** security
- **Description:** Plain text password comparison, no password hashing
- **Impact:** User credentials exposed if database accessed
- **Effort:** small
- **Action:** Add bcrypt/argon2 password hashing, implement proper session management

---

## 🟠 HIGH PRIORITY (Do Soon)

### 1. Missing error handling in Payback Engine

- **File:** `payback_engine.py`
- **Type:** bug-risk
- **Description:** No try-catch blocks around file I/O and JSON operations
- **Impact:** App crashes on corrupted files or disk issues
- **Effort:** small
- **Action:** Add comprehensive error handling with user-friendly messages

---

### 2. No input validation on customer phone numbers

- **File:** `app.py` (merchant dashboard, customer portal)
- **Type:** data-quality
- **Description:** Phone numbers not validated for format (should be 10 digits)
- **Impact:** Invalid data in database, duplicate customers with different formats
- **Effort:** small
- **Action:** Add regex validation for phone format, sanitize before storage

---

### 3. Transaction ID collision risk

- **File:** `payback_engine.py:135` (TransactionEngine)
- **Type:** bug
- **Description:** Transaction IDs generated with simple counter, no uniqueness guarantee across restarts
- **Impact:** Duplicate transaction IDs possible if counter resets
- **Effort:** small
- **Action:** Use UUID or timestamp-based IDs for true uniqueness

---

### 4. Customer redemption flow not implemented

- **File:** `app.py` (merchant dashboard Loyalty section)
- **Type:** missing-feature
- **Description:** Can record purchases and earn points, but no UI to redeem points
- **Impact:** Customers can't use earned points
- **Effort:** medium
- **Action:** Add redemption form and integrate RedemptionEngine

---

### 5. No customer portal

- **File:** None (missing)
- **Type:** missing-feature
- **Description:** Customers have no way to check balance or view transactions
- **Impact:** Poor customer experience, merchants get constant balance inquiries
- **Effort:** large
- **Action:** Build customer dashboard with balance, history, redemption

---

### 6. Points calculation loads all transactions

- **File:** `payback_engine.py` (PointsEngine)
- **Type:** performance
- **Description:** Loads entire transaction history on each calculation
- **Impact:** Slow performance as transaction count grows
- **Effort:** medium
- **Action:** Cache calculated values, only load recent transactions

---

## 🟡 MEDIUM PRIORITY (Plan For)

### 1. Duplicate color definitions

- **File:** `app.py` (multiple locations)
- **Type:** code-quality
- **Description:** MD_COLORS dictionary defined but then colors hardcoded in many places
- **Impact:** Inconsistent styling, hard to maintain theme
- **Effort:** small
- **Action:** Use MD_COLORS everywhere, remove hardcoded hex values

---

### 2. Missing unit tests

- **File:** `payback_engine.py`, all modules
- **Type:** testing
- **Description:** No automated tests for core business logic
- **Impact:** Bugs may go unnoticed, refactoring risky
- **Effort:** large
- **Action:** Add pytest suite with >80% coverage

---

### 3. No API documentation

- **File:** `payback_engine.py`
- **Type:** documentation
- **Description:** Classes and methods lack docstrings
- **Impact:** Hard for other developers to understand code
- **Effort:** medium
- **Action:** Add comprehensive docstrings with examples

---

### 4. Session state not persisted

- **File:** `app.py` (st.session_state)
- **Type:** ux-issue
- **Description:** User logged out on page refresh
- **Impact:** Poor UX, users have to re-login frequently
- **Effort:** medium
- **Action:** Implement persistent session with cookies or local storage

---

### 5. No transaction rollback mechanism

- **File:** `payback_engine.py` (TransactionEngine)
- **Type:** data-integrity
- **Description:** If transaction fails midway, partial data may be saved
- **Impact:** Data inconsistency, manual cleanup needed
- **Effort:** medium
- **Action:** Implement atomic transactions with rollback capability

---

### 6. Hardcoded file paths

- **File:** `app.py`, `payback_engine.py`
- **Type:** code-quality
- **Description:** File paths like 'merchant_data/', 'central_data/' hardcoded
- **Impact:** Hard to test, can't easily change storage location
- **Effort:** small
- **Action:** Use config file or environment variables for paths

---

### 7. No fraud detection testing

- **File:** `payback_engine.py` (FraudDetection class)
- **Type:** testing
- **Description:** Fraud detection logic exists but untested
- **Impact:** May not catch actual fraud, false positives unknown
- **Effort:** small
- **Action:** Create test cases for velocity checks, anomaly detection

---

## 🟢 LOW PRIORITY (Nice to Have)

### 1. Add keyboard shortcuts

- **File:** `app.py` (merchant dashboard)
- **Type:** ux-enhancement
- **Description:** No keyboard navigation or shortcuts
- **Impact:** Power users could be more efficient
- **Effort:** small
- **Action:** Add shortcuts like "/" for search, "n" for new customer

---

### 2. Export reports to PDF/Excel

- **File:** `app.py` (Analytics section)
- **Type:** feature-enhancement
- **Description:** Analytics only viewable in browser
- **Impact:** Merchants can't share reports easily
- **Effort:** medium
- **Action:** Add export buttons using reportlab or pandas.to_excel()

---

### 3. Dark mode toggle

- **File:** `app.py` (theme)
- **Type:** ux-enhancement
- **Description:** Only light theme available
- **Impact:** Harder to use in low-light environments
- **Effort:** medium
- **Action:** Add dark mode with CSS variable switching

---

## 📈 Backlog Metrics

- **Total Technical Debt:** 18 items
- **Effort Distribution:**
  - Small: 9 items (50%)
  - Medium: 7 items (39%)
  - Large: 2 items (11%)
- **Most Common Type:** code-quality (5 items)
- **Top 3 Files with Issues:**
  - app.py (8 items)
  - payback_engine.py (7 items)
  - All modules (3 items - testing/docs)

**Estimated Total Effort:** ~45 story points

---

## 💡 Recommendations

### **Immediate Actions (This Week):**
1. 🚨 **CRITICAL:** Set up automated backups (use GitHub for JSON files as interim solution)
2. 🚨 **CRITICAL:** Add password hashing (bcrypt library, 2 hours work)
3. ⚠️ **HIGH:** Add error handling in PaybackEngine (prevent crashes)

### **Sprint Planning (Next 2 Weeks):**
1. Add input validation for phone numbers
2. Fix transaction ID collision risk  
3. Implement customer redemption flow
4. Add basic error handling throughout

### **Technical Debt Sprint (Next Month):**
1. Create unit test suite for PaybackEngine
2. Build customer portal MVP
3. Add API documentation
4. Refactor hardcoded values

### **Long-term (Next Quarter):**
1. Database migration (consider PostgreSQL/MongoDB)
2. Performance optimization for large transaction volumes
3. Dark mode and advanced UX features
4. Export functionality

---

## 🎯 Quick Wins (Do These First!)

These are **high-impact, low-effort** items you can knock out quickly:

1. ✅ **Add password hashing** (2 hours, prevents major security issue)
2. ✅ **Validate phone numbers** (1 hour, improves data quality)
3. ✅ **Fix transaction ID risk** (1 hour, prevents future bugs)
4. ✅ **Add fraud detection tests** (2 hours, validates critical feature)
5. ✅ **Use config for file paths** (1 hour, easier testing)

**Total Quick Wins:** 7 hours = 1 day of focused work!

---

## 📊 Code Quality Score

Based on this backlog:

- **Security:** 🟡 6/10 (needs hashing, auth improvements)
- **Reliability:** 🟡 7/10 (needs error handling, testing)
- **Performance:** 🟢 8/10 (good now, will need optimization later)
- **Maintainability:** 🟡 7/10 (needs docs, tests, refactoring)
- **User Experience:** 🟢 8/10 (functional, needs polish)

**Overall:** 🟡 **7.2/10** - Good foundation, needs hardening

---

## 🔄 Progress Tracking

### **Week 1 (Current):**
- [x] Backlog created and prioritized
- [ ] Password hashing implemented
- [ ] Automated backups configured
- [ ] Error handling added

### **Week 2:**
- [ ] Input validation complete
- [ ] Transaction ID fix deployed
- [ ] Redemption flow built
- [ ] Quick wins completed

### **Month 1:**
- [ ] Unit tests at 50% coverage
- [ ] Customer portal MVP launched
- [ ] Documentation complete
- [ ] Code refactored

---

## 🎉 When This Backlog is Clear

You'll have:
- ✅ **Secure** authentication and data storage
- ✅ **Reliable** error handling and recovery
- ✅ **Fast** performance even with many transactions
- ✅ **Maintainable** codebase with tests and docs
- ✅ **Complete** feature set (customer portal, redemption)
- ✅ **Production-ready** system for real merchants

---

## 📝 Notes

### **Not Breaking Issues:**
The current system **works well** for the current scale. These items are improvements to make it production-ready for growth.

### **Priority Philosophy:**
- **Critical:** Data loss or security risks
- **High:** Missing features or reliability issues
- **Medium:** Code quality and technical debt
- **Low:** Nice-to-haves and polish

### **Effort Estimates:**
- **Small:** <4 hours (can do in one sitting)
- **Medium:** 4-16 hours (1-2 days)
- **Large:** >16 hours (3+ days or needs design)

---

**🎯 Backlog created! Pick your battles, tackle them systematically, and watch your code quality soar!** 🚀

*Last updated: 2026-08-21*  
*Next review: Weekly*
