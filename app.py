import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout = 'wide',
                   page_title = 'Criterion Title Quick Filter',
                   page_icon='🎞️')

st.title("Criterion Collection Quick Filter")
format_cols = ['DVD', 'Blu‑ray',
       'Blu-Ray/DVD Combo', '4K UHD+Blu-ray Combo', 'Collectors Sets']

col1, col2 = st.columns([0.1, 0.9])

filter_by = col1.selectbox(label = 'Filter By', options = ['Title', 'Director'], placeholder = 'Title')
search = col2.text_input(label = 'Search . . .')

df = pd.read_csv('criterion_export.csv')

if search:
    df = df[df[filter_by].str.contains(search, na=False)]
else:
    pass

df['Year'] = df['Year'].astype('Int64').astype(str)
df['Collectors Sets'] = df['Collectors Sets'].replace('[]', '')
st.dataframe(df, hide_index=True,
             width=2000)