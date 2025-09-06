import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from models import Analysis, MarketAssumptions, SaleAssumptions

@dataclass
class PropertyScenario:
    """Property sale and appreciation scenario"""
    name: str
    description: str
    sale_price: float
    appreciation_rate: float
    holding_period_years: int
    selling_costs_pct: float
    notes: str = ""

@dataclass  
class RentalScenario:
    """Rental income scenario"""
    name: str
    description: str
    unit_a_rent: float
    unit_b_rent: float
    vacancy_rate: float
    rent_growth_rate: float
    management_fee_pct: float
    notes: str = ""

@dataclass
class StockScenario:
    """Stock market investment scenario"""
    name: str
    description: str
    annual_return: float
    volatility: float
    tax_treatment: str
    dividend_yield: float
    rebalancing_costs: float
    notes: str = ""

@dataclass
class TaxScenario:
    """Tax treatment scenario"""
    name: str
    description: str
    state_income_tax_rate: float
    state_capital_gains_rate: float
    federal_capital_gains_rate: float
    depreciation_recapture_rate: float
    property_tax_deductible: bool = True
    mortgage_interest_deductible: bool = True
    primary_residence_exclusion: float = 0.0
    notes: str = ""

@dataclass
class CombinedScenario:
    """Combined scenario linking all scenario types"""
    name: str
    property_scenario: str
    rental_scenario: str
    stock_scenario: str
    tax_scenario: str
    description: str

