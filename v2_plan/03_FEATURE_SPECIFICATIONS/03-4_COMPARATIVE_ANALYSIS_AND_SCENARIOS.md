# Comparative Analysis & Scenario Modeling
## Decision Support Analytics

### Purpose
Enable investors to make data-driven decisions through side-by-side property comparisons, scenario modeling, and sensitivity analysis for acquisition, refinancing, and disposition decisions.

### User Goals
- **Acquisition Decisions**: Compare multiple properties to identify best opportunities
- **Refinancing Analysis**: Model impact of different loan terms and rates
- **Disposition Timing**: Optimize sale timing through scenario modeling
- **Portfolio Optimization**: Identify underperforming assets vs. opportunities

---

## Acquisition Comparison Interface

### Side-by-Side Property Comparison
**Purpose**: Standardized comparison of 2-4 potential acquisitions

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   Property A    │   Property B    │   Property C    │   Property D    │
│                 │                 │                 │                 │
│ 📍 123 Oak St   │ 📍 456 Pine Ave │ 📍 789 Elm Dr   │ 📍 321 Main St  │
│ $425,000       │ $380,000       │ $650,000       │ $520,000       │
│ SFR • 3/2       │ Duplex • 4/3    │ 4-plex • 8/4    │ Triplex • 6/3   │
│                 │                 │                 │                 │
│ Cap Rate: 7.2%  │ Cap Rate: 6.8%  │ Cap Rate: 6.5%  │ Cap Rate: 6.9%  │
│ CoC: 9.1%      │ CoC: 8.7%      │ CoC: -2.1% ❌   │ CoC: 8.3%      │
│ DSCR: 1.45x    │ DSCR: 1.38x    │ DSCR: 0.91x ❌  │ DSCR: 1.42x    │
│ Monthly CF: $850│ Monthly CF: $975│ Monthly CF: -$286│ Monthly CF: $780│
│                 │                 │                 │                 │
│ Score: 85/100 🥈│ Score: 92/100 🥇│ Score: 45/100 ❌│ Score: 78/100 🥉│
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Detailed Comparison Table
```
Financial Metrics Comparison:
                    Property A    Property B    Property C    Property D
Purchase Price      $425,000     $380,000     $650,000     $520,000
Down Payment (25%)  $106,250     $95,000      $162,500     $130,000
Total Cash Required $112,000     $101,000     $170,000     $137,000

Gross Monthly Income $2,550       $2,150       $4,400       $2,950
Operating Expenses  $765         $645         $1,521       $885
Net Operating Income $1,785       $1,505       $2,879       $2,065

Monthly Debt Service $935         $530         $3,165       $1,285
Monthly Cash Flow   $850         $975         -$286        $780

Annual Metrics:
Cap Rate           7.2%         6.8%         6.5%         6.9%
Cash-on-Cash       9.1%         8.7%         -2.1%        8.3%
DSCR               1.45x        1.38x        0.91x        1.42x

Risk Factors:
Property Age       1985         1978         1985         1992
Condition Rating   Good         Fair         Poor         Good
Location Score     8/10         9/10         7/10         8/10
Tenant Quality     Stable       New          Mixed        Stable
```

### Ranking & Scoring System
```
Deal Scoring Methodology (100-point scale):

Financial Performance (40 points):
├── Cap Rate vs. Target 6.5% (10 pts): A=9, B=8, C=6, D=8
├── Cash-on-Cash vs. Target 8% (15 pts): A=13, B=12, C=0, D=11  
├── DSCR vs. Minimum 1.25x (10 pts): A=8, B=7, C=0, D=8
└── Monthly Cash Flow (5 pts): A=4, B=5, C=0, D=4

Market Factors (25 points):
├── Location Desirability (15 pts): A=12, B=14, C=10, D=12
└── Property Condition (10 pts): A=8, B=6, C=4, D=8

Deal Structure (20 points):  
├── Financing Terms (10 pts): A=8, B=9, C=6, D=8
└── Purchase Price vs. Market (10 pts): A=8, B=9, C=7, D=7

Strategic Fit (15 points):
├── Portfolio Diversification (10 pts): A=8, B=10, C=6, D=7
└── Management Complexity (5 pts): A=5, B=4, C=2, D=4

Final Scores: A=85, B=92, C=45, D=78
Recommendation: Property B (456 Pine Ave)
```

---

## Scenario Modeling Interface

### Refinancing Scenario Analysis
**Purpose**: Model impact of refinancing existing properties

