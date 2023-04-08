import numpy as np

def calculate_alternative_weight(alternative_i, alternative_j, criteria_weights):
    """
    Calculates the weight of one alternative relative to another alternative
    based on the given criteria weights.
    """
    num_criteria = len(criteria_weights)
    score = 0
    for k in range(num_criteria):
        criterion = list(criteria_weights.keys())[k]
        weight = criteria_weights[criterion]
        if alternative_i[criterion] > alternative_j[criterion]:
            score += weight
        elif alternative_i[criterion] < alternative_j[criterion]:
            score -= weight
    return score

def perform_ahp(df, criteria):
    """
    Performs an AHP analysis on the given DataFrame using the given criteria.
    Returns a list of weights corresponding to each row in the DataFrame.
    """
    num_alternatives = len(df)
    num_criteria = len(criteria)
    
    # normalize the criteria weights
    criteria_weights_sum = sum(criteria.values())
    criteria_weights = {k: v/criteria_weights_sum for k, v in criteria.items()}

    # calculate the alternative weights
    alternative_weights = np.zeros(num_alternatives)
    for i in range(num_alternatives):
        alternative_i = df.iloc[i][list(criteria.keys())]
        alternative_score = 0
        for j in range(num_alternatives):
            if i != j:
                alternative_j = df.iloc[j][list(criteria.keys())]
                alternative_score += calculate_alternative_weight(alternative_i, alternative_j, criteria_weights)
        alternative_weights[i] = alternative_score
        
    # normalize the alternative weights
    alternative_weights_sum = sum(alternative_weights)
    normalized_weights = [w / alternative_weights_sum for w in alternative_weights]
    return normalized_weights