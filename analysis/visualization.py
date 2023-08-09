"""
A module for visualization in the analysis package.
"""
import itertools
import re
from typing import Any

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import cm
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from core.config import settings
from core.file_manager import DataType


def plot_count(
    dataframe: pd.DataFrame,
    variables: list[Any],
    hue: str,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    This method plots the counts of observations from the given variables
    :param dataframe: dataframe containing info
    :type dataframe: pd.DataFrame
    :param variables: list of columns to plot
    :type variables: list[Any]
    :param hue: Variable to use as filter
    :type hue: str
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    plt.suptitle("Count-plot for Discrete variables")
    plot_iterator: int = 1
    for column in variables:
        plt.subplot(1, 3, plot_iterator)
        sns.countplot(
            x=dataframe[column], hue=dataframe[hue], palette=settings.PALETTE
        )
        label: str = re.sub(
            pattern=settings.RE_PATTERN, repl=settings.RE_REPL, string=column
        )
        plt.xlabel(label, fontsize=15)
        plt.ylabel("Count", fontsize=15)
        plot_iterator += 1
        plt.savefig(f"{data_type.value}discrete_{column}.png")
        plt.show()


def plot_distribution(
    series: pd.Series, color: str, data_type: DataType = DataType.FIGURES
) -> None:
    """
    This method plots the distribution of the given quantitative
     continuous variable
    :param series: Single column
    :type series: pd.Series
    :param color: color for the distribution
    :type color: str
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    label: str = re.sub(
        pattern=settings.RE_PATTERN,
        repl=settings.RE_REPL,
        string=str(series.name),
    )
    sns.displot(x=series, kde=True, color=color, height=8, aspect=1.875)
    plt.title(f"Distribution Plot for {label}")
    plt.xlabel(label, fontsize=settings.FONT_SIZE)
    plt.ylabel("Frequency", fontsize=settings.FONT_SIZE)
    plt.savefig(f"{data_type.value}{str(series.name)}.png")
    plt.show()


def boxplot_dist(
    dataframe: pd.DataFrame,
    first_variable: str,
    second_variable: str,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    This method plots the distribution of the first variable data
    in regard to the second variable data in a boxplot
    :param dataframe: data to use for plot
    :type dataframe: pd.DataFrame
    :param first_variable: first variable to plot
    :type first_variable: str
    :param second_variable: second variable to plot
    :type second_variable: str
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    x_label: str = re.sub(
        pattern=settings.RE_PATTERN,
        repl=settings.RE_REPL,
        string=first_variable,
    )
    y_label: str = re.sub(
        pattern=settings.RE_PATTERN,
        repl=settings.RE_REPL,
        string=second_variable,
    )
    sns.boxplot(
        x=first_variable,
        y=second_variable,
        data=dataframe,
        palette=settings.PALETTE,
    )
    plt.title(
        x_label + " in regards to " + y_label, fontsize=settings.FONT_SIZE
    )
    plt.xlabel(x_label, fontsize=settings.FONT_SIZE)
    plt.ylabel(y_label, fontsize=settings.FONT_SIZE)
    plt.savefig(
        f"{data_type.value}discrete_{first_variable}_{second_variable}.png"
    )
    plt.show()


def plot_scatter(
    dataframe: pd.DataFrame,
    x_array: str,
    y_array: str,
    hue: str,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    This method plots the relationship between x and y for hue subset
    :param dataframe: dataframe containing the data
    :type dataframe: pd.DataFrame
    :param x_array: x-axis column name from dataframe
    :type x_array: str
    :param y_array: y-axis column name from dataframe
    :type y_array: str
    :param hue: grouping variable to filter plot
    :type hue: str
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    sns.scatterplot(
        x=x_array, data=dataframe, y=y_array, hue=hue, palette=settings.PALETTE
    )
    label: str = re.sub(
        pattern=settings.RE_PATTERN, repl=settings.RE_REPL, string=y_array
    )
    plt.title(f"{x_array} Wise {label} Distribution")
    print(dataframe[[x_array, y_array]].corr())
    plt.savefig(f"{data_type.value}{x_array}_{y_array}_{hue}.png")
    plt.show()


def plot_heatmap(
    dataframe: pd.DataFrame, data_type: DataType = DataType.FIGURES
) -> None:
    """
    Plot heatmap to analyze correlation between features
    :param dataframe: dataframe containing the data
    :type dataframe: pd.DataFrame
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    sns.heatmap(data=dataframe.corr(), annot=True, cmap="RdYlGn")
    plt.title(
        "Heatmap showing correlations among columns",
        fontsize=settings.FONT_SIZE,
    )
    plt.savefig(f"{data_type.value}correlations_heatmap.png")
    plt.show()


def elbow_method(
    matrix: np.ndarray,
    n_clusters_range: range,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    Perform elbow method for KMeans clustering to determine optimal
     number of clusters.
    :param matrix: The feature matrix of the data
    :type matrix: np.ndarray
    :param n_clusters_range: The range of number of clusters to test
    :type n_clusters_range: range
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    within_cluster_sum_square: list[float] = []
    for i in n_clusters_range:
        kmeans: KMeans = KMeans(n_clusters=i, n_init=10)
        kmeans.fit(matrix)
        within_cluster_sum_square.append(kmeans.inertia_)
    plt.plot(n_clusters_range, within_cluster_sum_square)
    plt.title("Elbow Method")
    plt.xlabel("Number of clusters")
    plt.ylabel("Within-cluster sum of squares (WCSS)")
    plt.savefig(f"{data_type.value}elbow.png")
    plt.show()
    print(within_cluster_sum_square)


def visualize_clusters(
    matrix: np.ndarray,
    labels: np.ndarray,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    Visualize clusters and display cluster characteristics.
    :param matrix: The feature matrix of the data.
    :type matrix: np.ndarray
    :param labels: The cluster labels assigned by the KMeans algorithm.
    :type labels: np.ndarray
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    plt.scatter(matrix[:, 0], matrix[:, 1], c=labels, cmap="rainbow")
    plt.title("Clusters")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    # legend_handles = [
    #     plt.Line2D([], [], color=cm.get_cmap("plasma", int(i / 2)),
    #                label=f"Group {i}") for i in range(2)]
    # plt.legend(handles=legend_handles)
    plt.savefig(f"{data_type.value}clusters.png")
    plt.show()
    for i in range(np.unique(labels).shape[0]):
        cluster = matrix[labels == i]
        print("Cluster", i, ":")
        print("Number of samples:", cluster.shape[0])
        print("Mean:", np.mean(cluster, axis=0))
        print("Median:", np.median(cluster, axis=0))
        print("Standard deviation:", np.std(cluster, axis=0))
        print("\n")
    unique_labels = np.unique(labels)
    if -1 in unique_labels:
        outliers = matrix[labels == -1]
        print("Outliers:")
        print(outliers)


def plot_confusion_matrix(
    conf_matrix: np.ndarray,
    classes: list[str],
    name: str,
    normalize: bool = False,
    data_type: DataType = DataType.FIGURES,
) -> None:
    """
    This function plots the Confusion Matrix of the test and pred arrays
    :param conf_matrix:
    :type conf_matrix: np.ndarray
    :param classes: List of class names
    :type classes: list[str]
    :param name: Name of the model
    :type name: str
    :param normalize: Whether to normalize the confusion matrix or not.
     The default is False
    :type normalize: bool
    :param data_type: folder where data will be saved. Defaults to FIGURES
    :type data_type: DataType
    :return: None
    :rtype: NoneType
    """
    if normalize:
        conf_matrix = (
            conf_matrix.astype("float") / conf_matrix.sum(axis=1)[:, np.newaxis]
        )
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")
    print(conf_matrix)
    plt.figure(figsize=settings.FIG_SIZE)
    plt.rcParams.update({"font.size": 16})
    plt.imshow(
        conf_matrix, interpolation="nearest", cmap=cm.get_cmap("viridis", 8)
    )
    plt.title("Confusion matrix")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, color="blue")
    plt.yticks(tick_marks, classes, color="blue")
    fmt: str = ".2f" if normalize else "d"
    thresh: float = conf_matrix.max(initial=0) / 2.0
    for i, j in itertools.product(
        range(conf_matrix.shape[0]), range(conf_matrix.shape[1])
    ):
        plt.text(
            j,
            i,
            format(conf_matrix[i, j], fmt),
            horizontalalignment="center",
            color="red" if conf_matrix[i, j] > thresh else "black",
        )
    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.savefig(f"{data_type.value}{name}_confusion_matrix.png")
    plt.show()
