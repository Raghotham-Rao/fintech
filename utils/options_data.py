import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from functools import reduce
import numpy as np

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

def load_option_chain_data(symbol):
    resp = requests.get(indices_url(symbol), headers=headers)

    current_expiry_date = reduce(
        lambda x, y: x if datetime.strptime(x, '%d-%b-%Y') < datetime.strptime(y, '%d-%b-%Y') else y,
        [i['expiryDate'] for i in resp.json()['records']['data']]
    )
    current_expiry_chain = list(filter(lambda x: x['expiryDate'] == current_expiry_date, resp.json()['records']['data']))

    current_expiry_chain = [
        {
            'expiryDate': i['expiryDate'],
            **{f'{k}_ce': v for k, v in i['CE'].items() if k in required_fields},
            'strikePrice': i['strikePrice'],
            **{f'{k}_pe': v for k, v in i['PE'].items() if k in required_fields}
        }
        
        for i in current_expiry_chain if 'PE' in i.keys() and 'CE' in i.keys()
    ]

    option_chain_df = pd.DataFrame(current_expiry_chain)
    option_chain_df.columns = [
        'expiry_date', 'OI_ce', 'delta_OI_ce', 'pct_delta_OI_ce', 'vol_ce', 'IV_ce', 'LTP_ce', 'chng_ce', 'pct_chg_ce', 
        'totalBuyQuantity_ce', 'totalSellQuantity_ce', 'bid_qty_ce',
        'bid_ce', 'ask_qty_ce', 'ask_ce', 'strike',
        'OI_pe', 'delta_OI_pe', 'pct_delta_OI_pe', 'vol_pe', 'IV_pe', 'LTP_pe', 'chng_pe', 'pct_chg_pe',
        'totalBuyQuantity_pe', 'totalSellQuantity_pe', 'bid_qty_pe',
        'bid_pe', 'ask_qty_pe', 'ask_pe'
    ]

    option_chain_df = option_chain_df.drop(['totalBuyQuantity_ce', 'totalBuyQuantity_pe', 'totalSellQuantity_ce', 'totalSellQuantity_pe', 'expiry_date'], axis=1).round(2)

    return option_chain_df