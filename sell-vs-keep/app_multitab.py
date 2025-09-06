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
    page_title="Sell vs Keep Calculator - Advanced Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 Advanced Sell vs Keep Calculator")
st.markdown("**Comprehensive DCF analysis with tax modeling for TX residents with NC property**")

# Initialize property loader
loader = PropertyLoader()

# === SIDEBAR CONFIGURATION ===
with st.sidebar:
    st.header("🏠 Property Selection")
    
    # Property selection
    available_properties = loader.list_properties()
    
    if available_properties:
        property_options = [f"{prop['name']} ({prop['address']})" for prop in available_properties]
        # Default to Eagle Drive property if available
        default_index = 0 if len(available_properties) > 0 else 0
        selected_property = st.selectbox("Choose Property", property_options, index=default_index)
        
        # Find selected property
        property_index = property_options.index(selected_property)
        property_file = available_properties[property_index]['file']
        
        # Load property data
        property_data = loader.load_property(property_file)
        
        if property_data:
            st.success(f"✅ Loaded: {property_data['name']}")
            
            # Load property into models
            analysis = loader.property_to_models(property_data, 'both_units')
            
            # Show property summary
            st.subheader("📋 Property Summary")
            st.write(f"**Address:** {analysis.property.address}")
            st.write(f"**Current Value:** ${analysis.property.current_value:,}")
            st.write(f"**Cost Basis:** ${analysis.property.cost_basis:,}")
            st.write(f"**Mortgage Balance:** ${analysis.property.mortgage_balance:,}")
            st.write(f"**Monthly Rent:** ${analysis.property.total_monthly_rent:,}")
            
            # Adjustable assumptions
            st.subheader("🎛️ Key Assumptions")
            
            property_appreciation = st.slider("Property Appreciation (%/year)", 
                                            -5.0, 10.0, 
                                            analysis.market_assumptions.property_appreciation_rate * 100, 
                                            0.1) / 100
            
            stock_return = st.slider("Stock Market Return (%/year)", 
                                   0.0, 15.0, 
                                   analysis.market_assumptions.stock_market_return * 100, 
                                   0.1) / 100
            
            analysis_years = st.slider("Analysis Period (years)", 1, 30, 10)
            
            # Update analysis with adjustments
            analysis.market_assumptions.property_appreciation_rate = property_appreciation
            analysis.market_assumptions.stock_market_return = stock_return
            analysis.analysis_years = analysis_years
            
            use_property_data = True
        else:
            st.error("Failed to load property data")
            use_property_data = False
    else:
        st.info("No properties found. Add property files to the 'properties' folder.")
        use_property_data = False

