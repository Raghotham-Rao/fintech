import streamlit as st
from utils.nse_data_load import get_indices_info
    
st.set_page_config(layout="wide")

st.title("FinTech")

indices_df = get_indices_info()
for i in indices_df['key'].unique():
    st.header(i)
    st.dataframe(indices_df[indices_df["key"] == i].iloc[:, 1:])