# Core Entities and Data Model

## Entity Relationship Overview

```
Portfolio (1) ←→ (M) Property ←→ (M) Unit ←→ (M) Lease
                     ↓
Property (1) ←→ (M) Loan
                     ↓  
Property (1) ←→ (M) Transaction
                     ↓
Property (1) ←→ (M) Alert
                     ↓
Portfolio (1) ←→ (M) Deal (Acquisition Pipeline)
```

---

## Core Entities

### Portfolio
**Purpose:** Top-level container for user's real estate investments
**Scope:** Typically one per user, but may support multiple portfolios (personal vs. business)

```python
class Portfolio(BaseModel):
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Portfolio name")
    owner_name: str = Field(..., description="Owner/investor name")
    created_date: date = Field(..., description="Portfolio creation date")
    
    # Calculated fields (derived from properties)
    total_properties: int = Field(0, description="Number of properties")
    total_value: Decimal = Field(0, description="Total portfolio value")
    total_debt: Decimal = Field(0, description="Total outstanding debt")
    total_equity: Decimal = Field(0, description="Total equity position")
    monthly_gross_income: Decimal = Field(0, description="Monthly gross rental income")
    monthly_noi: Decimal = Field(0, description="Monthly net operating income")
    blended_cap_rate: float = Field(0, description="Portfolio-weighted cap rate")
    portfolio_ltv: float = Field(0, description="Loan-to-value ratio")
```

### Property
**Purpose:** Individual real estate assets and their characteristics
**Scope:** Single property (may contain multiple units)

```python
class PropertyType(str, Enum):
    SFR = "Single Family Residential"
    DUPLEX = "Duplex" 
    TRIPLEX = "Triplex"
    FOURPLEX = "Fourplex"
    SMALL_MULTIFAMILY = "Small Multi-Family (5-10 units)"
    MULTIFAMILY = "Multi-Family (11+ units)"
    COMMERCIAL = "Commercial"
    MIXED_USE = "Mixed Use"

class PropertyStatus(str, Enum):
    ACTIVE = "Active"
    UNDER_CONTRACT = "Under Contract"
    SOLD = "Sold"
    INACTIVE = "Inactive"

class Property(BaseModel):
    id: str = Field(..., description="Unique identifier")
    portfolio_id: str = Field(..., description="Parent portfolio ID")
    
    # Basic Information
    address: str = Field(..., description="Property address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State/Province")
    zip_code: str = Field(..., description="ZIP/Postal code")
    property_type: PropertyType = Field(..., description="Property classification")
    status: PropertyStatus = Field(PropertyStatus.ACTIVE, description="Current status")
    
    # Financial Information  
    purchase_price: Decimal = Field(..., description="Acquisition price")
    purchase_date: date = Field(..., description="Date of acquisition")
    current_value: Optional[Decimal] = Field(None, description="Current estimated value")
    land_value: Optional[Decimal] = Field(None, description="Land value for depreciation")
    
    # Physical Characteristics
    year_built: Optional[int] = Field(None, description="Year constructed")
    total_sqft: Optional[int] = Field(None, description="Total square footage")
    lot_size: Optional[Decimal] = Field(None, description="Lot size in acres")
    
    # Operating Information
    monthly_taxes: Decimal = Field(0, description="Monthly property taxes")
    monthly_insurance: Decimal = Field(0, description="Monthly insurance premium")
    monthly_hoa: Decimal = Field(0, description="Monthly HOA/CAM fees")
    management_fee_pct: float = Field(0, description="Property management fee %")
    maintenance_reserve: Decimal = Field(0, description="Monthly maintenance reserve")
    
    # Calculated Fields
    gross_monthly_income: Decimal = Field(0, description="Total monthly rental income")
    monthly_operating_expenses: Decimal = Field(0, description="Total monthly OpEx")
    monthly_noi: Decimal = Field(0, description="Monthly net operating income")
    monthly_cash_flow: Decimal = Field(0, description="Monthly cash flow after debt service")
    cap_rate: float = Field(0, description="Current cap rate")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Property notes")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### Unit
**Purpose:** Individual rentable spaces within a property
**Scope:** Apartment, house, commercial space, etc.

```python
class Unit(BaseModel):
    id: str = Field(..., description="Unique identifier")
    property_id: str = Field(..., description="Parent property ID")
    
    # Unit Identification
    unit_number: str = Field(..., description="Unit identifier (A, 1, 101, etc.)")
    unit_type: str = Field("Residential", description="Unit type")
    
    # Physical Characteristics
    bedrooms: int = Field(0, description="Number of bedrooms")
    bathrooms: float = Field(0, description="Number of bathrooms")
    sqft: Optional[int] = Field(None, description="Unit square footage")
    
    # Financial Information
    market_rent: Decimal = Field(..., description="Current market rent")
    rent_per_sqft: Optional[Decimal] = Field(None, description="Rent per square foot")
    
    # Status
    is_occupied: bool = Field(True, description="Current occupancy status")
    is_rentable: bool = Field(True, description="Available for rent")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Unit-specific notes")
