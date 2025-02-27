import streamlit as st
import pandas as pd
import plotly.express as px




st.set_page_config(layout='wide')

st.title('E-Commerce Sales Dashboard')

df = pd.read_csv('ecomm_sales_data.csv')

#Convert Order Date to datetime format
df['Order Date'] =  pd.to_datetime(df['Order Date'])

def sales_by_month():
  #Sort values by Order Date in descending order
  sortedDf = df.sort_values(by='Order Date').reset_index()

  #Create new column to uniquely identif month. Conver to string so plotly doesn`t crash
  sortedDf['year-month'] = sortedDf['Order Date'].dt.to_period('M').astype(str)

  #Group by month and sum Sales
  grouping = sortedDf.groupby(sortedDf['year-month'])['Sales'].sum().reset_index()
  return grouping
  
monthly_sales = sales_by_month()

#Create plotly figure
fig = px.bar(monthly_sales, x='year-month', y='Sales',
             labels={'year-month': 'Month', 'Sales': 'Total Sales'},
             title='Monthly Sales')

# Display in Streamlit
st.plotly_chart(fig)



