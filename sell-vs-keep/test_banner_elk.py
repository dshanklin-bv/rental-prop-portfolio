#!/usr/bin/env python3

import sys
sys.path.append('.')

from property_loader import PropertyLoader

def test_banner_elk_property():
    """Test Banner Elk property loading and scenarios"""
    
    loader = PropertyLoader()
    property_data = loader.load_property('144_grandfather_farms_banner_elk')
    
    if not property_data:
        print("Failed to load property data")
        return
    
    print("=== BANNER ELK PROPERTY LOADED ===")
    print(f"Name: {property_data['name']}")
    print(f"Address: {property_data['address']}")
    print(f"Value: ${property_data['financial_details']['current_market_value']:,}")
    print()
    
    scenarios = property_data.get('scenarios', {})
    print("Available scenarios:")
    for key, scenario in scenarios.items():
        print(f"- {key}: {scenario.get('description', 'No description')}")
        if 'total_monthly_rent' in scenario:
            print(f"  Monthly rent: ${scenario['total_monthly_rent']:,.0f}")
        print()
    
    # Test converting to models
    print("=== TESTING MODEL CONVERSION ===")
    for scenario_name in list(scenarios.keys())[:2]:  # Test first 2 scenarios
        try:
            analysis = loader.property_to_models(property_data, scenario_name)
            print(f"✅ {scenario_name}: ${analysis.property.total_monthly_rent:,.0f}/month")
        except Exception as e:
            print(f"❌ {scenario_name}: Error - {e}")
    
if __name__ == "__main__":
    test_banner_elk_property()