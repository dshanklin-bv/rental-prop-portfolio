#!/usr/bin/env python3

import sys
sys.path.append('.')

from models import Analysis, Property, Expenses, MarketAssumptions, SaleAssumptions, Unit
from monthly_dcf_calculator import MonthlyDCFCalculator
from datetime import date

def test_monthly_dcf_calculator():
    """Test the monthly DCF calculator with sample data"""
    
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
        mortgage_payment=2783.80,  # From Wells Fargo statement
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
        market_assumptions=market_assumptions,
        sale_assumptions=sale_assumptions,
        analysis_years=10
    )
    
    # Test the calculator
    calculator = MonthlyDCFCalculator(analysis)
    
    print("Testing rental DCF calculation...")
    try:
        rental_dcf = calculator.calculate_monthly_rental_dcf()
        print(f"✓ Rental DCF calculated successfully")
        print(f"  - Monthly data points: {len(rental_dcf['monthly_data'])}")
        print(f"  - Final cash balance: ${rental_dcf['final_values']['final_cash_balance']:,.2f}")
        print(f"  - Final property value: ${rental_dcf['final_values']['final_property_value']:,.2f}")
        
        # Show first few months
        print(f"\nFirst 3 months of rental DCF:")
        for i in range(min(3, len(rental_dcf['monthly_data']))):
            month = rental_dcf['monthly_data'][i]
            print(f"  Month {month['month']}: Rent=${month['monthly_rent']:,.2f}, Cash Flow=${month['operating_cash_flow']:,.2f}, Cash Balance=${month['cash_balance']:,.2f}")
            
    except Exception as e:
        print(f"✗ Error in rental DCF: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTesting stock DCF calculation...")
    try:
        stock_dcf = calculator.calculate_monthly_stock_dcf()
        print(f"✓ Stock DCF calculated successfully")
        print(f"  - Initial investment: ${stock_dcf['initial_investment']:,.2f}")
        print(f"  - Final stock value: ${stock_dcf['final_stock_value']:,.2f}")
        print(f"  - Total gains: ${stock_dcf['total_stock_gains']:,.2f}")
        
    except Exception as e:
        print(f"✗ Error in stock DCF: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTesting scenario comparison...")
    try:
        comparison = calculator.compare_scenarios()
        print(f"✓ Comparison calculated successfully")
        print(f"  - Recommendation: {comparison['comparison']['recommendation']}")
        print(f"  - Rental total return: ${comparison['rental_scenario']['total_return']:,.2f}")
        print(f"  - Stock total return: ${comparison['stock_scenario']['total_return']:,.2f}")
        print(f"  - Advantage: ${comparison['comparison']['advantage_amount']:,.2f} ({comparison['comparison']['advantage_percent']:.1%})")
        
    except Exception as e:
        print(f"✗ Error in comparison: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_monthly_dcf_calculator()