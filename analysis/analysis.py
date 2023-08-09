"""
A module for analysis in the analysis package.
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import silhouette_score

from core.config import settings


def analyze_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Analyze the dataframe and its columns with inference statistics
    :param dataframe: DataFrame to analyze
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    print(dataframe.head())
    print(dataframe.shape)
    print(dataframe.dtypes)
    dataframe.info(memory_usage="deep")
    print(dataframe.memory_usage(deep=True))
    print(dataframe.describe(include="all", datetime_is_numeric=True))
    non_numeric_df = dataframe.select_dtypes(exclude=settings.NUMERICS)
    for column in non_numeric_df.columns:
        print(non_numeric_df[column].value_counts())
        print(non_numeric_df[column].unique())
        print(non_numeric_df[column].value_counts(normalize=True) * 100)


def latent_semantic_analysis(
    dataframe: pd.DataFrame, column: str, stop_words: list[str]
) -> np.ndarray:
    """
    Perform latent semantic analysis on a given dataframe column using
     TruncatedSVD.
    :param dataframe: The input DataFrame.
    :type dataframe: pd.DataFrame
    :param column: The name of the column containing text data.
    :type column: str
    :param stop_words: A list of stop words to be used in
     TfidfVectorizer
    :type stop_words: list[str]
    :return: The reduced matrix after LSA.
    :rtype: np.ndarray
    """
    tfidf_matrix: TfidfVectorizer = TfidfVectorizer(stop_words=stop_words)
    weighted_tfidf_matrix = tfidf_matrix.fit_transform(dataframe[column])
    svd: TruncatedSVD = TruncatedSVD(n_components=100)
    svd.fit(weighted_tfidf_matrix)
    var: np.ndarray = svd.explained_variance_ratio_
    plt.plot(var)
    plt.xlabel("Number of components")
    plt.ylabel("Explained variance ratio")
    plt.show()
    cumulative_explained_variance_ratio = np.cumsum(var)
    n_components = np.argmax(cumulative_explained_variance_ratio >= 0.9) + 1
    print(n_components)
    reduced_matrix: np.ndarray = svd.fit_transform(weighted_tfidf_matrix)
    return reduced_matrix


def latent_dirichlet_allocation(
    dataframe: pd.DataFrame, column: str, stop_words: list[str]
) -> np.ndarray:
    """
    Applies Latent Dirichlet Allocation (LDA) to the text in the
     specified column of the given dataframe
    :param dataframe: A pandas dataframe containing the text data
    :type dataframe: pd.DataFrame
    :param column: The name of the column containing the text data
    :type column: str
    :param stop_words: A list of stop words to be removed from the text
    :type stop_words: list[str]
    :return: A matrix of shape (n_samples, n_components) containing the
     topic weights for each sample
    :rtype: np.ndarray
    """
    token_counts_matrix: CountVectorizer = CountVectorizer(
        stop_words=stop_words, max_df=0.95, min_df=2
    )
    doc_term_matrix: csr_matrix = token_counts_matrix.fit_transform(
        dataframe[column]
    )
    lda_classifier: LatentDirichletAllocation = LatentDirichletAllocation(
        n_components=2, random_state=0
    )
    transformed_matrix: np.ndarray = lda_classifier.fit_transform(
        doc_term_matrix
    )  # x_topics
    return transformed_matrix


def silhouette_scores(matrix: np.ndarray, n_clusters_range: range) -> None:
    """
    Computes the average silhouette score for a range of cluster
     numbers
    :param matrix: The input matrix to cluster.
    :type matrix: np.ndarray
    :param n_clusters_range: The range of cluster numbers to try
    :type n_clusters_range: range
    :return: None
    :rtype: NoneType
    """
    for n_clusters in n_clusters_range:
        kmeans: KMeans = KMeans(n_clusters=n_clusters, n_init=10)
        labels: np.ndarray = kmeans.fit_predict(matrix)
        silhouette_avg: float = silhouette_score(matrix, labels)
        print(
            "For n_clusters =",
            n_clusters,
            "The average silhouette_score is :",
            silhouette_avg,
        )


def kmeans_clustering(x_transformed: np.ndarray, n_clusters: int) -> np.ndarray:
    """
    Applies K-means clustering to the transformed data and returns the
     predicted cluster labels
    :param x_transformed: The transformed data to cluster
    :type x_transformed: np.ndarray
    :param n_clusters: The number of clusters to use in K-means
    :type n_clusters: int
    :return: The predicted cluster labels.
    :rtype: np.ndarray
    """
    k_means: KMeans = KMeans(n_clusters=n_clusters, n_init=10)
    y_pred: np.ndarray = k_means.fit_predict(x_transformed)
    return y_pred
