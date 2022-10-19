import streamlit as st
from utils.load_data import DataLoader, YfinanceDataLoader
from ta.single_candlestick_patterns import *
from ta.multiple_candlestick_patterns import *
from ta.backtests import *
from ta.studies import load_ATR, load_ADX
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
        identify_paper_umbrellas, identify_piercing_or_dark_clouds, identify_shooting_stars]:
        data = fn(data)

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
    

# if script_name:

#     data = None
#     with st.spinner('Loading Data...'):
#         try:
#             current_price = YfinanceDataLoader.get_current_data(f"{script_name}.ns").iloc[-1, :].to_dict()
#             prev_day_price = YfinanceDataLoader.get_prev_day_data(f"{script_name}.ns").iloc[-2, :].to_dict()

#             change = round(current_price['Close'] - prev_day_price['Close'], 2)
#             pct_change = round(change * 100 / prev_day_price['Close'], 2)

#             font_color = BEAR_COLOR if change < 0 else BULL_COLOR

#             hc1, hc2 = st.columns([2.5, 1])

#             hc1.markdown(
#                 span(
#                     script_name, 
#                     {
#                         "font-size": "3em",
#                         "font_weight": "bolder"
#                     }
#                 ),
#                 unsafe_allow_html=True
#             )

#             hc2.markdown(
#                 span(
#                     f" {round(current_price['Close'], 2)}", 
#                     {
#                         "font-size": "3em",
#                         "font_weight": "bolder",
#                         "color": font_color
#                     }
#                 ) + 
#                 span(
#                     ARROW_UP_SVG if change > 0 else ARROW_DOWN_SVG,
#                     {
#                         "padding-bottom": "20px"
#                     }
#                 ),
#                 unsafe_allow_html=True
#             )

#             hc2.markdown(
#                 span(
#                     change, 
#                     {
#                         "font-size": "1.5em",
#                         "color": font_color,
#                         "margin-right": "2%"
#                     }
#                 ) + span(
#                     f'({pct_change}%)',
#                     {
#                         "font-size": "1.5em",
#                         "color": font_color
#                     }
#                 ),
#                 unsafe_allow_html=True
#             )

#             data = DataLoader. \
#                 load_data(script_name, from_date.strftime("%d-%m-%Y"), to_date.strftime("%d-%m-%Y"), "EQ").\
#                 sort_values('date').drop_duplicates()

#             high_52w, low_52w = data.iloc[-1, -2:].to_dict().values()

#             hc1.markdown(
#                 span(
#                     f'52w high: {round(high_52w, 2)}',
#                     {"font-size": "1em"}
#                 ) +
#                 span(
#                     f'&emsp;&emsp;&emsp; 52w low: {round(low_52w, 2)}',
#                     {"font-size": "1em"}
#                 ),
#                 unsafe_allow_html=True
#             )
            
#             data["next_day_open"] = data["open"].shift(-1)
#             data = load_ADX(load_ATR(data), 14)
#             for fn in [preprocess, get_returns, identify_marubozus, identify_engulfing, identify_haramis, 
#               identify_paper_umbrellas, identify_piercing_or_dark_clouds, identify_shooting_stars]:
#                 data = fn(data)

#             # c1, c2 = st.columns([3, 1])
#             # indicator_column = c2.selectbox(label="Indicator", options=["Marubozu", "Harami", "Engulfing", "Partial Engulfing", "Paper Umbrella"]).lower()

#             for indicator_column in ['marubozu', 'engulfing', 'harami', 'partial_engulfing', 'paper_umbrella_type'][:-1]:
#                 with st.container():
#                     st.subheader(indicator_column)

#                     res = show_performance(data.set_index('date'), indicator_column)

#                     aggregate_df = res.groupby(indicator_column).agg(
#                         {indicator_column: 'count'} | aggregate_dict
#                     )

#                     for i in range(aggregate_df.shape[0]):
#                         st.markdown(
#                             span(aggregate_df.index[i], {"font-size": "1.2em"}),
#                             unsafe_allow_html=True
#                         )
#                         st.text(f'Occurences: {aggregate_df.iloc[i, 0]}')
#                         display_table_df = pd.DataFrame(aggregate_df.iloc[i, 1:].to_numpy().reshape((5, 3)), columns=['Average Return percentage', 'No of Wins', 'expected movement'])
#                         display_table_df['Day'] = [f'Day {i}' for i in [2, 3, 5, 8, 13]]
                        
#                         st.table(display_table_df.set_index('Day').T)

#                     with st.expander('Show Data'):
#                             res
                        
            
#         except Exception as e:
#             st.text('An Error Occurred! Check inputs.' + str(e))
#             st.error(e)
#             raise(e)