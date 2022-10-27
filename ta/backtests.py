import numpy as np

def preprocess(df):
    df['candle_body_length'] = (df['open'] - df['close']).abs()
    df['candle_length'] = df['high'] - df['low']
    df['candle_body_ratio'] = df['candle_body_length'] / df['candle_length']
    df['candle_color'] = np.where(df.close > df.open, 'green', 'red')
    df['pct_change'] = (df['close'] - df['prev_close']) * 100 / df['prev_close']
    
    for i in ['open', 'high', 'close', 'low', 'candle_color', 'candle_body_ratio', 'candle_body_length']:
        df[f'prev_{i}'] = df[i].shift(1)
    return df

def get_returns(df):
    for i in [2, 3, 5, 8, 13]:
        df[f'd{i}_high'] = df['high'].shift(-i)
        df[f'd{i}_close'] = df['close'].shift(-i)
        df[f'd{i}_return_pct'] = (df[f'd{i}_close'] - df['next_day_open']) * 100 / df['next_day_open']
        df[f'd{i}_win_flag'] = df[f'd{i}_return_pct'] >= 2
    return df


def show_performance(df, indicator_column):
    col_set = [indicator_column] + ['symbol', 'next_day_open', 'ADX', 'plus_DI', 'minus_DI', 
                                    'rsi', 'rsi_bin', 'bb_upper', 'bb_lower']
    col_set += [i for i in df.columns if '_return_pct' in i or '_flag' in i] + [f'd{i}_indicator_conf' for i in [2, 3, 5, 8, 13]]

    for i in [2, 3, 5, 8, 13]:
        df[f'd{i}_indicator_conf'] = np.where(
            np.logical_or(
                (df[indicator_column].str.contains('bear', case=False) & (df[f'd{i}_return_pct'] < 0)),
                (df[indicator_column].str.contains('bull', case=False) & (df[f'd{i}_return_pct'] > 0))
            ),
            1, 0
        )
    
    return df[df[indicator_column].notna()][col_set]

def get_rsi_details(df):
    return df[np.where(
        np.logical_or.reduce([
            (df[f"d{i}_win_flag"] == True) for i in [2, 3, 5, 8, 13]
        ]),
        True,
        False
    )].groupby("rsi_bin").agg({"rsi_bin": "count"})