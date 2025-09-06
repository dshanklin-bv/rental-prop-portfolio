# Portfolio Dashboard
## Executive Summary View

### Purpose
Provide investors with a comprehensive, at-a-glance view of their entire real estate portfolio performance, health metrics, and actionable insights.

### User Goals
- **Portfolio Health Check**: Quickly assess overall portfolio performance vs. targets
- **Geographic Overview**: Understand property distribution and regional performance
- **Cash Flow Analysis**: Track monthly and annual cash flow trends
- **Alert Management**: Identify properties requiring immediate attention

---

## Key Performance Indicators (KPIs)

### Top-Level Metrics Row
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Total Value     │ Total Equity    │ Portfolio LTV   │ Blended Cap     │
│ $2,450,000     │ $1,225,000     │ 50.0%          │ 6.8%            │
│ ↑ 12% YTD      │ ↑ 18% YTD      │ ↓ 2.3% YTD     │ ↑ 0.4% YTD     │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Cash Flow Metrics Row  
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Monthly NOI     │ Monthly CF      │ Occupancy Rate  │ Avg DSCR        │
│ $14,250        │ $8,420         │ 92.3%          │ 1.45x           │
│ ↑ 6% vs Budget │ ↑ 8% vs Budget │ ↓ 2.1% vs Prior│ Healthy         │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Metric Definitions
- **Total Value**: Current estimated market value of all properties
- **Total Equity**: Market value minus outstanding debt
- **Portfolio LTV**: Total debt / total property values
- **Blended Cap Rate**: Portfolio-weighted average cap rate
- **Monthly NOI**: Net Operating Income across all properties
- **Monthly CF**: Cash flow after debt service
- **Occupancy Rate**: Occupied units / total rentable units
- **Avg DSCR**: Average debt service coverage ratio across levered properties

---

## Visual Components

### 1. Geographic Distribution Map
**Purpose**: Show property locations with performance color-coding

```
Interactive Map Features:
- Property markers sized by equity value
- Color coding: Green (outperforming), Yellow (on-target), Red (underperforming)  
- Click to view property summary card
- Filter by property type, performance, acquisition year
```

**Performance Criteria**:
- **Green**: Cash flow >110% of projection OR cap rate >target+0.5%
- **Yellow**: Cash flow 90-110% of projection AND cap rate within ±0.5% of target
- **Red**: Cash flow <90% of projection OR cap rate <target-0.5%

### 2. Portfolio Value Over Time
**Purpose**: Track portfolio growth and equity build-up

```
Stacked Area Chart:
- X-axis: Monthly periods (24 months historical + 12 months projected)
- Y-axis: Dollar value
- Areas: Property Value (top), Debt (bottom), Equity (difference)
- Overlay: Monthly net cash flow as line chart
```

### 3. Cash Flow Contribution by Property
**Purpose**: Identify highest and lowest performing properties

```
Horizontal Bar Chart:
- Properties ranked by monthly cash flow contribution
- Bars show: Gross Income (light blue), Operating Expenses (orange), Debt Service (red)
- Net cash flow shown as numerical value
- Click property bar to navigate to detailed view
```

### 4. Property Performance Matrix
**Purpose**: Two-dimensional analysis of risk vs. return

```
Scatter Plot:
- X-axis: Cap Rate (return proxy)
- Y-axis: DSCR (risk proxy)  
- Bubbles: Properties sized by equity value
- Quadrants: High Risk/High Return, Low Risk/High Return, etc.
- Target zones highlighted (DSCR >1.25, Cap Rate >6.0%)
```

---

## Alert Management Section

### Alert Priority Display
```
┌─────────────────────────────────────────────────────────────────┐
│ 🔴 CRITICAL (2)                                                │
│ • 123 Oak St: DSCR dropped to 1.15x (threshold: 1.20x)        │
│ • 456 Pine Ave: Lease expires in 15 days (no renewal signed)   │
│                                                                 │
│ 🟡 MEDIUM (3)                                                  │  
│ • 789 Elm Dr: Insurance renewal due in 30 days                 │
│ • 321 Main St: Property tax payment due in 45 days            │
│ • 654 Cedar Ln: Maintenance reserve below 6-month target      │
└─────────────────────────────────────────────────────────────────┘
```

