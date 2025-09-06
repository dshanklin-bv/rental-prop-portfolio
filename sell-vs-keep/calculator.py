import numpy as np
import numpy_financial as npf
from typing import Dict, List, Tuple
from models import Analysis
from datetime import datetime
import math

class SellVsKeepCalculator:
    """Calculate returns for selling now vs keeping as rental"""
    
    def __init__(self, analysis: Analysis):
        self.analysis = analysis
    
    def calculate_sell_now_scenario(self) -> Dict[str, float]:
        """Calculate returns if selling property now and investing in stocks"""
        prop = self.analysis.property
        sale = self.analysis.sale_assumptions
        market = self.analysis.market_assumptions
        years = self.analysis.analysis_years
        
        # Calculate net proceeds from sale
        gross_proceeds = prop.current_value
        selling_costs = gross_proceeds * sale.selling_costs_percent
        net_proceeds_before_tax = gross_proceeds - selling_costs - prop.mortgage_balance
        
        # Calculate capital gains tax
        capital_gains = prop.capital_gain
        capital_gains_tax = capital_gains * sale.capital_gains_tax_rate
        
        # After-tax proceeds available for investment
        after_tax_proceeds = net_proceeds_before_tax - capital_gains_tax
        
        # Future value if invested in stock market
        future_stock_value = after_tax_proceeds * ((1 + market.stock_market_return) ** years)
        
        return {
            'gross_proceeds': gross_proceeds,
            'selling_costs': selling_costs,
            'mortgage_payoff': prop.mortgage_balance,
            'net_proceeds_before_tax': net_proceeds_before_tax,
            'capital_gains': capital_gains,
            'capital_gains_tax': capital_gains_tax,
            'after_tax_proceeds': after_tax_proceeds,
            'future_stock_value': future_stock_value,
            'total_return': future_stock_value,
            'irr': market.stock_market_return  # Stock market return assumption
        }
    
    def calculate_keep_rental_scenario(self) -> Dict[str, float]:
        """Calculate returns if keeping property as rental with depreciation"""
        prop = self.analysis.property
        expenses = self.analysis.expenses
        market = self.analysis.market_assumptions
        sale = self.analysis.sale_assumptions
        years = self.analysis.analysis_years
        
        # Calculate monthly cash flow (before tax considerations)
        monthly_rent = prop.total_monthly_rent
        monthly_expenses = self._calculate_monthly_expenses(monthly_rent)
        monthly_cash_flow = monthly_rent - monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Get depreciation information
        depreciation_info = self.calculate_depreciation_schedule()
        annual_depreciation = depreciation_info['annual_depreciation']
        
        # Calculate taxable rental income (rental income minus expenses minus depreciation)
        # For TX resident with NC property: rental income taxed as ordinary income at marginal rate
        # Assuming high earner ($260k+): 32% federal + 4.25% NC = 36.25% marginal rate
        marginal_tax_rate = 0.3625  # Combined federal + NC for high earner
        
        # Annual tax savings from depreciation deduction
        annual_depreciation_tax_benefit = annual_depreciation * marginal_tax_rate
        
        # Adjusted annual cash flow (includes tax benefit from depreciation)
        annual_after_tax_cash_flow = annual_cash_flow + annual_depreciation_tax_benefit
        
        # Total cash flows over holding period (after-tax)
        total_after_tax_cash_flows = annual_after_tax_cash_flow * years
        
        # Future property value with appreciation
        future_property_value = prop.current_value * ((1 + market.property_appreciation_rate) ** years)
        
        # Net proceeds from future sale
        future_selling_costs = future_property_value * sale.selling_costs_percent
        
        # Calculate remaining mortgage balance using proper amortization
        amort_info = self.get_loan_payoff_info()
        amort_schedule = amort_info['amortization_schedule']
        
        if years * 12 <= len(amort_schedule):
            remaining_mortgage = amort_schedule[(years * 12) - 1]['balance']
        else:
            remaining_mortgage = 0  # Loan paid off
        
        # Calculate taxes on sale
        # 1. Capital gains tax on appreciation
        capital_gains = future_property_value - prop.current_value
        capital_gains_tax = capital_gains * sale.capital_gains_tax_rate
        
        # 2. Depreciation recapture tax
        depreciation_recapture = self.calculate_depreciation_recapture_tax(years)
        depreciation_recapture_tax = depreciation_recapture['total_recapture_tax']
        
        # Net proceeds after all taxes
        future_net_proceeds = (future_property_value - future_selling_costs - 
                              remaining_mortgage - capital_gains_tax - depreciation_recapture_tax)
        
        # Calculate IRR using after-tax cash flows
        cash_flows = [0] + [annual_after_tax_cash_flow] * (years - 1) + [annual_after_tax_cash_flow + future_net_proceeds]
        irr = self._calculate_irr(cash_flows)
        
        total_return = total_after_tax_cash_flows + future_net_proceeds
        
        return {
            'monthly_rent': monthly_rent,
            'monthly_expenses': monthly_expenses,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': annual_cash_flow,
            'annual_depreciation': annual_depreciation,
            'annual_depreciation_tax_benefit': annual_depreciation_tax_benefit,
            'annual_after_tax_cash_flow': annual_after_tax_cash_flow,
            'total_cash_flows': annual_cash_flow * years,  # Pre-tax total
            'total_after_tax_cash_flows': total_after_tax_cash_flows,
            'future_property_value': future_property_value,
            'future_selling_costs': future_selling_costs,
            'remaining_mortgage': remaining_mortgage,
            'capital_gains': capital_gains,
            'capital_gains_tax': capital_gains_tax,
            'depreciation_recapture_tax': depreciation_recapture_tax,
            'future_net_proceeds': future_net_proceeds,
            'total_return': total_return,
            'irr': irr,
            'marginal_tax_rate': marginal_tax_rate,
            'depreciation_info': depreciation_info
        }
    
    def calculate_cash_vs_equity_projection(self) -> Dict[str, any]:
        """Calculate year-by-year cash flows vs equity buildup"""
        prop = self.analysis.property
        expenses = self.analysis.expenses
        market = self.analysis.market_assumptions
        years = self.analysis.analysis_years
        
        # Initialize tracking arrays
        cash_projections = []
        equity_projections = []
        
        monthly_rent = prop.total_monthly_rent
        current_mortgage_balance = prop.mortgage_balance
        monthly_payment = expenses.mortgage_payment
        
        # Get the full amortization schedule once for accuracy
        amort_info = self.get_loan_payoff_info()
        amort_schedule = amort_info['amortization_schedule']
        
        for year in range(1, years + 1):
            # === CASH COMPONENTS ===
            
            # Calculate monthly expenses for this year
            monthly_expenses = self._calculate_monthly_expenses(monthly_rent)
            monthly_net_cash = monthly_rent - monthly_expenses
            annual_net_cash = monthly_net_cash * 12
            
            # === EQUITY COMPONENTS ===
            
            # Property appreciation for this year
            property_value_this_year = prop.current_value * ((1 + market.property_appreciation_rate) ** year)
            property_value_last_year = prop.current_value * ((1 + market.property_appreciation_rate) ** (year - 1))
            annual_appreciation = property_value_this_year - property_value_last_year
            
            # Mortgage principal paydown for this year (using proper amortization)
            if monthly_payment > 0 and current_mortgage_balance > 0 and amort_schedule:
                # Get the actual principal payments for this year from amortization schedule
                start_month = (year - 1) * 12
                end_month = min(year * 12, len(amort_schedule))
                
                if start_month < len(amort_schedule):
                    year_payments = amort_schedule[start_month:end_month]
                    annual_principal_paydown = sum(payment['principal'] for payment in year_payments)
                    
                    # Update balance with actual amortization
                    if end_month <= len(amort_schedule):
                        current_mortgage_balance = amort_schedule[end_month - 1]['balance']
                else:
                    annual_principal_paydown = 0
                    current_mortgage_balance = 0
            else:
                annual_principal_paydown = 0
            
            # Depreciation tax benefit for this year
            depreciation_info = self.calculate_depreciation_schedule()
            annual_depreciation = depreciation_info['annual_depreciation']
            marginal_tax_rate = 0.3625  # 32% federal + 4.25% NC for high earner
            annual_depreciation_tax_benefit = annual_depreciation * marginal_tax_rate
            
            # After-tax cash flow including depreciation benefit
            annual_after_tax_cash = annual_net_cash + annual_depreciation_tax_benefit
            
            # Store projections for this year
            cash_projections.append({
                'year': year,
                'monthly_rent': monthly_rent,
                'monthly_expenses': monthly_expenses,
                'monthly_net_cash': monthly_net_cash,
                'annual_net_cash': annual_net_cash,
                'annual_depreciation': annual_depreciation,
                'annual_depreciation_tax_benefit': annual_depreciation_tax_benefit,
                'annual_after_tax_cash': annual_after_tax_cash,
                'cumulative_cash': sum(p['annual_net_cash'] for p in cash_projections) + annual_net_cash,
                'cumulative_after_tax_cash': sum(p['annual_after_tax_cash'] for p in cash_projections) + annual_after_tax_cash,
                'cash_components': {
                    'rental_income': monthly_rent * 12,
                    'operating_expenses': -(monthly_expenses * 12),
                    'net_cash_flow': annual_net_cash,
                    'depreciation_tax_benefit': annual_depreciation_tax_benefit,
                    'after_tax_cash_flow': annual_after_tax_cash
                }
            })
            
            equity_projections.append({
                'year': year,
                'annual_appreciation': annual_appreciation,
                'annual_principal_paydown': annual_principal_paydown,
                'total_equity_gain': annual_appreciation + annual_principal_paydown,
                'property_value': property_value_this_year,
                'remaining_mortgage': current_mortgage_balance,
                'net_equity': property_value_this_year - current_mortgage_balance,
                'equity_components': {
                    'appreciation': annual_appreciation,
                    'principal_paydown': annual_principal_paydown,
                    'total_equity_buildup': annual_appreciation + annual_principal_paydown
                }
            })
        
        return {
            'cash_projections': cash_projections,
            'equity_projections': equity_projections,
            'summary': {
                'total_cumulative_cash': sum(p['annual_net_cash'] for p in cash_projections),
                'total_cumulative_after_tax_cash': sum(p['annual_after_tax_cash'] for p in cash_projections),
                'total_depreciation_tax_benefits': sum(p['annual_depreciation_tax_benefit'] for p in cash_projections),
                'total_equity_buildup': sum(p['total_equity_gain'] for p in equity_projections),
                'final_property_value': equity_projections[-1]['property_value'] if equity_projections else 0,
                'final_mortgage_balance': equity_projections[-1]['remaining_mortgage'] if equity_projections else 0,
                'final_net_equity': equity_projections[-1]['net_equity'] if equity_projections else 0,
                'depreciation_info': self.calculate_depreciation_schedule()
            }
        }
    
    def create_amortization_schedule(self, current_balance: float, rate: float, 
                                   payment: float, start_date: str = "2025-08-01") -> List[Dict]:
        """Create actual amortization schedule from current loan position"""
        schedule = []
        balance = current_balance
        monthly_rate = rate / 12
        month = 1
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        # Calculate until loan is paid off or 30 years max (360 payments)
        while balance > 0.01 and month <= 360:
            interest_payment = balance * monthly_rate
            
            # Handle final payment
            if balance + interest_payment < payment:
                principal_payment = balance
                actual_payment = balance + interest_payment
                balance = 0
            else:
                principal_payment = payment - interest_payment
                actual_payment = payment
                balance = balance - principal_payment
            
            schedule.append({
                'month': month,
                'date': current_date.strftime("%Y-%m-%d"),
                'payment': actual_payment,
                'principal': principal_payment,
                'interest': interest_payment,
                'balance': balance
            })
            
            current_date = current_date.replace(day=1)
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
            
            month += 1
            
            # Safety check
            if balance <= 0:
                break
        
        return schedule
    
    def get_loan_payoff_info(self) -> Dict:
        """Get loan payoff date and summary information"""
        prop = self.analysis.property
        
        # Get loan details from property data
        current_balance = prop.mortgage_balance
        
        # Get precise rate and payment from Wells Fargo statement data
        rate = 0.03875  # Exact 3.875% from August 2025 Wells Fargo statement
        payment = 2783.80  # Your actual P&I payment
        
        if current_balance <= 0 or payment <= 0:
            return {
                'payoff_date': None,
                'remaining_payments': 0,
                'total_interest_remaining': 0,
                'amortization_schedule': []
            }
        
        # Create amortization schedule
        schedule = self.create_amortization_schedule(current_balance, rate, payment)
        
        if not schedule:
            return {
                'payoff_date': None,
                'remaining_payments': 0,
                'total_interest_remaining': 0,
                'amortization_schedule': []
            }
        
        # Get payoff info
        payoff_date = schedule[-1]['date']
        remaining_payments = len(schedule)
        total_interest_remaining = sum(entry['interest'] for entry in schedule)
        
        # Calculate years remaining
        years_remaining = remaining_payments / 12
        
        return {
            'payoff_date': payoff_date,
            'remaining_payments': remaining_payments,
            'years_remaining': years_remaining,
            'total_interest_remaining': total_interest_remaining,
            'current_balance': current_balance,
            'monthly_payment': payment,
            'interest_rate': rate,
            'amortization_schedule': schedule
        }
    
    def _calculate_monthly_expenses(self, monthly_rent: float) -> float:
        """Calculate total monthly expenses"""
        exp = self.analysis.expenses
        
        maintenance = monthly_rent * exp.maintenance_percent
        vacancy = monthly_rent * exp.vacancy_percent
        management = monthly_rent * exp.management_percent
        
        total = (exp.property_tax_monthly + 
                exp.insurance_monthly + 
                exp.mortgage_payment + 
                maintenance + 
                vacancy + 
                management + 
                exp.other_monthly)
        
        return total
    
    def _calculate_irr(self, cash_flows: List[float]) -> float:
        """Calculate IRR with error handling"""
        try:
            return npf.irr(cash_flows)
        except:
            return 0.0
    
    def calculate_npv(self, cash_flows: List[float]) -> float:
        """Calculate NPV using discount rate"""
        try:
            return npf.npv(self.analysis.market_assumptions.discount_rate, cash_flows)
        except:
            return 0.0
    
    def get_recommendation(self) -> Dict[str, any]:
        """Get recommendation and comparison"""
        sell_scenario = self.calculate_sell_now_scenario()
        keep_scenario = self.calculate_keep_rental_scenario()
        
        # Determine recommendation
        if keep_scenario['total_return'] > sell_scenario['total_return']:
            recommendation = "KEEP"
            advantage = keep_scenario['total_return'] - sell_scenario['total_return']
            advantage_pct = advantage / sell_scenario['total_return']
        else:
            recommendation = "SELL"
            advantage = sell_scenario['total_return'] - keep_scenario['total_return']
            advantage_pct = advantage / keep_scenario['total_return']
        
        return {
            'recommendation': recommendation,
            'sell_scenario': sell_scenario,
            'keep_scenario': keep_scenario,
            'advantage_amount': advantage,
            'advantage_percent': advantage_pct,
            'break_even_rent': self._calculate_break_even_rent(),
            'break_even_appreciation': self._calculate_break_even_appreciation()
        }
    
    def _calculate_break_even_rent(self) -> float:
        """Calculate rent needed to break even with selling"""
        # Simplified calculation - what monthly rent makes scenarios equal
        sell_result = self.calculate_sell_now_scenario()
        target_return = sell_result['total_return']
        
        # Work backwards from target return
        # This is a simplified approximation
        years = self.analysis.analysis_years
        prop = self.analysis.property
        market = self.analysis.market_assumptions
        
        future_property_value = prop.current_value * ((1 + market.property_appreciation_rate) ** years)
        future_net_proceeds = future_property_value * 0.85  # Rough estimate after costs
        
        needed_cash_flows = target_return - future_net_proceeds
        needed_annual_cash_flow = needed_cash_flows / years
        
        # Estimate monthly expenses as percentage of rent
        expense_ratio = 0.6  # Rough estimate
        needed_monthly_rent = needed_annual_cash_flow / 12 / (1 - expense_ratio)
        
        return max(0, needed_monthly_rent)
    
    def _calculate_break_even_appreciation(self) -> float:
        """Calculate appreciation rate needed to break even with selling"""
        # Simplified calculation
        sell_result = self.calculate_sell_now_scenario()
        target_return = sell_result['total_return']
        
        keep_result = self.calculate_keep_rental_scenario()
        cash_flows = keep_result['total_cash_flows']
        
        needed_future_proceeds = target_return - cash_flows
        prop = self.analysis.property
        years = self.analysis.analysis_years
        
        # What property value do we need?
        needed_property_value = needed_future_proceeds / 0.85  # Rough estimate after costs
        
        # What appreciation rate gets us there?
        if needed_property_value > 0 and prop.current_value > 0:
            needed_appreciation_rate = ((needed_property_value / prop.current_value) ** (1/years)) - 1
            # Handle complex numbers from negative values
            if isinstance(needed_appreciation_rate, complex):
                needed_appreciation_rate = needed_appreciation_rate.real
        else:
            needed_appreciation_rate = 0
        
        return max(-0.5, min(0.5, needed_appreciation_rate))  # Cap at reasonable bounds
    
    def calculate_sell_now_dcf(self) -> Dict[str, any]:
        """Calculate DCF for selling now and investing proceeds in stock market"""
        prop = self.analysis.property
        sale = self.analysis.sale_assumptions
        market = self.analysis.market_assumptions
        years = self.analysis.analysis_years
        
        # Tax rates for TX resident with NC property
        tax_rates = {
            'federal_capital_gains': 0.20,  # 20% federal long-term capital gains on stocks
            'nc_flat': 0.0425,              # 4.25% NC flat tax on capital gains
            'combined_capital_gains': 0.2425, # 20% + 4.25% = 24.25%
            # Primary residence exclusion available for first $250k of gains
            'primary_residence_exclusion': 250000,
            'federal_ordinary': 0.32,       # 32% federal marginal for high earner 
            'combined_ordinary': 0.3625     # For any taxable portion above exclusion
        }
        
        # Calculate net proceeds from property sale
        gross_proceeds = prop.current_value
        selling_costs = gross_proceeds * sale.selling_costs_percent
        net_proceeds_before_tax = gross_proceeds - selling_costs - prop.mortgage_balance
        
        # Capital gains calculation with primary residence exclusion
        total_capital_gains = prop.capital_gain  # Current value - cost basis
        
        # Apply $250k federal exclusion (assuming primary residence qualification)
        taxable_capital_gains_federal = max(0, total_capital_gains - tax_rates['primary_residence_exclusion'])
        # NC has no primary residence exclusion - tax full gain at 4.25%
        taxable_capital_gains_nc = total_capital_gains
        
        federal_capital_gains_tax = taxable_capital_gains_federal * tax_rates['federal_capital_gains']
        nc_capital_gains_tax = taxable_capital_gains_nc * tax_rates['nc_flat']
        total_capital_gains_tax = federal_capital_gains_tax + nc_capital_gains_tax
        
        # After-tax proceeds available for stock investment
        after_tax_proceeds = net_proceeds_before_tax - total_capital_gains_tax
        
        # Stock market investment projections
        dcf_projections = []
        current_stock_value = after_tax_proceeds
        annual_stock_return = market.stock_market_return  # 7.5% assumed
        
        for year in range(1, years + 1):
            # Stock appreciation for the year
            beginning_value = current_stock_value
            ending_value = beginning_value * (1 + annual_stock_return)
            annual_appreciation = ending_value - beginning_value
            
            # No cash flow during holding period (assumes reinvestment)
            annual_cash_flow = 0
            
            # Update for next year
            current_stock_value = ending_value
            
            dcf_projections.append({
                'year': year,
                'beginning_stock_value': beginning_value,
                'annual_stock_return': annual_stock_return,
                'annual_appreciation': annual_appreciation,
                'ending_stock_value': ending_value,
                'annual_cash_flow': annual_cash_flow
            })
        
        # Terminal value (sell stocks at end of period)
        final_stock_value = dcf_projections[-1]['ending_stock_value']
        total_stock_appreciation = final_stock_value - after_tax_proceeds
        
        # Tax on stock gains (long-term capital gains rates)
        stock_capital_gains_tax = total_stock_appreciation * tax_rates['combined_capital_gains']
        
        # Net proceeds from stock sale
        net_stock_proceeds = final_stock_value - stock_capital_gains_tax
        
        # Terminal cash flow
        terminal_cash_flow = net_stock_proceeds
        
        # === NPV AND IRR CALCULATIONS ===
        # Cash flows: [Initial after-tax proceeds, $0 for years 1-9, Terminal value in year 10]
        cash_flow_series = [-after_tax_proceeds] + [0] * (years - 1) + [terminal_cash_flow]
        
        # Calculate NPV and IRR
        npv = self.calculate_npv(cash_flow_series)
        irr = self._calculate_irr(cash_flow_series)
        
        return {
            'sale_details': {
                'gross_proceeds': gross_proceeds,
                'selling_costs': selling_costs,
                'mortgage_payoff': prop.mortgage_balance,
                'net_proceeds_before_tax': net_proceeds_before_tax,
                'total_capital_gains': total_capital_gains,
                'federal_exclusion_used': min(total_capital_gains, tax_rates['primary_residence_exclusion']),
                'taxable_capital_gains_federal': taxable_capital_gains_federal,
                'taxable_capital_gains_nc': taxable_capital_gains_nc,
                'federal_capital_gains_tax': federal_capital_gains_tax,
                'nc_capital_gains_tax': nc_capital_gains_tax,
                'total_capital_gains_tax': total_capital_gains_tax,
                'after_tax_proceeds': after_tax_proceeds
            },
            'stock_projections': dcf_projections,
            'terminal_value': {
                'final_stock_value': final_stock_value,
                'total_stock_appreciation': total_stock_appreciation,
                'stock_capital_gains_tax': stock_capital_gains_tax,
                'net_stock_proceeds': net_stock_proceeds,
                'terminal_cash_flow': terminal_cash_flow
            },
            'summary_metrics': {
                'total_return': terminal_cash_flow,
                'total_appreciation': total_stock_appreciation,
                'npv': npv,
                'irr': irr,
                'cash_flow_series': cash_flow_series
            },
            'tax_assumptions': tax_rates,
            'assumptions': {
                'annual_stock_return': annual_stock_return,
                'primary_residence_exclusion_available': True
            }
        }
    
    def calculate_comprehensive_dcf(self) -> Dict[str, any]:
        """Build comprehensive DCF model with detailed tax calculations"""
        prop = self.analysis.property
        expenses = self.analysis.expenses
        market = self.analysis.market_assumptions
        sale = self.analysis.sale_assumptions
        years = self.analysis.analysis_years
        
        # Tax assumptions for TX resident with NC property, high income bracket ($260k+)
        tax_rates = {
            'federal_ordinary': 0.32,      # 32% federal marginal rate for high earner
            'federal_capital_gains': 0.20, # 20% federal long-term capital gains
            'federal_depreciation_recapture': 0.25, # 25% federal depreciation recapture
            'nc_flat': 0.0425,             # 4.25% NC flat tax (applies to all income for non-residents)
            'combined_ordinary': 0.3625,    # 32% + 4.25% = 36.25%
            'combined_capital_gains': 0.2425, # 20% + 4.25% = 24.25%
            'combined_depreciation_recapture': 0.2925 # 25% + 4.25% = 29.25%
        }
        
        # Get loan amortization and depreciation schedules
        loan_info = self.get_loan_payoff_info()
        amort_schedule = loan_info['amortization_schedule']
        depreciation_info = self.calculate_depreciation_schedule()
        
        # Initialize DCF projections
        dcf_projections = []
        
        # Assumptions
        rent_growth_rate = 0.03  # 3% annual rent growth
        expense_growth_rate = 0.025  # 2.5% annual expense inflation
        current_monthly_rent = prop.total_monthly_rent
        
        for year in range(1, years + 1):
            # === REVENUE CALCULATIONS ===
            annual_rent = current_monthly_rent * 12 * ((1 + rent_growth_rate) ** (year - 1))
            
            # === EXPENSE CALCULATIONS ===
            # Operating expenses (property tax, insurance, maintenance, vacancy, management, other)
            base_monthly_expenses = self._calculate_monthly_expenses(current_monthly_rent)
            # Exclude mortgage payment from operating expenses for DCF
            operating_monthly_expenses = (base_monthly_expenses - expenses.mortgage_payment)
            annual_operating_expenses = operating_monthly_expenses * 12 * ((1 + expense_growth_rate) ** (year - 1))
            
            # Mortgage payment (P&I from amortization schedule)
            if (year - 1) * 12 < len(amort_schedule):
                start_month = (year - 1) * 12
                end_month = min(year * 12, len(amort_schedule))
                year_payments = amort_schedule[start_month:end_month]
                
                annual_interest_payment = sum(payment['interest'] for payment in year_payments)
                annual_principal_payment = sum(payment['principal'] for payment in year_payments)
                mortgage_balance_end_of_year = year_payments[-1]['balance'] if year_payments else 0
            else:
                annual_interest_payment = 0
                annual_principal_payment = 0
                mortgage_balance_end_of_year = 0
            
            # === TAX CALCULATIONS ===
            # Net Operating Income (NOI)
            noi = annual_rent - annual_operating_expenses
            
            # Taxable income (NOI - mortgage interest - depreciation)
            annual_depreciation = depreciation_info['annual_depreciation']
            taxable_rental_income = noi - annual_interest_payment - annual_depreciation
            
            # Income tax on rental income (ordinary income rates)
            rental_income_tax = max(0, taxable_rental_income * tax_rates['combined_ordinary'])
            
            # === AFTER-TAX CASH FLOW ===
            # Cash flow = NOI - mortgage payment (P&I) - income taxes
            total_mortgage_payment = annual_interest_payment + annual_principal_payment
            after_tax_cash_flow = noi - total_mortgage_payment - rental_income_tax
            
            # === EQUITY BUILDUP ===
            property_value_eoy = prop.current_value * ((1 + market.property_appreciation_rate) ** year)
            equity_from_appreciation = property_value_eoy - (prop.current_value * ((1 + market.property_appreciation_rate) ** (year - 1)))
            equity_from_paydown = annual_principal_payment
            total_equity_gain = equity_from_appreciation + equity_from_paydown
            
            dcf_projections.append({
                'year': year,
                'annual_rent': annual_rent,
                'annual_operating_expenses': annual_operating_expenses,
                'noi': noi,
                'annual_interest_payment': annual_interest_payment,
                'annual_principal_payment': annual_principal_payment,
                'annual_depreciation': annual_depreciation,
                'taxable_rental_income': taxable_rental_income,
                'rental_income_tax': rental_income_tax,
                'after_tax_cash_flow': after_tax_cash_flow,
                'property_value_eoy': property_value_eoy,
                'mortgage_balance_eoy': mortgage_balance_end_of_year,
                'equity_from_appreciation': equity_from_appreciation,
                'equity_from_paydown': equity_from_paydown,
                'total_equity_gain': total_equity_gain,
                'accumulated_depreciation': min(annual_depreciation * year, depreciation_info['depreciable_basis'])
            })
        
        # === TERMINAL VALUE (Sale at end of holding period) ===
        final_year = dcf_projections[-1]
        final_property_value = final_year['property_value_eoy']
        final_mortgage_balance = final_year['mortgage_balance_eoy']
        
        # Selling costs
        selling_costs = final_property_value * sale.selling_costs_percent
        
        # Capital gains calculation
        total_appreciation = final_property_value - prop.current_value
        capital_gains_tax = total_appreciation * tax_rates['combined_capital_gains']
        
        # Depreciation recapture
        total_accumulated_depreciation = final_year['accumulated_depreciation']
        depreciation_recapture_tax = total_accumulated_depreciation * tax_rates['combined_depreciation_recapture']
        
        # Net sale proceeds after all costs and taxes
        net_sale_proceeds = (final_property_value - selling_costs - final_mortgage_balance - 
                           capital_gains_tax - depreciation_recapture_tax)
        
        # Total terminal cash flow (includes final year operating cash flow + sale proceeds)
        terminal_cash_flow = final_year['after_tax_cash_flow'] + net_sale_proceeds
        
        # === NPV AND IRR CALCULATIONS ===
        # Cash flows: [Initial investment, Year 1-9 cash flows, Terminal year total cash flow]
        initial_investment = 0  # Assuming already own the property
        annual_cash_flows = [proj['after_tax_cash_flow'] for proj in dcf_projections[:-1]]
        cash_flow_series = [initial_investment] + annual_cash_flows + [terminal_cash_flow]
        
        # Calculate NPV using discount rate
        npv = self.calculate_npv(cash_flow_series)
        
        # Calculate IRR
        irr = self._calculate_irr(cash_flow_series)
        
        return {
            'dcf_projections': dcf_projections,
            'terminal_value': {
                'final_property_value': final_property_value,
                'selling_costs': selling_costs,
                'final_mortgage_balance': final_mortgage_balance,
                'total_appreciation': total_appreciation,
                'capital_gains_tax': capital_gains_tax,
                'total_accumulated_depreciation': total_accumulated_depreciation,
                'depreciation_recapture_tax': depreciation_recapture_tax,
                'net_sale_proceeds': net_sale_proceeds,
                'terminal_cash_flow': terminal_cash_flow
            },
            'summary_metrics': {
                'total_after_tax_cash_flows': sum(proj['after_tax_cash_flow'] for proj in dcf_projections),
                'total_equity_buildup': sum(proj['total_equity_gain'] for proj in dcf_projections),
                'total_return': sum(proj['after_tax_cash_flow'] for proj in dcf_projections) + net_sale_proceeds,
                'npv': npv,
                'irr': irr,
                'cash_flow_series': cash_flow_series
            },
            'tax_assumptions': tax_rates,
            'assumptions': {
                'rent_growth_rate': rent_growth_rate,
                'expense_growth_rate': expense_growth_rate,
                'property_appreciation_rate': market.property_appreciation_rate,
                'discount_rate': market.discount_rate
            }
        }
    
    def get_comprehensive_comparison(self) -> Dict[str, any]:
        """Get comprehensive DCF comparison between sell now vs keep rental scenarios"""
        
        # Calculate both DCF models
        sell_now_dcf = self.calculate_sell_now_dcf()
        keep_rental_dcf = self.calculate_comprehensive_dcf()
        
        # Extract key metrics for comparison
        sell_metrics = sell_now_dcf['summary_metrics']
        keep_metrics = keep_rental_dcf['summary_metrics']
        
        # Calculate advantages
        if keep_metrics['total_return'] > sell_metrics['total_return']:
            recommended_scenario = 'KEEP_RENTAL'
            advantage_amount = keep_metrics['total_return'] - sell_metrics['total_return']
            advantage_percent = advantage_amount / sell_metrics['total_return'] if sell_metrics['total_return'] > 0 else 0
        else:
            recommended_scenario = 'SELL_NOW'
            advantage_amount = sell_metrics['total_return'] - keep_metrics['total_return']
            advantage_percent = advantage_amount / keep_metrics['total_return'] if keep_metrics['total_return'] > 0 else 0
        
        # IRR comparison
        irr_difference = keep_metrics['irr'] - sell_metrics['irr'] if (keep_metrics['irr'] and sell_metrics['irr']) else 0
        
        # NPV comparison  
        npv_difference = keep_metrics['npv'] - sell_metrics['npv'] if (keep_metrics['npv'] and sell_metrics['npv']) else 0
        
        # Risk analysis
        rental_risks = [
            "Vacancy and tenant management",
            "Property maintenance and repairs", 
            "Interest rate risk (if refinancing)",
            "Local market appreciation risk",
            "Illiquid asset - harder to exit",
            "Depreciation recapture tax liability",
            "Active management time commitment"
        ]
        
        stock_risks = [
            "Market volatility and timing risk",
            "Sequence of returns risk",
            "No tax advantages (no depreciation)",
            "Higher correlation with other investments", 
            "No leverage benefits",
            "No inflation hedge from rental income"
        ]
        
        # Cash flow comparison (rental generates cash, stocks don't until sale)
        rental_annual_cash = keep_metrics['total_after_tax_cash_flows'] / self.analysis.analysis_years
        stock_annual_cash = 0  # Assuming reinvestment strategy
        
        return {
            'recommendation': {
                'scenario': recommended_scenario,
                'advantage_amount': advantage_amount,
                'advantage_percent': advantage_percent,
                'reasoning': self._get_recommendation_reasoning(recommended_scenario, advantage_percent, 
                                                             keep_metrics, sell_metrics)
            },
            'scenarios': {
                'sell_now': sell_now_dcf,
                'keep_rental': keep_rental_dcf
            },
            'comparison_metrics': {
                'total_return_difference': keep_metrics['total_return'] - sell_metrics['total_return'],
                'irr_difference': irr_difference,
                'irr_difference_bps': irr_difference * 10000 if irr_difference else 0,  # Basis points
                'npv_difference': npv_difference,
                'cash_flow_comparison': {
                    'rental_annual_cash_flow': rental_annual_cash,
                    'stock_annual_cash_flow': stock_annual_cash,
                    'rental_provides_income': rental_annual_cash > 0,
                    'rental_total_cash_flows': keep_metrics['total_after_tax_cash_flows'],
                    'stock_total_cash_flows': 0
                }
            },
            'risk_analysis': {
                'rental_scenario_risks': rental_risks,
                'stock_scenario_risks': stock_risks,
                'liquidity_comparison': {
                    'rental_liquidity': 'Low - Real estate transaction required (3-6 months)',
                    'stock_liquidity': 'High - Can liquidate in 1-3 trading days'
                },
                'tax_complexity': {
                    'rental_complexity': 'High - Annual depreciation, passive loss rules, recapture',
                    'stock_complexity': 'Low - Simple capital gains treatment'
                }
            },
            'key_assumptions': {
                'primary_residence_exclusion': 250000,
                'rental_property_appreciation': keep_rental_dcf['assumptions']['property_appreciation_rate'],
                'stock_market_return': sell_now_dcf['assumptions']['annual_stock_return'],
                'tax_scenario': 'TX resident, NC property, $260k+ income',
                'holding_period': f"{self.analysis.analysis_years} years"
            }
        }
    
    def _get_recommendation_reasoning(self, scenario: str, advantage_percent: float, 
                                   keep_metrics: dict, sell_metrics: dict) -> str:
        """Generate reasoning for the recommendation"""
        
        if scenario == 'KEEP_RENTAL':
            if advantage_percent > 0.20:  # 20%+ advantage
                return f"Strong recommendation to KEEP as rental. The rental scenario provides {advantage_percent:.1%} higher returns, driven by leverage benefits, depreciation tax advantages, and steady cash flow generation."
            elif advantage_percent > 0.10:  # 10-20% advantage  
                return f"Moderate recommendation to KEEP as rental. Returns are {advantage_percent:.1%} higher, but consider your tolerance for active property management and illiquidity."
            else:  # <10% advantage
                return f"Slight edge to KEEP as rental ({advantage_percent:.1%} higher returns), but returns are close. Consider non-financial factors like time commitment and liquidity needs."
        else:  # SELL_NOW
            if advantage_percent > 0.20:  # 20%+ advantage
                return f"Strong recommendation to SELL now. Stock investment provides {advantage_percent:.1%} higher returns with much better liquidity and lower management burden. The primary residence exclusion saves significant taxes."
            elif advantage_percent > 0.10:  # 10-20% advantage
                return f"Moderate recommendation to SELL now. Returns are {advantage_percent:.1%} higher with stocks, plus you gain liquidity and avoid property management responsibilities."
            else:  # <10% advantage
                return f"Slight edge to SELL now ({advantage_percent:.1%} higher returns), but returns are close. The primary residence tax exclusion and simplicity may tip the scales toward selling."
    
    def calculate_depreciation_schedule(self) -> Dict[str, any]:
        """Calculate depreciation schedule for rental property (27.5 year residential)"""
        prop = self.analysis.property
        years = self.analysis.analysis_years
        
        # Calculate depreciable basis (excludes land value)
        # Standard assumption: land is 15-25% of total value, we'll use 20%
        land_percentage = 0.20
        depreciable_basis = prop.cost_basis * (1 - land_percentage)
        
        # Residential rental property: 27.5 year straight line
        annual_depreciation = depreciable_basis / 27.5
        
        # Create year-by-year schedule
        depreciation_schedule = []
        accumulated_depreciation = 0
        
        for year in range(1, years + 1):
            # Current year depreciation (capped at remaining basis)
            remaining_depreciable = depreciable_basis - accumulated_depreciation
            current_year_depreciation = min(annual_depreciation, remaining_depreciable)
            accumulated_depreciation += current_year_depreciation
            
            depreciation_schedule.append({
                'year': year,
                'annual_depreciation': current_year_depreciation,
                'accumulated_depreciation': accumulated_depreciation,
                'remaining_depreciable_basis': depreciable_basis - accumulated_depreciation,
                'adjusted_basis': prop.cost_basis - accumulated_depreciation
            })
        
        return {
            'cost_basis': prop.cost_basis,
            'land_value': prop.cost_basis * land_percentage,
            'depreciable_basis': depreciable_basis,
            'annual_depreciation': annual_depreciation,
            'years_to_fully_depreciate': 27.5,
            'schedule': depreciation_schedule,
            'total_accumulated_at_end': accumulated_depreciation
        }
    
    def calculate_depreciation_recapture_tax(self, holding_years: int) -> Dict[str, float]:
        """Calculate depreciation recapture tax when property is sold"""
        depreciation_info = self.calculate_depreciation_schedule()
        
        # Get accumulated depreciation at time of sale
        if holding_years <= len(depreciation_info['schedule']):
            accumulated_depreciation = depreciation_info['schedule'][holding_years - 1]['accumulated_depreciation']
        else:
            # If held longer than our schedule, use the total possible depreciation
            accumulated_depreciation = min(
                depreciation_info['annual_depreciation'] * holding_years,
                depreciation_info['depreciable_basis']
            )
        
        # Depreciation recapture is taxed at 25% federal rate
        federal_depreciation_recapture_rate = 0.25
        
        # NC also taxes depreciation recapture as ordinary income (4.25% flat rate)
        nc_depreciation_recapture_rate = 0.0425
        
        federal_recapture_tax = accumulated_depreciation * federal_depreciation_recapture_rate
        state_recapture_tax = accumulated_depreciation * nc_depreciation_recapture_rate
        total_recapture_tax = federal_recapture_tax + state_recapture_tax
        
        return {
            'accumulated_depreciation': accumulated_depreciation,
            'federal_recapture_tax': federal_recapture_tax,
            'state_recapture_tax': state_recapture_tax,
            'total_recapture_tax': total_recapture_tax,
            'effective_recapture_rate': (federal_depreciation_recapture_rate + nc_depreciation_recapture_rate)
        }