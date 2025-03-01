import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from millify import millify 
import us


st.set_page_config(layout='wide')

st.title('E-Commerce Sales Dashboard')


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

def sales_per_month():
  #Sort values by Order Date in descending order
  sortedDf = df.sort_values(by='Order Date').reset_index()

  #Group by month and sum Sales
  grouping = sortedDf.groupby(sortedDf['Year-month'])['Sales'].sum().reset_index()

  #Create plotly figure
  fig = px.bar(grouping, x='Year-month', y='Sales',
              labels={'Year-month': 'Month', 'Sales': 'Total Sales'},
             title='Sales per month')
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

def get_top_products():
  df_products = df.copy()
  top_products = df_products.groupby('Product ID')['Profit'].sum().sort_values(ascending=True).reset_index()
  fig = px.bar(top_products.tail(10), x='Profit', y='Product ID')
  st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --------------------------------------- #

df = load_data('ecomm_sales_data.csv')
 #Convert Order Date to datetime format
with st.expander('Sales Data Preview'):
  st.dataframe(df, column_config={'Order Date': st.column_config.DateColumn(format="DD/MM/YYYY"), 'Ship Date': st.column_config.DateColumn(format="DD/MM/YYYY")})
# Metrics

orders =df['Order ID'].nunique()
aov = df.groupby(df['Order ID'])['Sales'].sum().mean()
sales = df['Sales'].sum()

# Display in Streamlit

met1, met2, met3 = st.columns(3)

with met1:
  st.metric('Total Orders', orders, border=True)

with met2:  
  st.metric('Total Sales', millify(sales), border=True)

with met3:
  st.metric('Average Order Value', millify(aov), border=True)

with st.sidebar:
  sales_dropdown = st.selectbox("Year", np.sort(df['Year'].unique()), label_visibility='collapsed')

top_left, top_right = st.columns([0.7,0.3])
with top_left:
  st.subheader("Sales")
  if sales_dropdown == 'Month':
    #Monthly Sales
    sales_per_month()
  else:
    sales_per_year()

with top_right:
    st.markdown("### Top 10 Products ###")
    get_top_products()
    
#else:

  #Create plotly figure
  #fig = px.bar(yearly_sales, x='year', y='Sales',
              #labels={'year': 'Month', 'Sales': 'Total Sales'},
             #title='Sales per Year')
  #st.plotly_chart(fig, config={'displayModeBar': False})



