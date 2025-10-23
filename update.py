import json, os, datetime
from urllib import request, error

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

def load():
    if not os.path.exists(FILE):
        return {"current": None, "previous": None}
    try:
        with open(FILE) as f:
            data = json.load(f)
        if "current" not in data or "previous" not in data:
            return {"current": None, "previous": None}
        return data
    except:
        return {"current": None, "previous": None}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, separators=(',', ':'))

# ----
old = load()
try:
    with request.urlopen(URL, timeout=15) as resp:
        data = json.loads(resp.read().decode())
except error.URLError:
    data = {}

if "binancep2p" not in data:
    exit(0)  # no hay datos, no actualizamos

bnb = data["binancep2p"]

# Convertimos UTC+8 → UTC+0 (restamos 8 horas)
utc_time = bnb["time"] - 8 * 3600

new_entry = {
    "ask": bnb["ask"],
    "bid": bnb["bid"],
    "time": utc_time  # ← ya en UTC+0
}

if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    old["previous"] = old["current"]
    old["current"] = new_entry

save(old)
