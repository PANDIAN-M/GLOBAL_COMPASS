from typing import Union, Dict, List, Optional
import pandas as pd
import numpy as np

def format_number(value: Union[int, float]) -> str:
    """Format large numbers with appropriate units"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        value = float(value)
        if abs(value) >= 1e12:
            return f"{value/1e12:.1f}T"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.1f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}K"
        elif abs(value) >= 1:
            return f"{value:.1f}"
        else:
            return f"{value:.3f}"
    except (ValueError, TypeError):
        return "N/A"

def format_percentage(value: Union[int, float], decimal_places: int = 2) -> str:
    """Format percentage values"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        return f"{float(value):.{decimal_places}f}%"
    except (ValueError, TypeError):
        return "N/A"

def format_currency(value: Union[int, float], currency: str = "USD") -> str:
    """Format currency values"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        formatted_value = format_number(value)
        return f"{formatted_value} {currency}"
    except:
        return "N/A"

def get_metric_description(metric_name: str) -> Optional[str]:
    """Get description for metrics to help users understand the data"""
    descriptions = {
        "GDP per capita (current US$)": "Gross domestic product divided by midyear population, in current US dollars",
        "GDP growth (annual %)": "Annual percentage growth rate of GDP at market prices",
        "Population, total": "Total population based on the de facto definition",
        "Population growth (annual %)": "Annual population growth rate for year t",
        "Life expectancy at birth, total (years)": "Number of years a newborn infant would live if prevailing patterns of mortality continue",
        "Inflation, consumer prices (annual %)": "Annual percentage change in consumer price index",
        "Unemployment, total (% of total labor force)": "Share of the labor force that is without work but available and seeking employment",
        "School enrollment, primary (% net)": "Net enrollment rate in primary education",
        "Health expenditure, total (% of GDP)": "Current health expenditure as percentage of GDP",
        "Urban population (% of total population)": "People living in urban areas as percentage of total population",
        "CO2 emissions (metric tons per capita)": "Carbon dioxide emissions per capita",
        "Internet users (per 100 people)": "Individuals who have used the Internet in the last 3 months"
    }
    return descriptions.get(metric_name)

def validate_data_quality(data: Dict) -> Dict[str, Union[float, str]]:
    """Assess data quality for the provided dataset"""
    if not data:
        return {"completeness": 0.0, "quality": "Poor - No data available"}
    
    total_metrics = len(data)
    valid_metrics = sum(1 for v in data.values() if v is not None and not pd.isna(v))
    completeness = (valid_metrics / total_metrics) * 100 if total_metrics > 0 else 0
    
    if completeness >= 80:
        quality = "Excellent"
    elif completeness >= 60:
        quality = "Good"
    elif completeness >= 40:
        quality = "Fair"
    else:
        quality = "Poor"
    
    return {
        "completeness": completeness,
        "quality": quality,
        "valid_metrics": valid_metrics,
        "total_metrics": total_metrics
    }

def clean_country_name(country_name: str) -> str:
    """Clean and standardize country names"""
    if not country_name:
        return ""
    
    # Basic cleaning
    cleaned = country_name.strip()
    
    # Common replacements
    replacements = {
        "United States of America": "United States",
        "USA": "United States",
        "UK": "United Kingdom",
        "Russian Federation": "Russia"
    }
    
    return replacements.get(cleaned, cleaned)

def export_to_csv(data: Dict, filename: str = "country_data.csv") -> str:
    """Convert country data to CSV format"""
    try:
        df = pd.DataFrame.from_dict(data, orient='index')
        csv_string = df.to_csv()
        return csv_string
    except Exception as e:
        return f"Error exporting data: {str(e)}"

def calculate_growth_rate(current_value: float, previous_value: float) -> Optional[float]:
    """Calculate growth rate between two values"""
    if pd.isna(current_value) or pd.isna(previous_value) or previous_value == 0:
        return None
    
    try:
        growth_rate = ((current_value - previous_value) / previous_value) * 100
        return growth_rate
    except (ValueError, TypeError, ZeroDivisionError):
        return None