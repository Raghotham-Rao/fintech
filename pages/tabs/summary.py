import streamlit as st
from constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG
import plotly.graph_objects as go


def load_summary_tab_content(data):
    latest_record = data.iloc[-1, :].to_dict()

    change = round(latest_record['close'] - latest_record['prev_close'], 2)
    pct_change = round(change * 100 / latest_record['prev_close'], 2)

    col1, col2 = st.columns(2)
    font_color = BEAR_COLOR if change < 0 else BULL_COLOR

    with col1:
        st.markdown(f'<span style="font-size: 4em; font-weight: bolder; color: #{font_color}">{latest_record["close"]}</span><span style="padding-bottom: 20px">{ARROW_UP_SVG if change > 0 else ARROW_DOWN_SVG}</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="font-size: 1.5em; margin-right: 2%; color: #{font_color}">{change}</span> <span style="font-size: 1.5em; color: #{font_color}">({pct_change}%)</span>', unsafe_allow_html=True)

    with col2:
        for i in ["open", "high", "low", "close"]:
            st.text(f"{i.capitalize()}: {latest_record[i]}")

    last_90_days_data = data.iloc[-90:, :]

    fig = go.Figure(data=go.Candlestick(x=last_90_days_data['date'],
                            open=last_90_days_data['open'],
                            high=last_90_days_data['high'],
                            low=last_90_days_data['low'],
                            close=last_90_days_data['close'])
                    )

    fig.update_layout(xaxis_rangeslider_visible=False, title="90 day Movement", margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(line = dict(width=1))
    fig.update_xaxes(showgrid=False)

    st.plotly_chart(fig)

    expander = st.expander('Show Data')

    with expander:
        st.dataframe(last_90_days_data.set_index('date'))