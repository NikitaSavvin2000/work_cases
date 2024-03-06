from importlib.resources._common import _

import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px




st.set_page_config(page_title="Семантическая-карта", page_icon="📊", layout="wide")

trend_map_df_json = st.query_params.trend_map_df

trend_map_df = pd.read_json(trend_map_df_json)

def show_sem_map(trend_map_df):
    st.markdown("# Семантическая-карта")
    st.sidebar.header("Семантическая-карта")
    df_vis_sem = trend_map_df
    st.write(df_vis_sem)

if trend_map_df:
    show_sem_map(trend_map_df)



