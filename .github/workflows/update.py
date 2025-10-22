import requests, json, os

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return {"current": None, "previous": None}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, separators=(',', ':'))

# ----
old = load()
r = requests.get(URL, timeout=15).json()
bnb = r["binancep2p"]
new_entry = {"ask": bnb["ask"], "bid": bnb["bid"], "time": bnb["time"]}

# primer run: current = previous
if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    old["previous"] = old["current"]
    old["current"] = new_entry

save(old)
