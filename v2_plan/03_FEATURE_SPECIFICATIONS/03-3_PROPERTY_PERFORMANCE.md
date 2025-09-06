# Property Performance Tracking
## Individual Asset Management & Analytics

### Purpose
Provide detailed performance tracking and analysis for individual properties, enabling investors to monitor actual vs. projected performance, identify optimization opportunities, and make informed asset management decisions.

### User Goals
- **Performance Monitoring**: Track actual income/expenses vs. projections
- **Variance Analysis**: Identify and investigate significant performance deviations  
- **Trend Analysis**: Understand property performance patterns over time
- **Decision Support**: Data-driven insights for refinancing, renovation, or disposition decisions

---

## Property Performance Dashboard

### Property Header Card
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 🏠 789 Elm Drive, Charlotte, NC 28205                                  │
│ 4-Unit Multi-Family • Acquired 11/2020 • $650,000                     │
│                                                                         │
│ Current Value: $725,000 ↑11.5%  |  Equity: $315,000  |  LTV: 56.5%   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Performance Indicators Row
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Monthly NOI     │ Monthly CF      │ Cap Rate        │ DSCR           │
│ $2,879         │ $1,714         │ 6.8%           │ 1.52x          │
│ ↑ 3% vs Budget │ ↑ 8% vs Budget │ ↑ 0.3% vs Acq  │ Healthy        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Occupancy & Lease Status
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Unit Occupancy: 100% (4 of 4 units occupied)                          │
│                                                                         │
│ Unit A: $1,150/mo • Lease expires 03/2024 • 2BR/1BA                   │
│ Unit B: $1,100/mo • Lease expires 07/2024 • 2BR/1BA                   │  
│ Unit C: $1,050/mo • Month-to-month • 1BR/1BA ⚠️                       │
│ Unit D: $1,200/mo • Lease expires 12/2024 • 2BR/1.5BA                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Time-Based Performance Analysis  

### Monthly Performance Chart
**Purpose**: Visual trend analysis of key metrics over 24-month period

```
Line Chart - Multiple Series:
- Gross Income (blue line)
- Operating Expenses (red line)  
- Net Operating Income (green line)
- Cash Flow After Debt Service (purple line)

X-Axis: Monthly periods
Y-Axis: Dollar amounts
Interactive: Hover for exact values, click for monthly detail
```

### Quarterly Performance Summary
```
Performance Trend (Last 4 Quarters):
                Q4 2023   Q1 2024   Q2 2024   Q3 2024   Trend
Gross Income    $12,750   $13,100   $13,400   $13,500   ↗️ +5.9%
Operating Exp   $4,200    $4,580    $4,100    $4,350    ↗️ +3.6%
NOI            $8,550    $8,520    $9,300    $9,150    ↗️ +7.0%
Cash Flow      $4,950    $4,920    $5,700    $5,550    ↗️ +12.1%
Occupancy      87.5%     100%      100%      100%      ↗️ +12.5%
```

### Annual Comparison Table
```
Year-over-Year Analysis:
Metric                2022 Actual  2023 Actual  2024 Budget  2024 YTD    Var vs Budget
Gross Income         $50,400      $52,200      $54,000      $40,000     +3.7%
Vacancy Loss         $2,520       $1,566       $2,700       $1,200      ↗️ Better
Effective Income     $47,880      $50,634      $51,300      $38,800     +0.9%
Operating Expenses   $16,200      $17,230      $17,800      $13,030     ↗️ -2.1%
NOI                 $31,680      $33,404      $33,500      $25,770     +2.8%
Debt Service        $19,800      $19,800      $19,800      $14,850     On target
Cash Flow           $11,880      $13,604      $13,700      $10,920     +4.2%
```

---

## Income Analysis

