#!/usr/bin/env python3

import sys
sys.path.append('.')

from property_loader import PropertyLoader
from risk_analyzer import RiskAnalyzer

def test_risk_analysis():
    """Test risk analysis for different scenarios"""
    
    loader = PropertyLoader()
    property_data = loader.load_property("239_eagle_dr_boone")
    
    scenarios_to_test = [
        ("both_units", "Both Units Rented"),
        ("jt_scenario", "JT Family Scenario"),
        ("unit_b_only", "Unit B Only")
    ]
    
    for scenario_name, scenario_description in scenarios_to_test:
        print(f"\n{'='*60}")
        print(f"RISK ANALYSIS: {scenario_description}")
        print(f"{'='*60}")
        
        # Convert to models
        analysis = loader.property_to_models(property_data, scenario_name)
        
        # Create risk analyzer
        risk_analyzer = RiskAnalyzer(analysis, scenario_name)
        
        # Run comprehensive risk analysis
        risk_report = risk_analyzer.comprehensive_risk_report()
        
        # Display results
        print(f"\n=== VACANCY RISK ANALYSIS ===")
        monthly_cost = risk_report['risk_summary']['monthly_carrying_cost']
        print(f"Monthly carrying cost (no rent): ${monthly_cost:,.2f}")
        
        print(f"\nVacancy scenarios (6-month vacancy starting at different times):")
        
        for scenario in risk_report['vacancy_analysis']['vacancy_scenarios']:
            start_month = scenario['vacancy_start_month']
            max_shortfall = scenario['max_cash_shortfall']
            total_shortfall = scenario['total_cash_shortfall']
            
            if max_shortfall > 0:
                print(f"  Month {start_month:2d}: MAX SHORTFALL ${max_shortfall:,.0f}, Total shortfall: ${total_shortfall:,.0f} ⚠️")
            else:
                print(f"  Month {start_month:2d}: No cash shortfall ✅")
        
        print(f"\n=== PROPERTY VALUE SHOCK ANALYSIS ===")
        current_value = risk_report['property_value_shock_analysis']['current_property_value']
        current_ltv = risk_report['property_value_shock_analysis']['current_ltv']
        print(f"Current property value: ${current_value:,.0f}")
        print(f"Current LTV ratio: {current_ltv:.1%}")
        
        for shock in risk_report['property_value_shock_analysis']['shock_scenarios']:
            shock_pct = shock['shock_percentage']
            new_value = shock['shocked_property_value']
            new_ltv = shock['new_ltv_ratio']
            equity_loss = shock['equity_loss']
            
            status = ""
            if shock['is_underwater']:
                status = "🔴 UNDERWATER"
            elif not shock['can_refinance']:
                status = "🟡 NO REFI"
            else:
                status = "🟢 OK"
            
            print(f"  {shock_pct:3d}% decline: ${new_value:,.0f}, LTV {new_ltv:.1%}, Equity loss ${equity_loss:,.0f} {status}")
        
        print(f"\n=== RISK SUMMARY ===")
        summary = risk_report['risk_summary']
        print(f"Cash flexibility score: {summary['cash_flexibility_score']}")
        print(f"Recommended emergency fund: ${summary['recommended_emergency_fund']:,.0f}")
        
        if summary['high_risk_factors']:
            print(f"\n🚨 HIGH RISK FACTORS:")
            for risk in summary['high_risk_factors']:
                print(f"  - {risk}")
        else:
            print(f"\n✅ No major risk factors identified")

if __name__ == "__main__":
    test_risk_analysis()