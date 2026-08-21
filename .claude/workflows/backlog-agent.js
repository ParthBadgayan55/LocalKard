export const meta = {
  name: 'backlog-agent',
  description: 'Scan codebase for technical debt, bugs, and improvements. Generate prioritized backlog report.',
  whenToUse: 'Use when user asks to scan for technical debt, review backlog, or identify issues to fix',
  phases: [
    { title: 'Scan', detail: 'Search for TODO, FIXME, HACK, and other markers' },
    { title: 'Analyze', detail: 'Categorize and assess severity of issues' },
    { title: 'Prioritize', detail: 'Assign priority levels and effort estimates' },
    { title: 'Report', detail: 'Generate comprehensive backlog report' }
  ]
};

// Helper to categorize issue type
function categorizeIssue(line, marker) {
  const lowerLine = line.toLowerCase();

  if (marker === 'BUG' || marker === 'FIXME' || lowerLine.includes('crash') || lowerLine.includes('error')) {
    return { type: 'bug', severity: 'high' };
  }

  if (marker === 'XXX' || lowerLine.includes('security') || lowerLine.includes('vulnerability')) {
    return { type: 'security', severity: 'critical' };
  }

  if (marker === 'HACK' || lowerLine.includes('temporary') || lowerLine.includes('workaround')) {
    return { type: 'technical-debt', severity: 'medium' };
  }

  if (lowerLine.includes('performance') || lowerLine.includes('slow') || lowerLine.includes('optimize')) {
    return { type: 'performance', severity: 'high' };
  }

  if (marker === 'IMPROVE' || lowerLine.includes('enhancement') || lowerLine.includes('feature')) {
    return { type: 'improvement', severity: 'low' };
  }

  if (lowerLine.includes('document') || lowerLine.includes('readme') || lowerLine.includes('comment')) {
    return { type: 'documentation', severity: 'low' };
  }

  return { type: 'technical-debt', severity: 'medium' };
}

// Helper to estimate effort
function estimateEffort(description) {
  const desc = description.toLowerCase();

  if (desc.includes('refactor') || desc.includes('rewrite') || desc.includes('redesign')) {
    return 'large';
  }

  if (desc.includes('implement') || desc.includes('add feature') || desc.includes('integrate')) {
    return 'medium';
  }

  if (desc.includes('fix typo') || desc.includes('rename') || desc.includes('update text')) {
    return 'small';
  }

  const wordCount = desc.split(' ').length;
  if (wordCount > 15) return 'large';
  if (wordCount > 8) return 'medium';
  return 'small';
}

// Schema for backlog items
const BACKLOG_ITEM_SCHEMA = {
  type: 'object',
  properties: {
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string' },
          line: { type: 'number' },
          marker: { type: 'string' },
          description: { type: 'string' },
          type: { type: 'string' },
          severity: { type: 'string' },
          effort: { type: 'string' },
          context: { type: 'string' }
        },
        required: ['file', 'marker', 'description']
      }
    }
  },
  required: ['items']
};

// ============================================================================
// PHASE 1: SCAN FOR MARKERS
// ============================================================================

phase('Scan');

log('🔍 Scanning codebase for technical debt markers...');

// Define markers to search for
const MARKERS = ['TODO', 'FIXME', 'HACK', 'XXX', 'BUG', 'DEBT', 'IMPROVE', 'OPTIMIZE'];

// Search for each marker in parallel
const scanResults = await parallel(
  MARKERS.map(marker => () =>
    agent(`Search the codebase for "${marker}:" comments. For each occurrence, extract:
    - File path
    - Line number
    - The comment text
    - 2-3 lines of surrounding code for context

    Focus on .py files (Python code). Ignore node_modules, .git, __pycache__ directories.

    Return structured data for each finding.`, {
      label: `scan-${marker}`,
      phase: 'Scan',
      schema: BACKLOG_ITEM_SCHEMA
    })
  )
);

const allFindings = scanResults
  .filter(Boolean)
  .flatMap(result => result.items || [])
  .filter(item => item && item.description);

log(`Found ${allFindings.length} backlog items across ${MARKERS.length} marker types`);

// ============================================================================
// PHASE 2: ANALYZE & CATEGORIZE
// ============================================================================

phase('Analyze');

log('📊 Analyzing and categorizing issues...');

// Categorize each finding
const categorized = allFindings.map(item => {
  const { type, severity } = categorizeIssue(item.description, item.marker);
  const effort = estimateEffort(item.description);

  return {
    ...item,
    type: type,
    severity: severity,
    effort: effort
  };
});

// Group by severity
const bySeverity = {
  critical: categorized.filter(i => i.severity === 'critical'),
  high: categorized.filter(i => i.severity === 'high'),
  medium: categorized.filter(i => i.severity === 'medium'),
  low: categorized.filter(i => i.severity === 'low')
};

log(`Categorized: ${bySeverity.critical.length} critical, ${bySeverity.high.length} high, ${bySeverity.medium.length} medium, ${bySeverity.low.length} low`);

// ============================================================================
// PHASE 3: PRIORITIZE
// ============================================================================

phase('Prioritize');

log('🎯 Prioritizing backlog items...');

// Sort within each severity group by type priority
const typePriority = {
  'security': 1,
  'bug': 2,
  'performance': 3,
  'technical-debt': 4,
  'improvement': 5,
  'documentation': 6
};

