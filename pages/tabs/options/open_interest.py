import plotly.express as px
import streamlit as st

def show_open_interest(option_chain_df):
    oi_chart = px.bar(
        option_chain_df, 
        x='strike', 
        y=['OI_ce', 'OI_pe'], 
        barmode='group',
        color_discrete_sequence=['crimson', '#81c784']
    )

    oi_chart.update_layout(showlegend=False, height=600)

    st.plotly_chart(oi_chart, use_container_width=True)