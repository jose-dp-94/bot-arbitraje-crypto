import os
import time
import datetime
from binance.client import Client as BinanceClient
from cryptocom.exchange import Exchange as CryptoClient

# Leer claves desde variables de entorno
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY", "").strip()
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET", "").strip()
CRYPTO_API_KEY = os.environ.get("CRYPTO_API_KEY", "").strip()
CRYPTO_API_SECRET = os.environ.get("CRYPTO_API_SECRET", "").strip()

# Validación inicial de claves
if not all([BINANCE_API_KEY, BINANCE_API_SECRET, CRYPTO_API_KEY, CRYPTO_API_SECRET]):
    print("[❌ ERROR] Faltan claves de API. Revisa tus variables en Railway.")
    exit(1)

# Inicializar clientes
binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
crypto = CryptoClient()

# Función para obtener saldo de Binance
def obtener_saldo_binance(moneda="USDT"):
    try:
        balance = binance.get_asset_balance(asset=moneda)
        return float(balance["free"])
    except Exception as e:
        print(f"[❌ ERROR saldo Binance]: {e}")
        return 0.0

# Función para obtener saldo de Crypto.com
def obtener_saldo_crypto(moneda="USDC"):
    try:
        resumen = crypto.get_account_summary()
        return float(resumen["accounts"][0]["available"].get(moneda, 0.0))
    except Exception as e:
        print(f"[❌ ERROR saldo Crypto.com]: {e}")
        return 0.0

# Simulación de arbitraje (aquí va la lógica real si hay diferencias de precios)
def ejecutar_arbitraje():
    print(f"[🟡 {datetime.datetime.now()}] Ejecutando arbitraje...")

    saldo_binance = obtener_saldo_binance()
    saldo_crypto = obtener_saldo_crypto()

    print(f"-> Binance: {saldo_binance} USDT")
    print(f"-> Crypto.com: {saldo_crypto} USDC")

    # Aquí iría la lógica real de comparar precios y mover fondos
    # Por ahora simulamos ganancia
    ganancia_simulada = 2.50
    print(f"[✅ GANANCIA simulada]: {ganancia_simulada} €")

# Bucle principal del bot (entre las 09:00 y 23:00 cada día)
def iniciar_bot():
    while True:
        hora_actual = datetime.datetime.now().hour
        if 9 <= hora_actual <= 23:
            ejecutar_arbitraje()
        else:
            print(f"[⏸ Fuera de horario] Son las {hora_actual}h. Esperando...")
        
        time.sleep(3600)  # Ejecuta cada hora

if __name__ == "__main__":
    print("🚀 Iniciando bot de arbitraje automático...")
    iniciar_bot()
