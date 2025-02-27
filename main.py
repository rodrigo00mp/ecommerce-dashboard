import streamlit as st
import pandas as pd
import plotly.express as px
from millify import millify 



st.set_page_config(layout='wide')

st.title('E-Commerce Sales Dashboard')


### -------- Functions --------- ####

@st.cache_data
def load_data(path:str):
  data = pd.read_csv('ecomm_sales_data.csv')
  return data


#Monthly Sales Chart#

def sales_by_month():
  #Sort values by Order Date in descending order
  sortedDf = df.sort_values(by='Order Date').reset_index()

  #Create new column to uniquely identif month. Conver to string so plotly doesn`t crash
  sortedDf['year-month'] = sortedDf['Order Date'].dt.to_period('M').astype(str)

  #Group by month and sum Sales
  grouping = sortedDf.groupby(sortedDf['year-month'])['Sales'].sum().reset_index()
  return grouping

def sales_by_year():
  #Sort values by Order Date in descending order
  sortedDf = df.sort_values(by='Order Date').reset_index()

  #Create new column to uniquely identif month. Conver to string so plotly doesn`t crash
  sortedDf['year'] = sortedDf['Order Date'].dt.to_period('Y').astype(str)

  #Group by month and sum Sales
  grouping = sortedDf.groupby(sortedDf['year'])['Sales'].sum().reset_index()
  return grouping


# --------------------------------------- #


df = load_data('ecomm_sales_data.csv')
 #Convert Order Date to datetime format
df['Order Date'] =  pd.to_datetime(df['Order Date'])
# Metrics

orders =df['Order ID'].nunique()
aov = df.groupby(df['Order ID'])['Sales'].sum().mean()
sales = df['Sales'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Orders", millify(orders), "20%", border=True)
col2.metric("Sales", "$" + millify(sales), "-3%", border=True)
col3.metric("Average Order Value", "$" + millify(aov, precision=2), "4%", border=True)



 

# Display in Streamlit

# Monthly Sales
monthly_sales = sales_by_month()
    # Monthly Sales
yearly_sales = sales_by_year()


st.subheader("Sales")
sales_dropdown = st.selectbox("Sales by:", ('Month', 'Year'), label_visibility='collapsed')

if sales_dropdown == 'Month':
  
  #Create plotly figure
  fig = px.bar(monthly_sales, x='year-month', y='Sales',
              labels={'year-month': 'Month', 'Sales': 'Total Sales'},
             title='Sales per month')
  st.plotly_chart(fig, config={'displayModeBar': False})
else:

  #Create plotly figure
  fig = px.bar(yearly_sales, x='year', y='Sales',
              labels={'year': 'Month', 'Sales': 'Total Sales'},
             title='Sales per Year')
  st.plotly_chart(fig, config={'displayModeBar': False})



