import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
from models import Property, Unit, Expenses, SaleAssumptions, MarketAssumptions, Analysis
from monthly_dcf_calculator import MonthlyDCFCalculator
from property_loader import PropertyLoader
from scenario_manager import ScenarioManager
from risk_analyzer import RiskAnalyzer
from expense_documentation import ExpenseDocumentation

# Page config
st.set_page_config(
    page_title="Monthly DCF Rental Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 Monthly DCF Rental Analysis")
st.markdown("Month-by-month cash flow analysis with quarterly taxes and cash management")

# Initialize property loader and scenario manager
loader = PropertyLoader()
scenario_mgr = ScenarioManager()

# Sidebar for property selection and inputs
with st.sidebar:
    st.header("🏠 Select Property")
    
    # Property selection
    available_properties = loader.list_properties()
    
    if available_properties:
        property_options = ["Manual Entry"] + [f"{prop['name']} ({prop['address']})" for prop in available_properties]
        # Default to Eagle Drive property if available
        default_index = 1 if len(available_properties) > 0 else 0
        selected_property = st.selectbox("Choose Property", property_options, index=default_index)
        
        if selected_property != "Manual Entry":
            # Find selected property
            property_index = property_options.index(selected_property) - 1
            property_file = available_properties[property_index]['file']
            
            # Load property data
            property_data = loader.load_property(property_file)
            
            if property_data:
                st.success(f"✅ Loaded: {property_data['name']}")
                
                # Analysis parameters
                st.header("📊 Analysis Parameters")
                analysis_years = st.slider("Years to Analyze", 1, 30, 10)
                
                # 1031 Exchange option
                use_1031 = st.checkbox(
                    "Use 1031 Like-Kind Exchange at End", 
                    value=False,
                    help="Defer capital gains and depreciation recapture taxes by exchanging into another investment property"
                )
                
                # Scenario selection - dynamic based on property
                scenarios = property_data.get('scenarios', {})
                scenario_options = list(scenarios.keys())
                
                if not scenario_options:
                    st.error("No scenarios found in property data")
                    st.stop()
                
                # Create display names from scenario descriptions
                scenario_names = {}
                for scenario_key in scenario_options:
                    scenario_data = scenarios[scenario_key]
                    description = scenario_data.get('description', scenario_key.replace('_', ' ').title())
                    scenario_names[scenario_key] = description
                
                selected_scenario = st.selectbox(
                    "Rental Scenario",
                    scenario_options,
                    format_func=lambda x: scenario_names.get(x, x)
                )
                
                # Convert to models using property loader
                try:
                    analysis = loader.property_to_models(property_data, selected_scenario)
                    analysis.analysis_years = analysis_years  # Update with user selection
                except Exception as e:
                    st.error(f"Error converting property data: {e}")
                    st.stop()
            else:
                st.error("Failed to load property data")
                st.stop()
        else:
            st.error("Manual entry not implemented yet")
            st.stop()
    else:
        st.error("No properties found. Please add property files to the properties/ directory.")
        st.stop()

