#!/usr/bin/env python3

import sys
sys.path.append('.')

from property_loader import PropertyLoader
from monthly_dcf_calculator import MonthlyDCFCalculator
from risk_analyzer import RiskAnalyzer

def test_taylor_scenario():
    """Test the new Taylor scenario and compare with existing scenarios"""
    
    loader = PropertyLoader()
    property_data = loader.load_property("239_eagle_dr_boone")
    
    scenarios_to_compare = [
        ("both_units", "Both Units Rented (Original)"),
        ("taylor_scenario", "Taylor Scenario ($2,500 + $2,200)"),
        ("premium_rents", "Premium Rents"),
        ("jt_scenario", "JT Family Scenario")
    ]
    
    print("=" * 80)
    print("SCENARIO COMPARISON: Monthly Rents and Risk Analysis")
    print("=" * 80)
    
    results = []
    
    for scenario_name, scenario_description in scenarios_to_compare:
        print(f"\n🏠 {scenario_description}")
        print("-" * 60)
        
        # Convert to models
        analysis = loader.property_to_models(property_data, scenario_name)
        
        # Run DCF calculation
        calculator = MonthlyDCFCalculator(analysis, scenario_name)
        comparison = calculator.compare_scenarios()
        
        # Run risk analysis
        risk_analyzer = RiskAnalyzer(analysis, scenario_name)
        risk_report = risk_analyzer.comprehensive_risk_report()
        
        # Extract key metrics
        rental_scenario = comparison['rental_scenario']
        final_cash = rental_scenario['dcf']['final_values']['final_cash_balance']
        total_return = rental_scenario['total_return']
        
        # Get rent info
        starting_rent = rental_scenario['dcf']['monthly_data'][0]['monthly_rent']
        final_rent = rental_scenario['dcf']['monthly_data'][-1]['monthly_rent']
        
        # Risk metrics
        risk_summary = risk_report['risk_summary']
        cash_flexibility = risk_summary['cash_flexibility_score']
        max_shortfall = risk_summary['max_vacancy_cash_shortfall']
        
        print(f"Starting Monthly Rent: ${starting_rent:,.2f}")
        print(f"Final Monthly Rent:    ${final_rent:,.2f} (+{((final_rent/starting_rent)-1)*100:.1f}%)")
        print(f"Final Cash Balance:    ${final_cash:,.0f}")
        print(f"Total Return:          ${total_return:,.0f}")
        print(f"Max Vacancy Shortfall: ${max_shortfall:,.0f}")
        print(f"Cash Flexibility:      {cash_flexibility}")
        
        results.append({
            'scenario': scenario_description,
            'starting_rent': starting_rent,
            'final_cash': final_cash,
            'total_return': total_return,
            'max_shortfall': max_shortfall,
            'flexibility': cash_flexibility
        })
    
    # Summary comparison
    print(f"\n" + "=" * 80)
    print("RANKING BY TOTAL RETURN")
    print("=" * 80)
    
    # Sort by total return
    sorted_results = sorted(results, key=lambda x: x['total_return'], reverse=True)
    
    for i, result in enumerate(sorted_results, 1):
        flexibility_icon = "🟢" if "EXCELLENT" in result['flexibility'] else \
                          "🟡" if "GOOD" in result['flexibility'] or "MODERATE" in result['flexibility'] else "🔴"
        
        print(f"{i}. {result['scenario']:30} | ${result['total_return']:>8,.0f} | ${result['starting_rent']:>6.0f}/mo | {flexibility_icon}")
    
    # Find Taylor scenario specifically
    taylor_result = next((r for r in results if "Taylor" in r['scenario']), None)
    if taylor_result:
        print(f"\n🎯 TAYLOR SCENARIO DETAILS:")
        print(f"   Unit A (upstairs): $2,500/month")
        print(f"   Unit B (downstairs): $2,200/month") 
        print(f"   Total: ${taylor_result['starting_rent']:,.0f}/month")
        print(f"   10-year return: ${taylor_result['total_return']:,.0f}")
        print(f"   Cash flexibility: {taylor_result['flexibility']}")

if __name__ == "__main__":
    test_taylor_scenario()