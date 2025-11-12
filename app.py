# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
company_comparison = pd.read_csv('oil-palm/company_comparison.csv')
state_comparison = pd.read_csv('oil-palm/state_comparison.csv')
production_comparison = pd.read_csv('oil-palm/production_comparison.csv')
input_materials_comparison = pd.read_csv('oil-palm/input_materials_comparison.csv')
land_market = pd.read_csv('oil-palm/land_market.csv')
results = pd.read_csv('oil-palm/results.csv')

# Data Cleaning (if needed)
company_comparison.dropna(inplace=True)
state_comparison.dropna(inplace=True)
production_comparison.dropna(inplace=True)

# Streamlit UI
st.title("Palm Oil Profitability Dashboard")

# Filters
selected_state = st.selectbox("Select State", state_comparison['state'].unique())
selected_year = st.selectbox("Select Year", production_comparison['year'].unique())
selected_company = st.selectbox("Select Company", company_comparison['metric'].unique())

# Filter data based on selected options
filtered_state_data = state_comparison[state_comparison['state'] == selected_state]
filtered_production_data = production_comparison[production_comparison['year'] == selected_year]
filtered_company_data = company_comparison[company_comparison['metric'] == selected_company]

# Plot 1: State-wise Profitability (Profit per Hectare)
profit_per_hectare_fig = px.bar(filtered_state_data, 
                                x='state', 
                                y='avg_cost_per_ha', 
                                title=f"Cost per Hectare for {selected_state}",
                                labels={'avg_cost_per_ha': 'Cost per Hectare'},
                                hover_data=['state', 'avg_cost_per_ha'])
st.plotly_chart(profit_per_hectare_fig)

# Plot 2: Cost vs Revenue Comparison (Okomu vs Presco)
company_fig = px.bar(filtered_company_data, 
                     x='metric', 
                     y=['Revenue', 'Cost of revenue'], 
                     title=f"Cost vs Revenue for {selected_company}", 
                     labels={'metric': 'Metric'},
                     hover_data=['Revenue', 'Cost of revenue', 'Profit Margin'])
st.plotly_chart(company_fig)

# Plot 3: Historical Production Trends (using USDA and FAOSTAT data)
historical_production_fig = px.line(filtered_production_data, 
                                    x='year', 
                                    y=['Production', 'Imports', 'Exports'], 
                                    title=f"Historical Production Trends for {selected_year}", 
                                    labels={'year': 'Year', 'value': 'Metric Value'})
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
                              title="State-wise Cost per Hectare",
                              labels={'avg_cost_per_ha': 'Cost per Hectare'},
                              hover_data=['state', 'avg_cost_per_ha'])
st.plotly_chart(cost_per_hectare_fig)

# Plot 6: State-wise Climate Comparison (Temperature, Humidity, Wind Speed)
climate_comparison_fig = px.bar(state_comparison, 
                                x='state', 
                                y=['avg_temp', 'avg_humidity', 'avg_wind_speed'], 
                                title="State-wise Climate Comparison", 
                                labels={'state': 'State'},
                                hover_data=['avg_temp', 'avg_humidity', 'avg_wind_speed'])
st.plotly_chart(climate_comparison_fig)

# Plot 7: State-wise Soil Comparison (Soil pH, N, OC)
soil_comparison_fig = px.bar(state_comparison, 
                             x='state', 
                             y=['avg_ph', 'avg_n', 'avg_oc'], 
                             title="State-wise Soil Comparison", 
                             labels={'state': 'State'},
                             hover_data=['avg_ph', 'avg_n', 'avg_oc'])
st.plotly_chart(soil_comparison_fig)

# Add more calculated fields if necessary
roi = filtered_company_data['ROI'].values[0]
break_even = filtered_company_data['Break-even Point'].values[0]

st.write(f"ROI for {selected_company}: {roi:.2f}%")
st.write(f"Break-even Point for {selected_company}: {break_even:.2f} hectares")
