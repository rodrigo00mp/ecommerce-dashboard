import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from millify import millify 
import us


st.set_page_config(layout='wide')

### -------- Functions --------- ####


@st.cache_data
def load_data(path:str):
  data = pd.read_csv('ecomm_sales_data.csv')
  data['Order Date'] =  pd.to_datetime(data['Order Date'])
  data['Ship Date'] =  pd.to_datetime(data['Ship Date'])
  data['Year-month'] = data['Order Date'].dt.to_period('M').astype(str)
  data['Year'] = data['Order Date'].dt.to_period('Y').astype(str)
  return data


#Monthly Sales Chart#

def sales_per_month(year, region):
  #Sort values by Order Date in descending order
  selectedYear_df = df[(df['Year'] == year) & (df['Region'] == region)]
  sortedDf = selectedYear_df.sort_values(by='Order Date').reset_index()
  #Group by month and sum Sales
  grouping = sortedDf.groupby(['Year-month'])['Sales'].sum().reset_index()
  avg = grouping['Sales'].mean()
  #Create plotly figure
  fig = px.line(grouping, x='Year-month', y='Sales',
              labels={'Year-month': 'Month', 'Sales': 'Total Sales'},
             title='Sales per Month', markers=True)
  fig.update_traces(line=dict(width=2), fill='tonexty', fillcolor='rgba(0, 176, 246, 0.2)')
  
  fig.add_trace(go.Scatter(
      x=grouping['Year-month'], y=[avg] * len(grouping['Year-month']),  # Same y-value for all x-values
      mode="lines",
      name="Average",
      line=dict(color="red", dash="dash"),
      hoverinfo="y"
  ))

  fig.update_layout(yaxis=dict(tickprefix="$", tickformat=","))
  st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def sales_per_year():
  #Sort values by Order Date in descending order
  sortedDf = df.sort_values(by='Order Date').reset_index()


  #Group by month and sum Sales
  grouping = sortedDf.groupby(sortedDf['Year'])['Sales'].sum().reset_index()
  fig = px.bar(grouping, x='Year', y='Sales',
              labels={'Year': 'Year', 'Sales': 'Total Sales'},
             title='Sales per Year')
  st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})

def get_top_products(year, region):
  selectedYear_df = df[(df['Year'] == year) & (df['Region'] == region)]
  top_products = selectedYear_df.groupby(['Product ID','Product Name'])['Profit'].sum().sort_values(ascending=True).reset_index()
  fig = px.bar(top_products.tail(10), x='Profit', y='Product ID', title='Top Products',  hover_data=['Product ID', 'Product Name', 'Profit'])
  fig.update_layout(
    xaxis=dict(
        tickprefix="$",  # Add dollar sign
        tickformat=",",  # Add thousand separators
        title="Profit",
    )
  )
  st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def calculate_metrics(year, region):
  selectedYear_df = df[(df['Year'] == year) & (df['Region'] == region)]
  orders = selectedYear_df['Order ID'].nunique()
  aov = selectedYear_df.groupby(selectedYear_df['Order ID'])['Sales'].sum().mean()
  sales = selectedYear_df['Sales'].sum()
  fig_orders = go.Figure()
  fig_sales = go.Figure()
  fig_aov = go.Figure()
  fig_orders.add_trace(go.Indicator(
    mode = "number",
    value = orders,
    title = {'text':'Total Orders'},
    number={"font": {"size": 64}},
    ))
  
  fig_sales.add_trace(go.Indicator(
    mode = "number",
    value = sales,
    title = {'text':'Total Sales'},
    number={"font": {"size": 64}, "prefix":"$"},
    ))

  fig_aov.add_trace(go.Indicator(
    mode = "number",
    value = aov,
    title = {'text':'Average Order Value'},
    number={"font": {"size": 64}, "prefix":"$"},
  ))

  layout_config={
    "margin":dict(l=20, r=20, t=30, b=20),
    "height":140,
    "font":dict(
        size=18,  # Set the font size here
    )
  }
  fig_orders.update_layout(layout_config)
  fig_sales.update_layout(layout_config)
  fig_aov.update_layout(layout_config)


  st.plotly_chart(fig_orders, use_container_width=True, config={'displayModeBar': False})
  st.plotly_chart(fig_sales, use_container_width=True, config={'displayModeBar': False})
  st.plotly_chart(fig_aov, use_container_width=True, config={'displayModeBar': False})


def category_breakdown(year, region):
  selectedYear_df = df[(df['Year'] == year) & (df['Region'] == region)]
  categories_breakdown = selectedYear_df.groupby(['Category', 'Sub-Category'])['Sales'].sum().sort_values(ascending=False).reset_index()
  fig = px.bar(categories_breakdown, x='Category', y='Sales', color='Sub-Category', title='Sales per Category')
  st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def segment_chart(year, region):
  selectedYear_df = df[(df['Year'] == year) & (df['Region'] == region)]
  segment_breakdown = selectedYear_df.groupby(['Segment'])['Sales'].sum().reset_index()

  fig = px.pie(segment_breakdown, values='Sales', names='Segment', title='Segment Brerakdown')
  st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
# --------------------------------------- #



df = load_data('ecomm_sales_data.csv')
 #Convert Order Date to datetime format

with st.sidebar:
  st.title('E-Commerce Sales Dashboard')
  st.header('Settings')
  year_dropdown = st.selectbox("Year", np.sort(df['Year'].unique()))
  region_dropdown = st.selectbox("Region", np.sort(df['Region'].unique()))


top_left, top_right = st.columns([0.7, 0.3])
bottom_left, bottom_middle, bottom_right = st.columns([0.35,0.35,0.3])
with top_left:
  #st.subheader("Sales")
  sales_per_month(year_dropdown, region_dropdown)

with top_right:
  calculate_metrics(year_dropdown, region_dropdown)

with bottom_left:
  #st.markdown("### Top 10 Products ###")
  category_breakdown(year_dropdown, region_dropdown)

with bottom_middle:
  segment_chart(year_dropdown, region_dropdown)

with bottom_right:
  #st.markdown("### Top 10 Products ###")
  get_top_products(year_dropdown, region_dropdown)




