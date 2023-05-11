import streamlit as st
from utils.black_and_scholes import show_premiums
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def show_options_compare_ui():
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
        font_color_map[:, -3] = comparision_df["net_pl"].apply(lambda x: 'red' if x < 0 else 'green')
        font_color_map[:, -1] = comparision_df["net_pl"].apply(lambda x: 'red' if x < 0 else 'green')

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

        st.plotly_chart(comparision_table, use_container_width=True)
        # st.dataframe(comparision_df.set_index("strike"))
    except Exception as e:
        st.error(e)
