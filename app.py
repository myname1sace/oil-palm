# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load datasets
company_comparison = pd.read_csv("C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/company_comparison.csv")
state_comparison = pd.read_csv('C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/state_comparison.csv')
production_comparison = pd.read_csv('C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/production_comparison.csv')
input_materials_comparison = pd.read_csv('C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/input_materials_comparison.csv')
land_market = pd.read_csv('C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/land_market.csv')
results = pd.read_csv('C:/Users/USER/Downloads/HNG/Stage4/Dataset/datasets/results.csv')

# Data Preprocessing
# Clean data (drop missing values, handle calculations, etc.)
company_comparison.dropna(inplace=True)
state_comparison.dropna(inplace=True)
production_comparison.dropna(inplace=True)

# Calculated Fields
# Profit per Hectare
company_comparison['Profit per Hectare'] = (company_comparison['Revenue'] - company_comparison['Cost of revenue']) / state_comparison['total_estate_area']

# Profit Margin
company_comparison['Profit Margin'] = (company_comparison['Profit for the year'] / company_comparison['Revenue']) * 100

# ROI (Return on Investment) - assuming net assets represent investment
company_comparison['ROI'] = (company_comparison['Profit for the year'] / company_comparison['Net assets']) * 100

# Break-even Point Calculation - This is simplified, but you can refine it based on your business model.
company_comparison['Break-even Point'] = company_comparison['Cost of revenue'] / company_comparison['Profit per Hectare']

# Streamlit UI
st.title('Palm Oil Plantation Profitability Dashboard')

# Filters
# Dropdown for selecting State
selected_state = st.selectbox('Select State', state_comparison['state'].unique())

# Dropdown for selecting Year
selected_year = st.selectbox('Select Year', production_comparison['year'].unique())

# Dropdown for selecting Company (Okomu or Presco)
selected_company = st.selectbox('Select Company', company_comparison['metric'].unique())

# Filter data based on selected state
filtered_state_data = state_comparison[state_comparison['state'] == selected_state]

# Filter production data based on the selected year
filtered_production_data = production_comparison[production_comparison['year'] == selected_year]

# Filter company data based on selected company
filtered_company_data = company_comparison[company_comparison['metric'] == selected_company]

# Plot 1: State-wise Profitability (Profit per Hectare)
profit_per_hectare_fig = px.bar(filtered_state_data, 
                                x='state', 
                                y='avg_cost_per_ha', 
                                title=f"Cost per Hectare for {selected_state}",
                                labels={'avg_cost_per_ha': 'Cost per Hectare'},
                                hover_data=['state', 'avg_cost_per_ha'])  # Tooltips showing additional data

st.plotly_chart(profit_per_hectare_fig)

# Plot 2: Cost vs Revenue Comparison (for Okomu and Presco)
company_fig = px.bar(filtered_company_data, 
                     x='metric', 
                     y=['Revenue', 'Cost of revenue'], 
                     title=f'Cost vs Revenue for {selected_company}', 
                     labels={'metric': 'Metric'},
                     hover_data=['Revenue', 'Cost of revenue', 'Profit Margin'])

st.plotly_chart(company_fig)

# Plot 3: Historical Production Trends (using USDA and FAOSTAT data)
historical_production_fig = px.line(filtered_production_data, 
                                    x='year', 
                                    y=['Production', 'Imports', 'Exports'], 
                                    title=f'Historical Production Trends ({selected_year})', 
                                    labels={'year': 'Year', 'value': 'Metric Value'},
                                    hover_data=['Production', 'Imports', 'Exports'])

st.plotly_chart(historical_production_fig)

# Plot 4: Yield vs Rainfall (Scatter Plot)
yield_vs_rainfall_fig = px.scatter(state_comparison, 
                                   x='avg_temp', 
                                   y='avg_wind_speed', 
                                   title="Yield vs Rainfall", 
                                   labels={'avg_temp': 'Average Temperature', 'avg_wind_speed': 'Average Wind Speed'},
                                   hover_data=['avg_temp', 'avg_wind_speed', 'state'])

st.plotly_chart(yield_vs_rainfall_fig)

# Plot 5: State-wise Cost per Hectare
cost_per_hectare_fig = px.bar(state_comparison, 
                              x='state', 
                              y='avg_cost_per_ha', 
                              title='State-wise Cost per Hectare',
                              labels={'avg_cost_per_ha': 'Cost per Hectare'},
                              hover_data=['state', 'avg_cost_per_ha'])

st.plotly_chart(cost_per_hectare_fig)

# Plot 6: State-wise Climate Comparison (Temperature, Humidity, Wind Speed)
climate_comparison_fig = px.bar(state_comparison, 
                                x='state', 
                                y=['avg_temp', 'avg_humidity', 'avg_wind_speed'], 
                                title='State-wise Climate Comparison', 
                                labels={'state': 'State'},
                                hover_data=['avg_temp', 'avg_humidity', 'avg_wind_speed'])

st.plotly_chart(climate_comparison_fig)

# Plot 7: State-wise Soil Comparison (Soil pH, N, OC)
soil_comparison_fig = px.bar(state_comparison, 
                             x='state', 
                             y=['avg_ph', 'avg_n', 'avg_oc'], 
                             title='State-wise Soil Comparison', 
                             labels={'state': 'State'},
                             hover_data=['avg_ph', 'avg_n', 'avg_oc'])

st.plotly_chart(soil_comparison_fig)

# Additional Calculations and Insights:
# Show ROI and Break-even point for the selected company
roi = filtered_company_data['ROI'].values[0]
break_even = filtered_company_data['Break-even Point'].values[0]

st.write(f"ROI for {selected_company}: {roi:.2f}%")
st.write(f"Break-even Point for {selected_company}: {break_even:.2f} hectares")
