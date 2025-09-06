#!/usr/bin/env python3

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import random
from monthly_dcf_calculator import MonthlyDCFCalculator
from models import Analysis

class RiskAnalyzer:
    """Analyze downside risks including vacancy, property value shocks, and cash flexibility"""
    
    def __init__(self, analysis: Analysis, scenario_name: str = ""):
        self.analysis = analysis
        self.scenario_name = scenario_name
        self.calculator = MonthlyDCFCalculator(analysis, scenario_name)
        
    def analyze_vacancy_risk(self, vacancy_months: int = 6) -> Dict:
        """Analyze impact of extended vacancy on cash flow and mortgage coverage"""
        
        # Get baseline DCF
        baseline = self.calculator.calculate_monthly_rental_dcf()
        baseline_cash_balance = baseline['final_values']['final_cash_balance']
        
        # Simulate vacancy starting in month 6 (after initial cash is established)
        monthly_data = baseline['monthly_data'].copy()
        
        # Calculate monthly mortgage payment (P&I only)
        mortgage_payment = self.analysis.expenses.mortgage_payment
        property_tax = self.analysis.expenses.property_tax_monthly
        insurance = self.analysis.expenses.insurance_monthly
        other_expenses = self.analysis.expenses.other_monthly
        
        # Monthly carrying costs during vacancy
        monthly_carrying_cost = mortgage_payment + property_tax + insurance + other_expenses
        
        results = []
        
        for vacancy_start_month in [6, 12, 24, 36]:  # Test vacancy at different times
            # Clone the monthly data
            scenario_data = [m.copy() for m in monthly_data]
            cash_balance = 20000  # Reset to starting balance
            
            # Apply vacancy
            for month in range(len(scenario_data)):
                month_data = scenario_data[month]
                
                # Recalculate cash balance with vacancy applied
                if vacancy_start_month <= month < vacancy_start_month + vacancy_months:
                    # During vacancy - no rental income
                    month_data['monthly_rent'] = 0
                    month_data['operating_cash_flow'] = -monthly_carrying_cost
                    month_data['is_vacant'] = True
                else:
                    month_data['is_vacant'] = False
                
                # Update cash balance
                cash_balance += month_data['operating_cash_flow']
                cash_balance += month_data['cash_interest_earned']
                cash_balance -= month_data['quarterly_tax_payment']
                
                month_data['cash_balance_with_vacancy'] = cash_balance
                
                # Check if cash balance goes negative
                if cash_balance < 0:
                    month_data['requires_cash_injection'] = True
                    month_data['cash_shortfall'] = abs(cash_balance)
                else:
                    month_data['requires_cash_injection'] = False
                    month_data['cash_shortfall'] = 0
            
            # Calculate impact metrics
            total_lost_rent = 0
            max_cash_shortfall = 0
            months_negative = 0
            total_shortfall = 0
            
            for month in range(vacancy_start_month, min(vacancy_start_month + vacancy_months, len(scenario_data))):
                month_data = scenario_data[month]
                # Lost rent would be the baseline rent for that month
                baseline_rent = monthly_data[month]['monthly_rent']
                total_lost_rent += baseline_rent
                
            for month_data in scenario_data:
                if month_data.get('requires_cash_injection', False):
                    months_negative += 1
                    shortfall = month_data.get('cash_shortfall', 0)
                    max_cash_shortfall = max(max_cash_shortfall, shortfall)
                    total_shortfall += shortfall
            
            results.append({
                'vacancy_start_month': vacancy_start_month,
                'vacancy_months': vacancy_months,
                'total_lost_rent': total_lost_rent,
                'monthly_carrying_cost': monthly_carrying_cost,
                'max_cash_shortfall': max_cash_shortfall,
                'months_cash_negative': months_negative,
                'total_cash_shortfall': total_shortfall,
                'requires_emergency_fund': max_cash_shortfall > 0,
                'recommended_emergency_fund': max_cash_shortfall * 1.2  # 20% buffer
            })
        
        return {
            'vacancy_scenarios': results,
            'baseline_cash_balance': baseline_cash_balance,
            'monthly_carrying_cost': monthly_carrying_cost
        }
    
    def analyze_property_value_shock(self, shock_percentages: List[float] = [-10, -20, -30]) -> Dict:
        """Analyze impact of property value declines on equity and loan-to-value ratios"""
        
        baseline = self.calculator.calculate_monthly_rental_dcf()
        current_property_value = self.analysis.property.current_value
        current_mortgage_balance = self.analysis.property.mortgage_balance
        current_ltv = current_mortgage_balance / current_property_value
        
        shock_scenarios = []
        
        for shock_pct in shock_percentages:
            shocked_value = current_property_value * (1 + shock_pct / 100)
            new_ltv = current_mortgage_balance / shocked_value
            equity_loss = current_property_value - shocked_value
            underwater_amount = max(0, current_mortgage_balance - shocked_value)
            
            # Calculate impact on refinancing ability
            can_refinance = new_ltv <= 0.80  # Typical refi limit
            
            shock_scenarios.append({
                'shock_percentage': shock_pct,
                'shocked_property_value': shocked_value,
                'equity_loss': equity_loss,
                'new_ltv_ratio': new_ltv,
                'underwater_amount': underwater_amount,
                'is_underwater': underwater_amount > 0,
                'can_refinance': can_refinance,
                'current_equity': shocked_value - current_mortgage_balance
            })
        
        return {
            'current_property_value': current_property_value,
            'current_mortgage_balance': current_mortgage_balance,
            'current_ltv': current_ltv,
            'shock_scenarios': shock_scenarios
        }
    
    def monte_carlo_analysis(self, num_simulations: int = 1000) -> Dict:
        """Run Monte Carlo simulation with varying rent growth, vacancy, and property appreciation"""
        
        results = []
        
        for sim in range(num_simulations):
            # Random variations
            rent_growth_variation = np.random.normal(0, 0.01)  # ±1% std dev
            property_appreciation_variation = np.random.normal(0, 0.015)  # ±1.5% std dev
            
            # Random vacancy events (10% chance of 3-6 month vacancy per year)
            vacancy_events = []
            for year in range(self.analysis.analysis_years):
                if random.random() < 0.10:  # 10% chance per year
                    vacancy_months = random.randint(2, 6)
                    vacancy_start = year * 12 + random.randint(0, 11)
                    vacancy_events.append((vacancy_start, vacancy_months))
            
            # Modify analysis parameters
            modified_analysis = self.analysis.copy(deep=True)
            modified_analysis.market_assumptions.rent_growth_rate += rent_growth_variation
            modified_analysis.market_assumptions.property_appreciation_rate += property_appreciation_variation
            
            # Run simulation (simplified - would need full implementation)
            # This is a placeholder for the complex simulation logic
            final_cash_balance = np.random.normal(75000, 25000)  # Placeholder
            final_property_value = np.random.normal(1300000, 200000)  # Placeholder
            
            results.append({
                'simulation': sim,
                'rent_growth_rate': modified_analysis.market_assumptions.rent_growth_rate,
                'property_appreciation_rate': modified_analysis.market_assumptions.property_appreciation_rate,
                'vacancy_events': len(vacancy_events),
                'final_cash_balance': final_cash_balance,
                'final_property_value': final_property_value,
                'total_return': final_cash_balance + final_property_value - modified_analysis.property.mortgage_balance
            })
        
        # Calculate statistics
        total_returns = [r['total_return'] for r in results]
        cash_balances = [r['final_cash_balance'] for r in results]
        
        return {
            'simulations': results,
            'statistics': {
                'mean_total_return': np.mean(total_returns),
                'std_total_return': np.std(total_returns),
                'percentile_5': np.percentile(total_returns, 5),
                'percentile_25': np.percentile(total_returns, 25),
                'percentile_75': np.percentile(total_returns, 75),
                'percentile_95': np.percentile(total_returns, 95),
                'probability_negative_cash': sum(1 for cb in cash_balances if cb < 0) / len(cash_balances),
                'worst_case_return': min(total_returns),
                'best_case_return': max(total_returns)
            }
        }
    
    def comprehensive_risk_report(self) -> Dict:
        """Generate comprehensive risk analysis combining all risk factors"""
        
        vacancy_analysis = self.analyze_vacancy_risk()
        value_shock_analysis = self.analyze_property_value_shock()
        # monte_carlo_results = self.monte_carlo_analysis()
        
        # Calculate emergency fund recommendation
        max_vacancy_shortfall = max([s['max_cash_shortfall'] for s in vacancy_analysis['vacancy_scenarios']])
        monthly_carrying_cost = vacancy_analysis['monthly_carrying_cost']
        
        # Recommend 6-12 months of carrying costs
        recommended_emergency_fund = monthly_carrying_cost * 8  # 8 months buffer
        
        return {
            'vacancy_analysis': vacancy_analysis,
            'property_value_shock_analysis': value_shock_analysis,
            # 'monte_carlo_analysis': monte_carlo_results,
            'risk_summary': {
                'monthly_carrying_cost': monthly_carrying_cost,
                'max_vacancy_cash_shortfall': max_vacancy_shortfall,
                'recommended_emergency_fund': recommended_emergency_fund,
                'high_risk_factors': self._identify_high_risk_factors(vacancy_analysis, value_shock_analysis),
                'cash_flexibility_score': self._calculate_cash_flexibility_score(vacancy_analysis)
            }
        }
    
    def _identify_high_risk_factors(self, vacancy_analysis: Dict, value_shock_analysis: Dict) -> List[str]:
        """Identify the highest risk factors"""
        risks = []
        
        # Check vacancy risk
        max_shortfall = max([s['max_cash_shortfall'] for s in vacancy_analysis['vacancy_scenarios']])
        if max_shortfall > 50000:
            risks.append("HIGH VACANCY RISK: Extended vacancy could require $50K+ cash injection")
        elif max_shortfall > 20000:
            risks.append("MODERATE VACANCY RISK: Extended vacancy could require $20K+ cash injection")
        
        # Check property value risk
        for scenario in value_shock_analysis['shock_scenarios']:
            if scenario['shock_percentage'] == -20 and scenario['is_underwater']:
                risks.append("UNDERWATER RISK: 20% property decline puts mortgage underwater")
                break
            elif scenario['shock_percentage'] == -10 and not scenario['can_refinance']:
                risks.append("REFINANCE RISK: 10% property decline prevents refinancing (LTV > 80%)")
                break
        
        return risks
    
    def _calculate_cash_flexibility_score(self, vacancy_analysis: Dict) -> str:
        """Calculate cash flexibility score based on vacancy tolerance"""
        max_shortfall = max([s['max_cash_shortfall'] for s in vacancy_analysis['vacancy_scenarios']])
        
        if max_shortfall == 0:
            return "EXCELLENT - Can handle 6+ month vacancy without additional cash"
        elif max_shortfall < 10000:
            return "GOOD - May need $10K emergency fund for extended vacancy"
        elif max_shortfall < 30000:
            return "MODERATE - May need $30K emergency fund for extended vacancy"
        else:
            return "POOR - May need $30K+ emergency fund, consider higher cash reserves"