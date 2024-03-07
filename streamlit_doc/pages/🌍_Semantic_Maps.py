from importlib.resources._common import _

import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px




st.set_page_config(page_title="Семантическая-карта", page_icon="📊", layout="wide")
try:
    finish_calculate = st.session_state.finish_calculate
    if finish_calculate == False:
        st.write('📈 Строим карты... 📉')
        st.spinner('📈 Строим карты... 📉')
    elif finish_calculate == True:
        try:
            trend_map_df = st.session_state.trend_map_df
            st.write(trend_map_df)
        except:
            st.write('Что-то пошло не так...')
except:
    st.write('Введите параметры для вашей карты и на странице input params')


def show_sem_map(trend_map_df):
    st.markdown("# Семантическая-карта")
    st.sidebar.header("Семантическая-карта")
    df_vis_sem = trend_map_df
    st.write(df_vis_sem)





