import numpy as np

def perform_ahp(data, weights):
    """
    Perform the Analytic Hierarchy Process (AHP) on a dataset given a set of weights for each column.

    Parameters:
    data (pandas DataFrame): The dataset on which AHP is to be performed.
    weights (list): The weight for each column in the dataset.

    Returns:
    numpy array: The calculated AHP ranking of the rows in the dataset.
    """
    n = len(weights)
    # Create a pairwise comparison matrix with default values of 1
    comparison_matrix = np.ones((n, n))
    # Set diagonal values to 1 as they represent comparison with self
    np.fill_diagonal(comparison_matrix, 1)

    # Calculate comparison values for upper diagonal matrix elements
    for i in range(n):
        for j in range(i+1, n):
            comparison_matrix[i][j] = data.iloc[:, i].corr(data.iloc[:, j])

    # Calculate the sum of weights for each column
    col_sum = np.sum(comparison_matrix, axis=0)

    # Normalize the comparison matrix
    comparison_matrix = np.divide(comparison_matrix, col_sum)

    # Calculate the weighted sum of each row
    weighted_sum = np.dot(data.values, weights)

    # Calculate the AHP ranking of each row
    ahp_ranking = np.dot(comparison_matrix, weights)
    return ahp_ranking
