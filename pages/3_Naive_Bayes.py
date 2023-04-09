import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np

# Name Page
st.set_page_config(
    page_title="Dataset"
)

st.title(':orange[Naive Bayes Classifier]')
st.subheader('\n\n')

st.subheader('Upload Dataset')
uploaded_file = st.file_uploader('Upload Document Format .xlsx', type='xlsx')
if uploaded_file:
    st.markdown('Data Raw:')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)


