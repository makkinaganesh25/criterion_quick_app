import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout = 'wide',
                   page_title = 'Tweet Search',
                   page_icon='🎞️')

st.title("Criterion Collection Quick Filter")
format_cols = ['DVD', 'Blu‑ray',
       'Blu-Ray/DVD Combo', '4K UHD+Blu-ray Combo', 'Collectors Sets']

col1, col2, col3, col4 = st.columns([0.2, 0.4, 0.2,0.2])

filter_by = col1.selectbox(label = 'Filter', options = ['Search String', 'Search Hashtag', 'Search User'], placeholder = 'Title')
search = col2.text_input(label = 'Search')
date1 = col3.text_input(label = 'Date Range 1', placeholder='2023-01-01')
date2 = col4.text_input(label = 'Date Range 2', placeholder='2024-01-01')

df = pd.read_csv('criterion_export.csv')

if search:
    df = df[df[filter_by].str.contains(search, na=False)]
else:
    pass

df['Year'] = df['Year'].astype('Int64').astype(str)
df['Collectors Sets'] = df['Collectors Sets'].replace('[]', '')
st.dataframe(df, hide_index=True,
             width=2000)
