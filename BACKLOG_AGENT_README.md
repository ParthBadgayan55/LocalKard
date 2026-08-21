# 🤖 Backlog Agent - Technical Debt Manager

**Status:** ✅ ACTIVE  
**Created:** 2026-08-21  
**Purpose:** Automated technical backlog management and debt tracking

---

## 🎯 What is the Backlog Agent?

The Backlog Agent is your automated technical project manager. It scans your codebase, identifies technical debt, categorizes issues, and generates prioritized actionable reports.

Think of it as having a dedicated team member who:
- 🔍 Constantly monitors code quality
- 📊 Tracks technical debt
- 🎯 Prioritizes work items
- 📝 Generates clear reports
- 💡 Suggests next steps

---

## 🚀 How to Use the Backlog Agent

### **Method 1: Ask Claude**

Simply ask Claude to run the backlog agent:

```
"Run the backlog agent"
"Scan for technical debt"
"What's in the backlog?"
"Show me issues to fix"
```

### **Method 2: Workflow Command**

Use the Workflow tool directly:

```javascript
Workflow({
  scriptPath: ".claude/workflows/backlog-agent.js",
  description: "Scan codebase for backlog items"
})
```

### **Method 3: Scheduled Runs**

Set up automatic scans:
- Weekly: Monday mornings
- Sprint start: Every 2 weeks
- After major changes: Via CI/CD hook

---

## 📋 What the Agent Scans For

### **Code Markers:**
- `TODO:` - Things to implement
- `FIXME:` - Things to fix
- `HACK:` - Temporary workarounds
- `XXX:` - Urgent attention needed
- `BUG:` - Known bugs
- `DEBT:` - Technical debt
- `IMPROVE:` - Improvements
- `OPTIMIZE:` - Performance improvements

### **Code Quality Issues:**
- Long functions (>50 lines)
- Duplicate code blocks
- Complex nested logic
- Missing error handling
- Hardcoded values
- Poor naming conventions

### **Dependencies:**
- Unused imports
- Outdated packages
- Security vulnerabilities
- Missing requirements

### **Documentation:**
- Missing comments for complex logic
- Outdated documentation
- Incomplete API docs

---

## 📊 Report Structure

The agent generates `BACKLOG.md` with:

### **1. Priority Breakdown**
```
Total Items: 42
Critical: 3 | High: 8 | Medium: 20 | Low: 11
```

### **2. Categorized Items**

Each item includes:
- **File & Line:** Where the issue is
- **Type:** bug, security, performance, debt, improvement, docs
- **Severity:** critical, high, medium, low
- **Effort:** small, medium, large
- **Description:** What needs to be done
- **Context:** Surrounding code

### **3. Metrics**
- Total technical debt count
- Effort distribution
- Most common issue types
- Files with most issues

### **4. Recommendations**
- What to tackle first
- Sprint allocation suggestions
- Long-term planning advice

---

## 🎨 Priority Levels

### **🔴 CRITICAL (Do Immediately)**
- Security vulnerabilities
- Data loss risks
- System crashes
- Blocking production bugs

**Action:** Fix in next 24 hours

---

### **🟠 HIGH PRIORITY (Do Soon)**
- Performance bottlenecks
- User-facing bugs
- Missing critical features
- Integration issues

**Action:** Include in current sprint

---

### **🟡 MEDIUM PRIORITY (Plan For)**
- Code quality issues
- Minor bugs
- UX improvements
- Refactoring needs
- Documentation gaps

**Action:** Schedule for next sprint

---

### **🟢 LOW PRIORITY (Nice to Have)**
- Code style issues
- Nice-to-have features
- Minor optimizations
- Future enhancements

**Action:** Pick up when time permits

---

## 🔄 Workflow Phases

The agent runs in 4 phases:

### **Phase 1: SCAN** 🔍
```
Searches codebase for markers
Scans all .py files
Extracts issue descriptions
Captures code context
```

### **Phase 2: ANALYZE** 📊
```
Categorizes by type
Assesses severity
Groups by priority
Counts occurrences
```

