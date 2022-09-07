import streamlit as st
import plotly.graph_objects as go
from load_data import DataLoader
from pages.tabs.summary import load_summary_tab_content
from pages.tabs.technicals import load_technicals_tab_content


default_title = "Equities"
script_name = None

sidenav = st.sidebar

with sidenav:
    with st.form("equity_details"):
        script_name = st.text_input(label="Script Name", placeholder="Enter script name").upper()
        from_date = st.date_input(label="From")
        to_date = st.date_input(label="To")
        st.form_submit_button("Get Data")


# populate main area

st.title(script_name or default_title)

if script_name:

    data = None
    with st.spinner('Loading Data...'):
        try:
            data = DataLoader. \
                load_data(script_name, from_date.strftime("%d-%m-%Y"), to_date.strftime("%d-%m-%Y"), "EQ").\
                sort_values('date').drop_duplicates()
        except:
            st.text('An Error Occurred! Check inputs.')

    summary_tab, technicals_tab, others_tab = st.tabs(['Summary', 'Technicals', 'Others'])

    with summary_tab:
        load_summary_tab_content(data)

    with technicals_tab:
        load_technicals_tab_content(data)