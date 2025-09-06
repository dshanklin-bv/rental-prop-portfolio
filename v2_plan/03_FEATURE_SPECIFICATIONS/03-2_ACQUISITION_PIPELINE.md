# Acquisition Pipeline
## Deal Flow Management System

### Purpose
Enable investors to systematically track, evaluate, and compare potential property acquisitions from initial sourcing through closing, ensuring no opportunities are missed and decisions are data-driven.

### User Goals  
- **Deal Organization**: Track multiple opportunities through standardized stages
- **Comparative Analysis**: Side-by-side evaluation of competing properties
- **Decision Support**: Quantitative analysis to support offer decisions
- **Progress Tracking**: Monitor deal progress and key milestone dates

---

## Pipeline Stage Definitions

### Stage Progression Flow
```
Sourced → Initial Review → Underwriting → LOI Submitted → Under Contract → Due Diligence → Closing → [Closed/Rejected]
```

### Stage Details

#### 1. Sourced  
**Purpose**: Capture basic deal information
**Entry Criteria**: Property address + asking price
**Key Activities**: Initial property identification, basic market research
**Typical Duration**: 1-7 days
**Required Information**: Address, asking price, property type, lead source

#### 2. Initial Review
**Purpose**: Quick feasibility assessment  
**Entry Criteria**: Basic income/expense estimates completed
**Key Activities**: Rent comps, expense estimates, initial cash flow calculation
**Typical Duration**: 1-3 days
**Required Information**: Estimated rents, property taxes, insurance estimates

#### 3. Underwriting
**Purpose**: Detailed financial analysis
**Entry Criteria**: Detailed income/expense modeling completed
**Key Activities**: Full pro forma, sensitivity analysis, financing scenarios
**Typical Duration**: 3-7 days  
**Required Information**: Detailed rent roll, operating expense breakdown, financing terms

#### 4. LOI Submitted
**Purpose**: Initial offer made
**Entry Criteria**: Letter of Intent submitted to seller
**Key Activities**: Negotiation, follow-up with listing agent
**Typical Duration**: 1-14 days
**Required Information**: Offer price, key terms, contingencies

#### 5. Under Contract
**Purpose**: Purchase agreement executed
**Entry Criteria**: Signed purchase agreement
**Key Activities**: Loan application, inspection scheduling, due diligence planning
**Typical Duration**: 30-45 days
**Required Information**: Contract price, key dates (inspection, financing, closing)

#### 6. Due Diligence  
**Purpose**: Property and financial verification
**Entry Criteria**: Inspection period active
**Key Activities**: Physical inspection, document review, financial verification
**Typical Duration**: 7-21 days (within contract period)
**Required Information**: Inspection results, actual rent rolls, expense documentation

#### 7. Closing
**Purpose**: Final transaction preparation
**Entry Criteria**: Due diligence complete, financing approved
**Key Activities**: Final loan approval, title work, closing preparation
**Typical Duration**: 5-10 days
**Required Information**: Clear title, loan commitment, closing date scheduled

---

## Pipeline Dashboard View

### Deal Cards Layout
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│    SOURCED      │ INITIAL REVIEW  │ UNDERWRITING    │ LOI SUBMITTED   │
│                 │                 │                 │                 │
│ 📍 123 Oak St   │ 📍 456 Pine Ave │ 📍 789 Elm Dr   │ 📍 321 Main St  │
│ $425K asking    │ $380K asking    │ $650K asking    │ $520K asking    │
│ SFR • 3/2       │ Duplex • 4/3    │ 4-plex • 8/4    │ Triplex • 6/3   │
│ Est. 7.2% cap   │ Est. 6.8% cap   │ Est. 6.5% cap   │ Offered: $485K  │
│ Added: 2 days   │ Added: 5 days   │ Added: 8 days   │ LOI: 3 days ago │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Deal Card Information Hierarchy

**Top Line**: Property address (clickable to detail view)
**Second Line**: Asking price (or offer price if LOI submitted)  
**Third Line**: Property type • beds/baths summary
**Fourth Line**: Key metric (cap rate, cash flow, or deal status)
**Bottom Line**: Stage timing (days in stage or last activity)

### Visual Indicators
- **Color Coding**: Green (progressing well), Yellow (attention needed), Red (overdue/stalled)
- **Progress Bars**: Visual indicator of days remaining in stage  
- **Alert Icons**: 🔔 for approaching deadlines, ⚠️ for issues requiring attention

---

## Deal Detail View

### Deal Information Tabs

#### Basic Information Tab
```
Property Details:
├── Address: 789 Elm Drive, Charlotte, NC 28205
├── Property Type: 4-unit Multi-family
├── Year Built: 1985
├── Total Sq Ft: 3,200
├── Lot Size: 0.25 acres
└── Asking Price: $650,000

Deal Progress:
├── Current Stage: Underwriting
├── Days in Stage: 4 of 7 target
├── Next Milestone: Complete pro forma analysis
└── Source: MLS listing via agent referral

Key Contacts:
├── Listing Agent: Jane Smith, ABC Realty (555-1234)
├── Buyer Agent: John Doe, XYZ Realty (555-5678)  
├── Lender: First National Bank (555-9012)
└── Inspector: Mike's Inspections (555-3456)
```

#### Financial Analysis Tab

