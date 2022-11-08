import json

def run_log(s):
    """Simple logger"""
    execute("XADD", "run_log", "*", "l", s)

def process_event(x):
    """Process a cashflow event. x is an instance of cash_flow:*, a Redis Hash key
    event for scenario S, year Y."""

    ## cash_flow:S:Y
    scenario = x["key"].split(":")[1]
    year = x["key"].split(":")[2]

    ## Key for year averages. cash_flow_average:Y
    year_cash_flow_average = f"cash_flow_average{year}"

    ## Redis Gears 1.x is using RESP2 so we get back a list. Convert to dict.
    l = execute("HGETALL", year_cash_flow_average)
    d = {l[i]: l[i + 1] for i in range(0, len(l), 2)}

    run_log(json.dumps(x))

    ## No data seen yet, initialize averages
    if not d:
        new_n = 1
        new_avg_net_asset_value = x["value"]["net_asset_value"]
        new_avg_best_estimate_liability = x["value"]["best_estimate_liability"]
    
    ## Update year average
    else:
        new_n = int(d["n"]) + 1

        avg_net_asset_value = int(d["avg_net_asset_value"])
        new_avg_net_asset_value = avg_net_asset_value + ((int(x["value"]["net_asset_value"]) - avg_net_asset_value) / new_n)

        avg_best_estimate_liability = int(d["avg_best_estimate_liability"])
        new_avg_best_estimate_liability = avg_best_estimate_liability + ((int(x["value"]["best_estimate_liability"]) - avg_best_estimate_liability) / new_n)

    execute("HSET", year_cash_flow_average,
        "n", new_n,
        "avg_net_asset_value", new_avg_net_asset_value,
        "avg_best_estimate_liability", new_avg_best_estimate_liability
    )
    execute("LPUSH", "consumed_keys", x["key"])
    ##execute("UNLINK", x["key"])

gb = GB('KeysReader')
gb.foreach(process_event)
gb.register(mode = "sync", prefix="cash_flow:*", key_types = ["hash"], readValue = True)
