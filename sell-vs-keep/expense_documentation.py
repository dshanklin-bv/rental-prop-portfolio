"""
Interactive expense documentation component for Streamlit app.
Provides detailed explanations of expense estimation methodology.
"""

import streamlit as st
import pandas as pd
from expense_framework import ExpenseFramework, PropertyType, PropertyAge, RentalStrategy, LocationType

class ExpenseDocumentation:
    """Interactive documentation for rental property expense estimation"""
    
    def __init__(self):
        self.framework = ExpenseFramework()
    
    def show_expense_methodology(self):
        """Display comprehensive expense methodology documentation"""
        
        st.header("📊 Expense Estimation Methodology")
        st.markdown("""
        This tool uses industry research and 2024-2025 market data to estimate rental property expenses.
        All estimates are based on **percentage of monthly rent** for easy comparison across properties.
        """)
        
        # Main methodology tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔧 Maintenance", "🏠 Vacancy", "👥 Management", "📋 Other Expenses", "🧮 Calculator"
        ])
        
        with tab1:
            self._show_maintenance_methodology()
        
        with tab2:
            self._show_vacancy_methodology()
        
        with tab3:
            self._show_management_methodology()
        
        with tab4:
            self._show_other_methodology()
        
        with tab5:
            self._show_expense_calculator()
    
    def _show_maintenance_methodology(self):
        """Display maintenance cost methodology"""
        data = self.framework.maintenance_data
        
        st.subheader("🔧 Maintenance & Repairs")
        
        st.markdown(data['description'])
        
        # Age-based rates table
        st.markdown("### Maintenance Rates by Property Age")
        age_df = pd.DataFrame([
            {"Property Age": "0-5 years (New)", "Base Rate": "3.0%", "Rationale": "Minimal repairs, warranty coverage"},
            {"Property Age": "6-15 years (Recent)", "Base Rate": "6.0%", "Rationale": "Some systems aging, moderate repairs"},
            {"Property Age": "16-30 years (Mature)", "Base Rate": "9.0%", "Rationale": "Regular replacements needed"},
            {"Property Age": "31+ years (Old)", "Base Rate": "12.0%", "Rationale": "Frequent repairs, system replacements"}
        ])
        st.dataframe(age_df, use_container_width=True)
        
        # Property type adjustments
        st.markdown("### Property Type Adjustments")
        type_df = pd.DataFrame([
            {"Property Type": "Single Family", "Multiplier": "1.0x", "Reason": "Standard baseline"},
            {"Property Type": "Duplex", "Multiplier": "1.1x", "Reason": "Dual systems complexity"},
            {"Property Type": "Multifamily", "Multiplier": "1.2x", "Reason": "Complex systems, common areas"},
            {"Property Type": "Condo/Townhome", "Multiplier": "0.8x", "Reason": "HOA handles some maintenance"}
        ])
        st.dataframe(type_df, use_container_width=True)
        
        # Rental strategy impact
        st.markdown("### Rental Strategy Impact")
        strategy_df = pd.DataFrame([
            {"Strategy": "Long-Term Rental", "Multiplier": "1.0x", "Impact": "Normal wear from stable tenants"},
            {"Strategy": "Short-Term Rental", "Multiplier": "1.5x", "Impact": "50% more due to turnover, guest damage"},
            {"Strategy": "Hybrid", "Multiplier": "1.25x", "Impact": "25% more due to mixed usage patterns"}
        ])
        st.dataframe(strategy_df, use_container_width=True)
        
        # Alternative calculation methods
        st.markdown("### Cross-Check Methods")
        st.markdown("""
        The framework uses multiple estimation methods for accuracy:
        - **1% of Property Value**: Industry standard ($950k property = $9,500/year)
        - **$0.90 per Square Foot**: Based on 15,000+ work orders (2,000 sq ft = $1,800/year)
        - **Percentage of Rent**: Age-adjusted rates shown above
        
        The framework uses the **highest** of these estimates to ensure conservative planning.
        """)
        
        # Confidence levels
        st.markdown("### Confidence Levels")
        for level, description in data['confidence_factors'].items():
            color = {"high": "🟢", "medium": "🟡", "low": "🔴"}[level]
            st.markdown(f"**{color} {level.upper()}**: {description}")
    
    def _show_vacancy_methodology(self):
        """Display vacancy rate methodology"""
        data = self.framework.vacancy_data
        
        st.subheader("🏠 Vacancy Allowance")
        
        st.markdown(data['description'])
        
        # Current market data
        st.markdown("### 2024-2025 Market Data")
        market_df = pd.DataFrame([
            {"Market": "National Average", "Rate": "7.1%", "Source": "Q1 2025 Census Data"},
            {"Market": "Austin, TX", "Rate": "9.9%", "Source": "Oversupply from new construction"},
            {"Market": "Tampa, FL", "Rate": "10.0%+", "Source": "7,400 new units in 2024"},
            {"Market": "Memphis, TN", "Rate": "9.4%", "Source": "Improving from 13.5%"},
            {"Market": "Historical Average", "Rate": "7.3%", "Source": "Long-term US average"}
        ])
        st.dataframe(market_df, use_container_width=True)
        
        # Strategy-based rates
        st.markdown("### Base Rates by Rental Strategy")
        strategy_df = pd.DataFrame([
            {"Strategy": "Long-Term Rental", "Typical Rate": "6.0%", "Explanation": "Stable tenants, predictable turnover"},
            {"Strategy": "Short-Term Rental", "Typical Rate": "40.0%", "Explanation": "Seasonal demand, daily booking nature"},
            {"Strategy": "Hybrid", "Typical Rate": "15.0%", "Explanation": "Blend of LTR stability and STR seasonality"}
        ])
        st.dataframe(strategy_df, use_container_width=True)
        
        # Location adjustments
        st.markdown("### Location Impact")
        location_df = pd.DataFrame([
            {"Location Type": "Urban", "Adjustment": "-10%", "Reason": "High demand, multiple job centers"},
            {"Location Type": "Suburban", "Adjustment": "Base", "Reason": "Balanced supply/demand"},
            {"Location Type": "Rural", "Adjustment": "+30%", "Reason": "Limited demand, fewer opportunities"},
            {"Location Type": "Vacation", "Adjustment": "+20%", "Reason": "Seasonal patterns, weather dependent"}
        ])
        st.dataframe(location_df, use_container_width=True)
        
        # Market health indicators
        st.markdown("### Market Health Indicators")
        for market_type, info in data['market_indicators'].items():
            rate = info['rate']
            desc = info['description']
            color = "🟢" if rate < 0.06 else "🟡" if rate < 0.09 else "🔴"
            st.markdown(f"**{color} {market_type.replace('_', ' ').title()}** ({rate:.1%}): {desc}")
    
    def _show_management_methodology(self):
        """Display management cost methodology"""
        data = self.framework.management_data
        
        st.subheader("👥 Property Management")
        
        st.markdown(data['description'])
        
        # Fee comparison table
        st.markdown("### Management Fee Comparison")
        fee_df = pd.DataFrame([
            {"Service Type", "Long-Term Rental", "Short-Term Rental", "Why the Difference?"},
            ["Full Service", "10%", "25%", "STR requires 24/7 support, cleaning coordination"],
            ["Half Service", "6%", "15%", "LTR: Leasing only | STR: Marketing only"],
            ["Self-Managed", "2%", "5%", "Software, platform fees, misc costs"]
        ])
        st.dataframe(fee_df, use_container_width=True)
        
        # Service level breakdown
        st.markdown("### What's Included in Full Service?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Long-Term Rental Management:**")
            ltr_services = data['service_levels']['full_service']['ltr_includes'].split(', ')
            for service in ltr_services:
                st.markdown(f"• {service}")
        
        with col2:
            st.markdown("**Short-Term Rental Management:**")
            str_services = data['service_levels']['full_service']['str_includes'].split(', ')
            for service in str_services:
                st.markdown(f"• {service}")
        
        # Location impact
        st.markdown("### Location Impact on Management Costs")
        location_df = pd.DataFrame([
            {"Location", "Adjustment", "Reason"},
            ["Urban", "-10%", "More management companies, competition"],
            ["Suburban", "Base Rate", "Standard market rates"],
            ["Rural", "+30%", "Limited options, travel time costs"],
            ["Vacation", "+20%", "Seasonal complexity, specialized knowledge"]
        ])
        st.dataframe(location_df, use_container_width=True)
        
        # Performance impact
        st.markdown("### Performance Impact")
        st.info("""
        **Professional management often pays for itself:**
        - STR management typically increases revenue by 18-20%
        - LTR management reduces vacancy and maintenance issues
        - Better pricing optimization and market knowledge
        - Legal compliance and risk management
        """)
    
    def _show_other_methodology(self):
        """Display other expenses methodology"""
        data = self.framework.other_expenses_data
        
        st.subheader("📋 Other Operating Expenses")
        
        st.markdown(data['description'])
        
        # Expense breakdown by strategy
        st.markdown("### Expense Breakdown by Strategy")
        
        categories = data['categories']
        breakdown_data = []
        
        for category, info in categories.items():
            ltr_rate = info.get('ltr_rate', 0)
            str_rate = info.get('str_rate', 0)
            hybrid_rate = info.get('hybrid_rate', (ltr_rate + str_rate) / 2)
            
            breakdown_data.append({
                "Expense Category": category.replace('_', ' ').title(),
                "Long-Term": f"{ltr_rate:.1%}",
                "Short-Term": f"{str_rate:.1%}",
                "Hybrid": f"{hybrid_rate:.1%}",
                "Notes": info.get('includes', info.get('description', ''))
            })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)
        
        # Total by strategy
        st.markdown("### Total 'Other' Expenses by Strategy")
        total_df = pd.DataFrame([
            {"Strategy": "Long-Term Rental", "Total Rate": "4.0%", "Key Drivers": "Admin costs, minimal utilities"},
            {"Strategy": "Short-Term Rental", "Total Rate": "8.0%", "Key Drivers": "All utilities, supplies, higher insurance"},
            {"Strategy": "Hybrid", "Total Rate": "6.0%", "Key Drivers": "Seasonal utilities, mixed supplies"}
        ])
        st.dataframe(total_df, use_container_width=True)
        
        # Detailed category explanations
        st.markdown("### Category Details")
        
        with st.expander("💡 Utilities"):
            st.markdown("""
            **Long-Term (1%)**: Typically tenant responsibility, owner may pay water/sewer
            **Short-Term (3%)**: Owner pays all - electric, gas, water, internet, cable
            **Key factors**: Climate, property size, guest usage patterns
            """)
        
        with st.expander("🛡️ Insurance"):
            st.markdown("""
            **Base Rate**: ~0.8% of property value annually
            **STR Premium**: +30% for commercial coverage
            **Rural Premium**: +20% for remote properties
            **Covers**: Liability, property damage, loss of income
            """)
        
        with st.expander("🔨 CapEx Reserves"):
            st.markdown("""
            **Recommended**: 5% of rent for major replacements
            **Covers**: HVAC systems, roofing, flooring, appliances
            **Timeline**: Major systems typically last 10-20 years
            **Strategy**: Set aside monthly to avoid large surprise expenses
            """)
        
        with st.expander("📊 Administrative Costs"):
            st.markdown("""
            **LTR (0.5%)**: Basic accounting, legal, software
            **STR (1.5%)**: Channel management software, accounting, licenses
            **Includes**: QuickBooks, rental software, legal consultations, permits
            """)
        
        with st.expander("🧴 Supplies & Amenities"):
            st.markdown("""
            **LTR (0.2%)**: Minimal supplies for turnovers
            **STR (1.5%)**: Linens, toiletries, cleaning supplies, amenities
            **Includes**: Welcome baskets, coffee, paper goods, cleaning products
            """)
    
    def _show_expense_calculator(self):
        """Interactive expense calculator"""
        st.subheader("🧮 Interactive Expense Calculator")
        
        st.markdown("""
        Use this calculator to estimate expenses for any property based on its characteristics.
        All estimates are shown as **percentage of monthly rent**.
        """)
        
        # Input controls
        col1, col2 = st.columns(2)
        
        with col1:
            property_type = st.selectbox(
                "Property Type",
                options=[PropertyType.SINGLE_FAMILY, PropertyType.DUPLEX, PropertyType.MULTIFAMILY, PropertyType.CONDO_TOWNHOME],
                format_func=lambda x: x.value.replace('_', ' ').title()
            )
            
            rental_strategy = st.selectbox(
                "Rental Strategy",
                options=[RentalStrategy.LONG_TERM, RentalStrategy.SHORT_TERM, RentalStrategy.HYBRID],
                format_func=lambda x: x.value.replace('_', ' ').title()
            )
            
            property_value = st.number_input(
                "Property Value ($)",
                min_value=100000,
                max_value=5000000,
                value=500000,
                step=50000
            )
        
        with col2:
            property_age = st.selectbox(
                "Property Age",
                options=[PropertyAge.NEW, PropertyAge.RECENT, PropertyAge.MATURE, PropertyAge.OLD],
                format_func=lambda x: {
                    PropertyAge.NEW: "New (0-5 years)",
                    PropertyAge.RECENT: "Recent (6-15 years)", 
                    PropertyAge.MATURE: "Mature (16-30 years)",
                    PropertyAge.OLD: "Old (31+ years)"
                }[x]
            )
            
            location_type = st.selectbox(
                "Location Type",
                options=[LocationType.URBAN, LocationType.SUBURBAN, LocationType.RURAL, LocationType.VACATION],
                format_func=lambda x: x.value.replace('_', ' ').title()
            )
            
            square_footage = st.number_input(
                "Square Footage",
                min_value=500,
                max_value=10000,
                value=2000,
                step=100
            )
            
            monthly_rent = st.number_input(
                "Expected Monthly Rent ($)",
                min_value=500,
                max_value=20000,
                value=3000,
                step=100
            )
        
        # Calculate estimates
        if st.button("Calculate Expense Estimates", type="primary"):
            estimates = self.framework.estimate_expenses(
                property_type=property_type,
                property_age=property_age,
                rental_strategy=rental_strategy,
                location_type=location_type,
                property_value=property_value,
                square_footage=square_footage,
                monthly_rent=monthly_rent
            )
            
            # Display results
            st.markdown("### 📊 Expense Estimates")
            
            # Summary table
            results_data = []
            total_percentage = 0
            
            for category, estimate in estimates.items():
                monthly_cost = monthly_rent * estimate.percentage
                annual_cost = monthly_cost * 12
                total_percentage += estimate.percentage
                
                results_data.append({
                    "Category": category.replace('_', ' ').title(),
                    "% of Rent": f"{estimate.percentage:.1%}",
                    "Monthly Cost": f"${monthly_cost:,.0f}",
                    "Annual Cost": f"${annual_cost:,.0f}",
                    "Confidence": estimate.confidence.title()
                })
            
            # Add total row
            total_monthly = monthly_rent * total_percentage
            total_annual = total_monthly * 12
            results_data.append({
                "Category": "**TOTAL EXPENSES**",
                "% of Rent": f"**{total_percentage:.1%}**",
                "Monthly Cost": f"**${total_monthly:,.0f}**",
                "Annual Cost": f"**${total_annual:,.0f}**",
                "Confidence": "---"
            })
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True)
            
            # Cash flow estimate
            net_monthly = monthly_rent - total_monthly
            net_annual = net_monthly * 12
            
            if net_monthly > 0:
                st.success(f"**Estimated Net Cash Flow**: ${net_monthly:,.0f}/month (${net_annual:,.0f}/year)")
            else:
                st.error(f"**Estimated Cash Shortfall**: ${abs(net_monthly):,.0f}/month (${abs(net_annual):,.0f}/year)")
            
            # Detailed explanations
            st.markdown("### 📋 Detailed Explanations")
            for category, estimate in estimates.items():
                confidence_color = {"high": "🟢", "medium": "🟡", "low": "🔴"}[estimate.confidence]
                
                with st.expander(f"{category.replace('_', ' ').title()} - {estimate.percentage:.1%} {confidence_color}"):
                    st.markdown(f"**Description**: {estimate.description}")
                    st.markdown(f"**Confidence**: {estimate.confidence.title()}")
                    st.markdown(f"**Source**: {estimate.source}")

# Example usage in Streamlit app
if __name__ == "__main__":
    st.set_page_config(page_title="Expense Documentation", layout="wide")
    
    doc = ExpenseDocumentation()
    doc.show_expense_methodology()