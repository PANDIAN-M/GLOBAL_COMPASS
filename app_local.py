import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np

from data_service import DataService
from mistral_service import MistralService
from visualization import Visualization
from utils import format_number, get_metric_description

def main():
    st.set_page_config(
        page_title="Country & State Comparison Tool",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .enhanced-sidebar {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize services
    data_service = DataService()
    mistral_service = MistralService()
    visualization = Visualization()

    # Main header
    st.markdown('<h1 class="main-header">🌍 Advanced Country & State Comparison Tool</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by World Bank Open Data API & AI Analysis**")

    # Enhanced Sidebar with Color Selection
    with st.sidebar:
        st.markdown("## 🎨 Visualization Settings")
        
        # Color palette selection
        available_palettes = visualization.get_available_palettes()
        selected_palette = st.selectbox(
            "Choose Color Palette:",
            available_palettes,
            index=0,
            help="Select your preferred color scheme for all charts"
        )
        visualization.set_color_palette(selected_palette)
        
        # Preview selected colors
        st.markdown("**Color Preview:**")
        colors_html = ""
        for i, color in enumerate(visualization.color_palette[:6]):
            colors_html += f'<span style="background-color: {color}; width: 30px; height: 20px; display: inline-block; margin: 2px; border-radius: 3px;"></span>'
        st.markdown(colors_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 📊 Analysis Level")
        
        # Analysis level selection
        analysis_level = st.radio(
            "Select Analysis Level:",
            ["Country Level", "State/Province Level"],
            help="Choose between comparing countries or states/provinces within countries"
        )

        st.markdown("---")
        st.markdown("## 🌍 Data Selection")

        if analysis_level == "Country Level":
            # Country selection
            countries = data_service.get_available_countries()
            if countries:
                selected_countries = st.multiselect(
                    "Select Countries (2-10 recommended):",
                    countries,
                    default=["United States", "China", "Germany", "Japan"],
                    max_selections=15,
                    help="Choose countries to compare"
                )
            else:
                st.error("Unable to fetch country list. Please check your internet connection.")
                selected_countries = []

        else:
            # State-level analysis
            st.markdown("### Country Selection")
            available_countries_with_states = ["United States", "India", "Australia", "Canada"]
            selected_country_for_states = st.selectbox(
                "Select Country:",
                available_countries_with_states,
                help="Choose a country to analyze its states/provinces"
            )
            
            # State selection
            states = data_service.get_available_states(selected_country_for_states)
            if states:
                selected_states = st.multiselect(
                    f"Select {selected_country_for_states} States/Provinces:",
                    states,
                    default=states[:5] if len(states) >= 5 else states,
                    max_selections=20,
                    help=f"Choose states/provinces within {selected_country_for_states}"
                )
            else:
                st.warning(f"No state data available for {selected_country_for_states}")
                selected_states = []

        st.markdown("---")
        st.markdown("## 📈 Metrics Selection")

        # Enhanced metrics with categories
        metrics_categories = {
            "📊 Economic Indicators": [
                "GDP per capita (current US$)",
                "GDP growth (annual %)",
                "Inflation, consumer prices (annual %)",
                "Unemployment, total (% of total labor force)",
                "Trade (% of GDP)"
            ],
            "👥 Demographics": [
                "Population, total",
                "Population growth (annual %)",
                "Urban population (% of total population)",
                "Age dependency ratio (% of working-age population)"
            ],
            "🎓 Education & Innovation": [
                "School enrollment, primary (% net)",
                "Literacy rate, adult total (% of people ages 15 and above)",
                "Research and development expenditure (% of GDP)",
                "Scientific and technical journal articles"
            ],
            "🏥 Health & Wellbeing": [
                "Life expectancy at birth, total (years)",
                "Mortality rate, infant (per 1,000 live births)",
                "Health expenditure, total (% of GDP)",
                "Hospital beds (per 1,000 people)"
            ],
            "🏛️ Governance & Infrastructure": [
                "Government expenditure on education, total (% of GDP)",
                "Military expenditure (% of GDP)",
                "Internet users (per 100 people)",
                "CO2 emissions (metric tons per capita)"
            ]
        }

        selected_metrics = []
        
        # Quick select options at the top
        st.markdown("**🚀 Quick Select Presets:**")
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        with col1:
            if st.button("💰 Economic Focus", key="economic_preset"):
                st.session_state.selected_metrics = [
                    "GDP per capita (current US$)",
                    "GDP growth (annual %)",
                    "Unemployment, total (% of total labor force)"
                ]
                st.rerun()
        
        with col2:
            if st.button("👥 Social Focus", key="social_preset"):
                st.session_state.selected_metrics = [
                    "Life expectancy at birth, total (years)",
                    "Population growth (annual %)",
                    "Urban population (% of total population)"
                ]
                st.rerun()
        
        with col3:
            if st.button("🎓 Development", key="development_preset"):
                st.session_state.selected_metrics = [
                    "School enrollment, primary (% net)",
                    "Health expenditure, total (% of GDP)",
                    "Internet users (per 100 people)"
                ]
                st.rerun()
        
        with col4:
            if st.button("🌍 Comprehensive", key="comprehensive_preset"):
                st.session_state.selected_metrics = [
                    "GDP per capita (current US$)",
                    "Life expectancy at birth, total (years)",
                    "School enrollment, primary (% net)",
                    "Urban population (% of total population)"
                ]
                st.rerun()
        
        st.markdown("---")
        st.markdown("**📋 Manual Selection:**")
        
        # Initialize session state for selected metrics
        if 'selected_metrics' not in st.session_state:
            st.session_state.selected_metrics = []
        
        for category, metrics in metrics_categories.items():
            with st.expander(category, expanded=False):
                for metric in metrics:
                    checked = metric in st.session_state.selected_metrics
                    if st.checkbox(metric, value=checked, key=f"metric_{hash(metric)}"):
                        if metric not in st.session_state.selected_metrics:
                            st.session_state.selected_metrics.append(metric)
                    else:
                        if metric in st.session_state.selected_metrics:
                            st.session_state.selected_metrics.remove(metric)
        
        selected_metrics = st.session_state.selected_metrics

    # Main content area
    if analysis_level == "Country Level":
        entities = selected_countries
        data_type = "countries"
    else:
        entities = selected_states
        data_type = "states"
        
    if not entities:
        st.warning(f"Please select at least one {data_type[:-1]} to begin analysis.")
        return

    if not selected_metrics:
        st.warning("Please select at least one metric to analyze.")
        return

    # Fetch data
    with st.spinner(f"📡 Fetching real-time data from World Bank API for {len(entities)} {data_type}..."):
        all_data = {}
        
        for entity in entities:
            if analysis_level == "Country Level":
                entity_data = data_service.get_country_data(entity, selected_metrics)
            else:
                entity_data = data_service.get_state_data(selected_country_for_states, entity, selected_metrics)
            
            if entity_data:
                all_data[entity] = entity_data

    if not all_data:
        st.error(f"❌ Unable to fetch data for the selected {data_type}. Please try again or select different options.")
        return

    # Create DataFrame for visualization
    df_list = []
    for entity, data in all_data.items():
        row = {"Country" if analysis_level == "Country Level" else "State": entity}
        row.update(data)
        df_list.append(row)

    df = pd.DataFrame(df_list)
    entity_col = "Country" if analysis_level == "Country Level" else "State"

    # Success message
    st.success(f"✅ Successfully loaded data for {len(df)} {data_type} with {len(selected_metrics)} metrics!")

    # Enhanced Tabs with more visualization options
    tab1, tab2, tab3 = st.tabs(["📊 Standard Charts", "🎯 Advanced Visualizations", "🤖 AI Insights & Export"])

    with tab1:
        st.markdown("## 📊 Standard Visualization Options")
        
        # Chart type selection with descriptions
        chart_options = {
            "Bar Chart": "Compare values across entities with horizontal bars",
            "Line Chart": "Show trends and relationships between metrics",
            "Scatter Plot": "Explore correlations between different metrics",
            "Radar Chart": "Multi-dimensional comparison across all metrics"
        }
        
        selected_chart = st.selectbox(
            "Choose Visualization Type:",
            list(chart_options.keys()),
            help="Select the type of chart that best fits your analysis needs"
        )
        
        st.info(f"💡 {chart_options[selected_chart]}")

        if len(selected_metrics) >= 1:
            metric = selected_metrics[0]
            
            if selected_chart == "Bar Chart":
                fig = visualization.create_enhanced_bar_chart(df, metric)
            elif selected_chart == "Line Chart":
                fig = visualization.create_line_chart(df, metric)
            elif selected_chart == "Scatter Plot":
                fig = visualization.create_scatter_plot(df, metric)
            else:  # Radar Chart
                fig = visualization.create_radar_chart(df, selected_metrics[:5])  # Limit to 5 metrics for readability
                
            st.plotly_chart(fig, use_container_width=True)
            
            # Built-in AI Analysis
            with st.expander("🤖 AI Analysis for this Chart", expanded=False):
                valid_data = {entity: all_data[entity].get(metric) for entity in entities if entity in all_data and all_data[entity].get(metric) is not None}
                if valid_data:
                    best_entity = max(valid_data, key=valid_data.get)
                    worst_entity = min(valid_data, key=valid_data.get)
                    best_value = valid_data[best_entity]
                    worst_value = valid_data[worst_entity]
                    
                    st.markdown(f"""
                    **📊 Chart Analysis:**
                    
                    • **Top Performer:** {best_entity} leads with {format_number(best_value)}
                    • **Performance Gap:** {format_number(best_value - worst_value)} difference between highest and lowest
                    • **{metric} Insight:** This metric shows significant variation across {analysis_level.lower()}
                    • **Recommendation:** Focus on understanding what makes {best_entity} successful in this area
                    """)

    with tab2:
        st.markdown("## 🎯 Advanced Visualization Options")
        
        # Advanced chart selection
        adv_chart_col1, adv_chart_col2 = st.columns(2)
        
        with adv_chart_col1:
            st.markdown("### 🍩 Donut Chart")
            if len(selected_metrics) >= 1:
                donut_metric = st.selectbox("Select metric for donut chart:", selected_metrics, key="donut")
                fig_donut = visualization.create_donut_chart(df, donut_metric)
                st.plotly_chart(fig_donut, use_container_width=True)
                
                # AI Analysis for donut chart
                with st.expander("🤖 AI Analysis for Donut Chart", expanded=False):
                    valid_data = {entity: all_data[entity].get(donut_metric) for entity in entities if entity in all_data and all_data[entity].get(donut_metric) is not None}
                    if valid_data:
                        total_value = sum(valid_data.values())
                        largest_share = max(valid_data, key=valid_data.get)
                        largest_percentage = (valid_data[largest_share] / total_value) * 100
                        
                        insights_text = f"""
                        **🍩 Distribution Analysis:**
                        
                        • **Dominant Player:** {largest_share} accounts for {largest_percentage:.1f}% of total {donut_metric}
                        • **Market Share:** Shows relative contribution of each {analysis_level.lower()} to the overall metric
                        • **Concentration Level:** {'High concentration' if largest_percentage > 40 else 'Balanced distribution'} in this indicator
                        • **Strategic Insight:** Understanding proportional contributions helps identify key players and market dynamics
                        """
                        st.markdown(insights_text)
        
        with adv_chart_col2:
            st.markdown("### 📊 Box Plot (Statistical)")
            if len(selected_metrics) >= 1:
                box_metric = st.selectbox("Select metric for box plot:", selected_metrics, key="box")
                fig_box = visualization.create_box_plot(df, box_metric)
                st.plotly_chart(fig_box, use_container_width=True)

        if len(selected_metrics) >= 3:
            st.markdown("### 🫧 Bubble Chart (3 Metrics)")
            bubble_col1, bubble_col2, bubble_col3 = st.columns(3)
            with bubble_col1:
                x_metric = st.selectbox("X-axis metric:", selected_metrics, key="bubble_x")
            with bubble_col2:
                y_metric = st.selectbox("Y-axis metric:", selected_metrics, key="bubble_y", index=1)
            with bubble_col3:
                size_metric = st.selectbox("Bubble size metric:", selected_metrics, key="bubble_size", index=2)
            
            fig_bubble = visualization.create_bubble_chart(df, x_metric, y_metric, size_metric)
            st.plotly_chart(fig_bubble, use_container_width=True)

        if len(selected_metrics) >= 1:
            st.markdown("### 🌳 Treemap Visualization")
            treemap_metric = st.selectbox("Select metric for treemap:", selected_metrics, key="treemap")
            fig_treemap = visualization.create_treemap(df, treemap_metric)
            st.plotly_chart(fig_treemap, use_container_width=True)

    with tab3:
        st.markdown("## 🤖 AI Insights & Data Export")
        
        # AI Service Status
        if mistral_service.is_available():
            st.success("🤖 Mistral AI Service Connected - Enhanced insights available!")
            
            if st.button("🧠 Generate Comprehensive AI Analysis", key="ai_comprehensive"):
                with st.spinner("🤖 Generating comprehensive AI insights..."):
                    analysis_data = {
                        "entities": entities,
                        "metrics": selected_metrics,
                        "data": all_data,
                        "analysis_level": analysis_level
                    }
                    
                    insights = mistral_service.generate_country_insights(analysis_data)
                    if insights:
                        st.markdown("### 🧠 AI-Generated Insights")
                        st.markdown(insights)
                    else:
                        st.warning("Unable to generate AI insights at this time.")
        else:
            st.info("🔑 Add your Mistral API key to the .env file for enhanced AI insights!")
            st.markdown("**Current Analysis:** Basic statistical insights are provided under each chart.")
        
        # Data Export
        st.markdown("### 📊 Export Data")
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📁 Download CSV",
                    data=csv_data,
                    file_name=f"{data_type}_comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📋 Download JSON",
                    data=json_data,
                    file_name=f"{data_type}_comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
