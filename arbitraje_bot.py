import os
import time
import datetime
from binance.client import Client as BinanceClient
from cryptocom.exchange import Exchange as CryptoClient

# Obtener claves de entorno
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
CRYPTO_API_SECRET = os.getenv("CRYPTO_API_SECRET")

# Inicializar clientes con claves
binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
crypto = CryptoClient(api_key=CRYPTO_API_KEY, api_secret=CRYPTO_API_SECRET)

# Función para obtener saldo de Binance en USDT
def obtener_saldo_binance():
    try:
        cuenta = binance.get_account()
        for balance in cuenta['balances']:
            if balance['asset'] == 'USDT':
                return float(balance['free'])
    except Exception as e:
        print(f"[❌ ERROR Binance]: {e}")
    return 0.0

# Función para obtener saldo de Crypto.com en USDC
def obtener_saldo_crypto():
    try:
        cuentas = crypto.get_accounts()
        for cuenta in cuentas['result']['data']:
            if cuenta['instrument_name'] == 'USDC':
                return float(cuenta['available'])
    except Exception as e:
        print(f"[❌ ERROR Crypto.com]: {e}")
    return 0.0

# Simulación de arbitraje real (simplificada para ejemplo)
def ejecutar_arbitraje():
    saldo_binance = obtener_saldo_binance()
    saldo_crypto = obtener_saldo_crypto()
    
    print(f"-> Saldo Binance (USDT): {saldo_binance}")
    print(f"-> Saldo Crypto.com (USDC): {saldo_crypto}")

    if saldo_binance >= 10:
        try:
            orden = binance.order_market_buy(symbol="BTCUSDT", quoteOrderQty=10)
            print(f"[✅ Binance] Compra de BTC realizada: {orden}")
        except Exception as e:
            print(f"[❌ ERROR compra Binance]: {e}")

    if saldo_crypto >= 10:
        try:
            orden = crypto.create_market_order("BTC_USDC", "buy", notional=10)
            print(f"[✅ Crypto.com] Compra de BTC realizada: {orden}")
        except Exception as e:
            print(f"[❌ ERROR compra Crypto.com]: {e}")

# Inicio del bot en bucle horario
print("🚀 BOT DE ARBITRAJE REAL ACTIVADO")

while True:
    hora = datetime.datetime.now().hour
    if 10 <= hora < 22:
        print(f"🕒 {datetime.datetime.now()} - Ejecutando operaciones de arbitraje...")
        ejecutar_arbitraje()
    else:
        print(f"⏸️ {datetime.datetime.now()} - Fuera de horario.")
    time.sleep(3600)
