import json, os, datetime
from urllib import request, error
from pytz import timezone

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

# Zonas horarias
utc = timezone('UTC')
caracas = timezone('America/Caracas')

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

# Convertir timestamp a hora de Venezuela
ts_utc = datetime.datetime.utcfromtimestamp(bnb["time"]).replace(tzinfo=utc)
ts_caracas = ts_utc.astimezone(caracas)
hora_str = ts_caracas.strftime("%A, %d/%m/%Y %I:%M %p")

new_entry = {
    "ask": bnb["ask"],
    "bid": bnb["bid"],
    "time": bnb["time"],
    "horaVenezuela": hora_str
}

if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    old["previous"] = old["current"]
    old["current"] = new_entry

save(old)
