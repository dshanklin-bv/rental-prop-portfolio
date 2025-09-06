# Alerts & Task Management
## Proactive Portfolio Monitoring System

### Purpose
Provide investors with proactive notifications and task management to prevent missed opportunities, avoid compliance issues, and optimize portfolio performance through timely action items.

### User Goals
- **Proactive Management**: Early warning system for critical dates and thresholds
- **Risk Mitigation**: Avoid DSCR violations, vacancy issues, and missed renewals
- **Opportunity Identification**: Alert on rent increase opportunities and market changes
- **Task Organization**: Centralized action items with priority-based workflow

---

## Alert Categories & Triggers

### Critical Alerts (🔴 Immediate Action Required)
**Response Time**: Within 24-48 hours

#### Financial Performance Alerts
```
DSCR Below Threshold:
├── Trigger: Monthly DSCR drops below 1.20x
├── Property: 789 Elm Drive - DSCR: 1.15x
├── Impact: Loan covenant violation risk
├── Action Required: Review expenses, consider rent increases
└── Due Date: Immediate

Negative Cash Flow:
├── Trigger: Property shows negative cash flow for 2+ consecutive months
├── Property: 321 Main Street - Cash Flow: -$450/month
├── Impact: Personal financial drain
├── Action Required: Increase rents or reduce expenses
└── Due Date: Within 30 days
```

#### Lease Management Alerts
```
Lease Expiring Soon:
├── Trigger: Lease expires within 30 days, no renewal executed
├── Property: 456 Pine Ave, Unit A
├── Tenant: Johnson Family
├── Expiration: March 15, 2024 (22 days)
├── Action Required: Contact tenant for renewal negotiation
└── Risk: Vacancy and re-leasing costs

Month-to-Month Conversion:
├── Trigger: Fixed-term lease converted to month-to-month >60 days ago
├── Property: 789 Elm Drive, Unit C
├── Tenant: Williams
├── Status: Month-to-month since May 2024
├── Action Required: Convert to fixed-term lease with market rent
└── Opportunity: Rent increase + lease stability
```

#### Loan & Financial Alerts
```
Loan Maturity Approaching:
├── Trigger: Balloon payment due within 180 days
├── Property: 123 Oak Street
├── Maturity Date: September 15, 2024 (120 days)
├── Balance: $285,000
├── Action Required: Begin refinancing process
└── Risk: Forced sale if financing unavailable

Interest Rate Spike:
├── Trigger: Variable rate increased >0.5% from baseline
├── Property: 654 Cedar Lane (ARM loan)
├── Previous Rate: 5.75%, New Rate: 6.45%
├── Impact: +$185/month debt service
├── Action Required: Consider fixed-rate refinancing
└── Due Date: Within 60 days (before next adjustment)
```

### High Priority Alerts (🟡 Action Within 7-14 Days)

#### Property Management Alerts
```
High Vacancy Rate:
├── Trigger: Property vacancy >10% for 60+ days
├── Property: 987 Birch Drive
├── Vacant Units: 2 of 6 units (33% vacancy)
├── Duration: 75 days average vacancy
├── Action Required: Review pricing, marketing, property condition
└── Impact: Significant NOI reduction

Maintenance Reserve Low:
├── Trigger: Reserve balance <3 months of typical spending
├── Property: 456 Pine Ave  
├── Current Balance: $850
├── Monthly Spend Average: $320
├── Months Remaining: 2.7 months
├── Action Required: Increase reserve funding or defer non-critical items
└── Risk: Cash flow impact from large unexpected repairs
```

#### Market Opportunity Alerts
```
Below-Market Rent:
├── Trigger: Unit rent >10% below market comparables
├── Property: 789 Elm Drive, Unit B
├── Current Rent: $1,100
├── Market Rent: $1,225 (11% below market)
├── Annual Opportunity: $1,500
├── Action Required: Increase rent at lease renewal (July 2024)
└── Timing: Begin negotiation 60 days before renewal
```

### Medium Priority Alerts (🔵 Action Within 30-60 Days)

#### Administrative Alerts
```
Insurance Renewal Due:
├── Trigger: Policy expires within 60 days
├── Property: 123 Oak Street
├── Current Premium: $2,400/year
├── Renewal Date: May 15, 2024
├── Action Required: Shop for competitive quotes
└── Opportunity: Potential 10-15% savings with market shopping

Property Tax Assessment:
├── Trigger: New assessment >10% increase from prior year
├── Property: 789 Elm Drive
├── Prior Assessment: $650,000
├── New Assessment: $725,000 (+11.5%)
├── Tax Increase: +$2,250/year
├── Action Required: Consider appeal or budget adjustment
└── Due Date: Appeal deadline April 30, 2024
```

#### Performance Monitoring
```
Expense Variance:
├── Trigger: Monthly expenses >20% over budget for 2+ months
├── Property: 456 Pine Ave
├── Budget: $1,200/month, Actual: $1,485/month (+24%)
├── Primary Variance: Maintenance & repairs (+$285/month)
├── Action Required: Investigate recurring issues
└── Impact: -$3,420/year vs. budget
```

