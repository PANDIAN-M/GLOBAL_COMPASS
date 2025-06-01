# 🌍 Advanced Country & State Comparison Tool

A powerful web application built with Streamlit that enables comprehensive comparison of countries and states/provinces across multiple economic, demographic, and social indicators using real-time data from the World Bank API.

## ✨ Features

### 📊 Comprehensive Data Analysis
- **Country-level Analysis**: Compare up to 15 countries across various indicators
- **State/Province Analysis**: Analyze states within the US, India, Australia, and Canada
- **Real-time Data**: Direct integration with World Bank Open Data API
- **Multiple Metrics**: 20+ indicators across 5 categories

### 🎨 Advanced Visualizations
- **Standard Charts**: Bar charts, line charts, scatter plots, radar charts
- **Advanced Charts**: Donut charts, bubble charts, box plots, treemaps
- **Color Palettes**: 7 customizable color schemes (Professional, Vibrant, Ocean, etc.)
- **Interactive Elements**: Hover tooltips, animations, and responsive design

### 🤖 AI-Powered Insights
- **Mistral AI Integration**: Generate comprehensive analytical insights
- **Automated Analysis**: Key findings and strategic recommendations
- **Data Quality Assessment**: Automatic validation and quality scoring

### 📈 Metric Categories

#### 📊 Economic Indicators
- GDP per capita (current US$)
- GDP growth (annual %)
- Inflation, consumer prices (annual %)
- Unemployment rate
- Trade (% of GDP)

#### 👥 Demographics
- Population statistics and growth
- Urban population percentage
- Age dependency ratio

#### 🎓 Education & Innovation
- School enrollment rates
- Literacy rates
- R&D expenditure
- Scientific publications

#### 🏥 Health & Wellbeing
- Life expectancy
- Infant mortality rate
- Health expenditure
- Hospital beds per capita

#### 🏛️ Governance & Infrastructure
- Government education expenditure
- Military expenditure
- Internet penetration
- CO2 emissions per capita

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection for API access

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/country-comparison-tool.git
cd country-comparison-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (Optional for AI insights)
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_mistral_api_key_here" > .env
```

4. **Run the application**
```bash
streamlit run app_local.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:8501`

## 📋 Usage Guide

### Basic Usage

1. **Select Analysis Level**
   - Choose between "Country Level" or "State/Province Level"

2. **Choose Entities**
   - For countries: Select 2-10 countries from the dropdown
   - For states: Choose a country first, then select states/provinces

3. **Select Metrics**
   - Use quick presets (Economic Focus, Social Focus, etc.)
   - Or manually select from categorized metrics

4. **Explore Visualizations**
   - Standard Charts: Basic comparative visualizations
   - Advanced Visualizations: Complex multi-dimensional charts
   - AI Insights: Automated analysis and recommendations

### Advanced Features

#### Quick Select Presets
- **💰 Economic Focus**: GDP, growth, unemployment
- **👥 Social Focus**: Life expectancy, population, urbanization
- **🎓 Development**: Education, health, internet access
- **🌍 Comprehensive**: Balanced selection across categories

#### Color Palette Options
- Default, Professional, Vibrant
- Earth Tones, Ocean, Sunset, Pastel

#### Export Options
- CSV format for spreadsheet analysis
- JSON format for data integration

## 🏗️ Project Structure

```
country-comparison-tool/
├── app_local.py          # Main Streamlit application
├── data_service.py       # World Bank API integration
├── mistral_service.py    # AI insights service
├── visualization.py      # Chart creation and styling
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Optional: For AI-powered insights
MISTRAL_API_KEY=your_mistral_api_key_here
```

### API Rate Limits

The application includes built-in caching and rate limiting to respect World Bank API limits:
- Country data is cached for 1 hour
- Automatic retry logic for failed requests
- Graceful fallbacks for API connectivity issues

## 🌐 Supported Countries & States

### Countries (300+ available)
All countries with World Bank data, including major economies:
- United States, China, Germany, Japan
- India, United Kingdom, France, Brazil
- And many more...

### States/Provinces
- **United States**: All 50 states
- **India**: 28 states and union territories
- **Australia**: 8 states and territories
- **Canada**: 13 provinces and territories

## 📊 Data Sources

- **Primary**: World Bank Open Data API
- **Coverage**: Latest available data (typically 2018-2023)
- **Update Frequency**: Real-time API calls with intelligent caching
- **Data Quality**: Automatic validation and quality assessment

## 🤖 AI Integration

### Mistral AI Features
- Comprehensive data analysis
- Performance pattern identification
- Strategic recommendations
- Policy implications
- Comparative advantage analysis

### Usage Without AI
The application works fully without AI integration, providing:
- Built-in statistical analysis
- Chart-specific insights
- Data quality indicators

## 🎯 Use Cases

### Business Intelligence
- Market research and analysis
- Investment decision support
- Competitive benchmarking

### Academic Research
- Comparative studies
- Economic analysis
- Social science research

### Policy Analysis
- Government planning
- International comparisons
- Development indicators

### Educational Applications
- Teaching economics and geography
- Data visualization examples
- Statistical analysis demonstrations

## 🔍 Troubleshooting

### Common Issues

**"Unable to fetch country list"**
- Check internet connection
- Wait a moment and refresh (API rate limiting)
- Application will use fallback country list

**"No data available for selected countries"**
- Try different countries or metrics
- Some indicators may not be available for all countries
- Check data quality indicators in the interface

**Charts not displaying**
- Ensure you've selected at least one metric
- Check that selected entities have data for chosen metrics
- Try different visualization types

### Performance Tips
- Limit selections to 10-15 countries for optimal performance
- Use quick presets for faster metric selection
- Enable caching by avoiding frequent metric changes

## 🚀 Future Enhancements

- [ ] Historical trend analysis with time series data
- [ ] Additional data sources (IMF, OECD, UN)
- [ ] Custom metric calculations and ratios
- [ ] Advanced statistical analysis tools
- [ ] Export to PowerPoint/PDF reports
- [ ] User authentication and saved configurations
- [ ] Real-time data alerts and notifications

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include error handling for API calls
- Test with multiple countries and metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **World Bank** for providing comprehensive open data
- **Streamlit** for the excellent web framework
- **Plotly** for interactive visualization capabilities
- **Mistral AI** for advanced analytical insights

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the World Bank API documentation for data-related questions

---

**Built with ❤️ using Streamlit, Plotly, and World Bank Open Data**