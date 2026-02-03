import json, os, datetime, locale
from urllib import request, error

URL = "https://criptoya.com/api/usdt/ves"
FILE = "rates.json"

# Configuración de idioma para GitHub (Ubuntu)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    pass

def load():
    if not os.path.exists(FILE):
        return {"current": None, "previous": None}
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"current": None, "previous": None}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, separators=(',', ':'))

# ---- Inicio ----
print(f"--- Iniciando script: {datetime.datetime.now()} ---")
old = load()

try:
    req = request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        print("¡Conexión exitosa a la API de CriptoYa!")
except Exception as e:
    print(f"Error de conexión: {e}")
    exit(0)

if "binancep2p" not in data:
    print("No hay datos de binancep2p")
    exit(0)

bnb = data["binancep2p"]

# --- LÓGICA DE TIEMPO ---
ts_valor = bnb["time"]

# Detectar si son milisegundos (13 dígitos) o segundos (10 dígitos)
if ts_valor > 10000000000:
    ts_segundos = ts_valor / 1000
    print("Formato detectado: Milisegundos")
else:
    ts_segundos = ts_valor
    print("Formato detectado: Segundos")

# Ajuste a Venezuela (UTC-4)
dt_utc = datetime.datetime.fromtimestamp(ts_segundos, tz=datetime.timezone.utc)
dt_venezuela = dt_utc - datetime.timedelta(hours=4)
hora_str = dt_venezuela.strftime("%A, %d/%m/%Y %I:%M %p")

print(f"Fecha calculada: {hora_str}")

new_entry = {
    "ask": bnb["ask"],
    "bid": bnb["bid"],
    "time": ts_valor, # Guardamos el valor original (sea cual sea)
    "horaVenezuela": hora_str
}

# Lógica de actualización
if old["current"] is None:
    old["current"] = old["previous"] = new_entry
else:
    # Solo actualizamos si el timestamp es distinto al guardado
    if old["current"]["time"] != ts_valor:
        old["previous"] = old["current"]
        old["current"] = new_entry
    else:
        print("Los datos ya están actualizados. No se requiere nuevo registro.")

save(old)
print("Proceso completado.")