### Low Priority Alerts (🔷 Monitoring Items)

#### Optimization Opportunities
```
Rent Increase Opportunity:
├── Trigger: No rent increase in 18+ months, market rents rising
├── Property: 654 Cedar Lane
├── Last Increase: January 2023 (20 months ago)
├── Current Rent: $950, Market Rent: $1,025
├── Opportunity: $75/month (+$900/year)
├── Action Required: Plan increase at next renewal opportunity
└── Timing: Monitor lease renewal dates

Energy Efficiency Opportunity:
├── Trigger: Utility costs >20% above similar properties
├── Property: 321 Main Street
├── Monthly Utilities: $185 vs. $145 market average
├── Potential Savings: $40/month ($480/year)
├── Action Required: Energy audit and efficiency improvements
└── ROI Analysis: LED lighting, thermostat upgrades
```

---

## Alert Dashboard Interface

### Alert Summary Widget
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Portfolio Alerts Summary                               Last Updated: Now │
│                                                                         │
│ 🔴 CRITICAL: 3 alerts requiring immediate action                       │
│ 🟡 HIGH: 5 alerts requiring action within 2 weeks                     │
│ 🔵 MEDIUM: 8 alerts for next 30-60 days                              │
│ 🔷 LOW: 12 monitoring items and opportunities                         │
│                                                                         │
│ [ View All Alerts ] [ Mark as Read ] [ Export Report ]                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Alert Detail View
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🔴 CRITICAL ALERT                                                      │
│ DSCR Below Threshold - 789 Elm Drive                                   │
│                                                                         │
│ Alert Details:                                                          │
│ ├── Property: 789 Elm Drive, Charlotte, NC                            │
│ ├── Issue: Debt Service Coverage Ratio dropped to 1.15x               │
│ ├── Threshold: 1.20x minimum                                          │
│ ├── Triggered: March 1, 2024                                          │
│ ├── Current Status: Unresolved                                        │
│ └── Days Active: 5 days                                               │
│                                                                         │
│ Financial Impact:                                                       │
│ ├── Monthly NOI: $2,879                                               │
│ ├── Monthly Debt Service: $3,165                                      │
│ ├── Current DSCR: 1.15x                                              │
│ └── Required NOI for 1.20x: $3,198 (+$319/month)                     │
│                                                                         │
│ Recommended Actions:                                                    │
│ □ Review and reduce operating expenses                                  │
│ □ Increase rents on below-market units                                 │
│ □ Consider refinancing to lower debt service                          │
│ □ Evaluate property disposition if improvements not feasible           │
│                                                                         │
│ [ Create Task ] [ Mark Resolved ] [ Snooze Alert ] [ View Property ]   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Task Management System

### Task Creation & Assignment
```
Task Creation (Auto-generated from Alert):
┌─────────────────────────────────────────────────────────────────────────┐
│ Create New Task                                                         │
│                                                                         │
│ Title: [Increase rent at Unit B renewal - 789 Elm Dr]                  │
│ Description: [Market rent analysis shows $125/month opportunity]        │
│ Priority: [High ▼]                                                     │
│ Due Date: [May 15, 2024] (60 days before lease expiration)            │
│ Property: [789 Elm Drive ▼]                                           │
│ Category: [Revenue Management ▼]                                       │
│                                                                         │
│ Subtasks:                                                              │
│ □ Research market comparable rents                                      │
│ □ Prepare rent increase notice template                                 │
│ □ Schedule tenant meeting 60 days before expiration                    │
│ □ Document tenant response and negotiate if needed                      │
│ □ Execute new lease agreement or notice to vacate                      │
│                                                                         │
│ [ Save Task ] [ Cancel ]                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### Task Dashboard
```
Active Tasks (15 total):

🔴 HIGH PRIORITY (Due within 7 days):
├── Negotiate lease renewal - 456 Pine Ave Unit A (Due: Mar 10)
├── Submit refinance application - 123 Oak St (Due: Mar 12) 
└── Address DSCR violation - 789 Elm Dr (Due: Mar 8) ⚠️ Overdue

🟡 MEDIUM PRIORITY (Due within 30 days):
├── Shop insurance quotes - All properties (Due: Mar 25)
├── Schedule property inspections - Quarterly review (Due: Mar 30)
├── Review property tax assessments (Due: Apr 1)
└── Update rent roll documentation (Due: Mar 20)

🔵 LOW PRIORITY (Due within 90 days):
├── Plan capital improvements - 654 Cedar Lane (Due: May 15)
├── Research energy efficiency upgrades (Due: Apr 30)
└── Update emergency contact information (Due: June 1)

🔷 SOMEDAY/MAYBE:
├── Investigate additional properties in Charlotte market
├── Research property management software options
└── Plan portfolio expansion strategy
```

### Task Categories
```
Task Categories & Templates:

Revenue Management:
├── Rent increase negotiations
├── Lease renewal processes  
├── Market rent analysis
└── New tenant screening