### **Phase 3: PRIORITIZE** 🎯
```
Sorts by severity
Ranks by type
Estimates effort
Orders by urgency
```

### **Phase 4: REPORT** 📝
```
Generates markdown
Calculates metrics
Adds recommendations
Saves to BACKLOG.md
```

---

## 📁 Generated Files

### **BACKLOG.md**
Main backlog report with all items categorized and prioritized.

**Location:** Project root  
**Updated:** Every agent run  
**Format:** Markdown with emoji indicators

---

## 💡 Example Output

```markdown
# 🎯 Technical Backlog Report

**Generated:** 2026-08-21
**Total Items:** 15
**Priority Breakdown:** Critical: 1 | High: 4 | Medium: 7 | Low: 3

---

## 🔴 CRITICAL (Do Immediately)

### 1. Security vulnerability in authentication flow

- **File:** `app.py:450`
- **Type:** security
- **Marker:** `XXX`
- **Effort:** medium
- **Context:**
  ```python
  # XXX: Credentials stored in plaintext - major security risk
  user_data = {'password': password}  # This should be hashed!
  ```

---

## 🟠 HIGH PRIORITY (Do Soon)

### 1. Performance bottleneck in points calculation

- **File:** `payback_engine.py:180`
- **Type:** performance
- **Marker:** `OPTIMIZE`
- **Effort:** medium

### 2. Missing error handling in transaction processing

- **File:** `payback_engine.py:220`
- **Type:** bug
- **Marker:** `FIXME`
- **Effort:** small

---

## 📈 Backlog Metrics

- **Total Technical Debt:** 15 items
- **Effort Distribution:**
  - Small: 6 items
  - Medium: 7 items
  - Large: 2 items
- **Most Common Type:** technical-debt (8 items)
- **Top 3 Files with Issues:**
  - app.py (6 items)
  - payback_engine.py (5 items)
  - merchant_data.py (4 items)

---

## 💡 Recommendations

1. 🚨 URGENT: Address 1 critical item immediately
2. ⚠️ HIGH: Allocate 30-40% of sprint to 4 high-priority items
3. 📋 MEDIUM: Work on 7 medium items as time permits
4. ✨ LOW: 3 nice-to-have items - good for new contributors
5. ⏱️ ESTIMATED TOTAL EFFORT: ~38 story points

---

## 🎯 Next Steps

1. Review critical items in team standup
2. Assign owners to high-priority bugs
3. Schedule technical debt sprint
4. Update this report weekly
5. Celebrate when items are resolved! 🎉
```

---

## 📈 Integration Ideas

### **Sprint Planning**
```
Monday morning:
1. Run backlog agent
2. Review BACKLOG.md in standup
3. Pick items for sprint
4. Assign to team members
5. Track completion
```

### **Code Review**
```
Before PR approval:
1. Check if PR introduces new TODO/FIXME
2. Verify PR addresses backlog items
3. Run agent to see delta
4. Block if critical issues added
```

### **Weekly Maintenance**
```
Every Friday:
1. Run backlog agent
2. Track week-over-week progress
3. Celebrate debt reduction
4. Plan next week's cleanup
```

---

## 🎯 Success Metrics

### **Track These:**
- Total backlog items (want this ↓)
- Critical + High count (want this ↓)
- Items resolved per sprint (want this ↑)
- Average item age (want this ↓)
- Code quality score (want this ↑)

### **Goal:**
Reduce backlog by 20% per quarter while keeping critical items at 0.

---

## 🔧 Customization

### **Add New Markers:**
Edit `.claude/workflows/backlog-agent.js`:

```javascript
const MARKERS = [
  'TODO', 'FIXME', 'HACK', 'XXX', 'BUG', 'DEBT',
  'CUSTOM',  // Add your own!
  'REVIEW',  // Add your own!
];
```

### **Adjust Priority Weights:**
```javascript
const typePriority = {
  'security': 1,     // Highest
  'bug': 2,
  'performance': 3,
  'technical-debt': 4,
  'improvement': 5,
  'documentation': 6  // Lowest
};
```

### **Change Effort Thresholds:**
```javascript
function estimateEffort(description) {
  if (description.includes('refactor')) return 'large';
  if (description.includes('implement')) return 'medium';
  return 'small';
}
```