### Revenue Breakdown
```
Monthly Income Sources (Current):
├── Base Rent: $4,500 (4 units avg $1,125)
├── Pet Fees: $100 (2 pets × $50/mo)
├── Laundry Income: $120 (shared laundry)
├── Late Fees: $25 (occasional)
└── Total Gross: $4,745/month

Rent Roll Details:
Unit A: $1,150 • Tenant: Johnson • Lease: 9/2022-3/2024
Unit B: $1,100 • Tenant: Smith • Lease: 1/2023-7/2024  
Unit C: $1,050 • Tenant: Williams • Month-to-month since 5/2024 ⚠️
Unit D: $1,200 • Tenant: Davis • Lease: 6/2023-12/2024
```

### Rent Analysis
```
Market Rent Comparison:
Unit Type    Current Rent  Market Rent  Variance    Opportunity
2BR/1BA      $1,125       $1,175       -$50       +$100/mo potential
1BR/1BA      $1,050       $1,125       -$75       +$75/mo at renewal
2BR/1.5BA    $1,200       $1,225       -$25       +$25/mo at renewal

Total Monthly Opportunity: +$200/month (+$2,400/year)
```

### Vacancy Analysis
```
Vacancy History (Last 24 Months):
├── Unit A: 0 days vacant (excellent tenant retention)
├── Unit B: 15 days vacant (between tenants, 1/2023)
├── Unit C: 60 days vacant (renovation period, 4-5/2024)  
├── Unit D: 30 days vacant (tenant default, 5/2023)
└── Total: 105 days / 2,920 possible = 3.6% vacancy rate

Benchmark Comparison:
- Property Vacancy: 3.6%
- Market Average: 5.2% ↗️ Better
- Portfolio Average: 4.1% ↗️ Better
```

---

## Expense Analysis

### Operating Expense Breakdown
```
Monthly Operating Expenses (YTD Average):
├── Property Tax: $542 ($6,500 annually)
├── Insurance: $200 ($2,400 annually)  
├── Property Management: $380 (8% of gross income)
├── Maintenance & Repairs: $290 (varies monthly)
├── Utilities (Common Areas): $100 (hallway lighting, etc.)
├── Landscaping: $75 (quarterly service)
├── Other/Miscellaneous: $45
└── Total Monthly OpEx: $1,632

Expense Ratios:
- OpEx as % of Gross Income: 34.4%
- OpEx as % of NOI: 52.7%
- Benchmark Comparison: 38% (market avg) ↗️ Better efficiency
```

### Maintenance Tracking
```
Maintenance Reserve Analysis:
├── Reserve Target: $100/unit/month = $400/month
├── Current Reserve Balance: $2,450
├── YTD Maintenance Spending: $2,180
├── Reserve Health: 13.5 months at current burn rate ✅

Recent Major Expenses:
- 08/2024: Unit C HVAC repair - $850
- 06/2024: Exterior painting - $2,200  
- 04/2024: Unit B flooring replacement - $1,200
- 02/2024: Roof repairs - $1,850
```

### Capital Expenditures Tracking
```
CapEx Planning & History:
Planned (Next 12 Months):
├── Water heater replacements (Units A&D): $2,500 est.
├── Kitchen updates (Unit B): $4,000 est.  
├── Parking lot resurfacing: $3,500 est.
└── Total Planned CapEx: $10,000

Historical (Last 24 Months):
├── Exterior painting: $2,200 (06/2024)
├── Unit C renovation: $8,500 (04-05/2024)
├── HVAC system upgrade: $6,200 (11/2023)  
└── Total Historical: $16,900
```

---

## Financial Performance Metrics

### Return Analysis
```
Investment Returns (As of Current Month):
├── Total Cash Invested: $162,500 (down payment + closing costs)
├── Current Equity Position: $315,000
├── Cumulative Cash Flow: $45,200 (since acquisition)
├── Appreciation Gain: $75,000 (current value - purchase price)
└── Total Return: $120,200 (cash flow + appreciation)

Annualized Returns:
├── Cash-on-Cash Return: 8.2% (trailing 12 months)
├── Total Return on Equity: 12.8% (including appreciation)
├── IRR (since acquisition): 14.1%
└── Cap Rate (current): 6.8%
```

