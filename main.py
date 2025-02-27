import streamlit as st
import pandas as pd



st.set_page_config(layout='wide')

st.title('E-Commerce Sales Dashboard')

df = pd.read_csv('ecomm_sales_data.csv')

df
