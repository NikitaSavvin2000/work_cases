import streamlit as st
import pandas as pd
import plotly.express as px

def show_trend_map_page():
    st.markdown("# Тренд-карта 🎈")
    st.sidebar.markdown("# Тренд-карта 🎈")
    # Код для тренд-карты
    df_vis_sem = pd.read_csv(
        r'https://docs.google.com/spreadsheets/d/e/2PACX-1vRuKlvnZ01eveM-x0jRkDYKu8mkqQwPhVIb0V1K8PjBoN3zEgi69QR2JB8PLTSLjE7O4VkFOJNFXjZN/pub?gid=1103843369&single=true&output=csv')

    fig = px.scatter(df_vis_sem, x='x', y='y', color='cluster_name',
                     hover_data=['label', 'word2vec_centrality', 'freq', 'aagr'],
                     opacity=0.8, color_discrete_map={cluster: color for cluster, color in
                                                      zip(df_vis_sem['cluster_name'], df_vis_sem['color'])},
                     hover_name='label')
    fig.update_traces(text=df_vis_sem['label'], mode='markers+text', textposition='top center')
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, title_text="Динамичность")
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, title_text="Значимость")
    fig.update_traces(textfont=dict(size=10, color='white', family='Arial'))
    fig.update_traces(marker=dict(size=10))
    x_min = df_vis_sem['x'].min() - 0.05 * (df_vis_sem['x'].max() - df_vis_sem['x'].min())
    y_min = df_vis_sem['y'].min() - 0.05 * (df_vis_sem['y'].max() - df_vis_sem['y'].min())
    x_max = df_vis_sem['x'].max() + 0.05 * (df_vis_sem['x'].max() - df_vis_sem['x'].min())
    y_max = df_vis_sem['y'].max() + 0.05 * (df_vis_sem['y'].max() - df_vis_sem['y'].min())
    fig.update_layout(xaxis=dict(range=[x_min, x_max]), yaxis=dict(range=[y_min, y_max]))
    fig.update_layout(showlegend=True)

    # Добавляем вертикальную линию по середине оси X
    fig.add_shape(type="line",
                  x0=(x_max + x_min) / 2, y0=y_min,
                  x1=(x_max + x_min) / 2, y1=y_max,
                  line=dict(color="white", width=0.5))

    # Добавляем горизонтальную линию по середине оси Y
    fig.add_shape(type="line",
                  x0=x_min, y0=(y_max + y_min) / 2,
                  x1=x_max, y1=(y_max + y_min) / 2,
                  line=dict(color="white", width=0.5))

    fig.update_layout(annotations=[
        dict(xref='paper', yref='paper', x=0.02, y=0.98,
             text='Стабильные направления', showarrow=False, font=dict(color='white')),
        dict(xref='paper', yref='paper', x=0.98, y=0.98,
             text='Растущие направления', showarrow=False, font=dict(color='white')),
        dict(xref='paper', yref='paper', x=0.02, y=0.02,
             text='Возникающие тренды', showarrow=False, font=dict(color='white')),
        dict(xref='paper', yref='paper', x=0.98, y=0.02,
             text='Слабые сигналы', showarrow=False, font=dict(color='white'))
    ])
    # Отображаем основной график
    st.plotly_chart(fig, use_container_width=True)

    # Создаем отдельные графики для каждого квартала и добавляем логику для чекбокса "Скрыть названия точек"
    for quarter, data in df_vis_sem.groupby('quarter'):
        quarter_fig = px.scatter(data, x='x', y='y', color='cluster_name',
                                 hover_data=['label', 'word2vec_centrality', 'freq', 'aagr'], opacity=0.8,
                                 color_discrete_map={cluster: color for cluster, color in
                                                      zip(data['cluster_name'], data['color'])},
                                 hover_name='label')
        quarter_fig.update_traces(text=data['label'], mode='markers+text', textposition='top center')
        quarter_fig.update_traces(marker=dict(size=10))

        # Установка фиксированного диапазона для осей x и y
        x_min_quarter = data['x'].min() - 0.05 * (data['x'].max() - data['x'].min())
        y_min_quarter = data['y'].min() - 0.05 * (data['y'].max() - data['y'].min())
        x_max_quarter = data['x'].max() + 0.05 * (data['x'].max() - data['x'].min())
        y_max_quarter = data['y'].max() + 0.05 * (data['y'].max() - data['y'].min())
        quarter_fig.update_layout(xaxis=dict(range=[x_min_quarter, x_max_quarter]),
                                  yaxis=dict(range=[y_min_quarter, y_max_quarter]),
                                  xaxis_title=None, yaxis_title=None)

        quarter_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, title_text=None)
        quarter_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, title_text=None)

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

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    show_trend_map_page()
