Based on the comprehensive discussion between you and ChatGPT (and Claude's feedback), here are detailed instructions for Claude Code to build this real estate cash flow modeling tool:

## Project Instructions for Claude Code

### Core Architecture & Setup

```bash
# Project structure
rei_model/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Dependencies
├── .gitignore               # Include data/*, *.sqlite3, __pycache__
├── data/
│   ├── inbox/               # Local "S3" for uploaded/pasted content
│   ├── runs/                # Run JSON artifacts (*.json.gz)
│   ├── app.sqlite3          # SQLite for runtime logs
│   └── ingestions.jsonl     # Metadata log for all ingested content
├── engine/
│   ├── __init__.py
│   ├── schemas.py           # Pydantic models for validation
│   ├── cashflow.py          # Core financial calculations
│   ├── metrics.py           # IRR, NPV, CoC, DSCR calculations
│   ├── tax.py               # Depreciation, recapture, after-tax flows
│   ├── storage.py           # File storage & inbox management
│   ├── serializer.py        # Build Run JSON artifacts
│   ├── runlog.py            # Save/load Run JSONs
│   └── db.py                # SQLite setup for logging
├── agents/
│   ├── __init__.py
│   └── extract.py           # Stub parser (later: real OCR/LLM)
├── components/
│   ├── __init__.py
│   ├── inputs.py            # Reusable Streamlit widgets
│   └── charts.py            # Visualization components
└── tests/
    ├── test_cashflow.py     # Golden tests for financial math
    └── test_tax.py          # Tax calculation tests
```

### Phase 0: Core Implementation (Ship This First)

#### 1. Dependencies (`requirements.txt`)
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
numpy-financial>=1.0.0
pydantic>=2.0.0
plotly>=5.14.0
openpyxl>=3.1.0
reportlab>=4.0.0
python-dateutil>=2.8.0
```

#### 2. Core Engine Components

**`engine/schemas.py`** - Data models with Pydantic validation:
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import date, datetime
from enum import Enum

class PropertyType(str, Enum):
    SFR = "Single Family"
    DUPLEX = "Duplex"
    MULTI = "Multi-Family"
    COMMERCIAL = "Commercial"

class Unit(BaseModel):
    label: str
    beds: int
    baths: float
    sqft: int
    market_rent: float
    
class Lease(BaseModel):
    unit_label: str
    start_date: date
    end_date: date
    base_rent: float
    other_income: float = 0
    deposit: float
    
class Loan(BaseModel):
    amount: float
    rate: float  # As decimal (0.065 for 6.5%)
    term_months: int
    io_months: int = 0
    start_date: date
    
class Scenario(BaseModel):
    property_id: str
    name: str
    units: List[Unit]
    leases: List[Lease]
    loan: Optional[Loan]
    expenses: Dict[str, float]  # Category -> monthly amount
    hold_years: int = 10
    exit_cap_rate: float = 0.065
    selling_costs_pct: float = 0.06
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
```

**`engine/cashflow.py`** - Core financial calculations:
```python
import numpy as np
import numpy_financial as npf
from typing import Dict, List
from .schemas import Scenario, Loan

def calculate_monthly_cashflow(scenario: Scenario) -> Dict:
    """
    Returns monthly arrays for:
    - gross_income
    - vacancy_loss
    - effective_income
    - operating_expenses
    - noi
    - debt_service
    - cash_flow_before_tax
    """
    months = scenario.hold_years * 12
    
    # Initialize arrays
    gross_income = np.zeros(months)
    operating_expenses = np.zeros(months)
    
    # Calculate unit-level income
    for lease in scenario.leases:
        # Map lease to months (handle rollovers)
        # Add base_rent + other_income per month
        pass  # Implement lease scheduling
    
    # Apply vacancy (5% default)
    vacancy_rate = 0.05
    effective_income = gross_income * (1 - vacancy_rate)
    
    # Operating expenses
    for category, monthly_amount in scenario.expenses.items():
        operating_expenses += monthly_amount
    
    # NOI
    noi = effective_income - operating_expenses
    
    # Debt service
    debt_service = calculate_debt_service(scenario.loan, months) if scenario.loan else np.zeros(months)
    
    # Cash flow
    cash_flow_before_tax = noi - debt_service
    
    return {
        'gross_income': gross_income,
        'effective_income': effective_income,
        'operating_expenses': operating_expenses,
        'noi': noi,
        'debt_service': debt_service,
        'cash_flow_before_tax': cash_flow_before_tax
    }

def calculate_debt_service(loan: Loan, months: int) -> np.ndarray:
    """Calculate monthly P&I payments including IO period"""
    rate_monthly = loan.rate / 12
    
    # Handle interest-only period
    if loan.io_months > 0:
        io_payment = loan.amount * rate_monthly
        regular_payment = npf.pmt(rate_monthly, loan.term_months - loan.io_months, -loan.amount)
        
        payments = np.zeros(months)
        payments[:loan.io_months] = io_payment
        payments[loan.io_months:] = regular_payment
        return payments
    else:
        payment = npf.pmt(rate_monthly, loan.term_months, -loan.amount)
        return np.full(months, payment)
```

**`engine/tax.py`** - Tax calculations:
```python
def calculate_depreciation(purchase_price: float, land_value: float, recovery_years: float = 27.5) -> np.ndarray:
    """
    Calculate annual depreciation for residential (27.5 years) or commercial (39 years)
    """
    depreciable_basis = purchase_price - land_value
    annual_depreciation = depreciable_basis / recovery_years
    return annual_depreciation

def calculate_after_tax_cashflow(
    cash_flow_before_tax: np.ndarray,
    noi: np.ndarray,
    interest_expense: np.ndarray,
    depreciation: float,
    tax_rate: float = 0.28
) -> np.ndarray:
    """
    Calculate after-tax cash flow
    Taxable Income = NOI - Interest - Depreciation
    Tax = Taxable Income * Tax Rate
    ATCF = CFBT - Tax
    """
    taxable_income = noi - interest_expense - depreciation
    tax_due = np.maximum(taxable_income * tax_rate, 0)  # No negative taxes for simplicity
    return cash_flow_before_tax - tax_due
```

**`engine/metrics.py`** - Key metrics:
```python
def calculate_irr(cash_flows: List[float]) -> float:
    """Calculate IRR with error handling"""
    try:
        return npf.irr(cash_flows)
    except:
        return float('nan')
        
def calculate_cap_rate(annual_noi: float, property_value: float) -> float:
    """Cap Rate = NOI / Property Value"""
    return annual_noi / property_value if property_value > 0 else 0

def calculate_dscr(noi: float, debt_service: float) -> float:
    """Debt Service Coverage Ratio"""
    return noi / debt_service if debt_service > 0 else float('inf')
    
def calculate_coc_return(annual_cash_flow: float, initial_investment: float) -> float:
    """Cash-on-Cash Return"""
    return annual_cash_flow / initial_investment if initial_investment > 0 else 0
```

#### 3. Storage & Persistence

**`engine/storage.py`** - Local file storage:
```python
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any

DATA_DIR = Path(__file__).parent.parent / "data"
INBOX_DIR = DATA_DIR / "inbox"
RUNS_DIR = DATA_DIR / "runs"

def ensure_dirs():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(filename: str, content: bytes, tags: Dict = None) -> str:
    """Save uploaded file with timestamp and hash"""
    ensure_dirs()
    
    # Generate unique filename
    timestamp = datetime.now(timezone.utc).isoformat()
    file_hash = hashlib.sha256(content).hexdigest()[:8]
    stored_name = f"{timestamp}_{file_hash}_{filename}"
    
    # Save file
    file_path = INBOX_DIR / stored_name
    file_path.write_bytes(content)
    
    # Log to ingestions.jsonl
    log_ingestion({
        'timestamp': timestamp,
        'source_type': 'upload',
        'original_name': filename,
        'stored_name': stored_name,
        'size': len(content),
        'hash': file_hash,
        'tags': tags or {}
    })
    
    return stored_name

def save_pasted_text(text: str, tags: Dict = None) -> str:
    """Save pasted text as timestamped file"""
    ensure_dirs()
    
    timestamp = datetime.now(timezone.utc).isoformat()
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:8]
    filename = f"{timestamp}_{text_hash}_pasted.txt"
    
    file_path = INBOX_DIR / filename
    file_path.write_text(text)
    
    log_ingestion({
        'timestamp': timestamp,
        'source_type': 'paste',
        'stored_name': filename,
        'size': len(text),
        'hash': text_hash,
        'tags': tags or {}
    })
    
    return filename

def log_ingestion(record: Dict[str, Any]):
    """Append to ingestions.jsonl"""
    log_path = DATA_DIR / "ingestions.jsonl"
    with open(log_path, 'a') as f:
        f.write(json.dumps(record) + '\n')
```

**`engine/serializer.py`** - Run JSON creation:
```python
def build_run_json(scenario: Scenario, cashflows: Dict, metrics: Dict) -> Dict:
    """Create comprehensive Run JSON artifact"""
    return {
        'meta': {
            'run_id': f"{datetime.now(timezone.utc).isoformat()}_{scenario.property_id}_{uuid.uuid4().hex[:8]}",
            'engine_version': '0.1.0',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'scenario_id': scenario.property_id
        },
        'assumptions': scenario.dict(),
        'timelines_nominal': {
            'gross_income': cashflows['gross_income'].tolist(),
            'noi': cashflows['noi'].tolist(),
            'cash_flow_before_tax': cashflows['cash_flow_before_tax'].tolist(),
            'debt_service': cashflows['debt_service'].tolist()
        },
        'metrics': metrics,
        'validations': run_validations(scenario, cashflows, metrics)
    }

def run_validations(scenario, cashflows, metrics) -> List[Dict]:
    """Run validation rules and return warnings"""
    warnings = []
    
    # DSCR check
    if metrics.get('min_dscr', float('inf')) < 1.2:
        warnings.append({
            'level': 'warning',
            'rule': 'dscr_threshold',
            'message': f"DSCR of {metrics['min_dscr']:.2f} is below 1.20 threshold"
        })
    
    # Exit cap vs entry cap
    if scenario.exit_cap_rate < metrics.get('entry_cap_rate', 0):
        warnings.append({
            'level': 'warning',
            'rule': 'cap_rate_compression',
            'message': 'Exit cap rate lower than entry cap rate in rising rate environment'
        })
    
    return warnings
```

#### 4. Streamlit App

**`app.py`** - Main application:
```python
import streamlit as st
import pandas as pd
from engine import schemas, cashflow, metrics, storage, serializer
from pathlib import Path

st.set_page_config(page_title="REI Cash Flow Model", layout="wide")

# Initialize session state
if 'scenario' not in st.session_state:
    st.session_state.scenario = schemas.Scenario(
        property_id="property_001",
        name="Default Scenario",
        units=[],
        leases=[],
        loan=None,
        expenses={},
        hold_years=10
    )

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Property Setup", "Financials", "Run Analysis", "Upload & Parse", "Inbox"])

if page == "Property Setup":
    st.header("Property Setup")
    
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox("Property Type", ["Single Family", "Duplex", "Multi-Family"])
        num_units = st.number_input("Number of Units", 1, 20, 2)
    
    with col2:
        address = st.text_input("Property Address", "239 Eagle Dr, Boone, NC")
        purchase_price = st.number_input("Purchase Price", 0, 10000000, 400000)
    
    # Unit configuration
    st.subheader("Units")
    units = []
    for i in range(num_units):
        with st.expander(f"Unit {chr(65+i)}"):
            cols = st.columns(4)
            beds = cols[0].number_input(f"Beds", 1, 5, 2, key=f"beds_{i}")
            baths = cols[1].number_input(f"Baths", 1.0, 4.0, 1.0, key=f"baths_{i}")
            sqft = cols[2].number_input(f"Sq Ft", 100, 5000, 850, key=f"sqft_{i}")
            rent = cols[3].number_input(f"Rent", 0, 10000, 1600, key=f"rent_{i}")
            
            units.append(schemas.Unit(
                label=chr(65+i),
                beds=beds,
                baths=baths,
                sqft=sqft,
                market_rent=rent
            ))
    
    st.session_state.scenario.units = units

elif page == "Financials":
    st.header("Financing & Expenses")
    
    # Loan details
    st.subheader("Loan")
    use_financing = st.checkbox("Use Financing", True)
    
    if use_financing:
        col1, col2, col3 = st.columns(3)
        ltv = col1.slider("LTV", 0.0, 0.95, 0.75)
        rate = col2.number_input("Interest Rate (%)", 0.0, 15.0, 6.5) / 100
        term_years = col3.number_input("Term (years)", 1, 40, 30)
        
        loan_amount = st.session_state.scenario.units[0].market_rent * 12 * len(st.session_state.scenario.units) * 10 * ltv  # Rough calc
        
        st.session_state.scenario.loan = schemas.Loan(
            amount=loan_amount,
            rate=rate,
            term_months=term_years * 12,
            io_months=0,
            start_date=pd.Timestamp.now().date()
        )
    
    # Operating Expenses
    st.subheader("Operating Expenses (Monthly)")
    expenses = {}
    
    col1, col2 = st.columns(2)
    expenses['Property Tax'] = col1.number_input("Property Tax (annual)", 0, 50000, 2850) / 12
    expenses['Insurance'] = col1.number_input("Insurance (annual)", 0, 20000, 1450) / 12
    expenses['HOA'] = col2.number_input("HOA/CAM", 0.0, 2000.0, 0.0)
    expenses['Maintenance'] = col2.number_input("Maintenance Reserve", 0.0, 2000.0, 150.0)
    expenses['Property Mgmt'] = st.slider("Property Mgmt (% of income)", 0.0, 15.0, 8.0) / 100
    
    st.session_state.scenario.expenses = expenses

elif page == "Run Analysis":
    st.header("Run Analysis")
    
    if st.button("Run Cash Flow Analysis", type="primary"):
        scenario = st.session_state.scenario
        
        # Calculate cash flows
        cf = cashflow.calculate_monthly_cashflow(scenario)
        
        # Calculate metrics
        year1_noi = cf['noi'][:12].sum()
        property_value = 400000  # Use actual from scenario
        
        metrics_dict = {
            'cap_rate': metrics.calculate_cap_rate(year1_noi, property_value),
            'min_dscr': min([metrics.calculate_dscr(cf['noi'][i], cf['debt_service'][i]) 
                           for i in range(len(cf['noi'])) if cf['debt_service'][i] > 0]),
            'irr': metrics.calculate_irr([-100000] + cf['cash_flow_before_tax'].tolist())  # Simplified
        }
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Cap Rate", f"{metrics_dict['cap_rate']:.2%}")
        col2.metric("Min DSCR", f"{metrics_dict['min_dscr']:.2f}")
        col3.metric("IRR", f"{metrics_dict['irr']:.2%}")
        col4.metric("Year 1 NOI", f"${year1_noi:,.0f}")
        
        # Annual cash flow table
        st.subheader("Annual Cash Flow")
        annual_cf = pd.DataFrame({
            'Year': range(1, scenario.hold_years + 1),
            'NOI': [cf['noi'][i*12:(i+1)*12].sum() for i in range(scenario.hold_years)],
            'Debt Service': [cf['debt_service'][i*12:(i+1)*12].sum() for i in range(scenario.hold_years)],
            'Cash Flow': [cf['cash_flow_before_tax'][i*12:(i+1)*12].sum() for i in range(scenario.hold_years)]
        })
        st.dataframe(annual_cf.style.format({'NOI': '${:,.0f}', 'Debt Service': '${:,.0f}', 'Cash Flow': '${:,.0f}'}))
        
        # Save Run JSON
        if st.button("Save This Run"):
            run_json = serializer.build_run_json(scenario, cf, metrics_dict)
            run_id = serializer.save_run(run_json)
            st.success(f"Run saved: {run_id}")

elif page == "Upload & Parse":
    st.header("Upload & Parse Documents")
    
    # File upload
    files = st.file_uploader("Upload documents", type=['pdf', 'txt', 'csv', 'xlsx'], accept_multiple_files=True)
    
    # Text paste
    pasted_text = st.text_area("Or paste text here", height=150)
    
    if st.button("Save & Parse"):
        # Save uploaded files
        for file in files:
            content = file.read()
            stored = storage.save_uploaded_file(file.name, content, tags={'source': 'upload'})
            st.success(f"Saved: {stored}")
        
        # Save pasted text
        if pasted_text:
            stored = storage.save_pasted_text(pasted_text, tags={'source': 'paste'})
            st.success(f"Saved pasted text: {stored}")
        
        # Stub parser (replace with real implementation)
        st.info("Parser stub - would extract lease terms, bills, etc.")

elif page == "Inbox":
    st.header("Document Inbox")
    
    # Read ingestions log
    ingestions_path = Path("data/ingestions.jsonl")
    if ingestions_path.exists():
        import json
        
        records = []
        with open(ingestions_path) as f:
            for line in f:
                records.append(json.loads(line))
        
        df = pd.DataFrame(records)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)
            
            st.dataframe(df[['timestamp', 'source_type', 'original_name', 'size', 'hash']])
    else:
        st.info("No documents ingested yet")
```

### Key Implementation Notes for Claude Code:

1. **Start with Phase 0 only** - Get the core math working first with manual data entry
2. **Use stub parsers initially** - The extract.py should return fake but realistic data
3. **Validate against Excel** - Create 2-3 test cases in Excel and ensure IRR matches within ±2 bps
4. **Keep Run JSON minimal** - Only include what's shown in the v1 schema
5. **No external integrations** - Everything stays local for now
6. **Test the core math thoroughly** - Amortization, tax calculations, and IRR must be bulletproof

### Testing Requirements:

```python
# tests/test_cashflow.py
def test_loan_amortization():
    """Verify loan calculations match Excel/financial calculator"""
    loan = Loan(amount=300000, rate=0.065, term_months=360, io_months=0)
    payments = calculate_debt_service(loan, 360)
    
    # Monthly payment should be ~$1,896
    assert abs(payments[0] - 1896) < 1
    
def test_irr_calculation():
    """Verify IRR matches numpy_financial"""
    cash_flows = [-100000, 5000, 5000, 5000, 5000, 105000]
    irr = calculate_irr(cash_flows)
    assert abs(irr - 0.05) < 0.001  # Should be ~5%
```

### Stopping Criteria for Phase 0:
- Matches 2-3 Excel test cases within ±2 basis points on IRR
- Exports working CSV/XLSX with all assumptions and cash flows  
- Run JSON successfully captures a complete scenario
- Manual data entry works for duplex/multi-unit properties

Only proceed to Phase 1 (validation rules, logging) after Phase 0 is solid and tested.