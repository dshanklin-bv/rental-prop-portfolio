#!/usr/bin/env python3

import sys
sys.path.append('.')

from property_loader import PropertyLoader
from monthly_dcf_calculator import MonthlyDCFCalculator
import pandas as pd

def test_escrow_details():
    """Test escrow balance tracking"""
    
    loader = PropertyLoader()
    property_data = loader.load_property("239_eagle_dr_boone")
    analysis = loader.property_to_models(property_data, "taylor_scenario")
    
    calculator = MonthlyDCFCalculator(analysis, "taylor_scenario")
    comparison = calculator.compare_scenarios()
    
    # Get first 24 months to see escrow activity
    rental_data = comparison['rental_scenario']['dcf']['monthly_data'][:24]
    
    print("FIRST 24 MONTHS - ESCROW TRACKING")
    print("=" * 120)
    
    df = pd.DataFrame(rental_data)
    
    # Show key escrow columns
    display_cols = ['date', 'month_name', 'escrow_payment', 'escrow_balance', 
                   'property_tax_payment', 'insurance_payment', 'mortgage_pi_payment']
    
    for i, row in df[display_cols].iterrows():
        date = row['date']
        month = row['month_name']
        escrow_pay = row['escrow_payment']
        escrow_bal = row['escrow_balance']
        tax_pay = row['property_tax_payment']
        ins_pay = row['insurance_payment']
        pi_pay = row['mortgage_pi_payment']
        
        # Show payments when they occur
        payments = ""
        if tax_pay > 0:
            payments += f" | TAX: ${tax_pay:,.0f}"
        if ins_pay > 0:
            payments += f" | INS: ${ins_pay:,.0f}"
        
        print(f"{date} {month:>3}: Escrow +${escrow_pay:>6.0f} = ${escrow_bal:>7,.0f} | P&I: ${pi_pay:>6.0f}{payments}")

if __name__ == "__main__":
    test_escrow_details()