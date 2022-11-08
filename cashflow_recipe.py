# def log(s):
#     """Simple logger"""
#     execute("XADD", "run_log", "*", "l", s)

def process_event(x):
    """Process a key event"""
    log("foo")
    log(x['key'])

gb = GB('KeysReader')
gb.foreach(process_event)
gb.register(prefix="cash_flow:*", key_types = ["hash"], readValue = True)