### Alert Categories
- **CRITICAL**: Immediate action required (DSCR violations, lease expirations <30 days)
- **HIGH**: Action required within 2 weeks (loan maturities <90 days, high vacancy)
- **MEDIUM**: Action required within 30-60 days (insurance renewals, tax payments)
- **LOW**: Monitoring items (maintenance reserves, rent increase opportunities)

---

## Data Tables

### Property Summary Table
**Purpose**: Tabular view of all properties with key metrics

| Property | Type | Purchase Date | Value | Equity | Monthly CF | Cap Rate | DSCR | Occupancy |
|----------|------|---------------|-------|--------|------------|----------|------|-----------|
| 123 Oak St | SFR | 03/2022 | $425K | $127K | $850 | 7.2% | 1.45x | 100% |
| 456 Pine Ave | Duplex | 08/2021 | $380K | $152K | $1,200 | 6.8% | 1.38x | 100% |
| 789 Elm Dr | 4-plex | 11/2020 | $650K | $315K | $2,100 | 6.5% | 1.52x | 87.5% |

**Interactive Features**:
- Sortable columns
- Filter by property type, acquisition year, performance thresholds
- Color-coded cells based on performance vs. targets
- Click row to navigate to property detail page

### Recent Transactions Summary
**Purpose**: Show recent portfolio-level financial activity

| Date | Property | Category | Amount | Description |
|------|----------|----------|--------|-------------|
| 08/01 | Portfolio | Income | +$12,450 | Monthly rent collection |
| 08/01 | 789 Elm Dr | Expense | -$450 | HVAC repair - Unit C |
| 07/28 | 456 Pine Ave | Expense | -$1,250 | Property management fee |
| 07/25 | 123 Oak St | Expense | -$850 | Mortgage payment |

---

## Navigation and Actions

### Quick Actions Toolbar
```
┌─────────────────────────────────────────────────────────────────┐
│ [+ Add Property] [📁 Import Data] [📊 Generate Report] [⚙️ Settings] │
└─────────────────────────────────────────────────────────────────┘
```

### Dashboard Views
- **Executive**: High-level KPIs and visualizations (default view)
- **Financial**: Detailed cash flow analysis and variance reports
- **Operational**: Occupancy, maintenance, and operational metrics  
- **Pipeline**: Integration with acquisition pipeline for deal flow context

### Export Options
- **PDF Report**: Executive summary with key charts for stakeholder sharing
- **Excel Export**: Raw data export for detailed analysis
- **CSV Data**: Transaction and property data for accounting systems

---

## Responsive Design Requirements

### Desktop (>1200px)
- Full 4-column KPI layout
- Side-by-side charts and data tables  
- Interactive map with full property details

### Tablet (768-1200px)
- 2-column KPI layout
- Stacked chart components
- Simplified map with essential details

### Mobile (< 768px)
- Single-column KPI cards
- Swipeable chart carousel
- List view instead of map for property overview

---

## Performance Requirements

### Load Time Targets
- **Initial Dashboard Load**: <3 seconds for portfolios up to 20 properties
- **Chart Interactions**: <500ms response time for filters and drill-downs
- **Data Refresh**: <5 seconds for monthly data recalculation

### Data Refresh Strategy
- **Real-time**: Alert counts and critical notifications
- **Hourly**: KPI calculations and performance metrics
- **Daily**: Property valuations and market-based metrics
- **On-demand**: User-initiated data refresh button

---

## Integration Points

### Internal System Integration
- **Property Management**: Pull occupancy and lease data
- **Transaction System**: Aggregate income/expense data
- **Alert System**: Display prioritized notifications
- **Acquisition Pipeline**: Show pipeline deals in context

### External Data Sources (Future)
- **Market Data**: Property value estimates and comparable sales
- **Weather/Events**: Context for seasonal performance variations
- **Economic Indicators**: Interest rate and market trend overlays