class ScenarioManager:
    """Manage and combine different scenario types"""
    
    def __init__(self, scenarios_file: str = "properties/239_eagle_dr_scenarios.json"):
        self.scenarios_file = Path(scenarios_file)
        self.scenarios_data = self._load_scenarios()
    
    def _load_scenarios(self) -> Dict:
        """Load scenarios from JSON file"""
        if not self.scenarios_file.exists():
            return {}
        
        try:
            with open(self.scenarios_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading scenarios: {e}")
            return {}
    
    def get_property_scenarios(self) -> List[PropertyScenario]:
        """Get all property scenarios"""
        scenarios = []
        for key, data in self.scenarios_data.get('property_scenarios', {}).items():
            scenarios.append(PropertyScenario(**data))
        return scenarios
    
    def get_rental_scenarios(self) -> List[RentalScenario]:
        """Get all rental scenarios"""
        scenarios = []
        for key, data in self.scenarios_data.get('rental_scenarios', {}).items():
            scenarios.append(RentalScenario(**data))
        return scenarios
    
    def get_stock_scenarios(self) -> List[StockScenario]:
        """Get all stock market scenarios"""
        scenarios = []
        for key, data in self.scenarios_data.get('stock_market_scenarios', {}).items():
            scenarios.append(StockScenario(**data))
        return scenarios
    
    def get_tax_scenarios(self) -> List[TaxScenario]:
        """Get all tax scenarios"""
        scenarios = []
        for key, data in self.scenarios_data.get('tax_scenarios', {}).items():
            # Filter data to only include fields that TaxScenario expects
            valid_fields = ['name', 'description', 'state_income_tax_rate', 
                          'state_capital_gains_rate', 'federal_capital_gains_rate', 
                          'depreciation_recapture_rate', 'property_tax_deductible', 
                          'mortgage_interest_deductible', 'primary_residence_exclusion', 'notes']
            filtered_data = {k: v for k, v in data.items() if k in valid_fields}
            scenarios.append(TaxScenario(**filtered_data))
        return scenarios
    
    def get_combined_scenarios(self) -> List[CombinedScenario]:
        """Get predefined combined scenarios"""
        scenarios = []
        for key, data in self.scenarios_data.get('combined_scenarios', {}).items():
            scenarios.append(CombinedScenario(**data))
        return scenarios
    
    def build_analysis_from_scenarios(self, 
                                    base_analysis: Analysis,
                                    property_scenario_name: str,
                                    rental_scenario_name: str, 
                                    stock_scenario_name: str,
                                    tax_scenario_name: str) -> Analysis:
        """Build complete Analysis object from scenario selections"""
        
        # Get scenario data
        prop_data = self.scenarios_data['property_scenarios'][property_scenario_name]
        rental_data = self.scenarios_data['rental_scenarios'][rental_scenario_name]
        stock_data = self.scenarios_data['stock_market_scenarios'][stock_scenario_name]
        tax_data = self.scenarios_data['tax_scenarios'][tax_scenario_name]
        
        # Update property value and units
        base_analysis.property.current_value = prop_data['sale_price']
        base_analysis.property.units[0].monthly_rent = rental_data['unit_a_rent']
        base_analysis.property.units[1].monthly_rent = rental_data['unit_b_rent']
        
        # Update market assumptions
        base_analysis.market_assumptions.property_appreciation_rate = prop_data['appreciation_rate']
        base_analysis.market_assumptions.stock_market_return = stock_data['annual_return']
        
        # Update sale assumptions
        base_analysis.sale_assumptions.selling_costs_percent = prop_data['selling_costs_pct']
        
        # Calculate capital gains tax rate with primary residence exclusion
        capital_gain = base_analysis.property.capital_gain
        primary_exclusion = tax_data.get('primary_residence_exclusion', 0)
        
        if primary_exclusion > 0 and capital_gain > 0:
            # Apply primary residence exclusion to federal tax only
            taxable_federal_gain = max(0, capital_gain - primary_exclusion)
            federal_tax = taxable_federal_gain * tax_data['federal_capital_gains_rate']
            
            # State tax applies to full gain
            state_tax = capital_gain * tax_data['state_capital_gains_rate']
            
            # Calculate effective tax rate
            total_tax = federal_tax + state_tax
            effective_rate = total_tax / capital_gain if capital_gain > 0 else 0
        else:
            # No exclusion - use standard rates
            effective_rate = tax_data['federal_capital_gains_rate'] + tax_data['state_capital_gains_rate']
        
        base_analysis.sale_assumptions.capital_gains_tax_rate = effective_rate
        
        # Update expenses with rental scenario
        base_analysis.expenses.vacancy_percent = rental_data['vacancy_rate']
        base_analysis.expenses.management_percent = rental_data['management_fee_pct']
        
        # Update analysis period
        base_analysis.analysis_years = prop_data['holding_period_years']
        
        return base_analysis
    
    def calculate_effective_tax_rates(self, tax_scenario_name: str, income_type: str) -> float:
        """Calculate effective tax rates for different income types"""
        tax_data = self.scenarios_data['tax_scenarios'][tax_scenario_name]
        
        if income_type == "rental_income":
            # Rental income taxed as ordinary income
            return tax_data['federal_capital_gains_rate'] + tax_data['state_income_tax_rate']
        elif income_type == "capital_gains":
            # Long-term capital gains
            return tax_data['federal_capital_gains_rate'] + tax_data['state_capital_gains_rate']
        elif income_type == "depreciation_recapture":
            # Depreciation recapture
            return tax_data['depreciation_recapture_rate'] + tax_data['state_capital_gains_rate']
        else:
            return tax_data['federal_capital_gains_rate']
    
    def compare_scenarios(self, base_analysis: Analysis, scenario_combinations: List[Tuple]) -> Dict:
        """Compare multiple scenario combinations"""
        from calculator import SellVsKeepCalculator
        
        results = {}
        
        for combo in scenario_combinations:
            prop_scenario, rental_scenario, stock_scenario, tax_scenario = combo
            
            # Build analysis for this combination (use Pydantic copy method)
            import copy
            analysis_copy = copy.deepcopy(base_analysis)
            analysis = self.build_analysis_from_scenarios(
                analysis_copy,
                prop_scenario, rental_scenario, stock_scenario, tax_scenario
            )
            
            # Calculate results
            calculator = SellVsKeepCalculator(analysis)
            scenario_results = calculator.get_recommendation()
            
            combo_name = f"{prop_scenario}_{rental_scenario}_{stock_scenario}_{tax_scenario}"
            results[combo_name] = {
                'analysis': analysis,
                'results': scenario_results,
                'scenario_names': {
                    'property': prop_scenario,
                    'rental': rental_scenario, 
                    'stock': stock_scenario,
                    'tax': tax_scenario
                }
            }
        
        return results
    
    def get_scenario_summary(self) -> Dict:
        """Get summary of all available scenarios"""
        return {
            'property_scenarios': len(self.scenarios_data.get('property_scenarios', {})),
            'rental_scenarios': len(self.scenarios_data.get('rental_scenarios', {})),
            'stock_scenarios': len(self.scenarios_data.get('stock_market_scenarios', {})),
            'tax_scenarios': len(self.scenarios_data.get('tax_scenarios', {})),
            'combined_scenarios': len(self.scenarios_data.get('combined_scenarios', {}))
        }