---

## 🤖 Agent Behavior

### **What It DOES:**
- ✅ Scans all code files
- ✅ Reads markers and comments
- ✅ Categorizes issues
- ✅ Estimates effort
- ✅ Generates reports
- ✅ Provides recommendations

### **What It DOESN'T Do:**
- ❌ Make code changes
- ❌ Commit files
- ❌ Delete anything
- ❌ Run tests
- ❌ Deploy code

**The agent only REPORTS. YOU decide what to fix and when.**

---

## 🎉 Benefits

### **For Developers:**
- 🎯 Clear priorities - know what to work on
- 📊 Visible progress - see debt decrease
- 🚀 Less cognitive load - don't track in head
- 💪 Celebrate wins - items resolved!

### **For Teams:**
- 📋 Shared backlog - everyone sees same list
- 🤝 Better planning - data-driven decisions
- ⚡ Faster standups - refer to report
- 📈 Track velocity - measure debt paydown

### **For Product:**
- 🔍 Visibility - know technical state
- ⚠️ Early warning - catch issues early
- 💰 ROI tracking - see debt investment
- 🎯 Informed decisions - tech vs features

---

## 💬 Example Conversations

### **Ask the Agent:**

```
You: "Run backlog agent"
Claude: *runs workflow*
Claude: "✅ Backlog scan complete! Found 15 items:
        - 1 critical (security)
        - 4 high (bugs & performance)
        - 7 medium (code quality)
        - 3 low (improvements)
        
        Report saved to BACKLOG.md. 
        Recommend addressing the critical security issue ASAP!"
```

```
You: "What's the most urgent backlog item?"
Claude: *reads BACKLOG.md*
Claude: "🔴 CRITICAL: Security vulnerability in app.py:450
        Credentials stored in plaintext - should be hashed.
        This is a security risk and should be fixed immediately."
```

```
You: "How many items did we close this week?"
Claude: *compares reports*
Claude: "Great progress! 🎉
        Last week: 20 items
        This week: 15 items
        Closed: 5 items (25% reduction!)
        
        Keep it up!"
```

---

## 🚀 Getting Started

### **1. First Run**
```
Run: "backlog agent scan"
Wait: ~2-3 minutes
Result: BACKLOG.md generated
```

### **2. Review Report**
```
Open: BACKLOG.md
Read: Priority sections
Discuss: With team
```

### **3. Take Action**
```
Pick: Top 3 items
Assign: To team members
Track: In project board
```

### **4. Track Progress**
```
Weekly: Run agent again
Compare: Item counts
Celebrate: Reductions!
```

---

## 🎯 Pro Tips

### **Tip 1: Run Regularly**
Weekly runs show trends. Don't wait until backlog explodes.

### **Tip 2: Fix As You Go**
When you see a TODO, fix it immediately if it takes <5 minutes.

### **Tip 3: Allocate Time**
Reserve 20% of each sprint for backlog cleanup.

### **Tip 4: Celebrate Wins**
Every item closed is progress. Acknowledge it!

### **Tip 5: Prevent New Debt**
Code review should catch new TODOs before they merge.

---

## 📚 Further Reading

- **Technical Debt Management:** [Martin Fowler's Guide](https://martinfowler.com/bliki/TechnicalDebt.html)
- **Code Quality Metrics:** Industry standards
- **Agile Backlog Management:** Best practices

---

## ✅ Current Status

**Backlog Agent:** ✅ Active and running  
**Last Run:** Running now...  
**Next Run:** Run anytime by asking Claude!

---

## 🎊 Summary

You now have a **dedicated technical debt manager** that:

- 🔍 Automatically scans your codebase
- 📊 Categorizes and prioritizes issues
- 📝 Generates clear, actionable reports
- 🎯 Helps you make data-driven decisions
- 📈 Tracks progress over time

**The Backlog Agent keeps your codebase healthy and your team focused on what matters most!**

---

**🤖 Backlog Agent: Your automated technical project manager!**

*Run it often. Review it regularly. Act on it consistently.* 🚀
