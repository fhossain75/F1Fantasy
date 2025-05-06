# Find max possible points within cost budget - classic knapsack recursion
from itertools import combinations
import config

# Todo: move team limit up or add team limit to config page
# Todo: add comments
# Todo: create test cases
# We'll brute-force all combinations of 2 or more constructors, and for each such combo:
# Compute the remaining budget
# Use DP or backtracking to pick the best 5-driver combination that fits in that remaining budget.
def best_team_memoization(c_data, d_data, n, budget=config.budget_limit):

    best_team = []
    best_points = 0
    memo = {}

    constructors = c_data["Constructor"].tolist()
    # # Preload constructor info into a dict for fast lookup
    # constructor_dict = {
    #     row['Constructor']: {'points': row['Points'], 'cost': row['Cost']}
    #     for _, row in c_data.iterrows()
    # }
    #
    # constructors = list(constructor_dict.keys())

    for constructor_combo in combinations(constructors, 2):

        constructors_cost = sum(c_data.loc[c_data['Constructor'] == c, 'Cost'].values[0] for c in constructor_combo)
        constructors_points = sum(c_data.loc[c_data['Constructor'] == c, 'Points'].values[0] for c in constructor_combo)

        drivers, drivers_points = drivers_memoization(d_data, n, budget - constructors_cost, memo=memo) #Todo: Reuse memo for optimization?
        total_points = constructors_points + drivers_points

        if total_points > best_points:
            best_team = list(constructor_combo) + drivers
            best_points = total_points

    return best_team, float(best_points)

# todo: require 5 drivers not just limit
def drivers_memoization(driver_data, n, budget=config.budget_limit, limit=config.driver_limit, memo=None):

    # Init memo
    if not memo:
        memo = {}

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0 or limit == 0:
        return [], 0

    # Optimization: Re-use calculation
    elif (n, budget) in memo:
        return memo[(n, budget)]

    # Init variables
    index = n - 1
    points = driver_data["Points"].tolist()[index]
    cost = driver_data["Cost"].tolist()[index]
    driver = driver_data["Driver"].tolist()[index]

    # Optimization: Skip if current driver is over budget
    if cost > budget:
        return drivers_memoization(driver_data, budget, index, limit, memo)

    # Two choices:
    sub_team, sub_points = drivers_memoization(driver_data, budget - cost, index, limit - 1, memo)
    include_team = sub_team + [driver]
    include_points = sub_points + points

    exclude_team, exclude_points = drivers_memoization(driver_data, budget, index, limit, memo)

    if include_points > exclude_points:
        memo[(n, budget)] = include_team, include_points
    else:
        memo[(n, budget)] = exclude_team, exclude_points

    return memo[(n, budget)]


