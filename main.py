from algo import *
from utils import *
from tqdm import tqdm

def main(root_dir):
    # Load Data
    driver_points, driver_cost, constructor_points, constructor_cost = load_data(root_dir)

    # Pre-process Data
    driver_data = preprocess_data(driver_points, driver_cost, 'Driver')
    constructor_data = preprocess_data(constructor_points, constructor_cost, 'Constructor')

    # -- Generate Best Teams
    results = []
    current_race_number = max(constructor_data["Race"])
    for race_number in tqdm(range(1, current_race_number + 1), desc="Optimizing Races"):

        # Filter data by race
        d_data = driver_data[driver_data["Race"] == race_number]
        c_data = constructor_data[constructor_data["Race"] == race_number]

        n = len(d_data["Driver"].tolist())
        team, points = best_team_memoization(c_data, d_data, n)

        results.append({
            "Race": race_number,
            "Team": team,
            "Total Points": points
        })

    return pd.DataFrame(results)

# if __name__ == "__main__":
#     print(main("./data"))