```

### Lease  
**Purpose:** Rental agreements and tenant information
**Scope:** Single lease agreement for a unit

```python
class LeaseStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired" 
    TERMINATED = "Terminated"
    FUTURE = "Future"

class Lease(BaseModel):
    id: str = Field(..., description="Unique identifier")
    unit_id: str = Field(..., description="Parent unit ID")
    
    # Lease Terms
    start_date: date = Field(..., description="Lease start date")
    end_date: date = Field(..., description="Lease end date")
    base_rent: Decimal = Field(..., description="Monthly base rent")
    deposit: Decimal = Field(0, description="Security deposit amount")
    
    # Additional Income
    pet_rent: Decimal = Field(0, description="Monthly pet rent")
    parking_rent: Decimal = Field(0, description="Parking fees")
    other_income: Decimal = Field(0, description="Other monthly charges")
    
    # Tenant Information  
    tenant_name: str = Field(..., description="Primary tenant name")
    tenant_email: Optional[str] = Field(None, description="Tenant email")
    tenant_phone: Optional[str] = Field(None, description="Tenant phone")
    
    # Lease Status
    status: LeaseStatus = Field(LeaseStatus.ACTIVE, description="Current lease status")
    auto_renew: bool = Field(False, description="Auto-renewal flag")
    
    # Financial Tracking
    total_monthly_income: Decimal = Field(0, description="Total monthly income from lease")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Lease notes")
    created_at: datetime = Field(default_factory=datetime.now)
```

### Loan
**Purpose:** Debt financing secured by properties
**Scope:** Individual loan (may cover multiple properties for portfolio loans)

```python
class LoanType(str, Enum):
    CONVENTIONAL = "Conventional"
    PORTFOLIO = "Portfolio" 
    COMMERCIAL = "Commercial"
    HARD_MONEY = "Hard Money"
    SELLER_FINANCING = "Seller Financing"
    HELOC = "HELOC"

class Loan(BaseModel):
    id: str = Field(..., description="Unique identifier")
    property_id: str = Field(..., description="Primary property ID")
    
    # Loan Terms
    loan_type: LoanType = Field(..., description="Type of financing")
    original_amount: Decimal = Field(..., description="Original loan amount")
    current_balance: Decimal = Field(..., description="Current outstanding balance")
    interest_rate: float = Field(..., description="Annual interest rate (decimal)")
    term_months: int = Field(..., description="Total loan term in months")
    amortization_months: int = Field(..., description="Amortization period in months")
    
    # Payment Information
    monthly_payment: Decimal = Field(..., description="Monthly P&I payment")
    io_months: int = Field(0, description="Interest-only period in months")
    io_payment: Optional[Decimal] = Field(None, description="Interest-only payment amount")
    
    # Dates
    origination_date: date = Field(..., description="Loan origination date")
    first_payment_date: date = Field(..., description="First payment due date")
    maturity_date: date = Field(..., description="Loan maturity date")
    
    # Lender Information
    lender_name: str = Field(..., description="Lender institution")
    loan_number: Optional[str] = Field(None, description="Loan reference number")
    
    # Calculated Fields
    ltv_at_origination: float = Field(0, description="Loan-to-value at origination")
    current_ltv: float = Field(0, description="Current loan-to-value ratio")
    months_remaining: int = Field(0, description="Months until maturity")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Loan notes")
    created_at: datetime = Field(default_factory=datetime.now)
```

### Transaction
**Purpose:** Income and expense tracking for properties
**Scope:** Individual financial transaction

```python
class TransactionType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class TransactionCategory(str, Enum):
    # Income Categories
    RENT = "Rent"
    LATE_FEES = "Late Fees"
    PET_FEES = "Pet Fees"
    APPLICATION_FEES = "Application Fees" 
    OTHER_INCOME = "Other Income"
    
    # Expense Categories
    MORTGAGE = "Mortgage Payment"
    PROPERTY_TAX = "Property Tax"
    INSURANCE = "Insurance"
    HOA_CAM = "HOA/CAM Fees"
    PROPERTY_MANAGEMENT = "Property Management"
    MAINTENANCE = "Maintenance & Repairs"
    UTILITIES = "Utilities"
    PROFESSIONAL_SERVICES = "Professional Services"
    ADVERTISING = "Advertising"
    OTHER_EXPENSE = "Other Expense"

class Transaction(BaseModel):
    id: str = Field(..., description="Unique identifier")
    property_id: str = Field(..., description="Parent property ID")
    
    # Transaction Details
    date: date = Field(..., description="Transaction date")
    amount: Decimal = Field(..., description="Transaction amount (positive for income)")
    transaction_type: TransactionType = Field(..., description="Income or Expense")
    category: TransactionCategory = Field(..., description="Transaction category")
    description: str = Field(..., description="Transaction description")
    
    # References
    unit_id: Optional[str] = Field(None, description="Specific unit (if applicable)")
    vendor_payee: Optional[str] = Field(None, description="Vendor or tenant name")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(default_factory=datetime.now)
