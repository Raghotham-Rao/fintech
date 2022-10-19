import streamlit as st
import plotly.graph_objects as go
from utils.load_data import DataLoader
from utils.yahoo_data_load import get_historical_data, get_current_price
from pages.tabs.summary import load_summary_tab_content
from pages.tabs.technicals import load_technicals_tab_content
from pages.tabs.strategies import load_strategies_tab_content
from utils.constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG, ARROW_DOWN_SMALL_SVG, ARROW_UP_SMALL_SVG

def span(content, style_dict: dict=None):
    style_options = ""
    if style_dict is not None:
        style_options = "; ".join([f'{k}: {v}' for k, v in style_dict.items()])

    print(f'<span style="{style_options}">{content}</span>')

    return f'<span style="{style_options}">{content}</span>'


default_title = "Equities"
script_name = None
current_price_data = None

sidenav = st.sidebar

with sidenav:
    with st.form("equity_details"):
        script_name = st.text_input(label="Script Name", placeholder="Enter script name").upper()
        from_date = st.date_input(label="From")
        to_date = st.date_input(label="To")
        st.form_submit_button("Get Data")


col1, col2 = st.columns([3, 1])
col1.title(script_name or default_title)

if script_name:

    data = None
    with st.spinner('Loading Data...'):
        try:
            current_price_data = get_current_price(script_name)
            data = get_historical_data(script_name, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
        except:
            st.text('An Error Occurred! Check inputs.')

    with col2:
        change = round(current_price_data['change'], 2)
        pct_change = round(current_price_data['change_pct'], 2)
        font_color = BEAR_COLOR if change < 0 else BULL_COLOR
        
        st.markdown(
            span(
                f'{round(current_price_data["regularMarketPrice"], 2)}{ARROW_UP_SMALL_SVG if change > 0 else ARROW_DOWN_SMALL_SVG}', 
                {
                    "font-size": "3em",
                    "font_weight": "bolder",
                    "color": font_color,
                    "display": "inline-block",
                    "width": "100%",
                    "text-align": "right"
                }
            ),
            unsafe_allow_html=True
        )

    st.columns([3, 1])[1].markdown(
        span(
            f'{change}&ensp;({pct_change})%', 
            {
                "font-size": "1.15em",
                "color": font_color,
                "display": "inline-block",
                "width": "100%",
                "text-align": "right"
            }
        ),
        unsafe_allow_html=True
    )

    summary_tab, technicals_tab, strategies_tab, others_tab = st.tabs(['Summary', 'Technicals', 'Indicator Performance', 'Others'])

    with summary_tab:
        load_summary_tab_content(data)

    with technicals_tab:
        load_technicals_tab_content(data)

    with strategies_tab:
        load_strategies_tab_content(data)