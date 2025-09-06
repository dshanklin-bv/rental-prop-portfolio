import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
import numpy as np

class ChartGenerator:
    """Generate charts for the sell vs keep analysis"""
    
    @staticmethod
    def create_comparison_chart(sell_result: Dict, keep_result: Dict, years: int) -> go.Figure:
        """Create a comparison chart showing total returns"""
        
        scenarios = ['Sell Now<br>+ Stocks', 'Keep as<br>Rental']
        returns = [sell_result['total_return'], keep_result['total_return']]
        colors = ['#FF6B6B', '#4ECDC4']
        
        fig = go.Figure()
        
        bars = fig.add_trace(go.Bar(
            x=scenarios,
            y=returns,
            marker_color=colors,
            text=[f'${r:,.0f}' for r in returns],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Total Return: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Total Return Comparison After {years} Years',
            yaxis_title='Total Return ($)',
            yaxis_tickformat='$,.0f',
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_cash_projection_chart(cash_equity_data: Dict) -> go.Figure:
        """Create cash flow projection chart showing annual cash flows"""
        cash_projections = cash_equity_data['cash_projections']
        
        years = [p['year'] for p in cash_projections]
        annual_cash = [p['annual_net_cash'] for p in cash_projections]
        cumulative_cash = [p['cumulative_cash'] for p in cash_projections]
        
        fig = go.Figure()
        
        # Annual cash flow bars
        fig.add_trace(go.Bar(
            x=years,
            y=annual_cash,
            name='Annual Cash Flow',
            marker_color='#4ECDC4',
            text=[f'${cf:,.0f}' for cf in annual_cash],
            textposition='auto',
            hovertemplate='<b>Year %{x}</b><br>Annual Cash Flow: $%{y:,.0f}<extra></extra>'
        ))
        
        # Cumulative cash flow line
        fig.add_trace(go.Scatter(
            x=years,
            y=cumulative_cash,
            mode='lines+markers',
            name='Cumulative Cash',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Year %{x}</b><br>Cumulative Cash: $%{y:,.0f}<extra></extra>',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Cash Flow Projection (Liquid Risk)',
            xaxis_title='Year',
            yaxis_title='Annual Cash Flow ($)',
            yaxis2=dict(
                title='Cumulative Cash ($)',
                overlaying='y',
                side='right'
            ),
            yaxis_tickformat='$,.0f',
            yaxis2_tickformat='$,.0f',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            legend=dict(x=0.02, y=0.98)
        )
        
        return fig
    
    @staticmethod 
    def create_equity_buildup_chart(cash_equity_data: Dict) -> go.Figure:
        """Create equity buildup chart showing appreciation + principal paydown"""
        equity_projections = cash_equity_data['equity_projections']
        
        years = [p['year'] for p in equity_projections]
        appreciation = [p['annual_appreciation'] for p in equity_projections]
        principal_paydown = [p['annual_principal_paydown'] for p in equity_projections]
        total_equity = [p['net_equity'] for p in equity_projections]
        
        fig = go.Figure()
        
        # Stacked bar chart showing appreciation and principal components
        fig.add_trace(go.Bar(
            x=years,
            y=appreciation,
            name='Property Appreciation',
            marker_color='#95E1D3',
            hovertemplate='<b>Year %{x}</b><br>Appreciation: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=years,
            y=principal_paydown,
            name='Principal Paydown',
            marker_color='#F38BA8',
            hovertemplate='<b>Year %{x}</b><br>Principal: $%{y:,.0f}<extra></extra>'
        ))
        
        # Total equity line
        fig.add_trace(go.Scatter(
            x=years,
            y=total_equity,
            mode='lines+markers',
            name='Total Net Equity',
            line=dict(color='#2E4057', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Year %{x}</b><br>Total Equity: $%{y:,.0f}<extra></extra>',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Equity Buildup Projection (Illiquid Risk)',
            xaxis_title='Year',
            yaxis_title='Annual Equity Gain ($)',
            yaxis2=dict(
                title='Total Net Equity ($)',
                overlaying='y',
                side='right'
            ),
            yaxis_tickformat='$,.0f',
            yaxis2_tickformat='$,.0f',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            barmode='stack',
            legend=dict(x=0.02, y=0.98)
        )
        
        return fig
    
    @staticmethod
    def create_cash_flow_timeline(keep_result: Dict, years: int) -> go.Figure:
        """Create timeline showing rental cash flows"""
        
        annual_cf = keep_result['annual_cash_flow']
        years_list = list(range(1, years + 1))
        cumulative_cf = [annual_cf * year for year in years_list]
        
        fig = go.Figure()
        
        # Annual cash flow bars
        fig.add_trace(go.Bar(
            x=years_list,
            y=[annual_cf] * years,
            name='Annual Cash Flow',
            marker_color='#4ECDC4',
            opacity=0.7,
            yaxis='y1'
        ))
        
        # Cumulative cash flow line
        fig.add_trace(go.Scatter(
            x=years_list,
            y=cumulative_cf,
            mode='lines+markers',
            name='Cumulative Cash Flow',
            line=dict(color='#FF6B6B', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Rental Property Cash Flow Over Time',
            xaxis_title='Year',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(
                title='Annual Cash Flow ($)',
                side='left',
                tickformat='$,.0f'
            ),
            yaxis2=dict(
                title='Cumulative Cash Flow ($)',
                side='right',
                overlaying='y',
                tickformat='$,.0f'
            ),
            legend=dict(x=0.02, y=0.98),
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_sensitivity_analysis(base_rent: float, base_appreciation: float, 
                                  calculator) -> go.Figure:
        """Create sensitivity analysis chart"""
        
        # Range of rent values (±30% of base)
        rent_range = np.linspace(base_rent * 0.7, base_rent * 1.3, 10)
        appreciation_range = np.linspace(base_appreciation - 0.02, base_appreciation + 0.02, 10)
        
        # Calculate returns for different scenarios
        keep_returns = []
        sell_return = calculator.calculate_sell_now_scenario()['total_return']
        
        original_rent = calculator.analysis.property.total_monthly_rent
        
        for rent in rent_range:
            # Temporarily adjust rent
            for unit in calculator.analysis.property.units:
                unit.monthly_rent = rent / len(calculator.analysis.property.units)
            
            keep_result = calculator.calculate_keep_rental_scenario()
            keep_returns.append(keep_result['total_return'])
        
        # Restore original rent
        for i, unit in enumerate(calculator.analysis.property.units):
            unit.monthly_rent = original_rent / len(calculator.analysis.property.units)
        
        fig = go.Figure()
        
        # Keep scenario returns
        fig.add_trace(go.Scatter(
            x=rent_range,
            y=keep_returns,
            mode='lines+markers',
            name='Keep as Rental',
            line=dict(color='#4ECDC4', width=3),
            hovertemplate='Rent: $%{x:,.0f}<br>Return: $%{y:,.0f}<extra></extra>'
        ))
        
        # Sell scenario (flat line)
        fig.add_trace(go.Scatter(
            x=[rent_range[0], rent_range[-1]],
            y=[sell_return, sell_return],
            mode='lines',
            name='Sell Now + Stocks',
            line=dict(color='#FF6B6B', width=3, dash='dash'),
            hovertemplate='Return: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Sensitivity Analysis: How Rent Affects Returns',
            xaxis_title='Monthly Rent ($)',
            yaxis_title='Total Return ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.02, y=0.98),
            font=dict(size=12)
        )
        
        fig.update_layout(
            xaxis_tickformat='$,.0f',
            yaxis_tickformat='$,.0f'
        )
        
        return fig
    
    @staticmethod
    def create_breakdown_chart(sell_result: Dict, keep_result: Dict) -> go.Figure:
        """Create breakdown chart showing components of each scenario"""
        
        # Sell scenario components
        sell_components = [
            sell_result['after_tax_proceeds'],
            sell_result['future_stock_value'] - sell_result['after_tax_proceeds']
        ]
        sell_labels = ['Initial Investment', 'Stock Market Growth']
        
        # Keep scenario components  
        keep_components = [
            keep_result['total_cash_flows'],
            keep_result['future_net_proceeds']
        ]
        keep_labels = ['Rental Cash Flows', 'Future Sale Proceeds']
        
        fig = go.Figure()
        
        # Sell scenario
        fig.add_trace(go.Bar(
            name='Sell Now + Stocks',
            x=['Sell Scenario'],
            y=[sum(sell_components)],
            marker_color='#FF6B6B',
            hovertemplate='<b>Sell Now + Stocks</b><br>Total: $%{y:,.0f}<extra></extra>',
            width=0.4,
            offset=-0.2
        ))
        
        # Keep scenario
        fig.add_trace(go.Bar(
            name='Keep as Rental',
            x=['Keep Scenario'], 
            y=[sum(keep_components)],
            marker_color='#4ECDC4',
            hovertemplate='<b>Keep as Rental</b><br>Total: $%{y:,.0f}<extra></extra>',
            width=0.4,
            offset=0.2
        ))
        
        fig.update_layout(
            title='Return Components Breakdown',
            yaxis_title='Total Return ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            showlegend=True,
            font=dict(size=12)
        )
        
        fig.update_layout(yaxis_tickformat='$,.0f')
        
        return fig