import numpy as np
from sklearn.preprocessing import normalize


def perform_ahp(features, total_point=1):
    """
    Calculates the priorities of the given features using the AHP algorithm.

    Args:
        features (list): A list of two lists. The first list contains the feature names
            and the second list contains the feature comparisons in the form of a matrix.
            The matrix should be a lower triangular matrix with diagonal elements equal to 1.
        total_point (float, optional): The total point to be distributed among the features.
            Defaults to 1.

    Returns:
        list: A list containing the feature names and their calculated points.
    """
    # Extract the feature names and the comparison matrix from the input
    feature_names, comparison_matrix = features

    # Calculate the size of the comparison matrix
    n = len(feature_names)

    # Create an n x n ones matrix
    ahp_matrix = np.ones([n, n])

    # Fill the matrix according to AHP calculations
    for i in range(0, n):
        for j in range(i+1, n):
            ahp_matrix[i, j] = comparison_matrix[i][j]
            ahp_matrix[j, i] = 1 / ahp_matrix[i, j]

    # Normalize the matrix along the columns
    normed_matrix = normalize(ahp_matrix, axis=0, norm='l1')

    # Calculate the weights
    weights = normed_matrix.mean(axis=1)

    # Distribute the total point among the features according to the weights
    points = total_point * weights

    # Create a list of feature names and their corresponding points
    feature_points = [[feature_names[i], points[i]] for i in range(n)]

    return feature_points
