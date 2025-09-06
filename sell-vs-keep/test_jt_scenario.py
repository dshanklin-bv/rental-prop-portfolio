#!/usr/bin/env python3

import sys
sys.path.append('.')

from models import Analysis, Property, Expenses, MarketAssumptions, SaleAssumptions, Unit
from monthly_dcf_calculator import MonthlyDCFCalculator
from property_loader import PropertyLoader
from datetime import date

def test_jt_scenario():
    """Test the JT scenario with phase transitions"""
    
    loader = PropertyLoader()
    property_data = loader.load_property("239_eagle_dr_boone")
    
    if not property_data:
        print("❌ Could not load property data")
        return
    
    # Convert to models using JT scenario
    analysis = loader.property_to_models(property_data, "jt_scenario")
    
    # Test the calculator with JT scenario
    calculator = MonthlyDCFCalculator(analysis, "jt_scenario")
    
    print("=== JT SCENARIO ANALYSIS ===")
    print("Phase 1 (Years 1-2): Only Unit B at $2,200/month")
    print("Phase 2 (Years 3-10): Mom in Unit A at $1,500/month + Unit B at $2,300/month")
    
    # Test rent calculations at key months
    test_months = [0, 11, 23, 24, 35, 119]  # Start, end Y1, end Y2, start Y3, mid Y3, end Y10
    
    print(f"\n=== MONTHLY RENT TRANSITIONS ===")
    
    for month in test_months:
        years_elapsed = month / 12
        monthly_rent = calculator._get_monthly_rent(month, years_elapsed)
        
        year = int(years_elapsed) + 1
        month_in_year = (month % 12) + 1
        
        if month < 24:
            phase = "Phase 1"
            description = "Unit B only"
        else:
            phase = "Phase 2"  
            description = "Mom (Unit A) + Renter (Unit B)"
        
        print(f"Month {month+1:3d} (Year {year}, Month {month_in_year:2d}): ${monthly_rent:,.2f} - {phase} ({description})")
    
    # Run full DCF
    rental_dcf = calculator.calculate_monthly_rental_dcf()
    
    print(f"\n=== JT SCENARIO RESULTS ===")
    print(f"Final cash balance: ${rental_dcf['final_values']['final_cash_balance']:,.2f}")
    
    # Compare phase cash flows
    phase1_months = rental_dcf['monthly_data'][:24]  # First 24 months
    phase2_months = rental_dcf['monthly_data'][24:]  # Remaining months
    
    phase1_avg_rent = sum(m['monthly_rent'] for m in phase1_months) / len(phase1_months)
    phase2_avg_rent = sum(m['monthly_rent'] for m in phase2_months) / len(phase2_months)
    
    phase1_avg_cash_flow = sum(m['operating_cash_flow'] for m in phase1_months) / len(phase1_months)
    phase2_avg_cash_flow = sum(m['operating_cash_flow'] for m in phase2_months) / len(phase2_months)
    
    print(f"\nPhase 1 (Years 1-2) Averages:")
    print(f"  Average monthly rent: ${phase1_avg_rent:,.2f}")
    print(f"  Average monthly cash flow: ${phase1_avg_cash_flow:,.2f}")
    
    print(f"\nPhase 2 (Years 3-10) Averages:")
    print(f"  Average monthly rent: ${phase2_avg_rent:,.2f}")
    print(f"  Average monthly cash flow: ${phase2_avg_cash_flow:,.2f}")
    
    print(f"\nRent increase from Phase 1 to Phase 2: ${phase2_avg_rent - phase1_avg_rent:,.2f} (+{((phase2_avg_rent / phase1_avg_rent) - 1) * 100:.1f}%)")
    
    # Specific month checks
    print(f"\n=== PHASE TRANSITION VERIFICATION ===")
    month_23_data = rental_dcf['monthly_data'][23]  # Last month of Phase 1
    month_24_data = rental_dcf['monthly_data'][24]  # First month of Phase 2
    
    print(f"Month 24 (last of Phase 1): ${month_23_data['monthly_rent']:,.2f}")
    print(f"Month 25 (first of Phase 2): ${month_24_data['monthly_rent']:,.2f}")
    print(f"Rent jump: ${month_24_data['monthly_rent'] - month_23_data['monthly_rent']:,.2f}")

if __name__ == "__main__":
    test_jt_scenario()