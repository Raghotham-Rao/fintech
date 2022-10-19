from datetime import datetime, timedelta
import requests
import pandas as pd

REQUEST_HEADERS = {
    "user-agent": "Custom"
}

QUERY_PARAMS = {
    "formatted": "true",
    "lang": "en-US",
    "region": "US",
    "includeAdjustedClose": "true",
    "interval": "1d",
    "events": "capitalGain%7Cdiv%7Csplit",
    "useYfid": "true",
    "corsDomain": "finance.yahoo.com",
}

BASE_URL = 'https://query2.finance.yahoo.com/v8/finance/chart/'

column_order = ['date', 'symbol', 'open', 'high', 'low', 'close', 'prev_close', 'volume']


def get_historical_data(script_name:str, from_date:str = None, to_date:str = None, exchg:str='NS'):
    url = f'{BASE_URL}{script_name.upper()}.{exchg.upper()}'
    
    to_timestamp = int((datetime.strptime(to_date, '%Y-%m-%d') if to_date is not None else datetime.now()).timestamp())
    from_timestamp = int((datetime.strptime(from_date, '%Y-%m-%d') if from_date is not None else (datetime.now() - timedelta(days=90))).timestamp())

    query_params = {**QUERY_PARAMS, "period1": from_timestamp, "period2": to_timestamp}

    resp = requests.get(url, headers=REQUEST_HEADERS, params=query_params)

    content = resp.json()['chart']['result'][0]
    data_zip = zip(
        content['timestamp'], 
        content['indicators']['quote'][0]['open'],
        content['indicators']['quote'][0]['high'],
        content['indicators']['quote'][0]['low'],
        content['indicators']['quote'][0]['close'],
        content['indicators']['adjclose'][0]['adjclose'],
        content['indicators']['quote'][0]['volume'],
    )
    df = pd.DataFrame(data_zip, columns=['timestamp', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
    df['date'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x).date())
    df['symbol'] = script_name.upper()
    df['prev_close'] = df['close'].shift(1)

    return df[column_order]

def get_current_price(script_name:str, exchg:str='NS'):
    url = f'{BASE_URL}{script_name.upper()}.{exchg.upper()}'
    query_params = QUERY_PARAMS
    resp = requests.get(url, headers=REQUEST_HEADERS, params=query_params)
    resp_dict = resp.json()['chart']['result'][0]['meta']
    current_price_dict = {k: v for k, v in resp_dict.items() if k in ['regularMarketPrice', 'chartPreviousClose']}
    current_price_dict['change'] = current_price_dict['regularMarketPrice'] - current_price_dict['chartPreviousClose']
    current_price_dict['change_pct'] = current_price_dict['change'] * 100 / current_price_dict['chartPreviousClose']
    
    return current_price_dict