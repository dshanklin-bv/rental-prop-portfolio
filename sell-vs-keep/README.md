# Sell vs Keep Rental Property Calculator

A simple tool to help you decide whether to sell your multi-family rental property or keep it for cash flow.

## What It Does

You own a rental property. Should you:
- **Sell it now** and invest the proceeds in the stock market? 
- **Keep it as a rental** for monthly cash flow and appreciation?

This calculator compares both scenarios over your chosen time horizon and gives you a clear recommendation.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Enter your property details** in the sidebar

4. **Click "Calculate Sell vs Keep"** to see results

## Example Analysis

**Your Property:**
- 4-unit building worth $500K
- You paid $350K three years ago  
- Current mortgage: $200K
- Rent: $1,200/unit = $4,800/month total

**The Question:** Sell now or keep for 10 years?

**Results:**
- **Sell Now:** $622K after 10 years (invest proceeds in stocks)
- **Keep Rental:** $772K after 10 years (cash flow + future sale)
- **Recommendation:** Keep the rental! ($150K more)

## Key Features

- ✅ Simple, focused interface
- ✅ Clear visual comparisons  
- ✅ Sensitivity analysis (what if rent changes?)
- ✅ Break-even calculations
- ✅ Export results to CSV
- ✅ Tax considerations (capital gains)
- ✅ No database required

## Assumptions You Can Adjust

- Property appreciation rate (default: 3%/year)
- Stock market return (default: 10%/year)
- Selling costs (default: 6% of sale price)
- Capital gains tax rate (default: 20%)
- Maintenance, vacancy, management percentages
- Analysis time period (1-30 years)

## What It Doesn't Do

This is intentionally simple. It does NOT:
- Track multiple properties
- Handle complex tax situations
- Integrate with banks or property management
- Store your data (everything is session-based)
- Predict market conditions

## Files

- `app.py` - Main Streamlit interface (~350 lines)
- `calculator.py` - Financial calculations (~200 lines)  
- `models.py` - Data structures (~100 lines)
- `charts.py` - Visualizations (~150 lines)
- `requirements.txt` - Dependencies

**Total: ~800 lines of Python**

## Accuracy

The IRR and NPV calculations use `numpy-financial` for accuracy. Test results against Excel to verify.

---

**Disclaimer:** This tool provides estimates for comparison purposes only. Consult financial and tax professionals before making investment decisions.