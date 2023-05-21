import streamlit as st
from utils.constants import BULL_COLOR, BEAR_COLOR, ARROW_DOWN_SMALL_SVG, ARROW_UP_SMALL_SVG
from utils.black_and_scholes import show_premiums
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.components import span
from utils.yahoo_data_load import get_current_price
import plotly.express as px
import io


def download_data(df: pd.DataFrame):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet_1", index=False)
    writer.save()
    output.seek(0)
    return output


script_names = {
    'FINNIFTY': 'NIFTY_FIN_SERVICE.NS',
    'NIFTY': '^NSEI',
    'BANKNIFTY': '^NSEBANK'
}

symbol = 'NIFTY'

header_cols = st.columns([3, 1])
header_cols[0].header('Options')
symbol = header_cols[1].selectbox("Symbol", ['NIFTY', 'BANKNIFTY', 'FINNIFTY'])

st.markdown('---')

current_price_data = get_current_price(script_names[symbol], None)
current_price = round(current_price_data["regularMarketPrice"], 2)
change = round(current_price_data['change'], 2)
pct_change = round(current_price_data['change_pct'], 2)
font_color = BEAR_COLOR if change < 0 else BULL_COLOR

st.markdown(f'<h6>Underlying: {symbol} @ {span(current_price, color=font_color)}{ARROW_UP_SMALL_SVG if change > 0 else ARROW_DOWN_SMALL_SVG}({span(change, color=font_color)}, {span(str(pct_change) + "%", color=font_color)})</h6>', unsafe_allow_html=True)

with st.form("prem_calc_form"):
    sec_1_cols = st.columns(3)
    spot_price = sec_1_cols[0].number_input("Spot Price")
    r = sec_1_cols[1].number_input("Rate", min_value=0.0, max_value=1.0, value=0.05)
    t = sec_1_cols[2].number_input("Days to Expiry")

    st.markdown("---")

    sec_2_cols = st.columns(5)
    strike_price_1 = sec_2_cols[0].number_input("Option 1 Strike Price")
    option_type_1 = sec_2_cols[1].selectbox("Option 1 Type", ["CE", "PE"])
    iv_1 = sec_2_cols[2].number_input("Option 1 I.V", min_value=1.0, max_value=100.0)
    lot_size_1 = int(sec_2_cols[3].number_input("Option 1 Lot Size"))
    lots_1 = int(sec_2_cols[4].number_input("Option 1 Lots"))
    
    st.markdown("---")

    sec_3_cols = st.columns(5)
    strike_price_2 = sec_3_cols[0].number_input("Option 2 Strike Price")
    option_type_2 = sec_3_cols[1].selectbox("Option 2 Type", ["CE", "PE"])
    iv_2 = sec_3_cols[2].number_input("Option 2 I.V", min_value=1.0, max_value=100.0)
    lot_size_2 = int(sec_3_cols[3].number_input("Option 2 Lot Size"))
    lots_2 = int(sec_3_cols[4].number_input("Option 2 Lots"))

    st.markdown("---")

    sec_4_cols = st.columns(3)
    start = sec_4_cols[0].number_input("Start")
    end = sec_4_cols[1].number_input("End")
    step = sec_4_cols[2].number_input("Step")

    st.form_submit_button("Check")

try:
    premiums_1_df = show_premiums(spot_price, strike_price_1, r, iv_1 / 100, t / 365, spot_price, int(start), int(end), int(step), option_type_1)
    premiums_2_df = show_premiums(spot_price, strike_price_2, r, iv_2 / 100, t / 365, spot_price, int(start), int(end), int(step), option_type_2)

    comparision_df = pd.merge(premiums_1_df, premiums_2_df, on='strike', suffixes=['_call', '_put'])
    comparision_df['net_pl'] = comparision_df['pl_call'] + comparision_df['pl_put']
    comparision_df['investment'] = (comparision_df['premium_paid_call'] * lot_size_1 * lots_1) + (comparision_df['premium_paid_put'] * lot_size_2 * lots_2)
    comparision_df['ovl_pl'] = (comparision_df['pl_call'] * lot_size_1 * lots_1) + (comparision_df['pl_put'] * lot_size_2 * lots_2)

    comparision_df = comparision_df.round(2)

    format_text = lambda x: f'<b>{"+" if x >= 0 else ""}{x}</b>'
    font_color_map = np.full(comparision_df.shape, "#000000")
    font_color_map[:, -3] = comparision_df["net_pl"].apply(lambda x: BEAR_COLOR if x < 0 else BULL_COLOR)
    font_color_map[:, -1] = comparision_df["net_pl"].apply(lambda x: BEAR_COLOR if x < 0 else BULL_COLOR)

    comparision_table = go.Figure(
        data=go.Table(
            header=(dict(values=comparision_df.columns, fill=dict(color="#4a148c"), font=dict(color="white"))),
            cells=dict(
                values=[comparision_df[i] if i not in ['net_pl', 'ovl_pl'] else comparision_df[i].apply(format_text) for i in comparision_df.columns], 
                fill=dict(color="white"), 
                line_color="lightgrey",
                font=dict(color=font_color_map.T, size=14)
            )
        )
    )

    comparision_table.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=600)

    st.markdown('---')
    st.plotly_chart(comparision_table, use_container_width=True)
    st.download_button("Download", download_data(comparision_df), file_name="compare_options.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    line_chart_columns = st.columns(2)
    
    line_chart_columns[0].plotly_chart(
        px.line(
            comparision_df, 
            x="strike", 
            y=["premium_call", "premium_put"], 
            title=f"{strike_price_1}-{option_type_1} v/s {strike_price_2}-{option_type_2}"
        ).update_layout(height=500, showlegend=False, title=dict(font=dict(size=20), x=0.115)),
        use_container_width=True
    )

    line_chart_columns[1].plotly_chart(
        px.line(
            comparision_df, 
            x="strike", 
            y="net_pl", 
            title=f"PL chart",
            color_discrete_sequence=['#8bc34a']
        ).update_layout(height=500, title=dict(font=dict(size=20), x=0.115)),
        use_container_width=True,
    )
except Exception as e:
    st.error(e)