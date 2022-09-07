import streamlit as st
from constants import BULL_COLOR, BEAR_COLOR, ARROW_UP_SVG, ARROW_DOWN_SVG
import plotly.graph_objects as go


def load_technicals_tab_content(data):
    st.header('Technicals')

    st.dataframe(data)