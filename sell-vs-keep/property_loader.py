import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from models import Property, Unit, Expenses, SaleAssumptions, MarketAssumptions, Analysis

class PropertyLoader:
    """Load property data from JSON files"""
    
    def __init__(self, properties_dir: str = "properties"):
        self.properties_dir = Path(properties_dir)
    
    def list_properties(self) -> List[Dict[str, str]]:
        """List all available property JSON files"""
        properties = []
        
        if not self.properties_dir.exists():
            return properties
            
        for json_file in self.properties_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                    # Only include files that look like property files (have name and address)
                    if 'name' in data and 'address' in data:
                        properties.append({
                            'file': json_file.stem,
                            'name': data.get('name', json_file.stem),
                            'address': data.get('address', 'Unknown'),
                            'property_id': data.get('property_id', json_file.stem)
                        })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
                
        return properties
    
    def load_property(self, property_file: str) -> Optional[Dict]:
        """Load a specific property JSON file"""
        file_path = self.properties_dir / f"{property_file}.json"
        
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading property {property_file}: {e}")
            return None
    
    def property_to_models(self, property_data: Dict, scenario: str = "base_case") -> Analysis:
        """Convert JSON property data to Pydantic models"""
        
        # Convert units
        units = []
        scenario_data = property_data.get('scenarios', {}).get(scenario, {})
        
        for unit_data in property_data.get('units', []):
            rental_info = unit_data.get('rental_info', {})
            unit_id = unit_data.get('unit_id', '')
            
            # Use scenario-specific rent if available
            if scenario_data:
                # Check if scenario uses total_monthly_rent (single unit properties like Banner Elk)
                if 'total_monthly_rent' in scenario_data and len(property_data.get('units', [])) == 1:
                    rent = scenario_data.get('total_monthly_rent', 0)
                # Handle multi-phase JT scenario (use phase 1 rent for initial setup)
                elif scenario == "jt_scenario" and 'phase_1' in scenario_data:
                    phase1_data = scenario_data['phase_1']
                    if unit_id == 'unit_a':
                        rent = phase1_data.get('unit_a_rent', 0)
                    elif unit_id == 'unit_b':
                        rent = phase1_data.get('unit_b_rent', 0)
                    else:
                        rent = 0
                # Handle dual-unit properties (Eagle Drive style)
                elif unit_id == 'unit_a':
                    rent = scenario_data.get('unit_a_rent', rental_info.get('market_rent', 0))
                elif unit_id == 'unit_b':
                    rent = scenario_data.get('unit_b_rent', rental_info.get('market_rent', 0))
                else:
                    # Legacy support for old naming
                    if scenario == "unit_a_only" and 'mil_suite' in unit_id:
                        rent = 0
                    elif scenario == "optimistic":
                        rent = rental_info.get('market_rent', 0) * 1.15
                    else:
                        rent = rental_info.get('market_rent', 0)
            else:
                rent = rental_info.get('market_rent', 0)
            
            units.append(Unit(
                number=unit_data['unit_name'],
                bedrooms=unit_data['bedrooms'],
                bathrooms=unit_data['bathrooms'],
                monthly_rent=rent
            ))
        
        # Convert property
        financial = property_data.get('financial_details', {})
        property_model = Property(
            address=property_data.get('address', ''),
            current_value=financial.get('current_market_value', 0),
            original_purchase_price=financial.get('original_purchase_price', 0),
            cost_basis=financial.get('cost_basis', financial.get('original_purchase_price', 0)),
            purchase_date=datetime.strptime(financial.get('purchase_date', '2020-01-01'), '%Y-%m-%d').date(),
            mortgage_balance=financial.get('current_mortgage_balance', 0),
            units=units
        )
        
        # Convert expenses
        exp_data = property_data.get('expenses', {})
        
        # Mortgage payment includes both P&I + escrow
        mortgage_data = exp_data.get('mortgage', {})
        mortgage_payment = mortgage_data.get('total_payment', 0)  # Full payment including escrow
        escrow_payment = mortgage_data.get('escrow_payment', 0)
        
        expenses_model = Expenses(
            property_tax_monthly=exp_data.get('property_tax', {}).get('monthly_amount', 0),
            property_tax_annual=exp_data.get('property_tax', {}).get('annual_amount', 0),
            insurance_monthly=exp_data.get('insurance', {}).get('monthly_amount', 0),
            insurance_annual=exp_data.get('insurance', {}).get('annual_amount', 0),
            mortgage_payment=mortgage_payment,
            mortgage_escrow=escrow_payment,
            maintenance_percent=exp_data.get('maintenance_reserve', {}).get('percentage_of_rent', 0.05),
            vacancy_percent=exp_data.get('vacancy_allowance', {}).get('percentage_of_rent', 0.05),
            management_percent=exp_data.get('property_management', {}).get('percentage_of_rent', 0),
            other_monthly=exp_data.get('utilities', {}).get('monthly_amount', 0) + 
                         exp_data.get('other_expenses', {}).get('monthly_amount', 0)
        )
        
        # Convert sale assumptions
        sale_data = property_data.get('sale_assumptions', {})
        sale_assumptions = SaleAssumptions(
            selling_costs_percent=sale_data.get('selling_costs_percentage', 0.06),
            capital_gains_tax_rate=sale_data.get('capital_gains_tax_rate', 0.20)
        )
        
        # Convert market assumptions
        market_data = property_data.get('market_assumptions', {})
        market_assumptions = MarketAssumptions(
            property_appreciation_rate=market_data.get('property_appreciation_rate', 0.03),
            rent_growth_rate=market_data.get('rent_growth_rate', 0.035),  # Default 0.5% higher than property
            stock_market_return=market_data.get('stock_market_return', 0.075),  # From JSON or conservative default
            discount_rate=0.08  # Default
        )
        
        return Analysis(
            property=property_model,
            expenses=expenses_model,
            sale_assumptions=sale_assumptions,
            market_assumptions=market_assumptions,
            analysis_years=10
        )
    
    def get_property_summary(self, property_data: Dict) -> Dict[str, any]:
        """Get summary info about a property"""
        financial = property_data.get('financial_details', {})
        total_rent = sum(
            unit.get('rental_info', {}).get('market_rent', 0) 
            for unit in property_data.get('units', [])
        )
        
        return {
            'name': property_data.get('name', 'Unknown'),
            'address': property_data.get('address', 'Unknown'),
            'current_value': financial.get('current_market_value', 0),
            'purchase_price': financial.get('original_purchase_price', 0),
            'cost_basis': financial.get('cost_basis', financial.get('original_purchase_price', 0)),
            'mortgage_balance': financial.get('current_mortgage_balance', 0),
            'total_units': len(property_data.get('units', [])),
            'total_monthly_rent': total_rent,
            'property_type': property_data.get('property_type', 'Unknown'),
            'year_built': property_data.get('physical_details', {}).get('year_built', 'Unknown')
        }
    
    def create_amortization_schedule(self, loan_amount: float, rate: float, 
                                   term_years: int, start_date: str) -> List[Dict]:
        """Create loan amortization schedule - placeholder for your amort info"""
        # You mentioned you have amort info - this is where we'd integrate it
        schedule = []
        monthly_rate = rate / 12
        num_payments = term_years * 12
        
        if loan_amount > 0:
            # Calculate monthly payment
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                            ((1 + monthly_rate)**num_payments - 1)
            
            balance = loan_amount
            for month in range(1, num_payments + 1):
                interest_payment = balance * monthly_rate
                principal_payment = monthly_payment - interest_payment
                balance -= principal_payment
                
                schedule.append({
                    'month': month,
                    'payment': monthly_payment,
                    'principal': principal_payment,
                    'interest': interest_payment,
                    'balance': balance
                })
        
        return schedule