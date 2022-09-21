from turtle import colormode, fillcolor
import streamlit as st
from constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG
import plotly.graph_objects as go
import ta.single_candlestick_patterns as scp
import ta.multiple_candlestick_patterns as mcp
import ta.studies as stud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_candlestick(data):
    return go.Candlestick(
            x=data['date'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            line=dict(width=1),
            increasing=dict(fillcolor=BULL_COLOR),
            decreasing=dict(fillcolor=BEAR_COLOR)
        )


def load_technicals_tab_content(data):
    data = scp.pre_process(data)

    for fn in [scp.identify_marubozus, scp.identify_dojis, scp.identify_paper_umbrellas, scp.identify_shooting_stars]:
        data = fn(data)

    for fn in [mcp.identify_engulfing, mcp.identify_haramis, mcp.identify_piercing_or_dark_clouds]:
        data = fn(data)

    for study in [stud.load_volume_sma, stud.load_emas, stud.load_macd, stud.load_volume_sma, stud.load_rsi]:
        data = study(data)

    chart_data = data.iloc[-100:, :]
    latest_record = data.iloc[-1, :].to_dict()

    st.subheader('Volume Average')
    st.text(f"Volume Traded: {latest_record['volume']}")
    st.text("% diff with 10 SMA: {0:.2f}%".format((latest_record['volume'] - latest_record['vol_sma_10d']) * 100 / latest_record['vol_sma_10d']))

    fig = make_subplots(2, 1, row_heights=[0.7, 0.3])
    fig.add_trace(
        get_candlestick(chart_data),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=chart_data["date"],
            y=chart_data["volume"],
            opacity=0.8
        ),
        row=2,
        col=1
    )
    fig.add_trace(
        go.Scatter(
            x=chart_data["date"],
            y=chart_data["vol_sma_10d"]
        ),
        row=2,
        col=1
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    fig.update_xaxes(showgrid=False)

    st.plotly_chart(fig)

    st.markdown('---')

    st.subheader('MACD')
    st.text(f"MACD value: {latest_record['macd']}")

    fig = make_subplots(2, 1, row_heights=[0.7, 0.3])

    fig.add_trace(
        get_candlestick(chart_data),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data["date"],
            y=chart_data["macd"],
            opacity=0.8,
            name="macd"
        ),
        row=2,
        col=1
    )
    fig.add_trace(
        go.Scatter(
            x=chart_data["date"],
            y=chart_data["macd_9d_signal"],
            name="9d signal"
        ),
        row=2,
        col=1
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
    fig.update_traces(line = dict(width=1))
    fig.update_xaxes(showgrid=False)

    st.plotly_chart(fig)

    st.markdown('---')

    st.subheader('Moving Averages')
    moving_avg_combs = [(9, 21), (12, 26), (30, 50), (50, 100)]

    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"{i}-{j} Moving Average" for i, j in moving_avg_combs])

    for i, (fast, slow) in enumerate(moving_avg_combs):
        fig.add_trace(
            go.Scatter(
                x=chart_data["date"],
                y=chart_data[f"ema_{fast}d"],
                name=f"ema_{fast}d"
            ),
            row=i // 2 + 1,
            col=i % 2 + 1
        )
        fig.add_trace(
            go.Scatter(
                x=chart_data["date"],
                y=chart_data[f"ema_{slow}d"],
                name=f"ema_{slow}d"
            ),
            row=i // 2 + 1,
            col=i % 2 + 1
        )

    fig.update_layout(height=600, margin=dict(l=0, r=0))        
    st.plotly_chart(fig)

    st.dataframe(data)