```
Refinancing Analysis - 789 Elm Drive:

Current Loan:
├── Balance: $465,280
├── Rate: 6.75%
├── Monthly Payment: $3,165
├── Years Remaining: 26.5
└── Total Interest Remaining: $571,970

Refinancing Options:
                    Option 1      Option 2      Option 3
New Rate            6.25%        6.00%        5.75%
New Term            30 years     25 years     30 years
Monthly Payment     $2,866       $2,997       $2,716
Monthly Savings     $299         $168         $449
Annual Savings      $3,588       $2,016       $5,388

Refinancing Costs:
├── Origination Fee (1%): $4,653
├── Appraisal: $500
├── Title/Closing: $1,200
├── Attorney: $800
└── Total Costs: $7,153

Break-Even Analysis:
Option 1: 24 months (Recommended ✅)
Option 2: 43 months  
Option 3: 16 months (if rate available)

Net Present Value (5 years):
Option 1: $10,437 savings vs. current
Option 2: $2,927 savings vs. current  
Option 3: $19,781 savings vs. current
```

### Disposition Timing Analysis
**Purpose**: Compare hold vs. sell scenarios at different timeframes

```
Hold vs. Sell Analysis - 789 Elm Drive:

Current Property Value: $725,000
Current Loan Balance: $465,280  
Current Equity: $259,720

Sell Now (Year 1):
├── Sale Price: $725,000
├── Selling Costs (6%): -$43,500
├── Loan Payoff: -$465,280
├── Net Proceeds: $216,220
├── After-Tax Proceeds: $189,593 (after depreciation recapture)
└── IRR Since Acquisition: 12.4%

Hold 3 Years (Year 4):
├── Projected Value (3% appreciation): $792,271
├── Loan Balance: $421,887
├── Selling Costs: -$47,536
├── Net Proceeds: $322,848
├── Cumulative Cash Flow: +$62,052
├── Total Return: $384,900
└── Projected IRR: 15.8%

Hold 5 Years (Year 6):
├── Projected Value: $841,329
├── Loan Balance: $385,721
├── Selling Costs: -$50,480
├── Net Proceeds: $405,128
├── Cumulative Cash Flow: +$104,220
├── Total Return: $509,348
└── Projected IRR: 17.2%

Recommendation: Hold 5+ years for optimal returns
Risk Factors: Interest rate changes, market appreciation assumptions
```

### Capital Improvement Scenario Modeling
**Purpose**: Analyze impact of major renovations or improvements

```
Value-Add Scenario Analysis - Unit Renovation:

Base Case (No Renovation):
├── Current Monthly Rent: $4,500
├── Current Property Value: $725,000
├── Monthly Cash Flow: $1,714
└── Cap Rate: 6.8%

Renovation Scenario:
├── Renovation Cost: $25,000
├── Expected Rent Increase: +$200/month (+$2,400/year)
├── Increased Property Value: $760,000 (+$35,000)
├── New Monthly Cash Flow: $1,914 (+$200)
└── New Cap Rate: 7.1%

Financial Analysis:
├── Cash-on-Cash Return on Renovation: 9.6% ($2,400/$25,000)
├── Total Return (rent + appreciation): $37,400
├── Simple Payback Period: 10.4 months
├── NPV (5 years, 8% discount): $16,840
└── IRR on Renovation Investment: 18.3%

Risk Assessment:
├── Market Rent Support: Confirmed via comps ✅
├── Renovation Cost Estimates: 20% contingency included ✅  
├── Tenant Retention Risk: Medium (potential vacancy)
└── Recommendation: Proceed with renovation ✅
```

---

## Sensitivity Analysis

### Key Variable Impact Analysis
**Purpose**: Identify which assumptions most impact returns

```
Sensitivity Analysis - IRR Impact:
Base Case IRR: 14.1%

Variable Changes (±10%):
                    -10%      -5%       Base      +5%       +10%
Rent Growth         12.8%     13.4%     14.1%     14.7%     15.4%
Vacancy Rate        15.2%     14.6%     14.1%     13.5%     12.9%
OpEx Growth         15.4%     14.7%     14.1%     13.4%     12.7%
Exit Cap Rate       16.8%     15.3%     14.1%     12.8%     11.3%
Appreciation Rate   11.2%     12.6%     14.1%     15.7%     17.4%

Most Sensitive Variables:
1. Exit Cap Rate (±2.7% IRR impact)
2. Appreciation Rate (±3.3% IRR impact)  
3. Rent Growth (±1.3% IRR impact)
4. Operating Expense Growth (±1.4% IRR impact)
5. Vacancy Rate (±1.2% IRR impact)
```

