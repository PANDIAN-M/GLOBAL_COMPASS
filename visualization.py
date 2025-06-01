import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import List, Dict
from utils import format_number

class Visualization:
    """Enhanced service for creating interactive data visualizations with multiple chart types"""
    
    def __init__(self):
        # Define multiple color palettes for user selection
        self.color_palettes = {
            'Default': ['#FF4B4B', '#0068C9', '#09AB3B', '#FF8C00', '#8A2BE2', '#DC143C', '#00CED1', '#FFD700'],
            'Professional': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
            'Vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'],
            'Earth Tones': ['#8B4513', '#CD853F', '#D2691E', '#A0522D', '#F4A460', '#DEB887', '#D2B48C', '#BC8F8F'],
            'Ocean': ['#006994', '#13A3C4', '#BCF5F5', '#4DD0E1', '#0891B2', '#006BA6', '#1976D2', '#42A5F5'],
            'Sunset': ['#FF6B35', '#F7931E', '#FFD23F', '#FE4A49', '#FE6B8B', '#FF8A65', '#FFAB40', '#FFD54F'],
            'Pastel': ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#E1BAFF', '#FFE1BA', '#FFBAE1']
        }
        self.color_palette = self.color_palettes['Default']
        
        # Common layout settings
        self.layout_config = {
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'font': {'color': '#262730', 'size': 12},
            'margin': {'l': 50, 'r': 50, 't': 80, 'b': 50}
        }
    
    def set_color_palette(self, palette_name: str):
        """Set the color palette for visualizations"""
        if palette_name in self.color_palettes:
            self.color_palette = self.color_palettes[palette_name]
    
    def get_available_palettes(self) -> List[str]:
        """Get list of available color palettes"""
        return list(self.color_palettes.keys())
    
    def create_enhanced_bar_chart(self, df: pd.DataFrame, metric: str, show_values: bool = True) -> go.Figure:
        """Create an enhanced bar chart with animations and better styling"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            # Sort by metric value for better visualization
            df_sorted = df.sort_values(metric, ascending=True)
            
            fig = go.Figure(data=[
                go.Bar(
                    y=df_sorted.iloc[:, 0],  # First column (Country/State)
                    x=df_sorted[metric],
                    orientation='h',
                    marker_color=self.color_palette[:len(df_sorted)],
                    text=df_sorted[metric].apply(lambda x: format_number(x) if pd.notna(x) else 'N/A'),
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>' + metric + ': %{text}<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=f'{metric} Comparison',
                xaxis_title=metric,
                yaxis_title=df.columns[0],
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating bar chart: {str(e)}")
    
    def create_donut_chart(self, df: pd.DataFrame, metric: str) -> go.Figure:
        """Create a donut chart for metric distribution"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            # Filter out negative values and NaN
            df_clean = df[df[metric] > 0].copy()
            if df_clean.empty:
                return self._create_error_chart("No positive values available for donut chart")
            
            fig = go.Figure(data=[go.Pie(
                labels=df_clean.iloc[:, 0],  # First column (Country/State)
                values=df_clean[metric],
                hole=0.4,
                textinfo='label+percent',
                textposition='outside',
                marker=dict(
                    colors=self.color_palette[:len(df_clean)],
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>' +
                            'Value: %{value}<br>' +
                            'Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title=f'{metric} Distribution',
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating donut chart: {str(e)}")
    
    def create_bubble_chart(self, df: pd.DataFrame, x_metric: str, y_metric: str, size_metric: str) -> go.Figure:
        """Create a bubble chart with three metrics"""
        try:
            if df.empty or not all(col in df.columns for col in [x_metric, y_metric, size_metric]):
                return self._create_error_chart("Required metrics not available for bubble chart")
            
            # Clean data - remove rows with any NaN values in the three metrics
            df_clean = df.dropna(subset=[x_metric, y_metric, size_metric])
            if df_clean.empty:
                return self._create_error_chart("No complete data available for bubble chart")
            
            fig = go.Figure(data=go.Scatter(
                x=df_clean[x_metric],
                y=df_clean[y_metric],
                mode='markers',
                marker=dict(
                    size=df_clean[size_metric],
                    sizemode='diameter',
                    sizeref=2.*max(df_clean[size_metric])/(40.**2),
                    sizemin=4,
                    color=self.color_palette[:len(df_clean)],
                    line=dict(width=2, color='white')
                ),
                text=df_clean.iloc[:, 0],  # First column (Country/State)
                hovertemplate='<b>%{text}</b><br>' +
                            f'{x_metric}: %{{x}}<br>' +
                            f'{y_metric}: %{{y}}<br>' +
                            f'{size_metric}: %{{marker.size}}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'{x_metric} vs {y_metric} (Bubble size: {size_metric})',
                xaxis_title=x_metric,
                yaxis_title=y_metric,
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating bubble chart: {str(e)}")
    
    def create_box_plot(self, df: pd.DataFrame, metric: str) -> go.Figure:
        """Create a box plot for statistical distribution"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            # Remove NaN values
            df_clean = df.dropna(subset=[metric])
            if df_clean.empty:
                return self._create_error_chart("No valid data for box plot")
            
            fig = go.Figure(data=go.Box(
                y=df_clean[metric],
                name=metric,
                marker_color=self.color_palette[0],
                boxpoints='all',
                pointpos=0,
                text=df_clean.iloc[:, 0],  # First column (Country/State)
                hovertemplate='<b>%{text}</b><br>' + metric + ': %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'{metric} Distribution Analysis',
                yaxis_title=metric,
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating box plot: {str(e)}")
    
    def create_treemap(self, df: pd.DataFrame, metric: str) -> go.Figure:
        """Create a treemap visualization"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            # Filter positive values only
            df_clean = df[df[metric] > 0].copy()
            if df_clean.empty:
                return self._create_error_chart("No positive values for treemap")
            
            fig = go.Figure(go.Treemap(
                labels=df_clean.iloc[:, 0],  # First column (Country/State)
                values=df_clean[metric],
                parents=[""] * len(df_clean),
                textinfo="label+value",
                marker=dict(
                    colors=self.color_palette[:len(df_clean)],
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{label}</b><br>' + metric + ': %{value}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'{metric} Treemap View',
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating treemap: {str(e)}")
    
    def create_line_chart(self, df: pd.DataFrame, metric: str) -> go.Figure:
        """Create a line chart for trend visualization"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            fig = go.Figure()
            
            # Add line for each entity
            for i, (_, row) in enumerate(df.iterrows()):
                fig.add_trace(go.Scatter(
                    x=[0, 1],  # Simple x-axis for comparison
                    y=[0, row[metric]] if pd.notna(row[metric]) else [0, 0],
                    mode='lines+markers',
                    name=row.iloc[0],  # First column (Country/State)
                    line=dict(color=self.color_palette[i % len(self.color_palette)], width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title=f'{metric} Trends',
                xaxis_title='Comparison Scale',
                yaxis_title=metric,
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating line chart: {str(e)}")
    
    def create_scatter_plot(self, df: pd.DataFrame, metric: str) -> go.Figure:
        """Create a scatter plot with entity labels"""
        try:
            if df.empty or metric not in df.columns:
                return self._create_error_chart(f"No data available for {metric}")
            
            df_clean = df.dropna(subset=[metric])
            if df_clean.empty:
                return self._create_error_chart("No valid data for scatter plot")
            
            fig = go.Figure(data=go.Scatter(
                x=range(len(df_clean)),
                y=df_clean[metric],
                mode='markers+text',
                text=df_clean.iloc[:, 0],  # First column (Country/State)
                textposition='top center',
                marker=dict(
                    size=12,
                    color=self.color_palette[:len(df_clean)],
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{text}</b><br>' + metric + ': %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'{metric} Scatter Plot',
                xaxis_title='Entity Index',
                yaxis_title=metric,
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating scatter plot: {str(e)}")
    
    def create_radar_chart(self, df: pd.DataFrame, metrics: List[str]) -> go.Figure:
        """Create a radar chart for multi-metric comparison"""
        try:
            if df.empty or not metrics:
                return self._create_error_chart("No data available for radar chart")
            
            # Filter available metrics
            available_metrics = [m for m in metrics if m in df.columns]
            if not available_metrics:
                return self._create_error_chart("No valid metrics for radar chart")
            
            fig = go.Figure()
            
            for i, (_, row) in enumerate(df.iterrows()):
                # Normalize values for radar chart (0-100 scale)
                values = []
                for metric in available_metrics:
                    val = row[metric]
                    if pd.notna(val):
                        # Simple normalization based on max value in column
                        max_val = df[metric].max()
                        normalized = (val / max_val) * 100 if max_val > 0 else 0
                        values.append(normalized)
                    else:
                        values.append(0)
                
                # Close the radar chart
                values += values[:1]
                metric_labels = available_metrics + available_metrics[:1]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=metric_labels,
                    fill='toself',
                    name=row.iloc[0],  # First column (Country/State)
                    line=dict(color=self.color_palette[i % len(self.color_palette)])
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="Multi-Metric Radar Comparison",
                **self.layout_config
            )
            
            return fig
            
        except Exception as e:
            return self._create_error_chart(f"Error creating radar chart: {str(e)}")
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """Create a placeholder chart for errors"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"⚠️ {error_message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Chart Error",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            **self.layout_config
        )
        return fig