# Sell vs Keep Rental Property Calculator

## Purpose
You own a multi-family property. Should you **sell it now** and invest the proceeds in the stock market, or **keep it as a rental** for cash flow?

## Scope (What it IS)
- ✅ Single multi-family property you already own
- ✅ "Sell now" vs "Keep and rent" comparison
- ✅ Multi-unit rental income projections if you keep it
- ✅ Sale proceeds vs rental cash flow + appreciation analysis
- ✅ Tax implications (capital gains vs rental income)
- ✅ Stock market alternative comparison
- ✅ Simple Streamlit web interface
- ✅ Export results to CSV/Excel

## Non-Scope (What it's NOT)
- ❌ Property acquisition analysis (you already own it)
- ❌ Multiple property portfolio management
- ❌ Document parsing/OCR
- ❌ Database persistence 
- ❌ Property management features
- ❌ Market data integration
- ❌ Complex tax optimization

## Target: <800 Lines of Python

## Key Use Case
"I own a 4-unit building worth ~$500K. Should I sell it now and put the money in stocks, or keep it and rent it out for the next 10 years?"

## Technical Stack
- Python + Streamlit (frontend)
- numpy-financial (IRR/NPV calculations) 
- pandas (data handling)
- plotly (simple charts)
- No database needed - session state only

## File Structure
```
/
├── app.py              # Main Streamlit app (~300 lines)
├── calculator.py       # Financial calculations (~200 lines)
├── models.py          # Data models (~100 lines)  
├── charts.py          # Simple visualizations (~100 lines)
├── requirements.txt   # Dependencies
└── README.md         # Usage instructions
```

## Core Calculations

### Scenario A: Sell Now
1. **Current Market Value** - Selling Costs = Net Proceeds
2. **Capital Gains Tax** on (Sale Price - Original Basis)
3. **After-Tax Proceeds** available for stock investment
4. **Stock Market Growth** over analysis period (default 10% annually)
5. **Total Stock Value** after N years

### Scenario B: Keep as Rental  
1. **Monthly Cash Flow**: Rent - (Mortgage + Taxes + Insurance + Maintenance + Vacancy)
2. **Annual Cash Flow** accumulated over hold period
3. **Property Appreciation** at assumed rate (default 3% annually)
4. **Future Sale Value** after hold period minus selling costs and taxes
5. **Total Return**: Cash flows + Future sale proceeds

### Comparison Metrics
- **IRR**: Internal rate of return for each scenario
- **NPV**: Net present value at discount rate
- **Total Wealth**: Final dollar amount after N years
- **Break-Even**: At what rental yield or appreciation rate do scenarios tie?

## Interface Flow
1. **Current Property Details** (current value, original purchase price/date, mortgage balance)
2. **Unit Configuration** (# units, market rent per unit)
3. **Expenses** (taxes, insurance, maintenance %, vacancy %)
4. **Sale Assumptions** (selling costs %, capital gains tax rate)
5. **Market Assumptions** (property appreciation %, stock market return %)
6. **Time Horizon** (how many years to analyze)
7. **Results**: Clear recommendation with supporting numbers
8. **Export**: Download full analysis

## Success Criteria
- IRR calculations match Excel/financial calculator within ±5 basis points
- Complete analysis in <5 minutes
- Clear "sell now" vs "keep as rental" recommendation
- Runs on laptop without internet connection