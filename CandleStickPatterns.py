import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def marubozu(data):
    return pd.Series(np.where(np.logical_and(data['candle_body_ratio'] > 87.5, data['day_change_perc'] > 1.25), 
                                      data['candle_color'], "")).replace({'Red' : 'Bearish', 'Green' : 'Bullish'}).tolist()

def spinning_top_doji(data):
    wick_conditions = np.logical_and((data['upper_wick_length'] / 
                                      data['candle_length']).between(.25, .75), 
                                     (data['lower_wick_length'] / data['candle_length']).between(.25, .75)
                                )
    body_condition = np.where(data['candle_body_ratio'] <= 17.5, "Doji", 
                              np.where(data['candle_body_ratio'] <= 32.5, "Spinning Top", None)
                            )
    return np.where(np.logical_and(body_condition, wick_conditions), body_condition, "").tolist()

def paper_umbrella(data):
    return np.where(np.logical_and.reduce([(data['candle_body_ratio'] <= 37.5),
                                          (data['lower_wick_length'] / data['candle_length'] >= .60),
                                          (data['upper_wick_length'] / data['candle_length'] <= .125)]
                                         ), True, False).tolist()

def shooting_star(data):
    return np.where(np.logical_and.reduce([(data['candle_body_ratio'] <= 37.5),
                                          (data['upper_wick_length'] / data['candle_length'] >= .60),
                                          (data['lower_wick_length'] / data['candle_length'] <= .125)]
                                         ), True, False).tolist()

def engulfing(data):
    data['current_prev_cbr_ratio'] = data['candle_body_length'] / data['prev_candle_body_length']
    data['prev_current_cbr_ratio'] = data['prev_candle_body_length'] / data['candle_body_length']
    return np.where(np.logical_and.reduce([data['prev_candle_body_ratio'] >= 15, 
                                           data['prev_candle_color'] != data['candle_color'],
                                           data['prev_open'].between(data['body_min'], data['body_max']), 
                                           data['prev_close'].between(data['body_min'], data['body_max']), 
                                           data['prev_current_cbr_ratio'] < .95]),
                          data['candle_color'].replace({"Green" : 'Bullish Engulfing',
                                                       "Red" : 'Bearish Engulfing'}), "").tolist()

def harami(data):
    data['current_prev_cbr_ratio'] = data['candle_body_length'] / data['prev_candle_body_length']
    
    return np.where(np.logical_and.reduce([data['candle_body_ratio'] >= 15, 
                                           data['prev_candle_color'] != data['candle_color'],
                                           data['open'].between(data['prev_body_min'], data['prev_body_max']), 
                                           data['close'].between(data['prev_body_min'], data['prev_body_max']),
                                           data['current_prev_cbr_ratio'] < .95]),
                                          
                          data['candle_color'].replace({"Green" : 'Bullish Harami',
                                                       "Red" : 'Bearish Harami'}), "").tolist()
def partial_engulf(data):
    return np.where(np.logical_and.reduce([data['prev_candle_body_ratio'] >= 50, 
                 data['candle_color'] != data['prev_candle_color'], 
                 data['close'].between(data['prev_body_min'], data['prev_body_max']),
                 (data[['body_max', 'prev_body_max']].min(axis = 1) - data[['body_min', 'prev_body_min']].max(axis = 1)) / data['prev_candle_body_length'] >= 0.5]),
            data['candle_color'].replace({'Red' : 'Dark Cloud', 'Green' : 'Piercing'}), "")

def gap_opening(data):
    return np.where(data['prev_body_max'] < data['open'], "Gap Up", np.where(data['open'] < data['prev_body_min'], "Gap Down", ""))

def star(data):
    p1_day = data[['candle_color', 'day_change_perc']].shift(2)
    p2_day = data[['gap_open', 'spinning_top']].shift(1)
    p3_day = data[['gap_open','day_change_perc', 'candle_color']]
    return np.where(np.logical_and.reduce([p1_day['candle_color'] != p3_day['candle_color'], 
                           p2_day['gap_open'] != "", p2_day['spinning_top'] != "", 
                           p1_day['day_change_perc'] >= 0.5, p3_day['day_change_perc'] >= 0.5]), 
             p3_day['candle_color'].replace({'Red' : 'Evening Star', 'Green' : 'Morning Star'}), "")