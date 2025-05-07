import pandas as pd


def load_data():
    driver_points = pd.read_csv('./data/F1 Fantasy Driver Data - Points.csv')
    driver_cost = pd.read_csv('./data/F1 Fantasy Driver Data - Price.csv')
    constructor_points = pd.read_csv('./data/F1 Fantasy Constructor Data - Points.csv')
    constructor_cost = pd.read_csv('./data/F1 Fantasy Constructor Data - Price.csv')
    return driver_points, driver_cost, constructor_points, constructor_cost


def preprocess_data(points_df, cost_df, id_col):
    points_long = points_df.melt(id_vars=id_col, var_name='Race', value_name='Points')
    cost_long = cost_df.melt(id_vars=id_col, var_name='Race', value_name='Cost')

    data = pd.merge(points_long, cost_long, on=[id_col, 'Race'])
    data.dropna(inplace=True)
    data['Race'] = data['Race'].str.extract(r'(\d+)').astype(int)

    return data
