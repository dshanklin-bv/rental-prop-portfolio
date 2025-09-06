# Project Structure

## File Organization (~700-900 total lines)

```
rental-calculator/
├── app.py              # Streamlit interface (~300 lines)
├── calculator.py       # Financial math (~200 lines)
├── models.py          # Pydantic data models (~100 lines)
├── charts.py          # Plotly visualizations (~100 lines)
├── requirements.txt   # Dependencies (~10 lines)
└── README.md         # Instructions (~50 lines)
```

## Core Dependencies
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
numpy-financial>=1.0.0
pydantic>=2.0.0
plotly>=5.14.0
```

## Data Models (models.py)
```python
class Unit(BaseModel):
    number: str          # "Unit A", "Unit 1", etc
    bedrooms: int
    bathrooms: float
    monthly_rent: float

class Property(BaseModel):
    address: str
    purchase_price: float
    down_payment: float
    units: List[Unit]
    
class Expenses(BaseModel):
    property_tax_annual: float
    insurance_annual: float
    maintenance_percent: float = 0.05  # 5% of rent
    vacancy_percent: float = 0.05      # 5% vacancy
    management_percent: float = 0.08   # 8% if using property mgmt

class Loan(BaseModel):
    amount: float
    rate: float          # 0.065 for 6.5%
    term_years: int      # 30
    
class Analysis(BaseModel):
    property: Property
    expenses: Expenses
    loan: Loan
    hold_years: int = 10
    exit_cap_rate: float = 0.06
```

## Key Calculations (calculator.py)
```python
def calculate_monthly_cashflow(analysis: Analysis) -> np.ndarray:
    """Returns array of monthly cash flows"""
    
def calculate_irr(cash_flows: List[float]) -> float:
    """Calculate IRR using numpy-financial"""
    
def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """Calculate NPV at given discount rate"""
    
def calculate_metrics(analysis: Analysis) -> Dict[str, float]:
    """Calculate all key metrics"""
    return {
        'irr': ...,
        'npv': ..., 
        'cash_on_cash': ...,
        'dscr': ...,
        'total_return': ...
    }
    
def compare_to_stocks(initial_investment: float, years: int, stock_return: float = 0.10) -> Dict:
    """Compare real estate returns to stock market"""
```

## Streamlit Interface (app.py)
```python
# Page 1: Property Setup
with st.sidebar:
    st.header("Property Details")
    address = st.text_input("Address")
    price = st.number_input("Purchase Price", value=400000)
    down_payment = st.number_input("Down Payment", value=80000)

# Page 2: Units Configuration  
st.header("Unit Configuration")
num_units = st.number_input("Number of Units", 1, 10, 4)
units = []
for i in range(num_units):
    with st.expander(f"Unit {i+1}"):
        rent = st.number_input(f"Monthly Rent", key=f"rent_{i}")
        # ... collect unit details

# Page 3: Analysis Results
if st.button("Calculate Returns"):
    analysis = Analysis(...)
    metrics = calculate_metrics(analysis)
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("IRR", f"{metrics['irr']:.2%}")
    col2.metric("Cash-on-Cash", f"{metrics['cash_on_cash']:.2%}") 
    col3.metric("NPV", f"${metrics['npv']:,.0f}")
    
    # Compare to stocks
    stock_comparison = compare_to_stocks(down_payment, hold_years)
    
    # Recommendation
    if metrics['irr'] > stock_comparison['return']:
        st.success("✅ Real estate beats stock market!")
    else:
        st.warning("❌ Stock market likely better investment")
```

## Simple Visualizations (charts.py)
```python
def create_cashflow_chart(monthly_cashflows: np.ndarray) -> go.Figure:
    """Monthly cash flow over time"""

def create_comparison_chart(re_metrics: Dict, stock_metrics: Dict) -> go.Figure:
    """Real estate vs stock comparison"""
    
def create_breakeven_chart(analysis: Analysis) -> go.Figure:
    """Show breakeven scenarios"""
```

This focused approach delivers exactly what you need - a simple calculator to answer "should I buy this property or invest in stocks?" in under 1000 lines of code.