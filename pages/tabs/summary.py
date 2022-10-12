from enum import auto
from turtle import width
import streamlit as st
from utils.constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG
import plotly.graph_objects as go

def span(content, style_dict: dict=None):
    style_options = ""
    if style_dict is not None:
        style_options = "; ".join([f'{k}: {v}' for k, v in style_dict.items()])

    print(f'<span style="{style_options}">{content}</span>')

    return f'<span style="{style_options}">{content}</span>'


def load_summary_tab_content(data):
    latest_record = data.iloc[-1, :].to_dict()

    change = round(latest_record['close'] - latest_record['prev_close'], 2)
    pct_change = round(change * 100 / latest_record['prev_close'], 2)

    col1, col2 = st.columns(2)
    font_color = BEAR_COLOR if change < 0 else BULL_COLOR

    with col1:
        st.markdown(
            span(
                latest_record["close"], 
                {
                    "font-size": "4em",
                    "font_weight": "bolder",
                    "color": font_color,
                }
            ) + span(
                ARROW_UP_SVG if change > 0 else ARROW_DOWN_SVG,
                {
                    "padding-bottom": "20px"
                }
            ),
            unsafe_allow_html=True
        )
        st.markdown(
            span(
                change, 
                {
                    "font-size": "1.5em",
                    "color": font_color,
                    "margin-right": "2%"
                }
            ) + span(
                f'({pct_change}%)',
                {
                    "font-size": "1.5em",
                    "color": font_color
                }
            ),
            unsafe_allow_html=True
        )

    with col2:
        for i in ["open", "high", "low", "close"]:
            st.text("{0}: {1:0.2f}".format(i.capitalize(), round(latest_record[i], 2)))

    last_90_days_data = data.iloc[-90:, :]

    fig = go.Figure(data=go.Candlestick(x=last_90_days_data['date'],
                            open=last_90_days_data['open'],
                            high=last_90_days_data['high'],
                            low=last_90_days_data['low'],
                            close=last_90_days_data['close'])
                    )

    fig.update_layout(xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, b=0, t=0), autosize=True)
    fig.update_traces(line = dict(width=1))
    fig.update_xaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    expander = st.expander('Show Data')

    with expander:
        st.dataframe(last_90_days_data.set_index('date'))