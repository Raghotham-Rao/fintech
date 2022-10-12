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

def load_ATR(df):
    df['true_range'] = np.maximum.reduce([
        df['high'] - df['low'], 
        (df['high'] - df['prev_close']).abs(), 
        (df['low'] - df['prev_close']).abs()
    ])
    df['ATR'] = df['true_range'].ewm(alpha=1/14).mean()
    return df

def load_ADX(df, period):
    df["plus_DM"] = df['high'].diff(1)
    df["minus_DM"] = -df['low'].diff(1)
    df['plus_DX'] = np.where(
        np.logical_and(
            df['plus_DM'] > df["minus_DM"],
            df['plus_DM'] > 0
        ), df["plus_DM"], 0)
    df['minus_DX'] = np.where(
        np.logical_and(
            df['minus_DM'] > df["plus_DM"],
            df['minus_DM'] > 0
        ), df["minus_DM"], 0)
    
    df['smooth_DXp'] = df["plus_DX"].ewm(alpha=1/period).mean()
    df['smooth_DXm'] = df["minus_DX"].ewm(alpha=1/period).mean()
    
    df['plus_DI'] = df["smooth_DXp"] * 100 / df["ATR"]
    df['minus_DI'] = df["smooth_DXm"] * 100 / df['ATR']
    
    df['DX'] = ((df['plus_DI'] - df['minus_DI']).abs() * 100 / (df['plus_DI'] + df['minus_DI'])).abs()
    df['ADX'] = df['DX'].ewm(alpha=1/period).mean()
    
    return df

def load_aroon(df, period):
    """using argmax"""
    df["period"] = period
    df["days_since_period_high"] = df["high"].rolling(window=period).apply(lambda x: period - np.argmax(x) - 1)
    df["days_since_period_low"] = df["low"].rolling(window=period).apply(lambda x: period - np.argmin(x) - 1)
    
    df["aroon_up"] = (period - df["days_since_period_high"]) * 100 / period
    df["aroon_down"] = (period - df["days_since_period_low"]) * 100 / period
    
    return df