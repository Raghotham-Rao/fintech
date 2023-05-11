from math import log, sqrt, exp
import math
from scipy.stats import norm 
import pandas as pd
from datetime import datetime

def get_d1(St, K, r, v, t):
    return (log(St / K) + (r + (v ** 2) / 2) * t) / (v * sqrt(t))

def get_d2(St, K, r, v, t):
    return get_d1(St, K, r, v, t) - (v * sqrt(t))

def get_call_option_premium(St, K, r, v, t):
    return round((norm.cdf(get_d1(St, K, r, v, t)) * St) - (norm.cdf(get_d2(St, K, r, v, t)) * K * (exp(- r * t))), 2)

def get_put_option_premium(St, K, r, v, t):
    return round((norm.cdf(-get_d2(St, K, r, v, t)) * K * (exp(- r * t))) - (norm.cdf(-get_d1(St, K, r, v, t)) * St), 2)

def get_delta(St, K, r, v, t, option_type='call'):
    return norm.cdf(get_d1(St, K, r, v, t)) - (0 if option_type == 'call' else 1)

def show_premiums(St, K, r, v, t, initial_spot, spot_low, spot_high, steps, option_type="CE"):
    option_premium_funcs = {
        "CE": get_call_option_premium,
        "PE": get_put_option_premium
    }
    
    premiums = []
    
    for St in range(spot_low, spot_high, steps):
        premiums.append([
            St, 
            option_premium_funcs[option_type](St, K, r, v, t), 
            option_premium_funcs[option_type](initial_spot, K, r, v, t), 
            round(option_premium_funcs[option_type](St, K, r, v, t) - option_premium_funcs[option_type](initial_spot, K, r, v, t), 2)
        ])
    
    return pd.DataFrame(premiums, columns='strike, premium, premium_paid, pl'.split(', '))