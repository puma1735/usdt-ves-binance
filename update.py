import json, os, datetime, locale
from urllib import request, error

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

# Español si está disponible
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
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

# Paso 1: segundos → milisegundos
ts_ms = bnb["time"] * 1000

# Paso 2: UTC+0 → UTC-4 (restar 4 h)
ts_venezuela = (ts_ms // 1000) - 4 * 3600

# Paso 3: formatear en español
hora_str = datetime.datetime.utcfromtimestamp(ts_venezuela).strftime("%A, %d/%m/%Y %I:%M %p")

new_entry = {
    "ask": bnb["ask"],
    "bid": bnb["bid"],
    "time": ts_ms,  # milisegundos
    "horaVenezuela": hora_str
}

if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    old["previous"] = old["current"]
    old["current"] = new_entry

save(old)