**Quick Metrics Card**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Estimated Cap   │ Cash-on-Cash    │ Est. Monthly CF │ Total Cash Req  │
│ 6.5%           │ 8.2%            │ $1,850         │ $162,500        │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**Pro Forma Analysis**
```
Annual Income:
├── Gross Rental Income: $52,800 (4 units × $1,100/mo avg)
├── Vacancy Loss (5%): -$2,640  
├── Other Income: $1,200 (laundry, pet fees)
└── Effective Gross Income: $51,360

Operating Expenses:
├── Property Tax: $6,500
├── Insurance: $2,400
├── Property Management (8%): $4,109
├── Maintenance Reserve: $1,800
├── Utilities (common): $1,200
├── Other Expenses: $800
└── Total OpEx: $16,809

Net Operating Income: $34,551

Financing:
├── Loan Amount (75% LTV): $487,500
├── Interest Rate: 6.75%
├── Term: 30 years  
├── Monthly P&I: $3,165
└── Annual Debt Service: $37,980

Cash Flow:
├── Net Operating Income: $34,551
├── Annual Debt Service: -$37,980
└── Annual Cash Flow: -$3,429 ⚠️
```

#### Comparative Analysis Tab
**Purpose**: Side-by-side comparison with other pipeline deals and portfolio properties

```
Property Comparison:
                   789 Elm Dr    456 Pine Ave   Portfolio Avg
Purchase Price     $650,000      $380,000       $485,000
Cap Rate          6.5%          6.8%           6.9%
Cash-on-Cash      -2.1% ⚠️      9.2%           8.1%
Monthly CF        -$286 ⚠️      $975           $825
DSCR              0.91x ⚠️      1.45x          1.52x
Price/Unit        $162,500      $190,000       $175,000
```

#### Due Diligence Tab
**Purpose**: Track inspection items, document collection, and verification tasks

```
Inspection Checklist:
□ Structural inspection completed
□ HVAC systems evaluated  
□ Electrical systems checked
□ Plumbing systems assessed
□ Roof condition verified
□ Foundation inspection completed

Document Collection:
☑ Rent rolls (last 12 months)
☑ Operating expense statements (last 2 years) 
□ Lease agreements (all units)
□ Property tax records
□ Insurance claims history
□ Recent capital improvements list

Financial Verification:
□ Bank deposits match rent rolls
□ Expense receipts support statements
□ Vacancy periods verified
□ Market rent analysis completed
```

---

## Advanced Pipeline Features

### Batch Actions
- **Move Stage**: Move multiple deals to next/previous stage
- **Archive Deals**: Archive rejected or closed deals
- **Export Pipeline**: Generate pipeline report for team review
- **Set Reminders**: Bulk reminder setting for key dates

### Pipeline Analytics

#### Conversion Metrics
```
Pipeline Conversion Rates:
├── Sourced → Initial Review: 85% (17 of 20 deals)
├── Initial Review → Underwriting: 65% (11 of 17 deals)  
├── Underwriting → LOI: 45% (5 of 11 deals)
├── LOI → Under Contract: 60% (3 of 5 deals)
└── Under Contract → Closed: 75% (3 of 4 deals)

Overall Sourced → Closed: 15% (3 of 20 deals)
```

#### Time in Stage Analysis
```
Average Days by Stage:
├── Sourced: 3 days
├── Initial Review: 2 days
├── Underwriting: 6 days  
├── LOI Submitted: 8 days
├── Under Contract: 32 days
└── Due Diligence: 14 days

Total Average Deal Time: 65 days
```

### Deal Scoring System  
**Purpose**: Quantitative ranking of deals for prioritization

```
Deal Score Components (100 point scale):
├── Financial Metrics (40 points):
│   ├── Cap Rate vs. Target (15 points)
│   ├── Cash-on-Cash vs. Target (15 points)
│   └── DSCR vs. Minimum (10 points)
├── Market Factors (25 points):
│   ├── Location Desirability (15 points)
│   └── Property Condition (10 points)  
├── Deal Structure (20 points):
│   ├── Financing Attractiveness (10 points)
│   └── Purchase Terms (10 points)
└── Strategic Fit (15 points):
    ├── Portfolio Diversification (10 points)
    └── Management Complexity (5 points)
```

---

## Alerts and Notifications

### Automated Alert Triggers
- **Overdue Stage**: Deal in stage >150% of target duration
- **Key Date Approaching**: Contract deadlines within 7 days
- **Missing Information**: Required fields empty for stage progression
- **Market Changes**: Interest rate changes affecting deal viability
- **Competitive Intelligence**: Similar properties hitting market

### Notification Preferences
```
Notification Settings:
├── Deal Stage Changes: Email + In-app
├── Approaching Deadlines: Email + SMS  
├── Market Updates: Email only
├── Weekly Pipeline Summary: Email
└── Monthly Analytics Report: Email
```

---

## Integration Requirements

### CRM Integration (Future)
- Sync contact information for agents, lenders, inspectors
- Track communication history with deal stakeholders
- Automated follow-up reminders

### Financial Calculator Integration  
- Direct integration with underwriting calculations
- Scenario modeling within deal context
- Sensitivity analysis for key variables

### Document Management
- Upload and organize deal-related documents
- Version control for updated pro formas
- Sharing capabilities for team/partner review

### Market Data Integration (Future)
- Automated comparable sales analysis
- Real-time interest rate impacts on deals
- Market trend overlay for pricing decisions

---

## Export and Reporting

### Deal Summary Report
**Purpose**: Comprehensive deal package for review/approval

```
Executive Summary:
- Deal overview and key metrics
- Financial analysis summary  
- Risk assessment
- Recommendation and rationale

Detailed Analysis:
- Complete pro forma
- Sensitivity analysis
- Market comparables
- Due diligence findings

Appendices:
- Supporting documents
- Calculation details
- Market research
```

### Pipeline Performance Dashboard
- Deal velocity metrics
- Conversion rate analysis
- Time-to-close trends
- Deal source effectiveness

### Competitive Analysis Report
- Pipeline deals vs. market comparables
- Pricing strategy recommendations
- Market positioning analysis