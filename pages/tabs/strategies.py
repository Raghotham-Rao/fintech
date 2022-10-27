import streamlit as st
from utils.load_data import DataLoader, YfinanceDataLoader
from ta.single_candlestick_patterns import *
from ta.multiple_candlestick_patterns import *
from ta.backtests import *
from ta.studies import load_ATR, load_ADX, load_rsi, load_bollinger_bands
from utils.constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG
from functools import reduce


aggregate_dict = reduce(lambda x, a: x | a, [{f"d{i}_return_pct": "mean"} | {f"d{i}_win_flag": "sum"} | {f"d{i}_indicator_conf": "sum"} for i in [2, 3, 5, 8, 13]])

def span(content, style_dict: dict=None):
    style_options = ""
    if style_dict is not None:
        style_options = "; ".join([f'{k}: {v}' for k, v in style_dict.items()])

    print(f'<span style="{style_options}">{content}</span>')

    return f'<span style="{style_options}">{content}</span>'

def load_strategies_tab_content(data):
    data["next_day_open"] = data["open"].shift(-1)
    
    data = load_ADX(load_ATR(data), 14)
    for fn in [preprocess, get_returns, identify_marubozus, identify_engulfing, identify_haramis, 
              identify_paper_umbrellas, identify_piercing_or_dark_clouds, identify_shooting_stars, load_rsi, load_bollinger_bands]:
        data = fn(data)

    data['rsi_bin'] = pd.cut(data['rsi'], bins=[35, 40, 45, 50, 55, 60, 65])

    for indicator_column in ['marubozu', 'engulfing', 'harami', 'partial_engulfing', 'paper_umbrella_type'][:-1]:
        with st.container():
            st.subheader(indicator_column)

            res = show_performance(data.set_index('date'), indicator_column)

            aggregate_df = res.groupby(indicator_column).agg(
                {indicator_column: 'count'} | aggregate_dict
            )

            for i in range(aggregate_df.shape[0]):
                st.markdown(
                    span(aggregate_df.index[i], {"font-size": "1.2em"}),
                    unsafe_allow_html=True
                )
                st.text(f'Occurences: {aggregate_df.iloc[i, 0]}')

                display_table_df = pd.DataFrame(aggregate_df.iloc[i, 1:].to_numpy().reshape((5, 3)), columns=['Average Return percentage', 'No of Wins', 'expected movement'])
                display_table_df['Day'] = [f'Day {i}' for i in [2, 3, 5, 8, 13]]
                
                st.table(display_table_df.set_index('Day').T)

            with st.expander('Show Data'):
                    st.dataframe(res)