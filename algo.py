# Find max possible points within cost budget - classic knapsack recursion
from itertools import combinations
import config


# Todo: add comments
# Todo: create test cases
# We'll brute-force all combinations of 2 or more constructors, and for each such combo:
# Compute the remaining budget
# Use DP or backtracking to pick the best 5-driver combination that fits in that remaining budget.
def best_team_memoization(c_data, d_data, n, budget=config.budget_limit):
    memo = {}
    best_team = []
    best_points = 0

    constructors = c_data["Constructor"].tolist()

    for constructor_combo in combinations(constructors, 2):

        constructors_cost = sum(c_data.loc[c_data['Constructor'] == c, 'Cost'].values[0] for c in constructor_combo)
        constructors_points = sum(c_data.loc[c_data['Constructor'] == c, 'Points'].values[0] for c in constructor_combo)

        drivers, drivers_points = drivers_memoization(d_data, n, memo, budget - constructors_cost, config.driver_limit, False)
        total_points = constructors_points + drivers_points

        if total_points > best_points:
            best_team = sorted(list(constructor_combo)) + sorted(drivers)
            best_points = total_points

    return best_team, float(best_points)


def drivers_memoization(driver_data, n, memo, budget, limit, chip_used):

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0:
        if limit == 0:
            return [], 0 # valid team of exactly 5 drivers
        else:
            return [], float('-inf') # invalid team (not enough drivers)

    # Optimization: Re-use calculation
    elif (n, budget, limit, chip_used) in memo:
        return memo[(n, budget, limit, chip_used)]

    # Init variables
    index = n - 1
    points = driver_data["Points"].values[index]
    cost = driver_data["Cost"].values[index]
    driver = driver_data["Driver"].values[index]

    # Optimization: Skip if current driver is over budget
    if cost > budget:
        memo[(n, budget, limit, chip_used)] = drivers_memoization(driver_data, index, memo, budget, limit, chip_used)
        return memo[(n, budget, limit, chip_used)]

    # Choice 1 - Include w/o 2x DRS Chip:
    sub_team, sub_points = drivers_memoization(driver_data, index, memo, budget - cost, limit - 1, chip_used)
    include_team = sub_team + [driver]
    include_points = sub_points + points

    # Choice 2 - Include w 2x DRS Chip (only if not used yet):
    if not chip_used:
        chip_sub_team, chip_sub_points = drivers_memoization(driver_data, index, memo, budget - cost, limit - 1, True)
        chip_team = chip_sub_team + [driver + "_DRS"]
        chip_points = chip_sub_points + 2 * points

        if chip_points > include_points:
            include_team, include_points = chip_team, chip_points

    # Choice 3 - Exclude
    exclude_team, exclude_points = drivers_memoization(driver_data, index, memo, budget, limit, chip_used)

    # Eval sub-problem
    if include_points > exclude_points:
        memo[(n, budget, limit, chip_used)] = include_team, include_points
    else:
        memo[(n, budget, limit, chip_used)] = exclude_team, exclude_points

    return memo[(n, budget, limit, chip_used)]
