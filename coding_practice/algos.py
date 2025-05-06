# Find max possible points within cost budget - classic knapsack recursion
from itertools import combinations
from operator import index
#from main import costs, drivers

def knapsack_recursion(points, cost, budget, n):

    index = n - 1

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0:
        return 0

    # Optimization: Skip if current driver is over budget
    elif cost[index] > budget:
        return knapsack_recursion(points, cost, budget, index)

    # Two choices:
    else:
        include = points[index] + knapsack_recursion(points, cost, budget - cost[index], index)
        exclude = knapsack_recursion(points, cost, budget, index)

        return max(include, exclude)

# Find max possible points within cost budget - knapsack memoization
def knapsack_memoization(points, cost, budget, n, memo=None):

    # Init memoization array
    if memo is None:
        memo = {}

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0:
        return 0

    # Optimization: Re-use stored computation
    elif (n, budget) in memo:
        return memo[(n, budget)]

    # Optimization: Skip if current driver is over budget
    index = n - 1
    if cost[index] > budget:
        return knapsack_memoization(points, cost, budget, index, memo)

    # Two choices:
    else:
        include = points[index] + knapsack_memoization(points, cost, budget - cost[index], index, memo)
        exclude = knapsack_memoization(points, cost, budget, index, memo)

        memo[(n, budget)] = max(include, exclude)

        return memo[(n, budget)]

# Find the best drivers providing the max possible points within cost budget
def knapsack_recursion_drivers(points, cost, drivers, budget, n):

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0:
        return [], 0

    index = n - 1

    # Optimization: Skip if current driver is over budget
    if cost[index] > budget:
        return knapsack_recursion_drivers(points, cost, drivers, budget, index)

    # Two choices:
    sub_team, sub_points = knapsack_recursion_drivers(points, cost, drivers, budget - cost[index], index)
    include_team = sub_team + [drivers[index]]
    include_points = sub_points + points[index]

    exclude_team, exclude_points = knapsack_recursion_drivers(points, cost, drivers, budget, index)

    if include_points > exclude_points:
        return include_team, include_points
    else:
        return exclude_team, exclude_points

# Find the best drivers providing the max possible points within cost budget - memoization
def knapsack_memoization_drivers(points, cost, drivers, budget, n, memo=None):

    # Init memoization array
    if memo is None:
        memo = {}

    # Base case:
    if n == 0 or budget == 0:
        return [], 0

    # Optimization: Re-use stored computation
    elif (n, budget) in memo:
        return memo[(n, budget)]

    index = n-1

    # Optimization: budget exceeded
    if cost[index] > budget:
        return knapsack_memoization_drivers(points, cost, drivers, budget, index, memo)

    # Split two choices:
    include_team, include_points = knapsack_memoization_drivers(points, cost, drivers, budget - cost[index], index, memo)
    include_team = include_team + [drivers[index]]
    include_points += points[index]

    exclude_team, exclude_points = knapsack_memoization_drivers(points, cost, drivers, budget, index, memo)

    if include_points > exclude_points:
        memo[(n, budget)] = include_team, include_points
    else:
        memo[(n, budget)] = exclude_team, exclude_points

    return memo[(n, budget)]

# Find the best drivers providing the max possible points within cost budget and limit
# Todo: learn the extra limiting parameter - draw out tree
def knapsack_memoization_drivers_limit(points, cost, drivers, budget, limit, n, memo=None):

    # Init memo
    if not memo:
        memo = {}

    # Base Case - end of index or at capacity
    if n == 0 or budget == 0 or limit == 0:
        return [], 0

    # Optimization: Re-use calculation
    elif (n, budget) in memo:
        return memo[(n, budget)]

    index = n - 1

    # Optimization: Skip if current driver is over budget
    if cost[index] > budget:
        return knapsack_memoization_drivers_limit(points, cost, drivers, budget, limit, index, memo)

    # Two choices:
    sub_team, sub_points = knapsack_memoization_drivers_limit(points, cost, drivers, budget - cost[index], limit-1, index, memo)
    include_team = sub_team + [drivers[index]]
    include_points = sub_points + points[index]

    exclude_team, exclude_points = knapsack_memoization_drivers_limit(points, cost, drivers, budget, limit, index, memo)

    if include_points > exclude_points:
        memo[(n, budget)] = include_team, include_points
    else:
        memo[(n, budget)] = exclude_team, exclude_points

    return memo[(n, budget)]

def drivers_memoization_limit(driver_data, budget, n, limit=5, memo=None):

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
        return drivers_memoization_limit(driver_data, budget, index, limit, memo)

    # Two choices:
    sub_team, sub_points = drivers_memoization_limit(driver_data, budget - cost, index, limit - 1, memo)
    include_team = sub_team + [driver]
    include_points = sub_points + points

    exclude_team, exclude_points = drivers_memoization_limit(driver_data, budget, index, limit, memo)

    if include_points > exclude_points:
        memo[(n, budget)] = include_team, include_points
    else:
        memo[(n, budget)] = exclude_team, exclude_points

    return memo[(n, budget)]

# Todo: move team limit up or add team limit to config page
# We'll brute-force all combinations of 2 or more constructors, and for each such combo:
# Compute the remaining budget
# Use DP or backtracking to pick the best 5-driver combination that fits in that remaining budget.
def best_team_memoization(c_data, d_data, n, budget=100):

    best_team = []
    best_points = 0

    constructors = c_data["Constructor"].tolist()

    for constructor_combo in combinations(constructors, 2):
        constructors_points = sum(c_data.loc[c_data['Constructor'] == c, 'Points'].values[0] for c in constructor_combo)
        constructors_cost = sum(c_data.loc[c_data['Constructor'] == c, 'Cost'].values[0] for c in constructor_combo)

        remaining_budget = budget - constructors_cost
        if remaining_budget <= 0:
            continue

        drivers, drivers_points = drivers_memoization_limit(d_data, remaining_budget, n)
        total_points = constructors_points + drivers_points

        if total_points > best_points:
            best_team = list(constructor_combo) + drivers
            best_points = total_points

    return best_team, float(best_points)
