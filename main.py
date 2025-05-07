import pandas as pd
from algo import *
from utils import *

# Load Data
driver_points, driver_cost, constructor_points, constructor_cost = load_data()

# Pre-process Data
driver_data = preprocess_data(driver_points, driver_cost, 'Driver')
constructor_data = preprocess_data(constructor_points, constructor_cost, 'Constructor')

# -- Generate Best Teams
current_race_number = max(constructor_data["Race"])
for race_number in range(1, current_race_number + 1):

    # Filter data by race
    d_data = driver_data[driver_data["Race"] == race_number]
    c_data = constructor_data[constructor_data["Race"] == race_number]

    n = len(d_data["Driver"].tolist())

    result = best_team_memoization(c_data, d_data, n)
    print(f"Race {race_number}: {result}")
