import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px

from input import input_csv, choose_significant_terms, input_num_points, min_score, input_date_range, select_language, count_words_in_term


st.set_page_config(page_title="Семантическая-карта", page_icon="📊", layout="wide")

import streamlit as st
import pandas as pd



st.markdown("# Семантическая-карта")
st.sidebar.header("Семантическая-карта")

# df = input_csv()

# selected_option = choose_significant_terms()

num_points = input_num_points()
num_points = min_score()
start_date, end_date = input_date_range()
language = select_language()
ngram_size = count_words_in_term()
df_vis_sem = pd.read_csv(
    r'https://docs.google.com/spreadsheets/d/e/2PACX-1vRuKlvnZ01eveM-x0jRkDYKu8mkqQwPhVIb0V1K8PjBoN3zEgi69QR2JB8PLTSLjE7O4VkFOJNFXjZN/pub?gid=1103843369&single=true&output=csv')

st.write(df_vis_sem)
