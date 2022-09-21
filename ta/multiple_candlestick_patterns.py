import pandas as pd
import numpy as np

def identify_engulfing(df):
    for i in ['open', 'high', 'close', 'low', 'candle_color', 'candle_body_ratio', 'candle_body_length']:
        df[f'prev_{i}'] = df[i].shift(1)

    df['engulfing'] = np.where(
        np.logical_and.reduce([
            df['prev_candle_color'] != df['candle_color'],
            df['prev_candle_body_ratio'] >= 0.15,
            df['prev_open'].between(df[['open', 'close']].min(axis=1), df[['open', 'close']].max(axis=1)),
            df['prev_close'].between(df[['open', 'close']].min(axis=1), df[['open', 'close']].max(axis=1)),
            (df['prev_candle_body_length'] / df['candle_body_length']) < 0.95
        ]),
        np.where(df["candle_color"] == 'green', "Bullish Engulfing", "Bearish Engulfing"),
        None
    )
    
    return df

def identify_haramis(df):
    df['harami'] = np.where(
        np.logical_and.reduce([
            df['prev_candle_color'] != df['candle_color'],
            df['prev_candle_body_ratio'] >= 0.5,
            (df['candle_body_length'] / df['prev_candle_body_length']) < 0.5,
            df['open'].between(df[['prev_open', 'prev_close']].min(axis=1), df[['prev_open', 'prev_close']].max(axis=1)),
            df['close'].between(df[['prev_open', 'prev_close']].min(axis=1), df[['prev_open', 'prev_close']].max(axis=1)),
        ]),
        np.where(df['candle_color'] == 'green', "Bullish Harami", "Bearish Harami"),
        None
    )
    return df

def identify_piercing_or_dark_clouds(df):
    df["partial_engulfing"] = np.where(
        np.logical_and.reduce([
            df["close"].between(df[["prev_open", "prev_close"]].min(axis=1), df[["prev_open", "prev_close"]].max(axis=1)),
            df["prev_candle_body_ratio"] >= 0.5,
            df['candle_body_length'] >= df['prev_candle_body_length'] * 0.5,
            df["candle_color"] != df["prev_candle_color"]
        ]),
        np.where(
            (df["candle_color"] == "green") & (df['close'] >= (df['prev_open'] + df['prev_close']) / 2), 
            "Piercing Pattern",
            np.where(
                (df["candle_color"] == "red") & (df['close'] <= (df['prev_open'] + df['prev_close']) / 2),
                "Dark Cloud Cover",
                None
            )
        ),
        None
    )
    return df