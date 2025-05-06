import pandas as pd
from algo import *

# -- Load & Pre-process Data
driver_points = pd.read_csv('./data/F1 Fantasy Driver Data - Points.csv')
driver_cost = pd.read_csv('./data/F1 Fantasy Driver Data - Price.csv')
constructor_points = pd.read_csv('./data/F1 Fantasy Constructor Data - Points.csv')
constructor_cost = pd.read_csv('./data/F1 Fantasy Constructor Data - Price.csv')

# Store drivers and constructor names
drivers = driver_points['Driver']
constructors = constructor_points['Constructor']

# Remove irrelevant data
driver_points.drop('AVG', axis=1, inplace=True)
driver_cost.drop('AVG', axis=1, inplace=True)

# constructor_points.drop('AVG', axis=1, inplace=True)
# constructor_cost.drop('AVG', axis=1, inplace=True)

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

curr_race = max(constructor_data["Race"])

# -- Generate Best Teams
for race_number in range(1, curr_race + 1):
    d_data = driver_data[driver_data["Race"] == race_number]
    c_data = constructor_data[constructor_data["Race"] == race_number]

    result = best_team_memoization(c_data, d_data, len(d_data["Driver"].tolist()))
    print(f"Race {race_number}: {result}")
