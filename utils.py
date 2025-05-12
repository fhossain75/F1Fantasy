import ast
import os

import pandas as pd


def load_data(root_dir):
    """
    Loads F1 Fantasy data from CSV files.

    Returns:
        tuple: A tuple containing the following pandas DataFrames:
            - driver_points: Points data for drivers
            - driver_cost: Cost data for drivers
            - constructor_points: Points data for constructors
            - constructor_cost: Cost data for constructors
    """
    driver_points = pd.read_csv(os.path.join(root_dir, 'F1 Fantasy Driver Data - Points.csv'))
    driver_cost = pd.read_csv(os.path.join(root_dir, 'F1 Fantasy Driver Data - Price.csv'))
    constructor_points = pd.read_csv(os.path.join(root_dir, 'F1 Fantasy Constructor Data - Points.csv'))
    constructor_cost = pd.read_csv(os.path.join(root_dir, 'F1 Fantasy Constructor Data - Price.csv'))
    return driver_points, driver_cost, constructor_points, constructor_cost

def preprocess_data(points_df, cost_df, id_col):
    """
    Preprocesses F1 Fantasy data by reshaping it from wide to long format,
    merging point and cost data, cleaning missing values, and ensuring numeric types.

    Args:
        points_df (pd.DataFrame): DataFrame containing points per race.
        cost_df (pd.DataFrame): DataFrame containing cost per race in wide format.
        id_col (str): Column name that uniquely identifies the entity.

    Returns:
        pd.DataFrame: A long-format DataFrame with columns [id_col, Race, Points, Cost].
    """
    # Reshape wide-formatted data into long format
    points_long = points_df.melt(id_vars=id_col, var_name='Race', value_name='Points')
    cost_long = cost_df.melt(id_vars=id_col, var_name='Race', value_name='Cost')

    # Merge points and cost data, clean missing values
    data = pd.merge(points_long, cost_long, on=[id_col, 'Race'])
    data.dropna(inplace=True) #todo: check na dropping

    # Ensure numeric data values
    data['Race'] = data['Race'].str.extract(r'(\d+)').astype(int)
    data['Points'] = data['Points'].astype(float)
    data['Cost'] = data['Cost'].astype(float)

    return data

# TODO: include chips into total (3x, No negatives)
def calculate_personal_team(root_dir):
    """
    """
    # Load Data
    driver_points, driver_cost, constructor_points, constructor_cost = load_data(root_dir)
    personal_team_df = pd.read_csv(os.path.join(root_dir, 'Faisal Teams.csv'))

    # Pre-process Data
    d_data = preprocess_data(driver_points, driver_cost, 'Driver')
    c_data = preprocess_data(constructor_points, constructor_cost, 'Constructor')

    # Calculate total points
    results = []
    for _, row in personal_team_df.iterrows():

        # Init curr variables
        race = row["Race"]
        constructors = ast.literal_eval(row["Constructors"])
        drivers = ast.literal_eval(row["Drivers"])
        drs_driver = str(row["2xDRS"])

        # Get matching drivers and constructors for this race
        race_driver_data = d_data[(d_data["Race"] == race) & (d_data["Driver"].isin(drivers))]
        race_constructor_data = c_data[(c_data["Race"] == race) & (c_data["Constructor"].isin(constructors))]

        # Apply 2x multiplier on DRS driver
        race_driver_data.loc[(race_driver_data["Driver"] == drs_driver), "Points"] *= 2

        results.append({
            "Race": race,
            "Constructors": constructors,
            "Drivers": drivers,
            "2xDRS": drs_driver,
            "Total Points": race_driver_data["Points"].sum() + race_constructor_data["Points"].sum()
        })

    return pd.DataFrame(results)