### Loan Performance  
```
Loan Analysis:
├── Original Loan Amount: $487,500 (75% LTV)
├── Current Balance: $465,280
├── Principal Paydown: $22,220 (since origination)
├── Current LTV: 64.2% (improved from 75%)
└── Monthly P&I Payment: $3,165

Refinancing Analysis:
Current Loan: 6.75% rate, $3,165/month
Market Rate: 6.25% (est), $2,995/month potential
Savings: $170/month ($2,040/year)
Break-even: 18 months (accounting for refi costs)
Recommendation: ⚠️ Monitor rates, refi at 6.0% or below
```

---

## Performance Alerts & Recommendations

### Automated Performance Alerts
```
Active Alerts for 789 Elm Drive:
🟡 Unit C month-to-month lease (convert to fixed term)
🟡 Rent below market on Units A&B (increase at renewal)  
🟡 Water heater age >12 years Units A&D (plan replacement)
🔵 Property performing above budget (+4.2% cash flow YTD)
```

### Optimization Recommendations
```
Performance Improvement Opportunities:

1. Revenue Enhancement:
   ├── Increase Unit A rent to $1,200 at 3/2024 renewal (+$600/year)
   ├── Increase Unit B rent to $1,150 at 7/2024 renewal (+$600/year)
   ├── Convert Unit C to 12-month lease with $1,125 rent (+$900/year)
   └── Potential Annual Increase: +$2,100

2. Expense Optimization:  
   ├── Property management negotiation (8% → 7.5%) (-$180/year)
   ├── Insurance shopping (potential 10% savings) (-$240/year)
   ├── Energy efficiency improvements (LED, programmable thermostats) (-$300/year)
   └── Potential Annual Savings: -$720

3. Value-Add Opportunities:
   ├── Laundry room upgrade (newer machines) (+$50/month income)
   ├── Storage unit additions (+$25/unit/month) (+$1,200/year)
   └── Parking space designation/rental (+$25/space/month) (+$600/year)

Total Annual Impact: +$3,230 (+$269/month cash flow improvement)
```

---

## Comparative Analysis

### Property vs. Portfolio Benchmarking
```
Performance vs. Portfolio Average:
Metric              789 Elm Dr    Portfolio Avg    Variance
Cap Rate            6.8%         6.9%             -0.1% ↔️
Cash-on-Cash        8.2%         8.1%             +0.1% ↗️
Occupancy Rate      100%         95.3%            +4.7% ↗️
OpEx Ratio          34.4%        36.2%            -1.8% ↗️
Maintenance/Unit    $73/mo       $85/mo           -$12 ↗️
```

### Market Comparison
```
789 Elm Dr vs. Market Comparables:
Property Type: 4-Unit Multi-Family in Charlotte, NC

Metric              Property     Market Median    Quartile Rank
Rent/Unit          $1,186       $1,150           Q3 (above avg)
Cap Rate           6.8%         6.5%             Q3 (above avg)  
OpEx Ratio         34.4%        38%              Q1 (top quartile)
Vacancy Rate       3.6%         5.2%             Q1 (top quartile)
```

---

## Export and Reporting

### Property Performance Report
- **Executive Summary**: Key metrics and performance highlights
- **Financial Analysis**: Detailed income/expense breakdown
- **Market Position**: Comparative analysis vs. market and portfolio
- **Recommendations**: Actionable improvement opportunities
- **Appendix**: Supporting charts, transaction details, lease information

### Scenario Analysis Tools
- **Refinancing Impact**: Model different interest rates and terms
- **Rent Increase Scenarios**: Project impact of market rent adjustments
- **CapEx Planning**: Model major renovation or improvement projects
- **Disposition Analysis**: Compare hold vs. sell scenarios at different cap rates

### Data Export Options
- **Excel Export**: Raw transaction and performance data
- **CSV Export**: For integration with accounting systems
- **PDF Reports**: Professional reports for stakeholders
- **API Access**: For integration with external analytics tools