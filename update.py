import json, os, datetime, locale
from urllib import request, error

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

# Forzamos idioma español (si el sistema lo tiene)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    # Si no está disponible, usamos el default sin fallar
    pass

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

# Ajuste real: restamos 4 h 14 min 25 s (15265 segundos)
ajuste_seg = 4 * 3600 + 14 * 60 + 25
ts_local = bnb["time"] - ajust_seg
hora_str = datetime.datetime.utcfromtimestamp(ts_local).strftime("%A, %d/%m/%Y %I:%M %p")

new_entry = {
    "ask": bnb["ask"],
    "bid": bnb["bid"],
    "time": ts_local,  # ← ya en tu hora local
    "horaVenezuela": hora_str
}

if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    old["previous"] = old["current"]
    old["current"] = new_entry

save(old)
