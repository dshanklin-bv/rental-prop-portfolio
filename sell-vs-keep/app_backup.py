import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from models import Property, Unit, Expenses, SaleAssumptions, MarketAssumptions, Analysis
from calculator import SellVsKeepCalculator
from charts import ChartGenerator
from property_loader import PropertyLoader
from scenario_manager import ScenarioManager

# Page config
st.set_page_config(
    page_title="Sell vs Keep Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 Sell vs Keep Rental Property Calculator")
st.markdown("Should you sell your multi-family property now or keep it as a rental? Let's find out!")

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
                
                # Show property summary
                summary = loader.get_property_summary(property_data)
                st.markdown(f"""
                **Address:** {summary['address']}  
                **Type:** {summary['property_type']}  
                **Current Value:** ${summary['current_value']:,}  
                **Cost Basis:** ${summary['cost_basis']:,}  
                **Capital Gain:** ${summary['current_value'] - summary['cost_basis']:,}  
                **Units:** {summary['total_units']}  
                **Monthly Rent:** ${summary['total_monthly_rent']:,}
                """)
                
                # Get base analysis
                analysis = loader.property_to_models(property_data, 'both_units')
                
                # Scenario selection
                st.subheader("📊 Scenario Selection")
                
                # Check if we have scenario data available
                scenario_summary = scenario_mgr.get_scenario_summary()
                if scenario_summary['combined_scenarios'] > 0:
                    # Use comprehensive scenario system
                    combined_scenarios = scenario_mgr.get_combined_scenarios()
                    
                    # Quick scenario selection
                    scenario_names = [s.name for s in combined_scenarios]
                    selected_combined = st.selectbox("Quick Scenarios", scenario_names, 
                                                   help="Pre-configured scenario combinations")
                    
                    # Advanced scenario builder
                    with st.expander("🔧 Advanced Scenario Builder"):
                        st.markdown("*Mix and match individual scenario components:*")
                        
                        # Property scenarios
                        prop_scenarios = scenario_mgr.get_property_scenarios()
                        prop_names = [s.name for s in prop_scenarios]
                        selected_prop = st.selectbox("Property Sale Scenario", prop_names)
                        
                        # Rental scenarios  
                        rental_scenarios = scenario_mgr.get_rental_scenarios()
                        rental_names = [s.name for s in rental_scenarios]
                        selected_rental = st.selectbox("Rental Strategy", rental_names)
                        
                        # Stock scenarios
                        stock_scenarios = scenario_mgr.get_stock_scenarios()
                        stock_names = [s.name for s in stock_scenarios]  
                        selected_stock = st.selectbox("Stock Investment", stock_names)
                        
                        # Tax scenarios
                        tax_scenarios = scenario_mgr.get_tax_scenarios()
                        tax_names = [s.name for s in tax_scenarios]
                        selected_tax = st.selectbox("Tax Treatment", tax_names)
                        
                        use_custom_scenario = st.checkbox("Use Custom Scenario Combination")
                    
                    # Apply selected scenario
                    if 'use_custom_scenario' in locals() and use_custom_scenario:
                        # Find scenario keys from names
                        prop_key = [k for k, v in scenario_mgr.scenarios_data['property_scenarios'].items() 
                                  if v['name'] == selected_prop][0]
                        rental_key = [k for k, v in scenario_mgr.scenarios_data['rental_scenarios'].items() 
                                    if v['name'] == selected_rental][0]  
                        stock_key = [k for k, v in scenario_mgr.scenarios_data['stock_market_scenarios'].items() 
                                   if v['name'] == selected_stock][0]
                        tax_key = [k for k, v in scenario_mgr.scenarios_data['tax_scenarios'].items() 
                                 if v['name'] == selected_tax][0]
                        
                        analysis = scenario_mgr.build_analysis_from_scenarios(
                            analysis, prop_key, rental_key, stock_key, tax_key)
                        
                        st.info(f"Custom scenario: {selected_prop} + {selected_rental} + {selected_stock} + {selected_tax}")
                    else:
                        # Use combined scenario
                        selected_combo = [s for s in combined_scenarios if s.name == selected_combined][0]
                        analysis = scenario_mgr.build_analysis_from_scenarios(
                            analysis, 
                            selected_combo.property_scenario,
                            selected_combo.rental_scenario, 
                            selected_combo.stock_scenario,
                            selected_combo.tax_scenario
                        )
                        st.success(f"Using: {selected_combo.description}")
                
                else:
                    # Fallback to simple scenarios if comprehensive system not available
                    scenarios = list(property_data.get('scenarios', {'both_units': {}}).keys())
                    selected_scenario = st.selectbox("Rental Scenario", scenarios, 
                                                   format_func=lambda x: x.replace('_', ' ').title())
                    analysis = loader.property_to_models(property_data, selected_scenario)
                use_json_data = True
            else:
                st.error("Failed to load property data")
                use_json_data = False
        else:
            use_json_data = False
    else:
        st.info("No saved properties found. Using manual entry.")
        use_json_data = False
    
    # Manual entry section (only show if not using JSON)
    if not use_json_data:
        st.header("📝 Manual Property Details")
        
        # Basic property info
        address = st.text_input("Property Address", value="123 Main St, City, State")
        current_value = st.number_input("Current Market Value ($)", min_value=1000, value=500000, step=5000)
        purchase_price = st.number_input("Original Purchase Price ($)", min_value=1000, value=350000, step=5000)
        purchase_date = st.date_input("Purchase Date", value=date(2021, 1, 1))
        mortgage_balance = st.number_input("Current Mortgage Balance ($)", min_value=0, value=200000, step=1000)
    
        
        # Units configuration for manual entry
        st.header("🏠 Units Configuration")
        num_units = st.number_input("Number of Units", min_value=1, max_value=20, value=4)
        
        # Collect unit information
        units = []
        total_rent = 0
        
        # Simple unit entry (assume similar units)
        st.subheader("Unit Details")
        rent_per_unit = st.number_input("Rent per Unit ($/month)", min_value=0, value=1200, step=50)
        bedrooms = st.number_input("Bedrooms per Unit", min_value=0, value=2)
        bathrooms = st.number_input("Bathrooms per Unit", min_value=0.5, value=1.0, step=0.5)
        
        # Create units
        for i in range(num_units):
            units.append(Unit(
                number=f"Unit {i+1}",
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                monthly_rent=rent_per_unit
            ))
            total_rent += rent_per_unit
        
        st.metric("Total Monthly Rent", f"${total_rent:,.0f}")
    else:
        # For JSON properties, just show the rent total
        total_rent = analysis.property.total_monthly_rent
        st.metric("Total Monthly Rent", f"${total_rent:,.0f}")
        
    # Manual overrides and final adjustments
    if use_json_data:
        st.header("🔧 Manual Overrides")
        st.markdown("*Fine-tune the scenario assumptions:*")
        
        with st.expander("Individual Unit Rent Overrides"):
            # Create rent input for each unit
            for i, unit in enumerate(analysis.property.units):
                current_rent = unit.monthly_rent
                new_rent = st.number_input(
                    f"{unit.number} Monthly Rent ($)", 
                    min_value=0, 
                    value=int(current_rent), 
                    step=50,
                    key=f"unit_rent_{i}",
                    help="Set to $0 to keep vacant"
                )
                unit.monthly_rent = new_rent
            
            # Show updated total
            total_rent = analysis.property.total_monthly_rent
            st.metric("Total Monthly Rent", f"${total_rent:,.0f}")
        
        with st.expander("Property Value & Market Overrides"):
            col1, col2 = st.columns(2)
            with col1:
                value_adjustment = st.slider("Property Value Adjustment (%)", -30, 30, 0, 5)
                if value_adjustment != 0:
                    analysis.property.current_value *= (1 + value_adjustment/100)
            
            with col2:
                # Show current assumptions
                st.metric("Current Property Value", f"${analysis.property.current_value:,.0f}")
                st.metric("Property Appreciation", f"{analysis.market_assumptions.property_appreciation_rate:.1%}")
                st.metric("Stock Return", f"{analysis.market_assumptions.stock_market_return:.1%}")
        
        # Scenario comparison option
        st.header("📊 Scenario Comparison")
        if st.checkbox("Compare Multiple Scenarios"):
            # Let user select 2-3 scenarios to compare
            available_combos = scenario_mgr.get_combined_scenarios()
            combo_names = [s.name for s in available_combos]
            
            selected_scenarios = st.multiselect(
                "Select scenarios to compare", 
                combo_names,
                default=combo_names[:2] if len(combo_names) >= 2 else combo_names,
                max_selections=3
            )
            
            if len(selected_scenarios) > 1:
                st.session_state.compare_scenarios = selected_scenarios
                st.session_state.do_comparison = True
            else:
                st.session_state.do_comparison = False
    
    # Minor adjustments for manual entry
    elif not use_json_data:
        st.header("⚙️ Final Adjustments")
        total_rent = sum(unit.monthly_rent for unit in units)
        st.metric("Total Monthly Rent", f"${total_rent:,.0f}")

