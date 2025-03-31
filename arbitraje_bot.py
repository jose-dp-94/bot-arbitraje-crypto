import os
import time
from datetime import datetime
import pytz
from binance.client import Client as BinanceClient
from cryptocom.exchange import Exchange

# Cargar variables de entorno
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
CRYPTO_API_SECRET = os.getenv("CRYPTO_API_SECRET")

# Inicializar clientes de los exchanges
binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
crypto = Exchange()
crypto.set_credentials(api_key=CRYPTO_API_KEY, api_secret=CRYPTO_API_SECRET)

# Función para obtener saldo en Binance
def get_binance_balance():
    balance = binance.get_asset_balance(asset="USDT")
    return float(balance["free"]) if balance else 0.0

# Función para obtener saldo en Crypto.com
def get_crypto_balance():
    try:
        accounts = crypto.get_accounts()
        for acc in accounts:
            if acc["instrument_name"] == "USDC":
                return float(acc["available"])
        return 0.0
    except Exception as e:
        print("[❌ ERROR saldo Crypto.com]:", e)
        return 0.0

# Función para ejecutar arbitraje (simulado por ahora)
def ejecutar_arbitraje():
    print(f"⚙️ {datetime.now().isoformat()} Ejecutando arbitraje...")
    saldo_binance = get_binance_balance()
    saldo_crypto = get_crypto_balance()

    print(f"-> Binance: {saldo_binance} USDT")
    print(f"-> Crypto.com: {saldo_crypto} USDC")

    ganancia_simulada = round(2 + saldo_binance * 0.01, 2)
    print(f"✅ GANANCIA simulada: {ganancia_simulada} €")

# Bucle principal
print("🚀 Iniciando bot de arbitraje automático...")

timezone_es = pytz.timezone('Europe/Madrid')

while True:
    now = datetime.now(timezone_es)
    hora_actual = now.hour

    if 12 <= hora_actual < 23:
        ejecutar_arbitraje()
    else:
        print(f"[⏸️ Fuera de horario] Son las {hora_actual}h. Esperando...")

    time.sleep(3600)  # Espera una hora
