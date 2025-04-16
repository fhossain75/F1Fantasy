# Find max possible points within cost budget - classic knapsack recursion
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

        return max(include, exclude)