Property Maintenance:
├── Routine inspections
├── Preventive maintenance scheduling
├── Capital improvement planning
└── Emergency repair responses

Financial Management:
├── Loan refinancing processes
├── Insurance renewals and shopping
├── Tax planning and appeals
└── Budget variance investigations

Compliance & Legal:
├── Lease agreement updates
├── Safety inspection requirements
├── Local ordinance compliance
└── Eviction processes (if needed)

Strategic Planning:
├── Property disposition analysis
├── Acquisition opportunity evaluation
├── Portfolio optimization reviews
└── Market research projects
```

---

## Notification System

### Notification Channels
```
Notification Preferences by Alert Type:

Critical Alerts:
├── In-App: Immediate banner notification
├── Email: Within 5 minutes
├── SMS: Within 15 minutes (opt-in)
└── Push Notification: Mobile app (if available)

High Priority Alerts:
├── In-App: Notification badge
├── Email: Daily digest at 8:00 AM
└── Weekly Summary: Email on Sundays

Medium/Low Priority:
├── In-App: Notification center only
├── Email: Weekly digest on Sundays
└── Monthly Report: Comprehensive summary
```

### Notification Templates
```
EMAIL TEMPLATE - Critical Alert:
Subject: 🔴 URGENT: DSCR Below Threshold - 789 Elm Drive

[Property Name], your property at 789 Elm Drive has triggered a critical alert:

ISSUE: Debt Service Coverage Ratio has dropped to 1.15x, below your 1.20x threshold.

FINANCIAL IMPACT:
- Current monthly NOI: $2,879
- Monthly debt service: $3,165  
- Shortfall: $286/month to reach target DSCR

RECOMMENDED ACTIONS:
1. Review operating expenses for reduction opportunities
2. Evaluate rent increase potential on below-market units
3. Consider refinancing to reduce debt service
4. Log into your dashboard for detailed analysis

View Property Details: [Link]
Mark as Resolved: [Link]

This alert will continue until marked resolved or the DSCR returns above 1.20x.
```

### Alert Escalation Rules
```
Escalation Timeline:

Critical Alerts:
├── Day 1: Initial notification (all channels)
├── Day 2: Reminder if unread
├── Day 3: Escalation notice  
├── Day 7: Weekly summary includes unresolved critical items
└── Day 30: Monthly review flags persistent critical alerts

High Priority Alerts:
├── Week 1: Initial notification
├── Week 2: Reminder if unread
└── Monthly: Include in summary report

Snooze Options:
├── 1 day (for immediate items)
├── 1 week (for items requiring research)
├── 1 month (for seasonal or long-term items)
└── Until specific date (for calendar-dependent items)
```

---

## Performance Analytics

### Alert Response Metrics
```
Alert Management Performance (Last 90 Days):

Response Times:
├── Critical Alerts: Avg 4.2 hours (target: <24 hours) ✅
├── High Priority: Avg 2.1 days (target: <7 days) ✅  
├── Medium Priority: Avg 12.5 days (target: <30 days) ✅
└── Overall Response Rate: 94% within target timeframes

Alert Resolution:
├── Total Alerts Generated: 47
├── Resolved: 41 (87%)
├── Active: 6 (13%)
├── Average Time to Resolution: 8.3 days
└── False Positive Rate: 2.1% (1 of 47)

Most Common Alert Types:
1. Lease renewals (23% of alerts)
2. Below-market rents (19% of alerts)
3. Maintenance reserves low (15% of alerts)
4. Insurance renewals (13% of alerts)
5. Expense variances (11% of alerts)
```

### Proactive Management Score
```
Portfolio Health Score: 87/100

Score Components:
├── Alert Response Time (25 pts): 23/25 ✅
├── Preventive Actions Taken (20 pts): 18/20 ✅
├── Financial Threshold Compliance (25 pts): 20/25 ⚠️
├── Lease Management Efficiency (15 pts): 14/15 ✅  
├── Maintenance Planning (10 pts): 9/10 ✅
└── Strategic Planning Activity (5 pts): 3/5 ✅

Improvement Areas:
- Address DSCR violations more quickly
- Implement more proactive refinancing strategies
- Increase frequency of market rent reviews

Benchmark: Portfolio management score above 85 indicates excellent proactive management
```

---

## Integration & Automation

### Calendar Integration
- Sync critical dates to Google Calendar/Outlook
- Automatic reminders for lease expirations, loan maturities
- Task due dates integrated with personal calendar systems

### Property Management Integration (Future)
- Import lease expiration dates and rental payment data
- Automated vacancy alerts from property management systems
- Maintenance request escalation for recurring issues

### Market Data Integration (Future)  
- Automated market rent analysis updates
- Interest rate change alerts for refinancing opportunities
- Comparable sales alerts for valuation updates

### Reporting Integration
- Alert summary inclusion in monthly/quarterly reports
- Task completion metrics in performance dashboards
- Trend analysis of alert patterns for portfolio optimization