import time
from datetime import datetime
from binance.client import Client as BinanceClient
from cryptocom.exchange import Exchange

import os

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
CRYPTO_API_SECRET = os.getenv("CRYPTO_API_SECRET")

binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
crypto = Exchange()
crypto.api_key = CRYPTO_API_KEY
crypto.api_secret = CRYPTO_API_SECRET

def obtener_saldo_binance():
    usdt_balance = binance.get_asset_balance(asset='USDT')
    return float(usdt_balance['free']) if usdt_balance else 0.0

def obtener_saldo_crypto():
    try:
        balances = crypto.get_accounts()
        usdc_balance = next((float(acc['available']) for acc in balances if acc['asset'] == 'USDC'), 0.0)
        return usdc_balance
    except Exception as e:
        print(f"[❌ ERROR saldo Crypto.com]: {e}")
        return 0.0

def operar_arbitraje():
    print(f"⚙️ {datetime.now()} Ejecutando arbitraje...")
    saldo_binance = obtener_saldo_binance()
    saldo_crypto = obtener_saldo_crypto()

    print(f"-> Binance: {saldo_binance} USDT")
    print(f"-> Crypto.com: {saldo_crypto} USDC")

    if saldo_binance > saldo_crypto:
        ganancia = saldo_binance * 0.015
    else:
        ganancia = saldo_crypto * 0.015

    print(f"✅ GANANCIA simulada: {round(ganancia, 2)} €")

if __name__ == "__main__":
    print("🚀 Iniciando bot de arbitraje automático...")
    while True:
        hora_actual = datetime.now().hour
        if 12 <= hora_actual <= 23:
            operar_arbitraje()
        else:
            print(f"[⏸️ Fuera de horario] Son las {hora_actual}h. Esperando...")
        time.sleep(3600)
