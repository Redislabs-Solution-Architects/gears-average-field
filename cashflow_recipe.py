def run_log(s):
    """Simple logger"""
    execute("XADD", "run_log", "*", "l", s)

def process_event(x):
    """Process a cashflow event. x is an instance of cash_flow:*, a Redis Hash key
    event for scenario S, year Y."""

    ## cash_flow:S:Y
    scenario = f'cash_flow_average:{x["key"].split(":")[1]}'
    year = f'cash_flow_average:{x["key"].split(":")[2]}'

    ## Key for year averages. cash_flow_average:Y
    year_cash_flow_average = f"cash_flow_average{year}"

    d = execute("HGETALL", year_cash_flow_average)

    ## No data seen yet, initialize averages
    if not d:
        new_n = 1
        new_avg_net_asset_value = x["value"]["net_asset_value"]
        new_avg_best_estimate_liability = x["value"]["best_estimate_liability"]
    
    ## Update year average
    else:
        new_n = d["n"] + 1

        avg_net_asset_value = d["avg_net_asset_value"]
        new_avg_net_asset_value = avg_net_asset_value + ((x["value"]["net_asset_value"] - avg_net_asset_value) / new_n)

        avg_best_estimate_liability = d["avg_best_estimate_liability"]
        new_avg_best_estimate_liability = avg_best_estimate_liability + ((x["value"]["best_estimate_liability"] - avg_best_estimate_liability) / new_n)

    execute("HSET", year_cash_flow_average,
        "n", new_n,
        "avg_net_asset_value", new_avg_net_asset_value,
        "avg_best_estimate_liability", new_avg_best_estimate_liability
    )
    execute("LPUSH", "consumed_keys", x["key"])

gb = GB('KeysReader')
gb.foreach(process_event)
gb.register(prefix="cash_flow:*", key_types = ["hash"], readValue = True)