```

### Alert
**Purpose:** System-generated notifications and reminders
**Scope:** Portfolio or property-level alerts

```python
class AlertType(str, Enum):
    LEASE_EXPIRING = "Lease Expiring"
    LOAN_MATURING = "Loan Maturing"
    DSCR_WARNING = "DSCR Below Threshold"
    HIGH_VACANCY = "High Vacancy Rate"
    NEGATIVE_CASHFLOW = "Negative Cash Flow"
    MAINTENANCE_DUE = "Maintenance Due"
    TAX_PAYMENT_DUE = "Tax Payment Due"
    INSURANCE_RENEWAL = "Insurance Renewal"

class AlertPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"  
    HIGH = "High"
    CRITICAL = "Critical"

class Alert(BaseModel):
    id: str = Field(..., description="Unique identifier")
    property_id: Optional[str] = Field(None, description="Property ID (if property-specific)")
    portfolio_id: str = Field(..., description="Parent portfolio ID")
    
    # Alert Information
    alert_type: AlertType = Field(..., description="Type of alert")
    priority: AlertPriority = Field(..., description="Alert priority level")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert description")
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.now)
    trigger_date: Optional[date] = Field(None, description="Date that triggered alert")
    due_date: Optional[date] = Field(None, description="Action required by date")
    
    # Status
    is_read: bool = Field(False, description="User has viewed alert")
    is_resolved: bool = Field(False, description="Alert has been addressed")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")
    resolved_notes: Optional[str] = Field(None, description="Resolution notes")
```

### Deal (Acquisition Pipeline)
**Purpose:** Potential property acquisitions being evaluated
**Scope:** Single property under consideration

```python
class DealStage(str, Enum):
    SOURCED = "Sourced"
    INITIAL_REVIEW = "Initial Review"
    UNDERWRITING = "Underwriting" 
    LOI_SUBMITTED = "LOI Submitted"
    UNDER_CONTRACT = "Under Contract"
    DUE_DILIGENCE = "Due Diligence"
    CLOSING = "Closing"
    CLOSED = "Closed"
    REJECTED = "Rejected"

class Deal(BaseModel):
    id: str = Field(..., description="Unique identifier")
    portfolio_id: str = Field(..., description="Parent portfolio ID")
    
    # Property Information
    address: str = Field(..., description="Property address")
    asking_price: Decimal = Field(..., description="Listed/asking price")
    offer_price: Optional[Decimal] = Field(None, description="Offered price")
    property_type: PropertyType = Field(..., description="Property type")
    
    # Deal Progress
    stage: DealStage = Field(DealStage.SOURCED, description="Current deal stage")
    source: str = Field(..., description="Lead source (MLS, wholesaler, etc.)")
    date_sourced: date = Field(..., description="Date deal was identified")
    
    # Initial Analysis
    estimated_gross_income: Optional[Decimal] = Field(None, description="Est. monthly gross income")
    estimated_expenses: Optional[Decimal] = Field(None, description="Est. monthly expenses")
    estimated_noi: Optional[Decimal] = Field(None, description="Est. monthly NOI")
    estimated_cap_rate: Optional[float] = Field(None, description="Est. cap rate")
    estimated_cash_flow: Optional[Decimal] = Field(None, description="Est. monthly cash flow")
    
    # Deal Team
    listing_agent: Optional[str] = Field(None, description="Listing agent")
    buyer_agent: Optional[str] = Field(None, description="Buyer's agent")
    lender: Optional[str] = Field(None, description="Proposed lender")
    
    # Key Dates
    contract_date: Optional[date] = Field(None, description="Contract execution date")
    inspection_deadline: Optional[date] = Field(None, description="Inspection deadline")
    financing_deadline: Optional[date] = Field(None, description="Financing deadline") 
    closing_date: Optional[date] = Field(None, description="Scheduled closing date")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Deal notes")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

---

## Data Relationships and Business Rules

### Key Relationships
1. **Portfolio → Property**: One-to-many (user can have multiple properties)
2. **Property → Unit**: One-to-many (property can have multiple units)  
3. **Unit → Lease**: One-to-many (unit can have historical leases)
4. **Property → Loan**: One-to-many (property can have multiple loans)
5. **Property → Transaction**: One-to-many (property has many transactions)
6. **Portfolio → Alert**: One-to-many (alerts can be portfolio or property level)

### Business Rules
1. **Active Lease Constraint**: A unit can only have one active lease at a time
2. **Loan-to-Property Mapping**: Loans must be associated with at least one property
3. **Transaction Categorization**: All transactions must have a valid category
4. **Alert Auto-Generation**: System automatically creates alerts based on date triggers
5. **Deal Progression**: Deals can only move forward through stages (no backwards movement without explicit status change)

### Calculated Field Dependencies
- **Property.monthly_cash_flow**: Depends on NOI and loan payments
- **Portfolio.blended_cap_rate**: Weighted average of all property cap rates
- **Loan.current_ltv**: Requires current property value estimates
- **Alert triggers**: Based on lease end dates, loan maturity dates, financial thresholds