# Main content area
if 'analysis' in locals():
    # Run monthly DCF calculations
    calculator = MonthlyDCFCalculator(analysis, selected_scenario)
    
    with st.spinner("Calculating monthly DCF scenarios..."):
        comparison = calculator.compare_scenarios(use_1031_exchange=use_1031)
    
    # Extract results
    rental_scenario = comparison['rental_scenario']
    stock_scenario = comparison['stock_scenario']
    recommendation = comparison['comparison']['recommendation']
    advantage_amount = comparison['comparison']['advantage_amount']
    advantage_percent = comparison['comparison']['advantage_percent']
    
    # Display recommendation
    st.header("🎯 Recommendation")
    
    if recommendation == "KEEP_RENTAL":
        st.success(f"**KEEP THE RENTAL** - Advantage: ${advantage_amount:,.0f} ({advantage_percent:.1%})")
        st.markdown(f"**Rental Total Return:** ${rental_scenario['total_return']:,.0f}")
        st.markdown(f"**Stock Total Return:** ${stock_scenario['total_return']:,.0f}")
    else:
        st.error(f"**SELL NOW** - Advantage: ${advantage_amount:,.0f} ({advantage_percent:.1%})")
        st.markdown(f"**Stock Total Return:** ${stock_scenario['total_return']:,.0f}")
        st.markdown(f"**Rental Total Return:** ${rental_scenario['total_return']:,.0f}")
    
    # Create tabs for detailed analysis
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Monthly Cash Flows", 
        "💰 Cash vs Equity", 
        "📋 Cash Flow Tables",
        "⚠️ Risk Analysis",
        "🏠 Property Details",
        "📊 Summary Tables",
        "🔍 Methodology"
    ])
    
    with tab1:
        st.header("Monthly Cash Flows")
        
        # Convert monthly data to DataFrames
        rental_df = pd.DataFrame(rental_scenario['dcf']['monthly_data'])
        stock_df = pd.DataFrame(stock_scenario['dcf']['monthly_data'])
        
        # Cash flow chart
        fig = go.Figure()
        
        # Add rental cash flow
        fig.add_trace(go.Scatter(
            x=rental_df['date'],
            y=rental_df['operating_cash_flow'],
            mode='lines',
            name='Rental Cash Flow',
            line=dict(color='green', width=2)
        ))
        
        # Add cash balance
        fig.add_trace(go.Scatter(
            x=rental_df['date'],
            y=rental_df['cash_balance'],
            mode='lines',
            name='Cash Balance',
            line=dict(color='blue', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Monthly Cash Flow and Cash Balance",
            xaxis_title="Date",
            yaxis_title="Monthly Cash Flow ($)",
            yaxis2=dict(
                title="Cash Balance ($)",
                overlaying='y',
                side='right'
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Property value growth
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=rental_df['date'],
            y=rental_df['property_value'],
            mode='lines',
            name='Property Value',
            line=dict(color='orange', width=2)
        ))
        
        fig2.add_trace(go.Scatter(
            x=stock_df['date'],
            y=stock_df['stock_balance'],
            mode='lines',
            name='Stock Value',
            line=dict(color='purple', width=2)
        ))
        
        fig2.update_layout(
            title="Property Value vs Stock Investment Growth",
            xaxis_title="Date",
            yaxis_title="Value ($)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("Cash vs Equity Analysis")
        
        # Create cash vs equity breakdown
        fig = go.Figure()
        
        # Cash component (cash balance)
        fig.add_trace(go.Scatter(
            x=rental_df['date'],
            y=rental_df['cash_balance'],
            mode='lines',
            name='Cash (Liquid)',
            line=dict(color='green', width=2),
            fill='tozeroy'
        ))
        
        # Equity component (property equity)
        fig.add_trace(go.Scatter(
            x=rental_df['date'],
            y=rental_df['current_equity'],
            mode='lines',
            name='Property Equity (Illiquid)',
            line=dict(color='red', width=2)
        ))
        
        # Stock investment (for comparison)
        fig.add_trace(go.Scatter(
            x=stock_df['date'],
            y=stock_df['stock_balance'],
            mode='lines',
            name='Stock Investment (Liquid)',
            line=dict(color='purple', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Cash vs Equity Risk Analysis",
            xaxis_title="Date",
            yaxis_title="Value ($)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk metrics
        final_cash = rental_df.iloc[-1]['cash_balance']
        final_equity = rental_df.iloc[-1]['current_equity']
        total_rental_value = final_cash + final_equity
        
        st.subheader("Risk Breakdown (Final Year)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Cash (Liquid)", 
                f"${final_cash:,.0f}",
                f"{final_cash/total_rental_value:.1%} of total"
            )
        
        with col2:
            st.metric(
                "Equity (Illiquid)", 
                f"${final_equity:,.0f}",
                f"{final_equity/total_rental_value:.1%} of total"
            )
        
        with col3:
            st.metric(
                "Stock (Liquid)", 
                f"${stock_df.iloc[-1]['stock_balance']:,.0f}",
                "100% liquid"
            )
    
    with tab3:
        st.header("Detailed Cash Flow Tables")
        
        # Convert monthly data to DataFrames
        rental_df = pd.DataFrame(rental_scenario['dcf']['monthly_data'])
        stock_df = pd.DataFrame(stock_scenario['dcf']['monthly_data'])
        
        st.subheader("Scenario A: Rental Property Cash Flows")
        
        # Create detailed rental cash flow table with escrow breakdown
        rental_table_data = rental_df[[
            'date', 'month_name', 'year',
            'monthly_rent', 'operating_expenses', 'mortgage_pi_payment', 'total_mortgage_payment',
            'escrow_payment', 'escrow_balance', 'property_tax_payment', 'insurance_payment',
            'quarterly_tax_payment', 'operating_cash_flow', 'cash_interest_earned',
            'cash_balance', 'property_value', 'current_equity'
        ]].copy()
        
        # Format columns for display
        rental_table_data.columns = [
            'Date', 'Month', 'Year',
            'Rental Income', 'Operating Expenses', 'Mortgage P&I', 'Total Payment w/Escrow',
            'Escrow Payment', 'Escrow Balance', 'Property Tax Paid', 'Insurance Paid',
            'Quarterly Taxes', 'Operating Cash Flow', 'Cash Interest',
            'Cash Balance', 'Property Value', 'Total Equity'
        ]
        
        # Format currency columns
        currency_cols = ['Rental Income', 'Operating Expenses', 'Mortgage P&I', 'Total Payment w/Escrow',
                        'Escrow Payment', 'Escrow Balance', 'Property Tax Paid', 'Insurance Paid',
                        'Quarterly Taxes', 'Operating Cash Flow', 'Cash Interest',
                        'Cash Balance', 'Property Value', 'Total Equity']
        
        for col in currency_cols:
            rental_table_data[col] = rental_table_data[col].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(rental_table_data, use_container_width=True)
        
        # Add download button for rental data
        rental_csv = rental_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Rental Cash Flow CSV",
            data=rental_csv,
            file_name=f"rental_cashflow_{selected_scenario}_{analysis_years}yr.csv",
            mime="text/csv"
        )
        
        st.subheader("Scenario B: Stock Investment Cash Flows")
        
        # Create stock investment table
        stock_table_data = stock_df[[
            'date', 'month_name', 'year',
            'stock_balance', 'monthly_stock_return', 'cumulative_gains'
        ]].copy()
        
        stock_table_data.columns = [
            'Date', 'Month', 'Year',
            'Stock Balance', 'Monthly Return', 'Cumulative Gains'
        ]
        
        # Format currency columns for stock data
        stock_currency_cols = ['Stock Balance', 'Monthly Return', 'Cumulative Gains']
        for col in stock_currency_cols:
            stock_table_data[col] = stock_table_data[col].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(stock_table_data, use_container_width=True)
        
        # Add download button for stock data
        stock_csv = stock_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Stock Investment CSV",
            data=stock_csv,
            file_name=f"stock_investment_{analysis_years}yr.csv",
            mime="text/csv"
        )
        
        # Terminal value comparison table
        st.subheader("Terminal Value Comparison")
        
        rental_terminal = rental_scenario['terminal_value']
        stock_terminal = stock_scenario['terminal_value']
        
        terminal_comparison = pd.DataFrame({
            'Component': [
                'Final Asset Value',
                'Selling Costs',
                'Mortgage Balance',
                'Capital Gains Tax',
                'Depreciation Recapture Tax',
                'Net Sale Proceeds',
                '1031 Exchange Used'
            ],
            'Rental Property': [
                f"${rental_terminal['final_property_value']:,.0f}",
                f"${rental_terminal['selling_costs']:,.0f}",
                f"${rental_terminal['final_mortgage_balance']:,.0f}",
                f"${rental_terminal['capital_gains_tax']:,.0f}",
                f"${rental_terminal['depreciation_recapture_tax']:,.0f}",
                f"${rental_terminal['net_sale_proceeds']:,.0f}",
                f"{'Yes' if rental_terminal['is_1031_exchange'] else 'No'}"
            ],
            'Stock Investment': [
                f"${stock_terminal['final_stock_value']:,.0f}",
                "$0",
                "$0", 
                f"${stock_terminal['capital_gains_tax']:,.0f}",
                "$0",
                f"${stock_terminal['net_proceeds_after_tax']:,.0f}",
                "N/A"
            ]
        })
        
        st.table(terminal_comparison)
    
    with tab4:
        st.header("Risk Analysis")
        
        # Run risk analysis
        risk_analyzer = RiskAnalyzer(analysis, selected_scenario)
        
        with st.spinner("Analyzing downside risks..."):
            risk_report = risk_analyzer.comprehensive_risk_report()
        
        # Risk summary
        risk_summary = risk_report['risk_summary']
        
        st.subheader("🎯 Risk Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Monthly Carrying Cost",
                f"${risk_summary['monthly_carrying_cost']:,.0f}",
                help="Monthly cost to carry property with no rental income (mortgage + taxes + insurance + other)"
            )
        
        with col2:
            st.metric(
                "Max Vacancy Shortfall", 
                f"${risk_summary['max_vacancy_cash_shortfall']:,.0f}",
                help="Maximum cash injection needed for 6-month vacancy scenario"
            )
        
        with col3:
            st.metric(
                "Recommended Emergency Fund",
                f"${risk_summary['recommended_emergency_fund']:,.0f}",
                help="Recommended cash reserves for property operations"
            )
        
        # Cash flexibility score
        flexibility_score = risk_summary['cash_flexibility_score']
        if "EXCELLENT" in flexibility_score:
            st.success(f"💪 **Cash Flexibility:** {flexibility_score}")
        elif "GOOD" in flexibility_score:
            st.info(f"👍 **Cash Flexibility:** {flexibility_score}")
        elif "MODERATE" in flexibility_score:
            st.warning(f"⚠️ **Cash Flexibility:** {flexibility_score}")
        else:
            st.error(f"🚨 **Cash Flexibility:** {flexibility_score}")
        
        # High risk factors
        if risk_summary['high_risk_factors']:
            st.subheader("🚨 High Risk Factors")
            for risk in risk_summary['high_risk_factors']:
                st.error(f"• {risk}")
        else:
            st.success("✅ No major risk factors identified")
        
        # Vacancy analysis details
        st.subheader("📊 Vacancy Risk Analysis")
        
        vacancy_data = []
        for scenario in risk_report['vacancy_analysis']['vacancy_scenarios']:
            vacancy_data.append({
                'Vacancy Start (Month)': scenario['vacancy_start_month'],
                'Lost Rent': f"${scenario['total_lost_rent']:,.0f}",
                'Max Cash Shortfall': f"${scenario['max_cash_shortfall']:,.0f}",
                'Months Cash Negative': scenario['months_cash_negative'],
                'Risk Level': '🔴 HIGH' if scenario['max_cash_shortfall'] > 50000 
                           else '🟡 MEDIUM' if scenario['max_cash_shortfall'] > 10000 
                           else '🟢 LOW'
            })
        
        st.table(pd.DataFrame(vacancy_data))
        
        # Property value shock analysis
        st.subheader("🏠 Property Value Shock Analysis")
        
        current_value = risk_report['property_value_shock_analysis']['current_property_value']
        current_ltv = risk_report['property_value_shock_analysis']['current_ltv']
        
        st.write(f"**Current Property Value:** ${current_value:,.0f}")
        st.write(f"**Current Loan-to-Value:** {current_ltv:.1%}")
        
        shock_data = []
        for shock in risk_report['property_value_shock_analysis']['shock_scenarios']:
            status = "🔴 Underwater" if shock['is_underwater'] else \
                    "🟡 No Refinance" if not shock['can_refinance'] else \
                    "🟢 OK"
            
            shock_data.append({
                'Value Decline': f"{shock['shock_percentage']}%",
                'New Property Value': f"${shock['shocked_property_value']:,.0f}",
                'New LTV': f"{shock['new_ltv_ratio']:.1%}",
                'Equity Loss': f"${shock['equity_loss']:,.0f}",
                'Status': status
            })
        
        st.table(pd.DataFrame(shock_data))
        
        # Recommendations
        st.subheader("💡 Risk Management Recommendations")
        
        recommendations = []
        
        if risk_summary['max_vacancy_cash_shortfall'] > 0:
            recommendations.append(f"💰 Maintain emergency fund of ${risk_summary['recommended_emergency_fund']:,.0f}")
        
        if selected_scenario in ['jt_scenario', 'unit_b_only']:
            recommendations.append("🔄 Consider diversifying income streams (both units rented)")
        
        if risk_summary['max_vacancy_cash_shortfall'] > 30000:
            recommendations.append("📋 Consider landlord insurance with loss of rent coverage")
            recommendations.append("🔍 Implement rigorous tenant screening to minimize vacancy risk")
        
        recommendations.append("📈 Monitor local rental market conditions regularly")
        recommendations.append("🏠 Consider property improvements to justify higher rents")
        
        for rec in recommendations:
            st.write(f"• {rec}")
    
    with tab5:
        st.header("Property Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Property Info")
            st.write(f"**Address:** {analysis.property.address}")
            st.write(f"**Current Value:** ${analysis.property.current_value:,}")
            st.write(f"**Cost Basis:** ${analysis.property.cost_basis:,}")
            st.write(f"**Capital Gain:** ${analysis.property.capital_gain:,}")
            st.write(f"**Mortgage Balance:** ${analysis.property.mortgage_balance:,}")
            st.write(f"**Total Monthly Rent:** ${analysis.property.total_monthly_rent:,}")
        
        with col2:
            st.subheader("Monthly Expenses")
            st.write(f"**Property Tax:** ${analysis.expenses.property_tax_monthly:,}")
            st.write(f"**Insurance:** ${analysis.expenses.insurance_monthly:,}")
            st.write(f"**Mortgage Payment:** ${analysis.expenses.mortgage_payment:,}")
            st.write(f"**Maintenance:** {analysis.expenses.maintenance_percent:.1%} of rent")
            st.write(f"**Vacancy:** {analysis.expenses.vacancy_percent:.1%} of rent")
            st.write(f"**Management:** {analysis.expenses.management_percent:.1%} of rent")
            st.write(f"**Other:** ${analysis.expenses.other_monthly:,}")
        
        # Units table
        st.subheader("Units")
        units_data = []
        for unit in analysis.property.units:
            units_data.append({
                "Unit": unit.number,
                "Bedrooms": unit.bedrooms,
                "Bathrooms": unit.bathrooms,
                "Monthly Rent": f"${unit.monthly_rent:,}"
            })
        
        st.table(pd.DataFrame(units_data))
    
    with tab6:
        st.header("Summary Tables")
        
        # Rental scenario summary
        st.subheader("Rental Scenario Summary")
        rental_summary = rental_scenario['dcf']['summary']
        
        summary_data = {
            "Metric": [
                "Total Rental Income",
                "Total Expenses", 
                "Total Operating Cash Flow",
                "Total Cash Interest Earned",
                "Average Monthly Cash Flow",
                "Final Cash Balance"
            ],
            "Amount": [
                f"${rental_summary['total_rental_income']:,.0f}",
                f"${rental_summary['total_expenses']:,.0f}",
                f"${rental_summary['total_operating_cash_flow']:,.0f}",
                f"${rental_summary['total_cash_interest_earned']:,.0f}",
                f"${rental_summary['average_monthly_cash_flow']:,.0f}",
                f"${rental_summary['final_cash_balance']:,.0f}"
            ]
        }
        
        st.table(pd.DataFrame(summary_data))
        
        # Stock scenario summary
        st.subheader("Stock Scenario Summary")
        stock_summary = stock_scenario['dcf']['summary']
        
        stock_data = {
            "Metric": [
                "Initial Investment",
                "Final Stock Value",
                "Total Stock Gains",
                "Average Monthly Return"
            ],
            "Amount": [
                f"${stock_summary['initial_investment']:,.0f}",
                f"${stock_summary['final_stock_value']:,.0f}",
                f"${stock_summary['total_stock_gains']:,.0f}",
                f"${stock_summary['average_monthly_return']:,.0f}"
            ]
        }
        
        st.table(pd.DataFrame(stock_data))
        
        # Terminal values
        st.subheader("Terminal Value Analysis")
        rental_terminal = rental_scenario['terminal_value']
        stock_terminal = stock_scenario['terminal_value']
        
        terminal_data = {
            "Component": [
                "Rental: Final Property Value",
                "Rental: Selling Costs",
                "Rental: Final Mortgage Balance", 
                "Rental: Capital Gains Tax",
                "Rental: Depreciation Recapture Tax",
                "Rental: Net Sale Proceeds",
                "",
                "Stock: Final Stock Value",
                "Stock: Capital Gains Tax",
                "Stock: Net Proceeds After Tax"
            ],
            "Amount": [
                f"${rental_terminal['final_property_value']:,.0f}",
                f"${rental_terminal['selling_costs']:,.0f}",
                f"${rental_terminal['final_mortgage_balance']:,.0f}",
                f"${rental_terminal['capital_gains_tax']:,.0f}",
                f"${rental_terminal['depreciation_recapture_tax']:,.0f}",
                f"${rental_terminal['net_sale_proceeds']:,.0f}",
                "",
                f"${stock_terminal['final_stock_value']:,.0f}",
                f"${stock_terminal['capital_gains_tax']:,.0f}",
                f"${stock_terminal['net_proceeds_after_tax']:,.0f}"
            ]
        }
        
        st.table(pd.DataFrame(terminal_data))
    
    with tab7:
        st.header("Methodology")
        
        st.subheader("Monthly DCF Approach")
        st.markdown("""
        This analysis uses a month-by-month general ledger approach to model cash flows with the following key features:
        
        **Cash Management:**
        - Maintains $20,000 operating cash reserve at all times
        - Cash earns 4.5% annual interest (compounded monthly)
        - Excess cash above reserve compounds monthly
        
        **Tax Calculations:**
        - Quarterly estimated tax payments (Jan 15, Mar 15, Jun 15, Sep 15)
        - Combined tax rate: 36.25% (32% federal + 4.25% NC) on rental income
        - 27.5-year depreciation schedule reduces taxable income
        - Capital gains: 24.25% combined rate (20% federal + 4.25% NC)
        - Depreciation recapture: 29.25% combined rate (25% federal + 4.25% NC)
        
        **Growth Assumptions:**
        - Property appreciation: {analysis.market_assumptions.property_appreciation_rate:.1%} annually
        - Rent growth: {analysis.market_assumptions.rent_growth_rate:.1%} annually (higher than property due to demand/inflation)
        - Operating expense growth: 2.5% annually
        - Stock market return: {analysis.market_assumptions.stock_market_return:.1%} annually
        
        **Rental Scenario:**
        1. Monthly rental income (grows {analysis.market_assumptions.rent_growth_rate:.1%} annually)
        2. Monthly operating expenses (grow 2.5% annually)
        3. Monthly mortgage payments (principal + interest from amortization)
        4. Quarterly tax payments on taxable rental income
        5. Cash balance management with interest earnings
        6. Property appreciation and equity growth
        7. Terminal sale after analysis period
        
        **Stock Scenario:**
        - Initial investment from after-tax sale proceeds today
        - Monthly compounding at 7.5% annual rate
        - Terminal sale with capital gains tax
        
        **Primary Residence Tax Benefits:**
        - $250,000 federal capital gains exclusion (single filer)
        - Applies only to immediate sale, not future rental sale
        
        **1031 Like-Kind Exchange Option:**
        - IRC Section 1031 allows deferral of capital gains and depreciation recapture taxes
        - Must exchange into "like-kind" investment property within strict timelines
        - Defers taxes rather than eliminating them (taxes due when eventually sold)
        - Requires qualified intermediary and adherence to 45/180 day rules
        - When selected, terminal value calculation excludes capital gains and depreciation recapture taxes
        """)
        
        st.subheader("Key Assumptions")
        st.markdown(f"""
        - **Analysis Period:** {analysis_years} years
        - **Cash Savings Rate:** 4.5% annual
        - **Stock Market Return:** 7.5% annual
        - **Operating Cash Reserve:** $20,000
        - **Tax Status:** TX resident with NC rental property
        - **Income Level:** High earner (32% federal marginal rate)
        """)
        
        # Add expense methodology documentation
        st.divider()
        expense_doc = ExpenseDocumentation()
        expense_doc.show_expense_methodology()