# Main content area - only show if manual entry or allow adjustments for JSON
if not use_json_data:
    col1, col2 = st.columns(2)

    with col1:
        st.header("💰 Monthly Expenses")
        
        # Operating expenses
        prop_tax_annual = st.number_input("Property Tax (Annual $)", min_value=0, value=6000, step=100)
        insurance_annual = st.number_input("Insurance (Annual $)", min_value=0, value=2400, step=100)
        mortgage_payment = st.number_input("Mortgage Payment (Monthly $)", min_value=0, value=1200, step=50)
        
        # Percentage-based expenses
        maintenance_pct = st.slider("Maintenance (% of rent)", 0.0, 20.0, 5.0, 0.5) / 100
        vacancy_pct = st.slider("Vacancy Allowance (% of rent)", 0.0, 20.0, 5.0, 0.5) / 100
        management_pct = st.slider("Property Management (% of rent)", 0.0, 15.0, 0.0, 0.5) / 100
        
        other_monthly = st.number_input("Other Monthly Expenses ($)", min_value=0, value=0, step=25)

    with col2:
        st.header("📊 Analysis Assumptions")
        
        # Sale assumptions
        st.subheader("If You Sell")
        selling_costs_pct = st.slider("Selling Costs (% of sale price)", 0.0, 10.0, 6.0, 0.1) / 100
        cap_gains_tax = st.slider("Capital Gains Tax Rate (%)", 0.0, 40.0, 20.0, 1.0) / 100
        
        # Market assumptions
        st.subheader("Market Assumptions")
        property_appreciation = st.slider("Property Appreciation (% per year)", -5.0, 10.0, 3.0, 0.1) / 100
        stock_return = st.slider("Stock Market Return (% per year)", 0.0, 15.0, 10.0, 0.1) / 100
        
        # Analysis period
        analysis_years = st.slider("Analysis Period (years)", 1, 30, 10)
