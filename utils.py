import pandas as pd


def load_data():
    """
    Loads F1 Fantasy data from CSV files.

    Returns:
        tuple: A tuple containing the following pandas DataFrames:
            - driver_points: Points data for drivers
            - driver_cost: Cost data for drivers
            - constructor_points: Points data for constructors
            - constructor_cost: Cost data for constructors
    """
    driver_points = pd.read_csv('./data/F1 Fantasy Driver Data - Points.csv')
    driver_cost = pd.read_csv('./data/F1 Fantasy Driver Data - Price.csv')
    constructor_points = pd.read_csv('./data/F1 Fantasy Constructor Data - Points.csv')
    constructor_cost = pd.read_csv('./data/F1 Fantasy Constructor Data - Price.csv')
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
