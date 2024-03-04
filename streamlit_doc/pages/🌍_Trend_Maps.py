import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Тренд-карта", page_icon="📊", layout="wide")



st.markdown("# Тренд-карта")
st.sidebar.header("Тренд-карта")
df_vis_sem = pd.read_csv(
    r'https://docs.google.com/spreadsheets/d/e/2PACX-1vRuKlvnZ01eveM-x0jRkDYKu8mkqQwPhVIb0V1K8PjBoN3zEgi69QR2JB8PLTSLjE7O4VkFOJNFXjZN/pub?gid=1103843369&single=true&output=csv')

min_val = df_vis_sem['word2vec_centrality'].min()
max_val = df_vis_sem['word2vec_centrality'].max()

desired_min = 0.1
desired_max = 10

df_vis_sem['size'] = ((df_vis_sem['word2vec_centrality'] - min_val) / (max_val - min_val)) * (desired_max - desired_min) + desired_min
textfont_min = 5
textfont_max = 15
df_vis_sem['textsize'] = ((df_vis_sem['word2vec_centrality'] - min_val) / (max_val - min_val)) * (textfont_max - textfont_min) + textfont_min


fig = px.scatter(df_vis_sem,
                 x='aagr_rank',
                 y='freq_rank',
                 color='cluster_name',
                 hover_data=['label', 'word2vec_centrality', 'freq', 'aagr', 'quarter'],
                 size='size',
                 size_max=15,
                 color_discrete_map={cluster: color for cluster, color in zip(df_vis_sem['cluster_name'], df_vis_sem['color'])},
                 hover_name='label',
                 text='label',
                 custom_data=['textsize']
                 )


textfont_list = df_vis_sem['textsize'].tolist()
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, title_text="Динамичность")
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, title_text="Значимость")


x_min = df_vis_sem['aagr_rank'].min() - 0.1 * (df_vis_sem['aagr_rank'].max() - df_vis_sem['aagr_rank'].min())
y_min = df_vis_sem['freq_rank'].min() - 0.1 * (df_vis_sem['freq_rank'].max() - df_vis_sem['freq_rank'].min())
x_max = df_vis_sem['aagr_rank'].max() + 0.1 * (df_vis_sem['aagr_rank'].max() - df_vis_sem['aagr_rank'].min())
y_max = df_vis_sem['freq_rank'].max() + 0.1 * (df_vis_sem['freq_rank'].max() - df_vis_sem['freq_rank'].min())
fig.update_layout(xaxis=dict(range=[x_min, x_max]), yaxis=dict(range=[y_min, y_max]))
fig.update_layout(showlegend=True)

x_median = df_vis_sem['x_median_by_area'].max()
y_median = df_vis_sem['y_median_by_area'].max()

fig.add_shape(type="line",
              x0=x_median, y0=y_min,
              x1=x_median, y1=y_max,
              line=dict(color="white", width=0.5))

fig.add_shape(type="line",
              x0=x_min, y0=y_median,
              x1=x_max, y1=y_median,
              line=dict(color="white", width=0.5))

fig.update_layout(annotations=[
    dict(xref='paper', yref='paper', x=0.01, y=0.99,
         text='Стабильные направления', showarrow=False, font=dict(color='white')),
    dict(xref='paper', yref='paper', x=0.99, y=0.99,
         text='Растущие направления', showarrow=False, font=dict(color='white')),
    dict(xref='paper', yref='paper', x=0.01, y=0.01,
         text='Слабые сигналы',  showarrow=False, font=dict(color='white')),
    dict(xref='paper', yref='paper', x=0.99, y=0.01,
         text='Возникающие тренды', showarrow=False, font=dict(color='white'))
])


show_labels_main = st.checkbox('Скрыть названия точек')

if show_labels_main:
    fig.update_traces(textfont=dict(color='rgba(0,0,0,0)'))

fig.update_layout(height=int(700))
fig.update_layout(width=int(1600))

st.plotly_chart(fig, use_container_width=True)

for quarter, data in df_vis_sem.groupby('quarter'):
    quarter_fig = px.scatter(
                     data,
                     x='aagr_rank',
                     y='freq_rank',
                     color='cluster_name',
                     hover_data=['label', 'word2vec_centrality', 'freq', 'aagr', 'quarter'],
                     opacity=0.8,
                     color_discrete_map={cluster: color for cluster, color in
                                         zip(df_vis_sem['cluster_name'], df_vis_sem['color'])},
                     hover_name='label',
                     text='label',
                     size='size'
                    )

    x_min_quarter = data['aagr_rank'].min() - 0.1 * (data['aagr_rank'].max() - data['aagr_rank'].min())
    y_min_quarter = data['freq_rank'].min() - 0.1 * (data['freq_rank'].max() - data['freq_rank'].min())
    x_max_quarter = data['aagr_rank'].max() + 0.1 * (data['aagr_rank'].max() - data['aagr_rank'].min())
    y_max_quarter = data['freq_rank'].max() + 0.1 * (data['freq_rank'].max() - data['freq_rank'].min())
    quarter_fig.update_layout(xaxis=dict(range=[x_min_quarter, x_max_quarter]),
                              yaxis=dict(range=[y_min_quarter, y_max_quarter]),
                              xaxis_title=None, yaxis_title=None)

    quarter_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, title_text=None)
    quarter_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, title_text=None)

    show_labels_quarter = st.checkbox(f'Скрыть названия точек для {quarter}')

    if show_labels_quarter:
        quarter_fig.update_traces(textfont=dict(color='rgba(0,0,0,0)'))

    st.write(f"## {quarter}")
    st.plotly_chart(quarter_fig, use_container_width=True)

# Отображаем данные в виде таблицы Excel
df_for_dash = df_vis_sem[['term', 'word2vec_aggregate_centrality',
       'word2vec_centrality', 'word2vec_in_cluster_centrality',
       'area', 'label', 'freq', 'rel_freq', 'axis_year', 'aagr',
       'acceleration', 'acceleration_direction', 'freq_rank', 'aagr_rank',
       'agg_rank', 'cluster_name', 'x_median_by_area', 'y_median_by_area',
       'quarter']]

st.write(df_for_dash)
