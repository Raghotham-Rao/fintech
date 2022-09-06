import streamlit as st
import plotly.graph_objects as go
from load_data import DataLoader
import pandas as pd
from datetime import datetime, timedelta

default_title = "Fintech"
script_name = None

bull_color = '8bc34a'
bear_color = 'd32f2f'
arrow_up_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="3em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path fill="none" stroke="#{bull_color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 20V4m-7 7l7-7l7 7"/></svg>'
arrow_down_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="2em" height="60px" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path fill="none" stroke="#{bear_color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 20V4m-7 9l7 7l7-7"/></svg>'

sidenav = st.sidebar

with sidenav:
    st.markdown("<h1>Fintech</h1>", unsafe_allow_html=True)

    script_name = st.text_input(label="Script Name", placeholder="Enter script name").upper()
    from_date = st.date_input(label="From")
    to_date = st.date_input(label="To")


# populate main area

st.title(script_name or default_title)

if script_name:
    summary_tab, technicals_tab, others_tab = st.tabs(['Summary', 'Technicals', 'Others'])

    with summary_tab:

        data = None
        
        try:
            data = DataLoader. \
                load_data(script_name, from_date.strftime("%d-%m-%Y"), to_date.strftime("%d-%m-%Y"), "EQ").\
                sort_values('date').drop_duplicates()
        except:
            st.text('An Error Occurred! Check inputs.')

        latest_record = data.iloc[-1, :].to_dict()
        
        change = round(latest_record['close'] - latest_record['prev_close'], 2)
        pct_change = round(change * 100 / latest_record['prev_close'], 2)

        col1, col2 = st.columns(2)
        font_color = bear_color if change < 0 else bull_color

        with col1:
            st.markdown(f'<span style="font-size: 4em; font-weight: bolder; color: #{font_color}">{latest_record["close"]}</span><span style="padding-bottom: 20px">{arrow_up_svg if change > 0 else arrow_down_svg}</span>', unsafe_allow_html=True)
            st.markdown(f'<span style="font-size: 1.5em; margin-right: 2%; color: #{font_color}">{change}</span> <span style="font-size: 1.5em; color: #{font_color}">({pct_change}%)</span>', unsafe_allow_html=True)


        last_90_days_data = data.iloc[-90:, :]

        fig = go.Figure(data=go.Candlestick(x=last_90_days_data['date'],
                             open=last_90_days_data['open'],
                             high=last_90_days_data['high'],
                             low=last_90_days_data['low'],
                             close=last_90_days_data['close'])
                        )

        fig.update_layout(xaxis_rangeslider_visible=False, title="90 day Movement", margin=dict(l=0, r=0, t=0, b=0))
        fig.update_traces(line = dict(width=1))
        fig.update_xaxes(showgrid=False)

        st.plotly_chart(fig)

        expander = st.expander('Show Data')

        with expander:
            st.dataframe(last_90_days_data.set_index('date'))
