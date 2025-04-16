import pandas as pd
import itertools

# -- Load & Pre-process Data
driver_points = pd.read_csv('./data/F1 Fantasy Driver Data - Points.csv')
driver_cost = pd.read_csv('./data/F1 Fantasy Driver Data - Price.csv')
constructor_points = pd.read_csv('./data/F1 Fantasy Constructor Data - Points.csv')
constructor_cost = pd.read_csv('./data/F1 Fantasy Constructor Data - Points.csv')

# Store drivers and constructor names
drivers = driver_points['Driver']
constructors = constructor_points['Constructor']

# Remove irrelevant data
driver_points.drop('AVG', axis=1, inplace=True)
driver_cost.drop('AVG', axis=1, inplace=True)

constructor_points.drop('AVG', axis=1, inplace=True)
constructor_cost.drop('AVG', axis=1, inplace=True)

# Format data from wide to long
driver_points_long = driver_points.melt(id_vars='Driver', var_name='Race', value_name='Points')
driver_cost_long = driver_cost.melt(id_vars='Driver', var_name='Race', value_name='Cost')

constructor_points_long = constructor_points.melt(id_vars='Constructor', var_name='Race', value_name='Points')
constructor_cost_long = constructor_cost.melt(id_vars='Constructor', var_name='Race', value_name='Cost')

# Denormalize Data
driver_data = pd.merge(driver_points_long, driver_cost_long, on=['Driver', 'Race'])
driver_data.dropna(inplace=True)

constructor_data = pd.merge(constructor_points_long, constructor_cost_long, on=['Constructor', 'Race'])
constructor_data.dropna(inplace=True)

# Clean Race names ("Race 1" -> 1)
driver_data['Race'] = driver_data['Race'].str.extract(r'(\d+)').astype(int)
constructor_data['Race'] = constructor_data['Race'].str.extract(r'(\d+)').astype(int)

# print(driver_data)
# print(constructor_data)


constructor_combinations = list(itertools.combinations(constructors, 2))
print(constructor_combinations)

for combo in constructor_combinations:
    constructor_set_cost = sum(
        constructor_data.loc[constructor_data['Constructor'] == combo[0], 'Cost'],
        constructor_data.loc[constructor_data['Constructor'] == combo[1], 'Cost'],
    )
"""

max_points = knapsack_recursion(Points, Cost, Budget, len(Points))

# For loop each race and filter

# We'll brute-force all combinations of 2 or more constructors, and for each such combo:
# Compute the remaining budget
# Use DP or backtracking to pick the best 5-driver combination that fits in that remaining budget.

# Find max possible points with budget and including constructor - classic knapsack
def knapsack_recursion(points, cost, budget, n):

"""