else:
    # For JSON properties, show key assumptions with ability to adjust
    st.header("📊 Key Assumptions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        property_appreciation = st.slider("Property Appreciation (% per year)", 
                                        -5.0, 10.0, 
                                        analysis.market_assumptions.property_appreciation_rate * 100, 
                                        0.1) / 100
    with col2:
        stock_return = st.slider("Stock Market Return (% per year)", 
                               0.0, 15.0, 
                               analysis.market_assumptions.stock_market_return * 100, 
                               0.1) / 100
    with col3:
        analysis_years = st.slider("Analysis Period (years)", 1, 30, analysis.analysis_years)
    
    # Update the analysis with new values
    analysis.market_assumptions.property_appreciation_rate = property_appreciation
    analysis.market_assumptions.stock_market_return = stock_return
    analysis.analysis_years = analysis_years

# === TABBED ANALYSIS INTERFACE ===
st.header("🚀 Comprehensive Analysis")

# Always run calculations when we have data
if use_json_data or 'current_value' in locals():
    
    # Create models for manual entry mode
    if not use_json_data:
        property_model = Property(
            address=address,
            current_value=current_value,
            original_purchase_price=purchase_price,
            cost_basis=purchase_price,  # For manual entry, assume cost_basis equals purchase price
            purchase_date=purchase_date,
            mortgage_balance=mortgage_balance,
            units=units
        )
        
        expenses_model = Expenses(
            property_tax_monthly=prop_tax_annual / 12,
            insurance_monthly=insurance_annual / 12,
            mortgage_payment=mortgage_payment,
            maintenance_percent=maintenance_pct,
            vacancy_percent=vacancy_pct,
            management_percent=management_pct,
            other_monthly=other_monthly
        )
        
        sale_assumptions = SaleAssumptions(
            selling_costs_percent=selling_costs_pct,
            capital_gains_tax_rate=cap_gains_tax
        )
        
        market_assumptions = MarketAssumptions(
            property_appreciation_rate=property_appreciation,
            stock_market_return=stock_return
        )
        
        analysis = Analysis(
            property=property_model,
            expenses=expenses_model,
            sale_assumptions=sale_assumptions,
            market_assumptions=market_assumptions,
            analysis_years=analysis_years
        )
    
    # Run calculation
    calculator = SellVsKeepCalculator(analysis)
    results = calculator.get_recommendation()
    
    # Display recommendation
    recommendation = results['recommendation']
    advantage = results['advantage_amount']
    advantage_pct = results['advantage_percent']
    
    if recommendation == "KEEP":
        st.success(f"## 🏠 KEEP THE RENTAL!")
        st.success(f"Keeping the property gives you **${advantage:,.0f} more** ({advantage_pct:.1%} better) after {analysis_years} years")
    else:
        st.error(f"## 💰 SELL NOW!")
        st.error(f"Selling now gives you **${advantage:,.0f} more** ({advantage_pct:.1%} better) after {analysis_years} years")
    
    # Key metrics
    sell_result = results['sell_scenario']
    keep_result = results['keep_scenario']
    
    st.subheader("📊 Scenario Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Sell Now + Stocks",
            value=f"${sell_result['total_return']:,.0f}",
            delta=f"{sell_result['irr']:.1%} IRR"
        )
    
    with col2:
        st.metric(
            label="🏠 Keep as Rental", 
            value=f"${keep_result['total_return']:,.0f}",
            delta=f"{keep_result['irr']:.1%} IRR"
        )
    
    with col3:
        st.metric(
            label="💡 Advantage",
            value=f"${advantage:,.0f}",
            delta=f"{advantage_pct:.1%} better"
        )
    
    # Charts
    st.subheader("📈 Visual Analysis")
    
    chart_gen = ChartGenerator()
    
    # Main comparison chart
    comparison_chart = chart_gen.create_comparison_chart(sell_result, keep_result, analysis_years)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Cash vs Equity Analysis
    st.subheader("💰 Cash vs Equity Risk Analysis")
    cash_equity_data = calculator.calculate_cash_vs_equity_projection()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cash projection chart
        cash_chart = chart_gen.create_cash_projection_chart(cash_equity_data)
        st.plotly_chart(cash_chart, use_container_width=True)
    
    with col2:
        # Equity buildup chart
        equity_chart = chart_gen.create_equity_buildup_chart(cash_equity_data)
        st.plotly_chart(equity_chart, use_container_width=True)
    
    # Loan amortization info
    loan_info = calculator.get_loan_payoff_info()
    if loan_info['payoff_date']:
        st.subheader("🏦 Mortgage Analysis")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Payoff Date", loan_info['payoff_date'])
        with col2:
            st.metric("Years Remaining", f"{loan_info['years_remaining']:.1f}")
        with col3:
            st.metric("Payments Left", f"{loan_info['remaining_payments']:,}")
        with col4:
            st.metric("Interest Remaining", f"${loan_info['total_interest_remaining']:,.0f}")
        
        # Amortization table
        with st.expander("📋 View Full Amortization Schedule"):
            if loan_info['amortization_schedule']:
                # Show first 24 months and allow download of full schedule
                schedule_df = pd.DataFrame(loan_info['amortization_schedule'][:24])
                schedule_df['payment'] = schedule_df['payment'].round(2)
                schedule_df['principal'] = schedule_df['principal'].round(2)
                schedule_df['interest'] = schedule_df['interest'].round(2)
                schedule_df['balance'] = schedule_df['balance'].round(2)
                
                st.dataframe(
                    schedule_df[['date', 'payment', 'principal', 'interest', 'balance']], 
                    use_container_width=True
                )
                
                if len(loan_info['amortization_schedule']) > 24:
                    st.info(f"Showing first 24 payments of {len(loan_info['amortization_schedule'])} total payments")
                
                # Download option
                full_schedule_df = pd.DataFrame(loan_info['amortization_schedule'])
                csv = full_schedule_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Full Amortization Schedule",
                    data=csv,
                    file_name=f"amortization_schedule_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    # Summary metrics for cash vs equity
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cash (10yr)", f"${cash_equity_data['summary']['total_cumulative_cash']:,.0f}")
    with col2:
        st.metric("Total Equity Buildup", f"${cash_equity_data['summary']['total_equity_buildup']:,.0f}")  
    with col3:
        st.metric("Final Net Equity", f"${cash_equity_data['summary']['final_net_equity']:,.0f}")
    
    # Additional analysis
    st.subheader("📊 Traditional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cash flow timeline
        cashflow_chart = chart_gen.create_cash_flow_timeline(keep_result, analysis_years)
        st.plotly_chart(cashflow_chart, use_container_width=True)
    
    with col2:
        # Sensitivity analysis
        base_rent = total_rent
        sensitivity_chart = chart_gen.create_sensitivity_analysis(base_rent, property_appreciation, calculator)
        st.plotly_chart(sensitivity_chart, use_container_width=True)
    
    # Detailed breakdown
    with st.expander("📋 Detailed Breakdown"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Sell Now Scenario")
            sell_df = pd.DataFrame([
                ["Current Property Value", f"${sell_result['gross_proceeds']:,.0f}"],
                ["Selling Costs", f"-${sell_result['selling_costs']:,.0f}"],
                ["Mortgage Payoff", f"-${sell_result['mortgage_payoff']:,.0f}"],
                ["Capital Gains Tax", f"-${sell_result['capital_gains_tax']:,.0f}"],
                ["After-Tax Proceeds", f"${sell_result['after_tax_proceeds']:,.0f}"],
                ["Stock Value After 10 Years", f"${sell_result['future_stock_value']:,.0f}"]
            ], columns=["Item", "Amount"])
            st.table(sell_df)
        
        with col2:
            st.subheader("🏠 Keep Rental Scenario")
            keep_df = pd.DataFrame([
                ["Monthly Rent", f"${keep_result['monthly_rent']:,.0f}"],
                ["Monthly Expenses", f"-${keep_result['monthly_expenses']:,.0f}"],
                ["Monthly Cash Flow", f"${keep_result['monthly_cash_flow']:,.0f}"],
                ["Total Cash Flows", f"${keep_result['total_cash_flows']:,.0f}"],
                ["Future Property Value", f"${keep_result['future_property_value']:,.0f}"],
                ["Future Sale Proceeds", f"${keep_result['future_net_proceeds']:,.0f}"]
            ], columns=["Item", "Amount"])
            st.table(keep_df)
        
        # Break-even analysis
        st.subheader("⚖️ Break-Even Analysis")
        breakeven_rent = results['break_even_rent']
        breakeven_appreciation = results['break_even_appreciation']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Break-Even Monthly Rent", f"${breakeven_rent:,.0f}")
            if breakeven_rent > total_rent:
                st.warning(f"Need ${breakeven_rent - total_rent:,.0f} more rent per month")
            else:
                st.success("Current rent exceeds break-even!")
        
        with col2:
            st.metric("Break-Even Appreciation Rate", f"{breakeven_appreciation:.1%}")
            if breakeven_appreciation > property_appreciation:
                st.warning(f"Need {(breakeven_appreciation - property_appreciation)*100:.1f}% more appreciation")
            else:
                st.success("Current appreciation assumption exceeds break-even!")

# Scenario comparison (if requested)
if hasattr(st.session_state, 'do_comparison') and st.session_state.do_comparison and hasattr(st.session_state, 'compare_scenarios'):
    st.header("🔄 Scenario Comparison")
    
    # Get base analysis for comparison
    if use_json_data:
        base_analysis = loader.property_to_models(property_data, 'both_units')
    else:
        # Use the current analysis from manual entry
        base_analysis = analysis
    
    # Build scenario combinations
    combined_scenarios = scenario_mgr.get_combined_scenarios()
    scenario_combinations = []
    
    for scenario_name in st.session_state.compare_scenarios:
        selected_combo = [s for s in combined_scenarios if s.name == scenario_name][0]
        scenario_combinations.append((
            selected_combo.property_scenario,
            selected_combo.rental_scenario, 
            selected_combo.stock_scenario,
            selected_combo.tax_scenario
        ))
    
    # Run comparison
    comparison_results = scenario_mgr.compare_scenarios(base_analysis, scenario_combinations)
    
    # Display results
    col1, col2, col3 = st.columns(len(st.session_state.compare_scenarios))
    
    for i, scenario_name in enumerate(st.session_state.compare_scenarios):
        combo_key = list(comparison_results.keys())[i]
        scenario_result = comparison_results[combo_key]
        
        with [col1, col2, col3][i]:
            st.subheader(scenario_name)
            
            rec = scenario_result['results']['recommendation']
            advantage = scenario_result['results']['advantage_amount']
            
            if rec == "KEEP":
                st.success(f"KEEP: +${advantage:,.0f}")
            else:
                st.error(f"SELL: +${advantage:,.0f}")
            
            sell_total = scenario_result['results']['sell_scenario']['total_return']
            keep_total = scenario_result['results']['keep_scenario']['total_return']
            
            st.metric("Sell Total", f"${sell_total:,.0f}")
            st.metric("Keep Total", f"${keep_total:,.0f}")
    
    # Comparison chart
    chart_gen = ChartGenerator()
    if len(st.session_state.compare_scenarios) > 1:
        scenario_data = []
        for i, scenario_name in enumerate(st.session_state.compare_scenarios):
            combo_key = list(comparison_results.keys())[i]
            results = comparison_results[combo_key]['results']
            scenario_data.append({
                'Scenario': scenario_name,
                'Sell Total': results['sell_scenario']['total_return'],
                'Keep Total': results['keep_scenario']['total_return'],
                'Advantage': results['advantage_amount'],
                'Recommendation': results['recommendation']
            })
        
        comparison_df = pd.DataFrame(scenario_data)
        
        # Create comparison bar chart
        fig = px.bar(comparison_df, x='Scenario', y=['Sell Total', 'Keep Total'], 
                    title="Scenario Comparison: Total Returns",
                    barmode='group')
        fig.update_layout(yaxis_tickformat='$,.0f')
        st.plotly_chart(fig, use_container_width=True)

# Export functionality
st.header("📤 Export Results")

if st.button("💾 Download Analysis", use_container_width=True):
    # Create summary data for export
    if use_json_data:
        address_export = analysis.property.address
        value_export = analysis.property.current_value
    else:
        address_export = address if 'address' in locals() else 'Unknown'
        value_export = current_value if 'current_value' in locals() else 0
    
    export_data = {
        'Property Address': [address_export],
        'Current Value': [value_export],
        'Analysis Years': [analysis_years if 'analysis_years' in locals() else 10],
        'Sell Total Return': [sell_result['total_return'] if 'sell_result' in locals() else 0],
        'Keep Total Return': [keep_result['total_return'] if 'keep_result' in locals() else 0],
        'Recommendation': [recommendation if 'recommendation' in locals() else 'Run analysis first']
    }
    
    df = pd.DataFrame(export_data)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📊 Download CSV",
        data=csv,
        file_name=f"sell_vs_keep_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("**Note:** This analysis is for informational purposes only. Consult with financial and tax professionals before making investment decisions.")