### Monte Carlo Simulation (Advanced)
```
Monte Carlo Analysis (1,000 iterations):
Variable Ranges:
├── Rent Growth: 2-6% annually (normal distribution, mean 4%)
├── Vacancy: 3-8% (normal distribution, mean 5%)
├── OpEx Growth: 2-5% annually (normal distribution, mean 3.5%)
├── Exit Cap Rate: 5.5-7.5% (uniform distribution)
└── Property Appreciation: 1-5% annually (normal distribution, mean 3%)

Results Distribution:
├── IRR Range: 8.2% to 22.1%
├── Mean IRR: 14.3%
├── Standard Deviation: 2.8%
├── 90% Confidence Interval: 9.7% to 18.9%
└── Probability of IRR >12%: 87%

Risk Assessment: Low-to-moderate risk investment
Recommendation: Proceed with acquisition ✅
```

---

## Portfolio Optimization Analysis

### Property Ranking Dashboard
**Purpose**: Rank all portfolio properties by performance metrics

```
Portfolio Property Ranking (12 properties):

By Cash-on-Cash Return:
Rank  Property           CoC Return  Monthly CF  Current Value  Actions
1     456 Pine Ave       11.2%      $1,425     $415,000      Hold 💚
2     123 Oak St         9.8%       $985       $475,000      Hold 💚
3     789 Elm Dr         8.2%       $1,714     $725,000      Refi 🟡
4     654 Cedar Ln       7.1%       $892       $385,000      Market rent increase 🟡
5     321 Main St        6.8%       $1,205     $565,000      Hold 💚
...
12    987 Birch Dr       2.3%       $245       $325,000      Consider sale 🔴

By Cap Rate:
Rank  Property           Cap Rate   NOI        Value         Actions
1     789 Elm Dr         7.4%      $53,580    $725,000      Hold 💚
2     123 Oak St         6.9%      $32,670    $475,000      Hold 💚
3     456 Pine Ave       6.7%      $27,805    $415,000      Hold 💚
...
```

### Disposition Analysis
```
Properties to Consider Selling:

987 Birch Dr (Rank #12):
├── Performance Issues: Consistent negative cash flow, high vacancy
├── Market Conditions: Strong buyer demand in area
├── Disposition Benefits: Redeploy capital to higher-performing assets
├── Tax Implications: Minimal depreciation recapture
└── Recommendation: List for sale within 60 days

654 Cedar Ln (Rank #4):
├── Performance: Below portfolio average but improving
├── Optimization Potential: Rent increases could improve returns
├── Market Conditions: Hold market, limited buyer premium
└── Recommendation: Implement rent increases, reassess in 6 months
```

---

## Visual Analytics

### Waterfall Charts
**Purpose**: Show cash flow breakdowns and changes over time

```
Monthly Cash Flow Waterfall - 789 Elm Dr:
Starting Point: $0
+ Gross Rental Income: +$4,500
+ Other Income: +$245
- Property Tax: -$542
- Insurance: -$200  
- Property Management: -$380
- Maintenance: -$290
- Other OpEx: -$220
= Net Operating Income: $3,113
- Debt Service: -$3,165
= Net Cash Flow: -$52 (break-even property)

Improvement Opportunities:
+ Rent Increases: +$200
+ Expense Reductions: +$100
+ Refinancing Savings: +$299
= Projected Cash Flow: +$547
```

### Risk-Return Scatter Plot
**Purpose**: Portfolio positioning analysis

```
Risk-Return Matrix:
X-Axis: Standard Deviation of Returns (Risk)
Y-Axis: Average Annual Return
Bubble Size: Property equity value

Quadrants:
├── High Return, Low Risk (Target zone): Properties 1, 2, 5
├── High Return, High Risk (Growth zone): Properties 3, 7
├── Low Return, Low Risk (Bond-like): Properties 4, 6, 8
└── Low Return, High Risk (Problem zone): Properties 9, 12

Portfolio Optimization Recommendations:
- Reduce exposure to low return/high risk properties
- Increase allocation to high return/low risk opportunities
- Consider risk tolerance in new acquisitions
```

---

## Export and Integration

### Scenario Report Generation
- **Executive Summary**: Key findings and recommendations
- **Detailed Analysis**: Complete scenario modeling results
- **Sensitivity Analysis**: Variable impact charts and tables
- **Appendices**: Assumptions, calculations, supporting data

### Decision Support Tools
- **Investment Committee Reports**: Professional presentations for partners/investors
- **Lender Packages**: Refinancing analysis for loan applications  
- **Tax Planning**: Disposition timing analysis for tax optimization
- **Insurance Analysis**: Property replacement cost and coverage optimization

### API Integration Points
- **Market Data**: Real-time interest rates, cap rates, market rents
- **Valuation Models**: Automated property value updates
- **Economic Indicators**: Inflation, employment, demographic trends
- **Comparable Sales**: Recent transactions for disposition analysis