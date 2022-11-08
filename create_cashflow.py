import concurrent.futures
import random
import time

import redis

YEARS = 1
SCENARIOS = 1
DELAY_YEAR = 0
DELAY_SCENARIO = 0

random.seed()
def generate_cycle_data(year):
    """Return a cycle of data"""

    time.sleep(random.randint(0, DELAY_YEAR))

    return {
        "year": year,
        "net_asset_value": random.randrange(100, 100000),
        "best_estimate_liability": random.randrange(100,1000),
    }

r = redis.Redis(host='localhost', port=12000)
def send_cash_flow(scenario, scenario_years):
    """Send cash to cache for scenario s"""

    for y in scenario_years:
        r.hset(f'cash_flow:{scenario}:{y["year"]}', mapping = y)

def run_scenarios(scenario, years):
    """Create cash flow for scenarios"""

    time.sleep(random.randint(0, DELAY_SCENARIO))

    send_cash_flow(scenario, (generate_cycle_data(y) for y in years))
    return (f"run_scenarios {scenario}:{years}")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(run_scenarios, scenario, range(YEARS)) for scenario in range(SCENARIOS)]
    results = concurrent.futures.wait(futures, return_when = concurrent.futures.ALL_COMPLETED)
    print(results)