Object.keys(bySeverity).forEach(severity => {
  bySeverity[severity].sort((a, b) => {
    const aPrio = typePriority[a.type] || 999;
    const bPrio = typePriority[b.type] || 999;
    return aPrio - bPrio;
  });
});

// ============================================================================
// PHASE 4: GENERATE REPORT
// ============================================================================

phase('Report');

log('📝 Generating backlog report...');

const now = new Date().toISOString().split('T')[0];
const total = categorized.length;

// Build markdown report
let report = `# 🎯 Technical Backlog Report

**Generated:** ${now}
**Total Items:** ${total}
**Priority Breakdown:** Critical: ${bySeverity.critical.length} | High: ${bySeverity.high.length} | Medium: ${bySeverity.medium.length} | Low: ${bySeverity.low.length}

---

`;

// Helper to format items
function formatItems(items, emoji) {
  if (items.length === 0) return '';

  let section = '';
  items.forEach((item, idx) => {
    section += `### ${idx + 1}. ${item.description.substring(0, 80)}...

- **File:** \`${item.file}\`${item.line ? `:${item.line}` : ''}
- **Type:** ${item.type}
- **Marker:** \`${item.marker}\`
- **Effort:** ${item.effort}
${item.context ? `- **Context:**\n  \`\`\`\n  ${item.context}\n  \`\`\`` : ''}

---

`;
  });

  return section;
}

// Add each severity section
if (bySeverity.critical.length > 0) {
  report += `## 🔴 CRITICAL (Do Immediately)

${formatItems(bySeverity.critical, '🔴')}

`;
}

if (bySeverity.high.length > 0) {
  report += `## 🟠 HIGH PRIORITY (Do Soon)

${formatItems(bySeverity.high, '🟠')}

`;
}

if (bySeverity.medium.length > 0) {
  report += `## 🟡 MEDIUM PRIORITY (Plan For)

${formatItems(bySeverity.medium, '🟡')}

`;
}

if (bySeverity.low.length > 0) {
  report += `## 🟢 LOW PRIORITY (Nice to Have)

${formatItems(bySeverity.low, '🟢')}

`;
}

// Add metrics section
const effortCounts = {
  small: categorized.filter(i => i.effort === 'small').length,
  medium: categorized.filter(i => i.effort === 'medium').length,
  large: categorized.filter(i => i.effort === 'large').length
};

const typeCounts = {};
categorized.forEach(item => {
  typeCounts[item.type] = (typeCounts[item.type] || 0) + 1;
});

const mostCommonType = Object.entries(typeCounts).sort((a, b) => b[1] - a[1])[0];

report += `## 📈 Backlog Metrics

- **Total Technical Debt:** ${total} items
- **Effort Distribution:**
  - Small: ${effortCounts.small} items
  - Medium: ${effortCounts.medium} items
  - Large: ${effortCounts.large} items
- **Most Common Type:** ${mostCommonType ? mostCommonType[0] : 'N/A'} (${mostCommonType ? mostCommonType[1] : 0} items)
- **Top 3 Files with Issues:**
`;

// Find files with most issues
const fileCount = {};
categorized.forEach(item => {
  fileCount[item.file] = (fileCount[item.file] || 0) + 1;
});

const topFiles = Object.entries(fileCount)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 3);

topFiles.forEach(([file, count]) => {
  report += `  - ${file} (${count} items)\n`;
});

report += `

---

## 💡 Recommendations

`;

if (bySeverity.critical.length > 0) {
  report += `1. **🚨 URGENT:** Address ${bySeverity.critical.length} critical items immediately\n`;
}

if (bySeverity.high.length > 5) {
  report += `2. **⚠️ HIGH:** Allocate 30-40% of sprint to ${bySeverity.high.length} high-priority items\n`;
} else if (bySeverity.high.length > 0) {
  report += `2. **⚠️ HIGH:** ${bySeverity.high.length} high-priority items - tackle in next sprint\n`;
}

if (bySeverity.medium.length > 10) {
  report += `3. **📋 MEDIUM:** ${bySeverity.medium.length} medium items - create dedicated "debt reduction" sprint\n`;
} else if (bySeverity.medium.length > 0) {
  report += `3. **📋 MEDIUM:** Work on ${bySeverity.medium.length} medium items as time permits\n`;
}

if (bySeverity.low.length > 0) {
  report += `4. **✨ LOW:** ${bySeverity.low.length} nice-to-have items - good for new contributors\n`;
}

const totalEffort = effortCounts.small + (effortCounts.medium * 3) + (effortCounts.large * 10);
report += `5. **⏱️ ESTIMATED TOTAL EFFORT:** ~${totalEffort} story points\n`;

report += `

---

## 🎯 Next Steps

1. Review critical items in team standup
2. Assign owners to high-priority bugs
3. Schedule technical debt sprint
4. Update this report weekly
5. Celebrate when items are resolved! 🎉

---

**Generated by Backlog Agent** 🤖
*Run again anytime to update this report*
`;

log('✅ Backlog report generated successfully!');

// Return the report
return {
  success: true,
  report: report,
  summary: {
    total: total,
    critical: bySeverity.critical.length,
    high: bySeverity.high.length,
    medium: bySeverity.medium.length,
    low: bySeverity.low.length,
    mostCommonType: mostCommonType ? mostCommonType[0] : 'N/A'
  },
  items: categorized
};
