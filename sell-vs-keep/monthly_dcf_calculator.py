import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from models import Analysis
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

class MonthlyDCFCalculator:
    """Month-by-month general ledger DCF calculator with cash management and quarterly taxes"""
    
    def __init__(self, analysis: Analysis, scenario_name: str = ""):
        self.analysis = analysis
        self.scenario_name = scenario_name
        # Financial assumptions
        self.cash_savings_rate = 0.045  # 4.5% annual on cash reserves
        self.stock_market_rate = 0.075  # 7.5% annual stock return
        self.operating_cash_reserve = 20000  # $20K minimum cash balance
        
        # Tax assumptions for TX resident with NC rental property
        self.federal_marginal_rate = 0.32  # 32% for $260k+ earner
        self.nc_rental_tax_rate = 0.0425   # 4.25% NC flat tax on rental income
        self.combined_ordinary_rate = self.federal_marginal_rate + self.nc_rental_tax_rate
        
        # Quarterly tax payment dates
        self.quarterly_tax_dates = [
            (1, 15),   # Q4 previous year - Jan 15
            (3, 15),   # Q1 - Mar 15  
            (6, 15),   # Q2 - Jun 15
            (9, 15)    # Q3 - Sep 15
        ]
        
    def calculate_monthly_rental_dcf(self) -> Dict:
        """Calculate month-by-month rental scenario with cash management"""
        
        prop = self.analysis.property
        expenses = self.analysis.expenses
        market = self.analysis.market_assumptions
        years = self.analysis.analysis_years
        
        # Initialize tracking variables
        monthly_data = []
        cash_balance = self.operating_cash_reserve  # Start with $20K reserve
        property_value = prop.current_value
        quarterly_tax_liability = 0
        annual_depreciation = self._calculate_annual_depreciation()
        monthly_depreciation = annual_depreciation / 12
        
        # Initialize escrow balance (start with current balance from property data)
        escrow_balance = 652.01  # From Wells Fargo statement
        
        # Quarterly tracking for accurate tax calculations
        quarterly_rental_income = 0
        quarterly_operating_expenses = 0
        quarterly_interest = 0
        quarterly_depreciation = 0
        
        # Get mortgage amortization schedule
        loan_info = self._get_loan_info()
        amort_schedule = loan_info.get('amortization_schedule', [])
        
        # Calculate initial quarterly tax estimate (assume same as prior year)
        estimated_quarterly_tax = self._estimate_quarterly_tax_payment()
        
        # Monthly calculations for the analysis period
        current_date = datetime(2025, 9, 1)  # Start September 2025
        
        for month in range(years * 12):
            month_year = current_date + relativedelta(months=month)
            
            # === MONTHLY INCOME ===
            # Rental income (grows at market rent growth rate, with scenario-specific adjustments)
            years_elapsed = month / 12
            monthly_rent = self._get_monthly_rent(month, years_elapsed)
            
            # === MONTHLY EXPENSES ===
            # Operating expenses (grow 2.5% annually)
            monthly_operating_expenses = self._calculate_monthly_operating_expenses(
                monthly_rent, years_elapsed
            )
            
            # Mortgage payment (P&I from amortization schedule)
            if month < len(amort_schedule):
                principal_payment = amort_schedule[month]['principal']
                interest_payment = amort_schedule[month]['interest']
                mortgage_pi_payment = principal_payment + interest_payment  # P&I only
                mortgage_balance = amort_schedule[month]['balance']
            else:
                principal_payment = interest_payment = mortgage_pi_payment = 0
                mortgage_balance = 0
            
            # Escrow payment (separate from P&I)
            monthly_escrow_payment = expenses.mortgage_escrow  # $582.08
            escrow_balance += monthly_escrow_payment
            
            # === ESCROW DISBURSEMENTS ===
            # Property tax payments (twice yearly - typically April and October for NC)
            property_tax_payment = 0
            insurance_payment = 0
            
            # Property tax paid in April (month 8) and October (month 2 of following year)
            # Adjust for our start date of September 2025
            if (month_year.month == 4) or (month_year.month == 10):
                # Semi-annual property tax payment
                property_tax_payment = expenses.property_tax_annual / 2  # $2,136.51
                escrow_balance -= property_tax_payment
            
            # Insurance payment (annually - typically at policy renewal)
            if month_year.month == 1:  # Assume January renewal
                insurance_payment = expenses.insurance_annual  # $4,201
                escrow_balance -= insurance_payment
            
            # === NET OPERATING INCOME ===
            noi = monthly_rent - monthly_operating_expenses
            
            # === CASH FLOW CALCULATION ===
            # Total mortgage payment now includes P&I + escrow
            total_mortgage_payment = mortgage_pi_payment + monthly_escrow_payment
            operating_cash_flow = noi - total_mortgage_payment
            
            # Add cash flow to balance
            cash_balance += operating_cash_flow
            
            # === QUARTERLY DATA ACCUMULATION ===
            # Accumulate quarterly data for tax calculations
            quarterly_rental_income += monthly_rent
            quarterly_operating_expenses += monthly_operating_expenses
            quarterly_interest += interest_payment
            quarterly_depreciation += monthly_depreciation
            
            # === CASH MANAGEMENT ===
            # Calculate interest on cash balance (monthly compounding)
            monthly_cash_rate = self.cash_savings_rate / 12
            cash_interest_earned = cash_balance * monthly_cash_rate
            cash_balance += cash_interest_earned
            
            # Determine excess cash (above $20K reserve)
            excess_cash = max(0, cash_balance - self.operating_cash_reserve)
            investable_cash = cash_balance - self.operating_cash_reserve
            
            # === QUARTERLY TAX PAYMENTS ===
            quarterly_tax_payment = 0
            if self._is_quarterly_tax_month(month_year.month):
                # Calculate tax based on accumulated quarterly data
                quarterly_taxable_income = (quarterly_rental_income - quarterly_operating_expenses - 
                                          quarterly_interest - quarterly_depreciation)
                
                if quarterly_taxable_income > 0:
                    quarterly_tax_payment = quarterly_taxable_income * self.combined_ordinary_rate
                else:
                    quarterly_tax_payment = 0
                
                cash_balance -= quarterly_tax_payment
                
                # Reset quarterly accumulators after tax payment
                quarterly_rental_income = 0
                quarterly_operating_expenses = 0
                quarterly_interest = 0
                quarterly_depreciation = 0
            
            # === PROPERTY VALUE AND EQUITY ===
            # Property appreciation (monthly)
            monthly_appreciation_rate = market.property_appreciation_rate / 12
            monthly_appreciation = property_value * monthly_appreciation_rate
            property_value += monthly_appreciation
            
            # Current equity (property value minus mortgage balance)
            current_equity = property_value - mortgage_balance
            
            # === RECORD MONTHLY DATA ===
            monthly_data.append({
                'month': month + 1,
                'date': month_year.strftime('%Y-%m-%d'),
                'year': month_year.year,
                'month_name': month_year.strftime('%B'),
                
                # Income
                'monthly_rent': monthly_rent,
                'cash_interest_earned': cash_interest_earned,
                
                # Expenses  
                'operating_expenses': monthly_operating_expenses,
                'mortgage_pi_payment': mortgage_pi_payment,
                'escrow_payment': monthly_escrow_payment,
                'total_mortgage_payment': total_mortgage_payment,
                'principal_payment': principal_payment,
                'interest_payment': interest_payment,
                'quarterly_tax_payment': quarterly_tax_payment,
                
                # Escrow activity
                'escrow_balance': escrow_balance,
                'property_tax_payment': property_tax_payment,
                'insurance_payment': insurance_payment,
                
                # Cash flow
                'noi': noi,
                'operating_cash_flow': operating_cash_flow,
                'net_cash_flow_after_taxes': operating_cash_flow - quarterly_tax_payment,
                
                # Balances
                'cash_balance': cash_balance,
                'excess_cash': excess_cash,
                'operating_reserve': min(cash_balance, self.operating_cash_reserve),
                
                # Property and equity
                'property_value': property_value,
                'mortgage_balance': mortgage_balance,
                'monthly_appreciation': monthly_appreciation,
                'principal_paydown': principal_payment,
                'current_equity': current_equity,
                'monthly_depreciation': monthly_depreciation,
                
                # Tax items (monthly taxable income for reference)
                'monthly_taxable_income': noi - interest_payment - monthly_depreciation,
                'quarterly_tax_liability': quarterly_tax_liability
            })
        
        return {
            'monthly_data': monthly_data,
            'summary': self._calculate_rental_summary(monthly_data),
            'final_values': {
                'final_cash_balance': cash_balance,
                'final_property_value': property_value,
                'final_mortgage_balance': mortgage_balance,
                'final_equity': current_equity
            }
        }
    
    def calculate_monthly_stock_dcf(self) -> Dict:
        """Calculate month-by-month stock investment scenario"""
        
        prop = self.analysis.property
        sale = self.analysis.sale_assumptions
        years = self.analysis.analysis_years
        
        # Calculate initial investment from property sale
        initial_investment = self._calculate_after_tax_sale_proceeds()
        
        # Initialize tracking
        monthly_data = []
        stock_balance = initial_investment
        
        current_date = datetime(2025, 9, 1)
        
        for month in range(years * 12):
            month_year = current_date + relativedelta(months=month)
            
            # === STOCK APPRECIATION ===
            monthly_stock_rate = self.stock_market_rate / 12
            monthly_stock_return = stock_balance * monthly_stock_rate
            stock_balance += monthly_stock_return
            
            # === RECORD MONTHLY DATA ===
            monthly_data.append({
                'month': month + 1,
                'date': month_year.strftime('%Y-%m-%d'),
                'year': month_year.year,
                'month_name': month_year.strftime('%B'),
                
                # Stock investment
                'stock_balance': stock_balance,
                'monthly_stock_return': monthly_stock_return,
                'cumulative_gains': stock_balance - initial_investment,
                
                # No cash flows during holding period
                'monthly_cash_flow': 0,
                'cash_balance': 0,
                'operating_cash_flow': 0
            })
        
        return {
            'monthly_data': monthly_data,
            'initial_investment': initial_investment,
            'final_stock_value': stock_balance,
            'total_stock_gains': stock_balance - initial_investment,
            'summary': self._calculate_stock_summary(monthly_data, initial_investment)
        }
    
    def compare_scenarios(self, use_1031_exchange: bool = False) -> Dict:
        """Compare rental vs stock scenarios with terminal values"""
        
        rental_dcf = self.calculate_monthly_rental_dcf()
        stock_dcf = self.calculate_monthly_stock_dcf()
        years = self.analysis.analysis_years
        
        # Calculate terminal values (sale at end of period)
        rental_terminal = self._calculate_rental_terminal_value(rental_dcf, use_1031_exchange)
        stock_terminal = self._calculate_stock_terminal_value(stock_dcf)
        
        # Total returns
        rental_total_return = (rental_dcf['final_values']['final_cash_balance'] + 
                              rental_terminal['net_sale_proceeds'])
        
        stock_total_return = stock_terminal['net_proceeds_after_tax']
        
        # Determine recommendation
        if rental_total_return > stock_total_return:
            recommendation = "KEEP_RENTAL"
            advantage = rental_total_return - stock_total_return
            advantage_pct = advantage / stock_total_return
        else:
            recommendation = "SELL_NOW"
            advantage = stock_total_return - rental_total_return
            advantage_pct = advantage / rental_total_return
        
        return {
            'rental_scenario': {
                'dcf': rental_dcf,
                'terminal_value': rental_terminal,
                'total_return': rental_total_return
            },
            'stock_scenario': {
                'dcf': stock_dcf,  
                'terminal_value': stock_terminal,
                'total_return': stock_total_return
            },
            'comparison': {
                'recommendation': recommendation,
                'advantage_amount': advantage,
                'advantage_percent': advantage_pct,
                'total_return_difference': rental_total_return - stock_total_return
            }
        }
    
    # === HELPER METHODS ===
    
    def _get_monthly_rent(self, month: int, years_elapsed: float) -> float:
        """Get monthly rent accounting for scenario-specific phase transitions and annual rent increases"""
        prop = self.analysis.property
        market = self.analysis.market_assumptions
        
        # Calculate which year we're in (0-based) for annual rent increases
        year_number = int(years_elapsed)  # This floors to get complete years
        
        # Handle JT scenario phase transition
        if self.scenario_name == "jt_scenario":
            # Phase 1: First 2 years (24 months) - Only Unit B at $2,200
            if month < 24:
                base_rent = 2200
                # Apply annual rent increases (only complete years)
                return base_rent * ((1 + market.rent_growth_rate) ** year_number)
            else:
                # Phase 2: After 2 years - Mom in Unit A ($1,500) + Unit B continues ($2,300)
                unit_a_base = 1500  # Family rate for mom
                unit_b_base = 2300  # Market rate continues
                
                # Apply rent growth from start of phase 2 (complete years since year 2)
                phase_years = max(0, year_number - 2)  # Years since phase 2 started
                unit_a_rent = unit_a_base * ((1 + market.rent_growth_rate) ** phase_years)
                unit_b_rent = unit_b_base * ((1 + market.rent_growth_rate) ** phase_years)
                
                return unit_a_rent + unit_b_rent
        else:
            # Standard scenario - annual rent increases only
            return prop.total_monthly_rent * ((1 + market.rent_growth_rate) ** year_number)
    
    def _calculate_annual_depreciation(self) -> float:
        """Calculate annual depreciation (27.5 year residential)"""
        prop = self.analysis.property
        # Assume 20% land value (non-depreciable)
        depreciable_basis = prop.cost_basis * 0.80
        return depreciable_basis / 27.5
    
    def _calculate_monthly_operating_expenses(self, monthly_rent: float, years_elapsed: float) -> float:
        """Calculate monthly operating expenses (excluding mortgage)"""
        exp = self.analysis.expenses
        
        # Expenses that grow with inflation (2.5% annually)
        inflation_factor = (1 + 0.025) ** years_elapsed
        
        # Base expenses (excluding mortgage payment)
        base_expenses = (
            exp.property_tax_monthly + 
            exp.insurance_monthly + 
            exp.other_monthly
        ) * inflation_factor
        
        # Percentage-based expenses (based on current rent)
        percentage_expenses = monthly_rent * (
            exp.maintenance_percent + 
            exp.vacancy_percent + 
            exp.management_percent
        )
        
        return base_expenses + percentage_expenses
    
    def _get_loan_info(self) -> Dict:
        """Get loan amortization info from main calculator"""
        from calculator import SellVsKeepCalculator
        calc = SellVsKeepCalculator(self.analysis)
        return calc.get_loan_payoff_info()
    
    def _is_quarterly_tax_month(self, month: int) -> bool:
        """Check if current month has quarterly tax payment"""
        return any(month == tax_month for tax_month, _ in self.quarterly_tax_dates)
    
    def _estimate_quarterly_tax_payment(self) -> float:
        """Estimate quarterly tax payment (simplified)"""
        # For now, use a simplified estimate
        # In practice, this would be 25% of estimated annual tax liability
        prop = self.analysis.property
        annual_rent = prop.total_monthly_rent * 12
        annual_depreciation = self._calculate_annual_depreciation()
        
        # Rough estimate of taxable rental income
        estimated_annual_taxable = annual_rent * 0.3  # Rough after expenses/interest/depreciation
        estimated_annual_tax = estimated_annual_taxable * self.combined_ordinary_rate
        
        return estimated_annual_tax / 4  # Quarterly payment
    
    def _calculate_quarterly_tax_payment(self, monthly_rent: float, monthly_expenses: float, 
                                       interest_payment: float, monthly_depreciation: float,
                                       estimated_payment: float) -> float:
        """Calculate actual quarterly tax payment based on taxable rental income"""
        
        # Calculate quarterly taxable rental income
        # Rental income - operating expenses - mortgage interest - depreciation
        quarterly_gross_income = monthly_rent * 3  # 3 months in quarter
        quarterly_operating_expenses = monthly_expenses * 3
        quarterly_interest = interest_payment * 3
        quarterly_depreciation = monthly_depreciation * 3
        
        # Taxable income = rental income - all deductible expenses
        quarterly_taxable_income = (quarterly_gross_income - quarterly_operating_expenses - 
                                  quarterly_interest - quarterly_depreciation)
        
        # Apply combined tax rate (32% federal + 4.25% NC = 36.25%)
        if quarterly_taxable_income > 0:
            quarterly_tax = quarterly_taxable_income * self.combined_ordinary_rate
            return max(0, quarterly_tax)
        else:
            # If loss, no tax payment (though in practice, losses might offset other income)
            return 0
    
    def _calculate_after_tax_sale_proceeds(self) -> float:
        """Calculate after-tax proceeds from selling property now"""
        prop = self.analysis.property
        sale = self.analysis.sale_assumptions
        
        # Sale proceeds
        gross_proceeds = prop.current_value
        selling_costs = gross_proceeds * sale.selling_costs_percent
        mortgage_payoff = prop.mortgage_balance
        
        # Capital gains with primary residence exclusion
        capital_gains = prop.capital_gain  # current_value - cost_basis
        primary_residence_exclusion = 250000  # Federal exclusion
        
        # Federal tax (with exclusion)
        federal_taxable_gains = max(0, capital_gains - primary_residence_exclusion)
        federal_tax = federal_taxable_gains * 0.20  # 20% federal capital gains
        
        # NC tax (no exclusion)
        nc_tax = capital_gains * 0.0425  # 4.25% NC tax
        
        total_tax = federal_tax + nc_tax
        
        return gross_proceeds - selling_costs - mortgage_payoff - total_tax
    
    def _calculate_rental_summary(self, monthly_data: List[Dict]) -> Dict:
        """Calculate summary metrics for rental scenario"""
        total_rent = sum(d['monthly_rent'] for d in monthly_data)
        total_expenses = sum(d['operating_expenses'] + d['total_mortgage_payment'] + d['quarterly_tax_payment'] 
                           for d in monthly_data)
        total_cash_flow = sum(d['operating_cash_flow'] for d in monthly_data)
        total_cash_interest = sum(d['cash_interest_earned'] for d in monthly_data)
        
        return {
            'total_rental_income': total_rent,
            'total_expenses': total_expenses,
            'total_operating_cash_flow': total_cash_flow,
            'total_cash_interest_earned': total_cash_interest,
            'average_monthly_cash_flow': total_cash_flow / len(monthly_data),
            'final_cash_balance': monthly_data[-1]['cash_balance']
        }
    
    def _calculate_stock_summary(self, monthly_data: List[Dict], initial_investment: float) -> Dict:
        """Calculate summary metrics for stock scenario"""
        final_balance = monthly_data[-1]['stock_balance']
        total_gains = final_balance - initial_investment
        
        return {
            'initial_investment': initial_investment,
            'final_stock_value': final_balance,
            'total_stock_gains': total_gains,
            'average_monthly_return': total_gains / len(monthly_data)
        }
    
    def _calculate_rental_terminal_value(self, rental_dcf: Dict, use_1031_exchange: bool = False) -> Dict:
        """Calculate proceeds from selling rental property at end"""
        final_values = rental_dcf['final_values']
        sale = self.analysis.sale_assumptions
        
        final_property_value = final_values['final_property_value']
        final_mortgage_balance = final_values['final_mortgage_balance']
        
        # Selling costs
        selling_costs = final_property_value * sale.selling_costs_percent
        
        if use_1031_exchange:
            # 1031 Like-Kind Exchange - defer all taxes
            capital_gains_tax = 0
            depreciation_recapture_tax = 0
            net_sale_proceeds = final_property_value - selling_costs - final_mortgage_balance
        else:
            # Regular sale with taxes
            # Capital gains tax
            total_appreciation = final_property_value - self.analysis.property.current_value
            capital_gains_tax = total_appreciation * 0.2425  # 24.25% combined rate
            
            # Depreciation recapture
            total_depreciation = self._calculate_annual_depreciation() * self.analysis.analysis_years
            depreciation_recapture_tax = total_depreciation * 0.2925  # 29.25% combined rate
            
            # Net proceeds
            net_sale_proceeds = (final_property_value - selling_costs - final_mortgage_balance - 
                               capital_gains_tax - depreciation_recapture_tax)
        
        return {
            'final_property_value': final_property_value,
            'selling_costs': selling_costs,
            'final_mortgage_balance': final_mortgage_balance,
            'capital_gains_tax': capital_gains_tax,
            'depreciation_recapture_tax': depreciation_recapture_tax,
            'net_sale_proceeds': net_sale_proceeds,
            'is_1031_exchange': use_1031_exchange
        }
    
    def _calculate_stock_terminal_value(self, stock_dcf: Dict) -> Dict:
        """Calculate after-tax proceeds from selling stocks at end"""
        final_stock_value = stock_dcf['final_stock_value']
        initial_investment = stock_dcf['initial_investment']
        
        # Capital gains on stocks
        stock_gains = final_stock_value - initial_investment
        capital_gains_tax = stock_gains * 0.2425  # 24.25% combined rate
        
        net_proceeds = final_stock_value - capital_gains_tax
        
        return {
            'final_stock_value': final_stock_value,
            'stock_capital_gains': stock_gains,
            'capital_gains_tax': capital_gains_tax,
            'net_proceeds_after_tax': net_proceeds
        }