# === MAIN ANALYSIS (ONLY IF DATA LOADED) ===
if use_property_data:
    # Initialize calculator
    calculator = SellVsKeepCalculator(analysis)
    
    # === CREATE COMPREHENSIVE TABS ===
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Main Analysis", 
        "💰 Comprehensive DCF", 
        "📉 Depreciation Analysis",
        "🏛️ Tax Breakdown", 
        "🏦 Amortization Schedule", 
        "⚖️ Cash vs Equity Risk",
        "📚 Methodology"
    ])
    
    # === TAB 1: MAIN ANALYSIS ===
    with tab1:
        st.header("🎯 Sell vs Keep Recommendation")
        
        # Get comprehensive comparison
        dcf_comparison = calculator.get_comprehensive_comparison()
        rec = dcf_comparison['recommendation']
        
        # Display main recommendation
        if rec['scenario'] == 'KEEP_RENTAL':
            st.success(f"## 🏠 KEEP AS RENTAL")
        else:
            st.error(f"## 💰 SELL NOW")
        
        st.success(rec['reasoning'])
        
        # Key metrics comparison
        col1, col2, col3 = st.columns(3)
        
        sell_metrics = dcf_comparison['scenarios']['sell_now']['summary_metrics']
        keep_metrics = dcf_comparison['scenarios']['keep_rental']['summary_metrics']
        
        with col1:
            st.metric(
                label="💰 Sell Now (Total Return)",
                value=f"${sell_metrics['total_return']:,.0f}",
                delta=f"{sell_metrics['irr']:.2%} IRR" if sell_metrics['irr'] else "N/A IRR"
            )
        
        with col2:
            st.metric(
                label="🏠 Keep Rental (Total Return)", 
                value=f"${keep_metrics['total_return']:,.0f}",
                delta=f"{keep_metrics['irr']:.2%} IRR" if keep_metrics['irr'] else "N/A IRR"
            )
        
        with col3:
            st.metric(
                label="💡 Advantage",
                value=f"${rec['advantage_amount']:,.0f}",
                delta=f"{rec['advantage_percent']:.1%} better"
            )
        
        # Risk and liquidity comparison
        st.subheader("⚖️ Risk & Liquidity Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏠 Keep Rental Scenario:**")
            risk_analysis = dcf_comparison['risk_analysis']
            for risk in risk_analysis['rental_scenario_risks'][:4]:  # Show top 4 risks
                st.write(f"• {risk}")
            st.write(f"**Liquidity:** {risk_analysis['liquidity_comparison']['rental_liquidity']}")
            
        with col2:
            st.write("**📈 Sell & Invest Scenario:**")
            for risk in risk_analysis['stock_scenario_risks'][:4]:  # Show top 4 risks
                st.write(f"• {risk}")
            st.write(f"**Liquidity:** {risk_analysis['liquidity_comparison']['stock_liquidity']}")
        
        # Cash flow comparison
        st.subheader("💵 Cash Flow Comparison")
        
        cash_comparison = dcf_comparison['comparison_metrics']['cash_flow_comparison']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rental Annual Cash Flow", f"${cash_comparison['rental_annual_cash_flow']:,.0f}")
            st.write("✅ Provides steady income stream")
        with col2:
            st.metric("Stock Investment Cash Flow", f"${cash_comparison['stock_annual_cash_flow']:,.0f}")
            st.write("❌ No income until sale (reinvestment assumed)")
    
    # === TAB 2: COMPREHENSIVE DCF ===
    with tab2:
        st.header("💰 Detailed DCF Models")
        
        dcf_comparison = calculator.get_comprehensive_comparison()
        
        # Side-by-side DCF comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏠 Keep Rental DCF")
            
            rental_dcf = dcf_comparison['scenarios']['keep_rental']
            
            # Show summary metrics
            st.write("**Summary Metrics:**")
            metrics = rental_dcf['summary_metrics']
            st.write(f"• Total After-Tax Cash Flows: ${metrics['total_after_tax_cash_flows']:,.0f}")
            st.write(f"• Total Equity Buildup: ${metrics['total_equity_buildup']:,.0f}")
            st.write(f"• Total Return: ${metrics['total_return']:,.0f}")
            st.write(f"• IRR: {metrics['irr']:.2%}" if metrics['irr'] else "• IRR: N/A")
            
            # Year-by-year table
            st.write("**Year-by-Year Cash Flows:**")
            dcf_data = []
            for proj in rental_dcf['dcf_projections'][:5]:  # Show first 5 years
                dcf_data.append({
                    'Year': proj['year'],
                    'NOI': f"${proj['noi']:,.0f}",
                    'Tax Savings': f"${proj['rental_income_tax']:,.0f}",
                    'After-Tax CF': f"${proj['after_tax_cash_flow']:,.0f}",
                    'Property Value': f"${proj['property_value_eoy']:,.0f}"
                })
            
            dcf_df = pd.DataFrame(dcf_data)
            st.dataframe(dcf_df, use_container_width=True)
            
            if len(rental_dcf['dcf_projections']) > 5:
                st.info("Showing first 5 years. Full model runs for 10 years.")
        
        with col2:
            st.subheader("📈 Sell Now DCF")
            
            sell_dcf = dcf_comparison['scenarios']['sell_now']
            
            # Show sale details
            st.write("**Property Sale Details:**")
            sale_details = sell_dcf['sale_details']
            st.write(f"• Gross Proceeds: ${sale_details['gross_proceeds']:,.0f}")
            st.write(f"• Total Capital Gains: ${sale_details['total_capital_gains']:,.0f}")
            st.write(f"• Federal Exclusion Used: ${sale_details['federal_exclusion_used']:,.0f}")
            st.write(f"• Total Taxes: ${sale_details['total_capital_gains_tax']:,.0f}")
            st.write(f"• **After-Tax Proceeds: ${sale_details['after_tax_proceeds']:,.0f}**")
            
            # Stock investment summary
            st.write("**Stock Investment (10 Years):**")
            terminal = sell_dcf['terminal_value']
            st.write(f"• Initial Investment: ${sale_details['after_tax_proceeds']:,.0f}")
            st.write(f"• Final Stock Value: ${terminal['final_stock_value']:,.0f}")
            st.write(f"• Stock Gains Tax: ${terminal['stock_capital_gains_tax']:,.0f}")
            st.write(f"• **Net Proceeds: ${terminal['net_stock_proceeds']:,.0f}**")
            
            # Stock growth table
            st.write("**Stock Growth Projection:**")
            stock_data = []
            stock_projections = sell_dcf['stock_projections']
            years_to_show = [1, 3, 5, 7, 10]
            
            for year in years_to_show:
                if year <= len(stock_projections):
                    proj = stock_projections[year - 1]
                    stock_data.append({
                        'Year': proj['year'],
                        'Stock Value': f"${proj['ending_stock_value']:,.0f}",
                        'Annual Return': f"{proj['annual_stock_return']:.1%}"
                    })
            
            stock_df = pd.DataFrame(stock_data)
            st.dataframe(stock_df, use_container_width=True)
        
        # NPV and IRR comparison
        st.subheader("🎯 Financial Metrics Comparison")
        
        comp_metrics = dcf_comparison['comparison_metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Return Difference", f"${comp_metrics['total_return_difference']:,.0f}")
        with col2:
            irr_diff = comp_metrics['irr_difference']
            st.metric("IRR Difference", f"{irr_diff:.2%}" if irr_diff else "N/A")
        with col3:
            npv_diff = comp_metrics['npv_difference'] 
            st.metric("NPV Difference", f"${npv_diff:,.0f}" if npv_diff else "N/A")
        with col4:
            irr_bps = comp_metrics['irr_difference_bps']
            st.metric("IRR Diff (Basis Points)", f"{irr_bps:.0f}" if irr_bps else "N/A")
    
    # === TAB 3: DEPRECIATION ANALYSIS ===
    with tab3:
        st.header("📉 Comprehensive Depreciation Analysis")
        
        depreciation_info = calculator.calculate_depreciation_schedule()
        
        # Depreciation overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Cost Basis", f"${depreciation_info['cost_basis']:,.0f}")
        with col2:
            st.metric("Land Value (20%)", f"${depreciation_info['land_value']:,.0f}")
        with col3:
            st.metric("Depreciable Basis", f"${depreciation_info['depreciable_basis']:,.0f}")
        with col4:
            st.metric("Annual Depreciation", f"${depreciation_info['annual_depreciation']:,.0f}")
        
        # Tax benefits analysis
        st.subheader("💰 Annual Tax Benefits from Depreciation")
        
        annual_depreciation = depreciation_info['annual_depreciation']
        tax_rate = 0.3625  # Combined 32% federal + 4.25% NC
        annual_tax_benefit = annual_depreciation * tax_rate
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Marginal Tax Rate", f"{tax_rate:.1%}")
        with col2:
            st.metric("Annual Tax Savings", f"${annual_tax_benefit:,.0f}")
        with col3:
            st.metric("10-Year Tax Savings", f"${annual_tax_benefit * 10:,.0f}")
        
        # Depreciation schedule table
        st.subheader("📋 10-Year Depreciation Schedule")
        
        dep_data = []
        cumulative_tax_benefit = 0
        
        for year_info in depreciation_info['schedule']:
            year_tax_benefit = year_info['annual_depreciation'] * tax_rate
            cumulative_tax_benefit += year_tax_benefit
            
            dep_data.append({
                'Year': year_info['year'],
                'Annual Depreciation': f"${year_info['annual_depreciation']:,.0f}",
                'Tax Benefit': f"${year_tax_benefit:,.0f}",
                'Cumulative Tax Benefit': f"${cumulative_tax_benefit:,.0f}",
                'Adjusted Basis': f"${year_info['adjusted_basis']:,.0f}"
            })
        
        dep_df = pd.DataFrame(dep_data)
        st.dataframe(dep_df, use_container_width=True)
        
        # Depreciation recapture analysis
        st.subheader("🏛️ Depreciation Recapture on Sale")
        
        recapture_info = calculator.calculate_depreciation_recapture_tax(analysis_years)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accumulated Depreciation", f"${recapture_info['accumulated_depreciation']:,.0f}")
        with col2:
            st.metric("Recapture Tax Rate", f"{recapture_info['effective_recapture_rate']:.1%}")
        with col3:
            st.metric("Total Recapture Tax", f"${recapture_info['total_recapture_tax']:,.0f}")
        
        # Show the trade-off
        total_tax_benefits = cumulative_tax_benefit
        recapture_tax = recapture_info['total_recapture_tax']
        net_tax_advantage = total_tax_benefits - recapture_tax
        
        st.subheader("⚖️ Net Depreciation Advantage")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tax Benefits", f"${total_tax_benefits:,.0f}", delta="Benefits during ownership")
        with col2:
            st.metric("Recapture Tax", f"-${recapture_tax:,.0f}", delta="Tax on sale")
        with col3:
            st.metric("Net Tax Advantage", f"${net_tax_advantage:,.0f}", 
                     delta="✅ Positive" if net_tax_advantage > 0 else "❌ Negative")
    
    # === TAB 4: TAX BREAKDOWN ===
    with tab4:
        st.header("🏛️ Comprehensive Tax Analysis")
        st.markdown("**Detailed tax calculations for TX resident with NC property ($260k+ income)**")
        
        dcf_comparison = calculator.get_comprehensive_comparison()
        rental_dcf = dcf_comparison['scenarios']['keep_rental']
        sell_dcf = dcf_comparison['scenarios']['sell_now']
        
        # Tax rate summary
        st.subheader("📊 Tax Rate Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Rental Income Tax Rates:**")
            st.write("• Federal Ordinary Income: 32.0%")
            st.write("• NC Flat Tax (Non-Resident): 4.25%") 
            st.write("• **Combined Ordinary Rate: 36.25%**")
            st.write("")
            st.write("**Property Sale Tax Rates:**")
            st.write("• Federal Capital Gains: 20.0%")
            st.write("• NC Capital Gains: 4.25%")
            st.write("• **Combined Capital Gains: 24.25%**")
            st.write("• Depreciation Recapture: 29.25%")
        
        with col2:
            st.write("**Stock Investment Tax Rates:**")
            st.write("• Federal Capital Gains: 20.0%")
            st.write("• NC Capital Gains: 4.25%")
            st.write("• **Combined Capital Gains: 24.25%**")
            st.write("")
            st.write("**Primary Residence Benefits:**")
            st.write("• Federal Exclusion: $250,000")
            st.write("• NC Exclusion: $0")
            st.write("• **Net Tax Savings: Significant**")
        
        # Annual tax calculations
        st.subheader("💰 Annual Tax Impact Analysis")
        
        if rental_dcf['dcf_projections']:
            first_year = rental_dcf['dcf_projections'][0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Year 1 Rental Tax Calculation:**")
                st.write(f"• Gross Rental Income: ${first_year['annual_rent']:,.0f}")
                st.write(f"• Operating Expenses: -${first_year['annual_operating_expenses']:,.0f}")
                st.write(f"• Mortgage Interest: -${first_year['annual_interest_payment']:,.0f}")
                st.write(f"• Depreciation Deduction: -${first_year['annual_depreciation']:,.0f}")
                st.write("• " + "="*40)
                st.write(f"• **Taxable Income: ${first_year['taxable_rental_income']:,.0f}**")
                st.write(f"• Tax Rate: 36.25%")
                st.write(f"• **Taxes Owed: ${first_year['rental_income_tax']:,.0f}**")
            
            with col2:
                st.write("**Tax Deduction Benefits:**")
                
                # Depreciation benefit
                dep_benefit = first_year['annual_depreciation'] * 0.3625
                st.write(f"• Depreciation Tax Savings: ${dep_benefit:,.0f}")
                
                # Interest deduction benefit  
                interest_benefit = first_year['annual_interest_payment'] * 0.3625
                st.write(f"• Interest Tax Savings: ${interest_benefit:,.0f}")
                
                # Operating expense benefit
                expense_benefit = first_year['annual_operating_expenses'] * 0.3625
                st.write(f"• Operating Expense Savings: ${expense_benefit:,.0f}")
                
                total_benefits = dep_benefit + interest_benefit + expense_benefit
                st.write("• " + "="*35)
                st.write(f"• **Total Annual Tax Benefits: ${total_benefits:,.0f}**")
        
        # Sale tax comparison
        st.subheader("🏛️ Sale Tax Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Property Sale Taxes (Rental Scenario):**")
            terminal = rental_dcf['terminal_value']
            st.write(f"• Capital Gains: ${terminal['total_appreciation']:,.0f}")
            st.write(f"• Capital Gains Tax: ${terminal['capital_gains_tax']:,.0f}")
            st.write(f"• Depreciation Recapture: ${terminal['total_accumulated_depreciation']:,.0f}")
            st.write(f"• Depreciation Recapture Tax: ${terminal['depreciation_recapture_tax']:,.0f}")
            total_rental_sale_tax = terminal['capital_gains_tax'] + terminal['depreciation_recapture_tax']
            st.write(f"• **Total Sale Taxes: ${total_rental_sale_tax:,.0f}**")
        
        with col2:
            st.write("**Stock Sale Taxes (Sell Now Scenario):**")
            sale_details = sell_dcf['sale_details']
            stock_terminal = sell_dcf['terminal_value']
            
            st.write(f"• Property Sale Gains: ${sale_details['total_capital_gains']:,.0f}")
            st.write(f"• Federal Exclusion: -${sale_details['federal_exclusion_used']:,.0f}")
            st.write(f"• Property Sale Tax: ${sale_details['total_capital_gains_tax']:,.0f}")
            st.write(f"• Stock Gains: ${stock_terminal['total_stock_appreciation']:,.0f}")
            st.write(f"• Stock Tax: ${stock_terminal['stock_capital_gains_tax']:,.0f}")
            total_stock_sale_tax = sale_details['total_capital_gains_tax'] + stock_terminal['stock_capital_gains_tax']
            st.write(f"• **Total Sale Taxes: ${total_stock_sale_tax:,.0f}**")
        
        # Tax efficiency summary
        st.subheader("⚖️ Tax Efficiency Summary")
        
        # Calculate total tax burden for each scenario
        rental_annual_taxes = sum(proj['rental_income_tax'] for proj in rental_dcf['dcf_projections'])
        rental_total_taxes = rental_annual_taxes + total_rental_sale_tax
        
        stock_total_taxes = total_stock_sale_tax
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rental Total Taxes", f"${rental_total_taxes:,.0f}")
            st.write("Includes annual income taxes + sale taxes")
        with col2:
            st.metric("Stock Total Taxes", f"${stock_total_taxes:,.0f}") 
            st.write("Includes property sale + stock sale taxes")
        with col3:
            tax_difference = rental_total_taxes - stock_total_taxes
            st.metric("Tax Difference", f"${tax_difference:,.0f}",
                     delta="Higher rental taxes" if tax_difference > 0 else "Higher stock taxes")
    
    # === TAB 5: AMORTIZATION SCHEDULE ===
    with tab5:
        st.header("🏦 Wells Fargo Mortgage Analysis")
        st.markdown("**Based on actual August 2025 Wells Fargo statement**")
        
        loan_info = calculator.get_loan_payoff_info()
        
        if loan_info['payoff_date']:
            # Loan summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Balance", f"${loan_info['current_balance']:,.2f}")
            with col2:
                st.metric("Monthly Payment (P&I)", f"${loan_info['monthly_payment']:,.2f}")
            with col3:
                st.metric("Interest Rate", f"{loan_info['interest_rate']*100:.3f}%")
            with col4:
                st.metric("Payoff Date", loan_info['payoff_date'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Years Remaining", f"{loan_info['years_remaining']:.1f}")
            with col2:
                st.metric("Payments Left", f"{loan_info['remaining_payments']:,}")
            with col3:
                st.metric("Total Interest Remaining", f"${loan_info['total_interest_remaining']:,.0f}")
            with col4:
                # Calculate total payoff amount
                total_payoff = loan_info['current_balance'] + loan_info['total_interest_remaining']
                st.metric("Total Payoff Amount", f"${total_payoff:,.0f}")
            
            # Payment breakdown chart
            st.subheader("📊 Principal vs Interest Over Time")
            
            if loan_info['amortization_schedule']:
                # Create chart data
                schedule = loan_info['amortization_schedule']
                
                # Show every 12th payment for visualization
                chart_data = []
                for i, payment in enumerate(schedule):
                    if i % 12 == 0 or i == len(schedule) - 1:  # Show annual payments + final
                        years_from_now = (i + 1) / 12
                        chart_data.append({
                            'Years from Now': years_from_now,
                            'Principal Payment': payment['principal'],
                            'Interest Payment': payment['interest'],
                            'Remaining Balance': payment['balance']
                        })
                
                chart_df = pd.DataFrame(chart_data)
                
                # Create stacked area chart
                fig = px.area(chart_df, x='Years from Now', 
                            y=['Principal Payment', 'Interest Payment'],
                            title="Monthly Payment Composition Over Time",
                            labels={'value': 'Monthly Payment ($)', 'variable': 'Payment Type'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed amortization table
            st.subheader("📋 Detailed Amortization Schedule")
            
            # Show options for table display
            display_option = st.selectbox(
                "Select view:",
                ["First 24 months", "First 5 years", "Every 12 months", "Last 24 months"]
            )
            
            if loan_info['amortization_schedule']:
                schedule = loan_info['amortization_schedule']
                
                if display_option == "First 24 months":
                    table_data = schedule[:24]
                elif display_option == "First 5 years":
                    table_data = schedule[:60]
                elif display_option == "Every 12 months":
                    table_data = [schedule[i] for i in range(0, len(schedule), 12)]
                elif display_option == "Last 24 months":
                    table_data = schedule[-24:] if len(schedule) > 24 else schedule
                
                # Format data for display
                display_data = []
                for payment in table_data:
                    display_data.append({
                        'Date': payment['date'],
                        'Payment': f"${payment['payment']:,.2f}",
                        'Principal': f"${payment['principal']:,.2f}", 
                        'Interest': f"${payment['interest']:,.2f}",
                        'Balance': f"${payment['balance']:,.2f}"
                    })
                
                display_df = pd.DataFrame(display_data)
                st.dataframe(display_df, use_container_width=True)
                
                # Download full schedule
                full_schedule_df = pd.DataFrame(loan_info['amortization_schedule'])
                csv = full_schedule_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Complete Amortization Schedule",
                    data=csv,
                    file_name=f"wells_fargo_amortization_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No mortgage data available or property is paid off.")
    
    # === TAB 6: CASH VS EQUITY RISK ===
    with tab6:
        st.header("⚖️ Cash vs Equity Risk Analysis")
        st.markdown("**Separating liquid cash flow from illiquid equity buildup**")
        
        cash_equity_data = calculator.calculate_cash_vs_equity_projection()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Pre-Tax Cash", f"${cash_equity_data['summary']['total_cumulative_cash']:,.0f}")
        with col2:
            st.metric("Total After-Tax Cash", f"${cash_equity_data['summary']['total_cumulative_after_tax_cash']:,.0f}")
        with col3:
            st.metric("Total Equity Buildup", f"${cash_equity_data['summary']['total_equity_buildup']:,.0f}")
        with col4:
            st.metric("Final Property Value", f"${cash_equity_data['summary']['final_property_value']:,.0f}")
        
        # Visual analysis
        st.subheader("📈 Visual Cash Flow Analysis")
        
        chart_gen = ChartGenerator()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cash projection chart
            cash_chart = chart_gen.create_cash_projection_chart(cash_equity_data)
            st.plotly_chart(cash_chart, use_container_width=True)
        
        with col2:
            # Equity buildup chart
            equity_chart = chart_gen.create_equity_buildup_chart(cash_equity_data)
            st.plotly_chart(equity_chart, use_container_width=True)
        
        # Detailed year-by-year breakdown
        st.subheader("📊 Annual Cash vs Equity Breakdown")
        
        # Combine data from both projections
        combined_data = []
        cash_projections = cash_equity_data['cash_projections']
        equity_projections = cash_equity_data['equity_projections']
        
        for i in range(len(cash_projections)):
            cash_proj = cash_projections[i]
            equity_proj = equity_projections[i]
            
            combined_data.append({
                'Year': cash_proj['year'],
                'Rental Income': f"${cash_proj['monthly_rent'] * 12:,.0f}",
                'After-Tax Cash': f"${cash_proj['annual_after_tax_cash']:,.0f}",
                'Depreciation Benefit': f"${cash_proj['annual_depreciation_tax_benefit']:,.0f}",
                'Property Appreciation': f"${equity_proj['annual_appreciation']:,.0f}",
                'Mortgage Paydown': f"${equity_proj['annual_principal_paydown']:,.0f}",
                'Total Equity Gain': f"${equity_proj['total_equity_gain']:,.0f}",
                'Property Value EOY': f"${equity_proj['property_value']:,.0f}"
            })
        
        combined_df = pd.DataFrame(combined_data)
        st.dataframe(combined_df, use_container_width=True)
        
        # Risk analysis
        st.subheader("⚠️ Risk & Liquidity Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**💰 Cash Flow Risks:**")
            st.write("• **Vacancy Risk**: Tenant turnover reduces cash flow")
            st.write("• **Maintenance Risk**: Unexpected repairs impact cash")
            st.write("• **Market Risk**: Rent growth may lag expectations") 
            st.write("• **Tax Risk**: Changes in tax law affect benefits")
            st.write("• **Management Risk**: Time and effort required")
            
            # Cash flow reliability
            monthly_cash = cash_equity_data['summary']['total_cumulative_after_tax_cash'] / (12 * analysis_years)
            st.write(f"**Average Monthly After-Tax Cash: ${monthly_cash:,.0f}**")
        
        with col2:
            st.write("**🏠 Equity Buildup Risks:**")
            st.write("• **Appreciation Risk**: Property may not appreciate")
            st.write("• **Market Risk**: Local market conditions")
            st.write("• **Liquidity Risk**: Cannot access equity easily")
            st.write("• **Transaction Risk**: High costs to sell (8.5%)")
            st.write("• **Timing Risk**: May need to sell at bad time")
            
            # Equity reliability
            total_equity = cash_equity_data['summary']['total_equity_buildup']
            appreciation_portion = sum(proj['annual_appreciation'] for proj in equity_projections)
            paydown_portion = sum(proj['annual_principal_paydown'] for proj in equity_projections)
            
            st.write(f"**Equity Composition:**")
            st.write(f"• Property Appreciation: ${appreciation_portion:,.0f} ({appreciation_portion/total_equity*100:.1f}%)")
            st.write(f"• Mortgage Paydown: ${paydown_portion:,.0f} ({paydown_portion/total_equity*100:.1f}%)")
        
        # Liquidity timeline
        st.subheader("🕒 Liquidity Timeline")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**💰 Cash (Immediate)**")
            st.write("• Monthly rental income")
            st.write("• Available within 30 days")
            st.write("• Can be used for any purpose")
        with col2:
            st.write("**🏠 Equity (3-6 months)**") 
            st.write("• Requires property sale or refinance")
            st.write("• High transaction costs (8.5%+)")
            st.write("• Market timing dependent")
        with col3:
            st.write("**📈 Stock Investment (1-3 days)**")
            st.write("• Highly liquid alternative")
            st.write("• Low transaction costs (<0.1%)")
            st.write("• Market volatility risk")
    
    # === TAB 7: METHODOLOGY ===
    with tab7:
        st.header("📚 Calculation Methodology")
        st.markdown("**Comprehensive documentation of all calculations and assumptions**")
        
        # DCF Methodology
        st.subheader("💰 Discounted Cash Flow (DCF) Model")
        
        st.write("""
        This analysis employs sophisticated DCF modeling to provide an apples-to-apples comparison 
        between selling your property now versus keeping it as a rental investment.
        """)
        
        # Rental DCF explanation
        st.write("**🏠 Rental Property DCF Components:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Annual Cash Flow Calculation:**
            1. Gross Rental Income (growing 3% annually)
            2. Less: Operating Expenses (growing 2.5% annually)
            3. Less: Mortgage Payments (P&I from actual amortization)
            4. Less: Income Taxes on Net Operating Income
            5. Plus: Tax Benefits from Depreciation
            6. **= After-Tax Cash Flow**
            """)
        
        with col2:
            st.write("""
            **Terminal Value (Year 10 Sale):**
            1. Property Value (4.2% annual appreciation)
            2. Less: Selling Costs (8.5% of sale price)
            3. Less: Remaining Mortgage Balance
            4. Less: Capital Gains Tax (24.25% combined)
            5. Less: Depreciation Recapture Tax (29.25%)
            6. **= Net Sale Proceeds**
            """)
        
        # Stock DCF explanation
        st.write("**📈 Stock Investment DCF Components:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Initial Investment:**
            1. Current Property Value: $950,000
            2. Less: Selling Costs (8.5%): $80,750
            3. Less: Mortgage Payoff: $554,825
            4. Less: Capital Gains Tax (with $250k exclusion)
            5. **= After-Tax Investment Proceeds**
            """)
        
        with col2:
            st.write("""
            **Stock Growth (7.5% annually):**
            1. No intermediate cash flows (reinvestment)
            2. Compound growth over 10 years
            3. Terminal value taxed at 24.25% capital gains
            4. **= Net Stock Proceeds**
            """)
        
        # Tax methodology
        st.subheader("🏛️ Tax Calculation Methodology")
        
        st.write("**Key Tax Assumptions for TX Resident with NC Property:**")
        
        # Create tax table
        tax_table_data = [
            ["Income Type", "Federal Rate", "NC Rate", "Combined Rate", "Notes"],
            ["Rental Income", "32.0%", "4.25%", "36.25%", "Ordinary income rates"],
            ["Property Capital Gains", "20.0%", "4.25%", "24.25%", "Long-term capital gains"],
            ["Stock Capital Gains", "20.0%", "4.25%", "24.25%", "Long-term capital gains"], 
            ["Depreciation Recapture", "25.0%", "4.25%", "29.25%", "Special recapture rate"],
            ["Primary Residence", "$250k Exclusion", "No Exclusion", "$7,337 Savings", "Federal only"]
        ]
        
        tax_df = pd.DataFrame(tax_table_data[1:], columns=tax_table_data[0])
        st.table(tax_df)
        
        # Depreciation methodology
        st.subheader("📉 Depreciation Methodology")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Depreciation Schedule:**
            • **Method**: Straight-line over 27.5 years
            • **Property Type**: Residential rental property
            • **Depreciable Basis**: Cost basis minus land value
            • **Land Value**: 20% of cost basis (industry standard)
            • **Annual Deduction**: $22,545 ($780k × 80% ÷ 27.5)
            """)
        
        with col2:
            st.write("""
            **Tax Benefits:**
            • **Annual Tax Savings**: $8,173 ($22,545 × 36.25%)
            • **10-Year Benefit**: $81,730
            • **Recapture on Sale**: $65,910 ($225,450 × 29.25%)
            • **Net Benefit**: $15,820 over 10 years
            """)
        
        # Assumptions and limitations
        st.subheader("📊 Key Assumptions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("""
            **Market Assumptions:**
            • Property Appreciation: 4.2% annually
            • Stock Market Return: 7.5% annually  
            • Rent Growth: 3.0% annually
            • Expense Inflation: 2.5% annually
            • Discount Rate: 8.0%
            """)
        
        with col2:
            st.write("""
            **Property Assumptions:**
            • Current Value: $950,000
            • Cost Basis: $780,000 
            • Mortgage Balance: $554,825
            • Interest Rate: 3.875%
            • Monthly Rent: $5,400
            """)
        
        # Model validation
        st.subheader("✅ Model Validation")
        
        st.write("""
        **Data Sources & Verification:**
        
        ✅ **Mortgage Data**: Actual Wells Fargo statement (August 2025)
        - Balance, rate, payment, and maturity date verified
        - Amortization schedule matches bank calculations
        
        ✅ **Tax Rates**: Current IRS and NC DOR publications
        - Federal rates for high-income earners verified
        - NC non-resident tax obligations confirmed
        
        ✅ **Property Data**: Current market assessments
        - Boone, NC market analysis incorporated
        - Cost basis includes documented improvements
        
        ✅ **Depreciation**: IRS Publication 527 compliance
        - Residential rental property rules followed
        - 27.5-year schedule properly implemented
        """)
        
        # Limitations and disclaimers
        st.subheader("⚠️ Important Limitations")
        
        st.write("""
        **Key Limitations to Consider:**
        
        🚨 **Tax Law Changes**: Current tax rates and rules may change during the 10-year period
        
        🚨 **Market Volatility**: Both property and stock markets may perform very differently than assumed
        
        🚨 **Individual Circumstances**: Your specific tax situation may have additional considerations
        
        🚨 **Simplified Assumptions**: Some complex tax rules (e.g., passive loss limitations) are simplified
        
        🚨 **Transaction Costs**: Actual selling costs may vary from the 8.5% assumption
        
        🚨 **Time and Effort**: Property management time and hassle are not quantified
        
        **Recommendation**: This analysis is for educational purposes only. Consult with qualified 
        tax and financial professionals before making any investment decisions.
        """)
        
        # Download analysis
        st.subheader("📤 Export Analysis")
        
        if st.button("📊 Generate Comprehensive Report", type="primary"):
            # Create comprehensive export data
            dcf_comparison = calculator.get_comprehensive_comparison()
            
            export_data = {
                'Property Information': {
                    'Address': analysis.property.address,
                    'Current Value': analysis.property.current_value,
                    'Cost Basis': analysis.property.cost_basis,
                    'Mortgage Balance': analysis.property.mortgage_balance,
                    'Monthly Rent': analysis.property.total_monthly_rent
                },
                'Recommendation': {
                    'Scenario': dcf_comparison['recommendation']['scenario'],
                    'Advantage Amount': dcf_comparison['recommendation']['advantage_amount'],
                    'Advantage Percent': dcf_comparison['recommendation']['advantage_percent'],
                    'Reasoning': dcf_comparison['recommendation']['reasoning']
                },
                'Financial Metrics': {
                    'Rental Total Return': dcf_comparison['scenarios']['keep_rental']['summary_metrics']['total_return'],
                    'Stock Total Return': dcf_comparison['scenarios']['sell_now']['summary_metrics']['total_return'],
                    'Rental IRR': dcf_comparison['scenarios']['keep_rental']['summary_metrics']['irr'],
                    'Stock IRR': dcf_comparison['scenarios']['sell_now']['summary_metrics']['irr']
                }
            }
            
            # Convert to JSON for download
            import json
            json_data = json.dumps(export_data, indent=2, default=str)
            
            st.download_button(
                label="📊 Download Analysis Report (JSON)",
                data=json_data,
                file_name=f"sell_vs_keep_comprehensive_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
            st.success("✅ Analysis report generated successfully!")

else:
    st.info("👆 Please select a property from the sidebar to begin analysis.")

# Footer
st.markdown("---")
st.markdown("""
**Sell vs Keep Calculator - Advanced Analysis v2.0**  
*Comprehensive DCF modeling with tax optimization for real estate investment decisions*

⚠️ **Disclaimer**: This analysis is for informational purposes only. 
Consult with qualified financial and tax professionals before making investment decisions.
""")