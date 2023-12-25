from typing import Any, Callable, List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from ripser import ripser
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import pairwise_distances_argmin_min
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm


def str_vector_to_list(df_vectors: pd.DataFrame) -> pd.DataFrame:
    for idx, row in tqdm(df_vectors.iterrows(), total=len(df_vectors)):
        df_vectors.at[idx, 'vector'] = [
            float(value) for value in row['vector'].split()]
    return df_vectors


def perform_agglomerative_clustering(df: pd.DataFrame, n_clusters: int = 3,
                                     affinity: str = 'euclidean', linkage: str = 'ward') -> pd.DataFrame:
    """
    Performs agglomerative clustering based on vectors in the DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame with 'term' and 'vector' columns.
    - n_clusters (int): Number of clusters (default is 3).
    - affinity (str): Distance metric (default is 'euclidean').
    - linkage (str): Cluster linkage method (default is 'ward').

    Returns:
    - pd.DataFrame: Original DataFrame with an added 'cluster' column containing cluster labels.
    """
    vectors_term_list = df['vector'].tolist()
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, affinity=affinity, linkage=linkage)
    df['cluster'] = clustering.fit_predict(vectors_term_list)
    return df


def perform_agglomerative_clustering(df: pd.DataFrame,
                                     n_clusters: Union[int, None] = None,
                                     affinity: str = 'euclidean',
                                     linkage: str = 'ward',
                                     distance_threshold: Union[float,
                                                               None] = None,
                                     compute_full_tree: Union[str,
                                                              bool] = 'auto',
                                     connectivity: Union[List[List[int]],
                                                         Callable, None] = None,
                                     memory: Union[str, Any] = None,
                                     compute_distances: bool = False) -> pd.DataFrame:
    X = df['vector'].tolist()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    if n_clusters is None and distance_threshold is None:
        distance_threshold = 0.5
    clustering = AgglomerativeClustering(n_clusters=n_clusters,
                                         affinity=affinity,
                                         linkage=linkage,
                                         distance_threshold=distance_threshold,
                                         compute_full_tree=compute_full_tree,
                                         connectivity=connectivity,
                                         memory=memory,
                                         compute_distances=compute_distances)
    df['cluster'] = clustering.fit_predict(X_scaled)
    return df


def recommend_clusters(df, height=0.1, threshold=None, distance=None, prominence=0.4, width=None, plateau_size=None):
    X = np.array(df["vector"].tolist())
    distance_matrix = pairwise_distances(X)
    result = ripser(distance_matrix)
    diagram = result['dgms'][1]
    interval_lengths = np.array([point[1] - point[0] for point in diagram])
    peaks, _ = find_peaks(interval_lengths, height=height, threshold=threshold,
                          distance=distance, prominence=prominence,
                          width=width, plateau_size=plateau_size)

    num_clusters = len(peaks)
    print(f"Рекомендованное количество кластеров: {num_clusters}")
    return num_clusters


def clusterize_terms_DBSCAN(df, eps=0.5, min_samples=2):
    tfidf_vectorizer = TfidfVectorizer()
    df["vector_str"] = df["vector"].apply(lambda vec: ' '.join(map(str, vec)))
    X = tfidf_vectorizer.fit_transform(df["vector_str"])
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df["cluster"] = dbscan.fit_predict(X)
    df["representative_term"] = df["cluster"].apply(
        lambda cluster: pairwise_distances_argmin_min(X[cluster], X[cluster])[0][0])
    return df


def clusterize_terms_KMeans(df):
    X = np.array(df["vector"].tolist())
    num_clusters_range = range(1, 50)
    inertia = []
    for num_clusters in num_clusters_range:
        kmeans = KMeans(n_clusters=num_clusters, random_state=10)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    plt.plot(num_clusters_range, inertia, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.show()
    optimal_num_clusters = num_clusters_range[2]
    kmeans = KMeans(n_clusters=optimal_num_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    df["representative_term"] = df["cluster"].apply(
        lambda cluster: pairwise_distances_argmin_min(X[df["cluster"] == cluster], X[df["cluster"] == cluster])[0][0])
    return df


def hierarchical_clustering(df):
    X = np.array(df["vector"].tolist())
    linkage_matrix = linkage(X, method='ward', metric='euclidean')
    dendrogram(linkage_matrix, no_labels=True)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    plt.show()
    num_clusters = 10
    df["cluster"] = fcluster(
        linkage_matrix, num_clusters, criterion='maxclust')
    return df


def perform_agglomerative_clustering_seaborn(df: pd.DataFrame,
                                             n_clusters: int = 10,
                                             affinity: str = 'euclidean',
                                             linkage_method: str = 'ward',
                                             distance_threshold: Union[float, None] = None) -> pd.DataFrame:
    X = df['vector'].tolist()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clustering = AgglomerativeClustering(n_clusters=n_clusters,
                                         affinity=affinity,
                                         linkage=linkage_method,
                                         distance_threshold=distance_threshold)
    df['cluster'] = clustering.fit_predict(X_scaled)
    cmap = 'coolwarm'
    metric_option = 'euclidean'
    linkage_options = ['ward', 'complete', 'average', 'single']
    for linkage_option in linkage_options:
        sns.clustermap(X_scaled, method=linkage_option, metric=metric_option, row_cluster=False, col_cluster=True,
                       cmap=cmap)
        plt.title(
            f'Hierarchical Clustering Dendrogram (method={linkage_option}, cmap={cmap})')
        plt.show()

    return df

import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram


def perform_agglomerative_clustering_dendrogram(df: pd.DataFrame,
                                                n_clusters: int = 10,
                                                affinity: str = 'euclidean',
                                                linkage_method: str = 'ward') -> pd.DataFrame:
    X = df['vector'].tolist()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clustering = AgglomerativeClustering(n_clusters=n_clusters,
                                         affinity=affinity,
                                         linkage=linkage_method)
    df['cluster'] = clustering.fit_predict(X_scaled)

    # Create linkage matrix and then plot the dendrogram
    counts = np.zeros(clustering.children_.shape[0])
    n_samples = len(clustering.labels_)
    for i, merge in enumerate(clustering.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [clustering.children_, clustering.distances_, counts]
    ).astype(float)

    # Plot the dendrogram
    plt.figure(figsize=(12, 6))
    plt.title("Hierarchical Clustering Dendrogram")
    dendrogram(linkage_matrix, truncate_mode="level", p=3)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.show()

    cmap = 'coolwarm'
    metric_option = 'euclidean'
    linkage_options = ['ward', 'complete', 'average', 'single']
    for linkage_option in linkage_options:
        sns.clustermap(X_scaled, method=linkage_option, metric=metric_option, row_cluster=False, col_cluster=True,
                       cmap=cmap)
        plt.title(
            f'Hierarchical Clustering Dendrogram (method={linkage_option}, cmap={cmap})')
        plt.show()

    return df
