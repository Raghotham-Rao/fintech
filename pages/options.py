import streamlit as st
from utils.yahoo_data_load import get_current_price
from pages.tabs.options.option_chain import show_option_chain
from pages.tabs.options.open_interest import show_open_interest
from pages.tabs.options.compare_options import show_options_compare_ui
from utils.components import span
from utils.constants import BULL_COLOR, BEAR_COLOR, ARROW_DOWN_SMALL_SVG, ARROW_UP_SMALL_SVG
from utils.options_data import load_option_chain_data


script_names = {
    'FINNIFTY': 'NIFTY_FIN_SERVICE.NS',
    'NIFTY': '^NSEI',
    'BANKNIFTY': '^NSEBANK'
}

symbol = 'NIFTY'

header_cols = st.columns([3, 1])
header_cols[0].header('Options')
symbol = header_cols[1].selectbox("Symbol", ['NIFTY', 'BANKNIFTY', 'FINNIFTY'])

option_chain_tab, oi_tab = st.tabs(['Option Chain', 'Open Interest'])

current_price_data = get_current_price(script_names[symbol], None)
current_price = round(current_price_data["regularMarketPrice"], 2)
change = round(current_price_data['change'], 2)
pct_change = round(current_price_data['change_pct'], 2)
font_color = BEAR_COLOR if change < 0 else BULL_COLOR

option_chain_df = load_option_chain_data(symbol)

with option_chain_tab:
    st.markdown(f'<h6>Underlying: {symbol} @ {span(current_price, color=font_color)}{ARROW_UP_SMALL_SVG if change > 0 else ARROW_DOWN_SMALL_SVG}({span(change, color=font_color)}, {span(str(pct_change) + "%", color=font_color)})</h6>', unsafe_allow_html=True)
    show_option_chain(option_chain_df, current_price)

with oi_tab:
    st.markdown(f'<h6>Underlying: {symbol} @ {span(current_price, color=font_color)}{ARROW_UP_SMALL_SVG if change > 0 else ARROW_DOWN_SMALL_SVG}({span(change, color=font_color)}, {span(str(pct_change) + "%", color=font_color)})</h6>', unsafe_allow_html=True)
    show_open_interest(option_chain_df)