import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from functools import reduce
import numpy as np
import plotly.graph_objects as go

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "cookie": '',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

required_fields = ["openInterest", "changeinOpenInterest", "pchangeinOpenInterest", "totalTradedVolume", "impliedVolatility", "lastPrice", "change", "pChange", "totalBuyQuantity", "totalSellQuantity", "bidQty", "bidprice", "askQty", "askPrice",]

indices_url = lambda x: f'https://www.nseindia.com/api/option-chain-indices?symbol={x}'
equities_url = lambda x: f'https://www.nseindia.com/api/option-chain-equities?symbol={x}'

def show_option_chain(option_chain_df, current_price):
    call_colors = np.where(option_chain_df['strike'] < current_price, '#ffecb3', 'white')
    put_colors = np.where(option_chain_df['strike'] > current_price, '#ffecb3', 'white')
    col_dist = [call_colors for i in option_chain_df.columns if 'ce' in i] + ['white'] + [put_colors for i in option_chain_df.columns if 'ce' in i]

    option_chain_fig = go.Figure(data=go.Table(
        header=dict(values=option_chain_df.columns, height=25, fill=dict(color='#4a148c'), font=dict(color="white")),
        cells=dict(values=[
            (option_chain_df[i] if 'LTP' not in i else option_chain_df[i].apply(lambda x: f'<b>{x}</b>')) for i in option_chain_df.columns
        ], height=25, fill=dict(color=col_dist), line_color="lightgrey"),
        columnwidth=[80 for i in option_chain_df.columns]
    ))

    option_chain_fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=600)

    st.plotly_chart(
        option_chain_fig,
        use_container_width=True
    )