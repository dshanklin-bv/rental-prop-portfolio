#!/usr/bin/env python3

import sys
sys.path.append('.')

from models import Analysis, Property, Expenses, MarketAssumptions, SaleAssumptions, Unit
from monthly_dcf_calculator import MonthlyDCFCalculator
from datetime import date

def test_quarterly_tax_details():
    """Test the quarterly tax calculations with depreciation details"""
    
    # Create test analysis data
    units = [
        Unit(number="Unit A", bedrooms=2, bathrooms=2.0, monthly_rent=2250),
        Unit(number="Unit B", bedrooms=2, bathrooms=2.0, monthly_rent=2250)
    ]
    
    property_data = Property(
        address="239 Eagle Dr, Boone, NC",
        current_value=950000,
        original_purchase_price=750000,
        cost_basis=780000,
        purchase_date=date(2020, 6, 15),
        mortgage_balance=554825,
        units=units
    )
    
    expenses = Expenses(
        property_tax_monthly=650,
        insurance_monthly=150,
        mortgage_payment=2783.80,
        maintenance_percent=0.05,
        vacancy_percent=0.05,
        management_percent=0.08,
        other_monthly=200
    )
    
    market_assumptions = MarketAssumptions(
        property_appreciation_rate=0.03,
        stock_market_return=0.075,
        discount_rate=0.08
    )
    
    sale_assumptions = SaleAssumptions(
        selling_costs_percent=0.075,
        capital_gains_tax_rate=0.20
    )
    
    analysis = Analysis(
        property=property_data,
        expenses=expenses,
        sale_assumptions=sale_assumptions,
        market_assumptions=market_assumptions,
        analysis_years=10
    )
    
    # Test the calculator
    calculator = MonthlyDCFCalculator(analysis)
    rental_dcf = calculator.calculate_monthly_rental_dcf()
    
    # Calculate annual depreciation to verify
    annual_depreciation = calculator._calculate_annual_depreciation()
    monthly_depreciation = annual_depreciation / 12
    
    print(f"=== DEPRECIATION ANALYSIS ===")
    print(f"Cost Basis: ${property_data.cost_basis:,}")
    print(f"Depreciable Basis (80% of cost): ${property_data.cost_basis * 0.8:,}")
    print(f"Annual Depreciation (27.5 years): ${annual_depreciation:,.2f}")
    print(f"Monthly Depreciation: ${monthly_depreciation:,.2f}")
    
    print(f"\n=== QUARTERLY TAX ANALYSIS ===")
    
    # Look at first quarter (months 1-3) when quarterly tax is paid in March (month 3)
    quarterly_months = [2]  # March is month 3 (0-indexed = 2)
    
    for q_month in quarterly_months:
        month_data = rental_dcf['monthly_data'][q_month]
        
        print(f"\nQuarter ending {month_data['month_name']} {month_data['year']}:")
        
        # Calculate what the quarterly amounts should be
        # Get the 3 months of data for this quarter
        q1_months = rental_dcf['monthly_data'][0:3]  # Jan, Feb, Mar
        
        total_rent = sum(m['monthly_rent'] for m in q1_months)
        total_expenses = sum(m['operating_expenses'] for m in q1_months)
        total_interest = sum(m['interest_payment'] for m in q1_months)
        total_depreciation = monthly_depreciation * 3
        
        quarterly_taxable = total_rent - total_expenses - total_interest - total_depreciation
        expected_tax = quarterly_taxable * 0.3625 if quarterly_taxable > 0 else 0
        
        print(f"  Quarterly Rental Income: ${total_rent:,.2f}")
        print(f"  Quarterly Operating Expenses: ${total_expenses:,.2f}")
        print(f"  Quarterly Interest: ${total_interest:,.2f}")
        print(f"  Quarterly Depreciation: ${total_depreciation:,.2f}")
        print(f"  Quarterly Taxable Income: ${quarterly_taxable:,.2f}")
        print(f"  Expected Tax (36.25%): ${expected_tax:,.2f}")
        print(f"  Actual Tax Paid: ${month_data['quarterly_tax_payment']:,.2f}")
        
        if abs(expected_tax - month_data['quarterly_tax_payment']) < 0.01:
            print(f"  ✅ Tax calculation CORRECT")
        else:
            print(f"  ❌ Tax calculation INCORRECT - Difference: ${abs(expected_tax - month_data['quarterly_tax_payment']):,.2f}")
    
    print(f"\n=== CASH FLOW IMPACT ===")
    print(f"Without proper depreciation, taxes would be much higher.")
    print(f"Depreciation saves approximately ${monthly_depreciation * 0.3625:,.2f} per month in taxes")
    print(f"Annual tax savings from depreciation: ${annual_depreciation * 0.3625:,.2f}")

if __name__ == "__main__":
    test_quarterly_tax_details()