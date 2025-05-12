from itertools import combinations, count
import config
# Todo: create test cases


def best_team_memoization(c_data, d_data, n, budget=config.budget_limit):
    """
        Determines the F1 Fantasy team with the most points under a given budget by evaluating
        all 2-constructor combinations and recursively selecting the optimal 5-driver team .

        Args:
            c_data (pd.DataFrame): Constructor data with columns ['Constructor', 'Cost', 'Points'].
            d_data (pd.DataFrame): Driver data with columns ['Driver', 'Cost', 'Points'].
            n (int): Number of drivers to consider.
            budget (float): Total team budget limit.

        Returns:
            tuple:
                - best_team (list): List of selected constructor and driver names.
                - best_points (float): Total points for the best team combination.
        """
    # Init variables
    memo = {}
    best_team, best_points = [], 0

    # Try every pair of constructors
    for constructor_combo in combinations(c_data["Constructor"].tolist(), 2):

        # Sum up cost and points for the constructor pair
        constructors_cost = sum(c_data.loc[c_data['Constructor'] == c, 'Cost'].values[0] for c in constructor_combo)
        constructors_points = sum(c_data.loc[c_data['Constructor'] == c, 'Points'].values[0] for c in constructor_combo)

        # Find the best driver combination under remaining budget after constructors
        drivers, drivers_points = drivers_memoization(d_data, n, memo, budget - constructors_cost, config.driver_limit, False)
        total_points = constructors_points + drivers_points

        # Update best team if this combination scores higher
        if total_points > best_points:
            best_team = sorted(list(constructor_combo)) + sorted(drivers)
            best_points = total_points

    return best_team, float(best_points)


def drivers_memoization(driver_data, n, memo, budget, limit, chip_used):
    """
    Dynamic programming function to select the highest-scoring set of drivers within a budget,
    and the best driver to have the 2x DRS chip.

    Args:
        driver_data (pd.DataFrame): Driver data with columns ['Driver', 'Cost', 'Points'].
        n (int): Number of drivers left to consider.
        memo (dict): Memoization dictionary to cache computed subproblems.
        budget (float): Remaining budget.
        limit (int): Number of drivers still needed to complete the team.
        chip_used (bool): Whether the DRS chip has already been used.

    Returns:
        tuple:
            - team (list): Selected driver names (with "_DRS" suffix if chip applied).
            - points (float): Total points earned by the selected team.
    """
    # Base cases: no drivers or budget left
    if n == 0 or budget == 0:
        if limit == 0:
            return [], 0 # valid team of exactly 5 drivers
        else:
            return [], float('-inf') # invalid team (not enough drivers)

    # Optimization: Re-use cached result if already computed
    elif (n, budget, limit, chip_used) in memo:
        return memo[(n, budget, limit, chip_used)]

    # Get current driver data
    index = n - 1
    points = driver_data["Points"].values[index]
    cost = driver_data["Cost"].values[index]
    driver = driver_data["Driver"].values[index]

    # Optimization: If over budget, skip current driver
    if cost > budget:
        memo[(n, budget, limit, chip_used)] = drivers_memoization(driver_data, index, memo, budget, limit, chip_used)
        return memo[(n, budget, limit, chip_used)]

    # Choice 1 - Include w/o 2x DRS Chip:
    sub_team, sub_points = drivers_memoization(driver_data, index, memo, budget - cost, limit - 1, chip_used)
    include_team = sub_team + [driver]
    include_points = sub_points + points

    # Choice 2 - Include w 2x DRS Chip (if not used yet):
    if not chip_used:
        chip_sub_team, chip_sub_points = drivers_memoization(driver_data, index, memo, budget - cost, limit - 1, True)
        chip_team = chip_sub_team + [driver + "_DRS"]
        chip_points = chip_sub_points + 2 * points

        if chip_points > include_points:
            include_team, include_points = chip_team, chip_points

    # Choice 3 - Exclude
    exclude_team, exclude_points = drivers_memoization(driver_data, index, memo, budget, limit, chip_used)

    # Evaluate subproblem: Take the option with the higher score
    if include_points > exclude_points:
        memo[(n, budget, limit, chip_used)] = include_team, include_points
    else:
        memo[(n, budget, limit, chip_used)] = exclude_team, exclude_points

    return memo[(n, budget, limit, chip_used)]
