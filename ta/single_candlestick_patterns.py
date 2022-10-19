import pandas as pd
import numpy as np

def pre_process(df):
    df['candle_body_length'] = (df['open'] - df['close']).abs()
    df['candle_length'] = df['high'] - df['low']
    df['candle_body_ratio'] = df['candle_body_length'] / df['candle_length']
    df['candle_color'] = np.where(df.close > df.open, 'green', 'red')
    df['pct_change'] = (df['close'] - df['prev_close']) * 100 / df['prev_close']
    return df

def identify_marubozus(df):
    df['marubozu'] = np.where(
        np.logical_and.reduce([
             df['candle_body_ratio'] > 0.85, 
             df['pct_change'].abs() > 0.5
        ]),
        df["candle_color"].replace({"green": "Bullish", "red": "Bearish"}),
        None
    )
    return df

def identify_dojis(df):
    df['is_doji'] = np.where(
        np.logical_or(
            np.logical_and.reduce(
                [
                    df['candle_body_ratio'] < 0.15,
                    df['candle_color'] == 'red',
                    ((df['high'] - df['open']) / df['candle_length']).between(.33, .67)
                ]
            ),
            np.logical_and.reduce(
                [
                    df['candle_body_ratio'] < 0.15,
                    df['candle_color'] == 'green',
                    ((df['high'] - df['close']) / df['candle_length']).between(.33, .67)
                ]
            ),
        ),
        True,
        False
    )
    return df

def identify_paper_umbrellas(df):
    df['paper_umbrella_type'] = np.where(
        np.logical_or(
            np.logical_and.reduce([
                df['candle_body_ratio'] < 0.38,
                df['candle_color'] == 'green',
                ((df['open'] - df['low']) / df['candle_length']) >= 0.60,
                ((df['high'] - df['close']) / df['candle_length']) <= 0.125,
            ]),
            np.logical_and.reduce([
                df['candle_body_ratio'] < 0.38,
                df['candle_color'] == 'red',
                ((df['close'] - df['low']) / df['candle_length']) >= 0.60,
                ((df['high'] - df['open']) / df['candle_length']) <= 0.125,
            ])
        ),
        'Yes',
        'No'
    )
    return df

def identify_shooting_stars(df):
    df['is_shooting_star'] = np.where(
        np.logical_or(
            np.logical_and.reduce([
                df['candle_body_ratio'] < 0.38,
                df['candle_color'] == 'green',
                ((df['high'] - df['close']) / df['candle_length']) >= 0.6
            ]),
            np.logical_and.reduce([
                df['candle_body_ratio'] < 0.38,
                df['candle_color'] == 'red',
                ((df['high'] - df['open']) / df['candle_length']) >= 0.6
            ])
        ),
        True,
        False
    )
    return df