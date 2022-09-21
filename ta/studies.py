import pandas as pd
import numpy as np

def load_volume_sma(df):
    df['vol_sma_10d'] = df.volume.rolling(window=10).mean()
    return df

def load_emas(df):
    ema_spans = [9, 21, 30, 50, 100, 12, 26]
    for i in ema_spans:
        df[f'ema_{i}d'] = df.close.ewm(span=i).mean()
    return df

def load_macd(df):
    df['macd'] = df.ema_12d - df.ema_26d
    df['macd_9d_signal'] = df.macd.ewm(9).mean()
    return df
    
def load_bollinger_bands(df):
    df['sma_20d'] = df.close.rolling(window=20).mean()
    df['bb_upper'] = df.sma_20d + 2 * df.close.rolling(20).std()
    df['bb_lower'] = df.sma_20d - 2 * df.close.rolling(20).std()
    return df

def load_rsi(df):
    df['gain_pts'] = np.where(df["close"].diff() > 0, df["close"].diff(), 0)
    df['loss_pts'] = np.where(df["close"].diff() < 0, df["close"].diff().abs(), 0)
    df['gain_avg'] = df['gain_pts'].ewm(alpha=1/14, adjust=True, min_periods=14).mean()
    df['loss_avg'] = df['loss_pts'].ewm(alpha=1/14, adjust=True, min_periods=14).mean()
    df['rsi'] = 100 - (100 / (1 + df['gain_avg'] / df['loss_avg']))
    return df