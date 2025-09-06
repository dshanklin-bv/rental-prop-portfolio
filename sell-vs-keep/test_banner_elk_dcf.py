#!/usr/bin/env python3

import sys
sys.path.append('.')

from property_loader import PropertyLoader
from monthly_dcf_calculator import MonthlyDCFCalculator

def test_banner_elk_dcf():
    """Test DCF calculation for Banner Elk property"""
    
    loader = PropertyLoader()
    property_data = loader.load_property('144_grandfather_farms_banner_elk')
    
    scenarios_to_test = ['traditional_ltr', 'grandfather_str', 'seasonal_hybrid']
    
    print("=== BANNER ELK DCF ANALYSIS ===\n")
    
    for scenario_name in scenarios_to_test:
        print(f"🏠 {scenario_name.replace('_', ' ').title()}")
        print("-" * 50)
        
        # Convert to models
        analysis = loader.property_to_models(property_data, scenario_name)
        
        # Run DCF calculation
        calculator = MonthlyDCFCalculator(analysis, scenario_name)
        comparison = calculator.compare_scenarios()
        
        # Extract key metrics
        rental_scenario = comparison['rental_scenario']
        final_cash = rental_scenario['dcf']['final_values']['final_cash_balance']
        total_return = rental_scenario['total_return']
        
        # Get rent info
        starting_rent = rental_scenario['dcf']['monthly_data'][0]['monthly_rent']
        final_rent = rental_scenario['dcf']['monthly_data'][-1]['monthly_rent']
        
        print(f"Starting Monthly Rent: ${starting_rent:,.0f}")
        print(f"Final Monthly Rent:    ${final_rent:,.0f} (+{((final_rent/starting_rent)-1)*100:.1f}%)")
        print(f"Final Cash Balance:    ${final_cash:,.0f}")
        print(f"Total Return:          ${total_return:,.0f}")
        print()

if __name__ == "__main__":
    test_banner_elk_dcf()