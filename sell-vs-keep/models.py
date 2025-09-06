from pydantic import BaseModel, Field
from typing import List
from datetime import date

class Unit(BaseModel):
    """Individual unit in the property"""
    number: str = Field(description="Unit identifier (e.g., 'Unit A', '1', etc.)")
    bedrooms: int = Field(ge=0, description="Number of bedrooms")
    bathrooms: float = Field(ge=0, description="Number of bathrooms")
    monthly_rent: float = Field(ge=0, description="Monthly rent for this unit")

class Property(BaseModel):
    """The property you currently own"""
    address: str = Field(description="Property address")
    current_value: float = Field(gt=0, description="Current market value")
    original_purchase_price: float = Field(gt=0, description="What you originally paid")
    cost_basis: float = Field(gt=0, description="Cost basis including improvements for tax purposes")
    purchase_date: date = Field(description="When you bought it")
    mortgage_balance: float = Field(ge=0, description="Current mortgage balance")
    units: List[Unit] = Field(min_items=1, description="List of units in the property")
    
    @property
    def total_monthly_rent(self) -> float:
        """Calculate total monthly rent from all units"""
        return sum(unit.monthly_rent for unit in self.units)
    
    @property
    def capital_gain(self) -> float:
        """Calculate capital gain if sold at current value using cost basis"""
        return self.current_value - self.cost_basis

class Expenses(BaseModel):
    """Monthly operating expenses for the rental property"""
    property_tax_monthly: float = Field(ge=0, description="Monthly property tax")
    property_tax_annual: float = Field(ge=0, description="Annual property tax")
    insurance_monthly: float = Field(ge=0, description="Monthly insurance")
    insurance_annual: float = Field(ge=0, description="Annual insurance")
    mortgage_payment: float = Field(ge=0, description="Monthly mortgage payment (P&I + escrow)")
    mortgage_escrow: float = Field(ge=0, description="Monthly escrow payment")
    maintenance_percent: float = Field(ge=0, le=1, default=0.05, description="Maintenance as % of rent")
    vacancy_percent: float = Field(ge=0, le=1, default=0.05, description="Vacancy allowance as % of rent")
    management_percent: float = Field(ge=0, le=1, default=0.0, description="Property management as % of rent")
    other_monthly: float = Field(ge=0, default=0, description="Other monthly expenses")

class SaleAssumptions(BaseModel):
    """Assumptions for selling the property"""
    selling_costs_percent: float = Field(ge=0, le=1, default=0.06, description="Selling costs as % of sale price")
    capital_gains_tax_rate: float = Field(ge=0, le=1, default=0.20, description="Capital gains tax rate")

class MarketAssumptions(BaseModel):
    """Market assumptions for analysis"""
    property_appreciation_rate: float = Field(default=0.03, description="Annual property appreciation rate")
    rent_growth_rate: float = Field(default=0.035, description="Annual rent growth rate (typically higher than property appreciation)")
    stock_market_return: float = Field(default=0.10, description="Annual stock market return")
    discount_rate: float = Field(default=0.08, description="Discount rate for NPV calculations")

class Analysis(BaseModel):
    """Complete analysis parameters"""
    property: Property
    expenses: Expenses
    sale_assumptions: SaleAssumptions
    market_assumptions: MarketAssumptions
    analysis_years: int = Field(ge=1, le=50, default=10, description="Years to analyze")