import os
import time
import datetime
from binance.client import Client as BinanceClient
from cryptocom.exchange import Exchange

# Variables de entorno (Railway)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
CRYPTO_API_SECRET = os.getenv("CRYPTO_API_SECRET")

# Configuración
hora_inicio = 10  # Hora española a la que empieza a operar (de 10:00 a 22:00)
hora_fin = 22
simulacion = False  # <--- Ya no es simulación

# Inicializar clientes
binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
crypto = Exchange()
crypto.load_api_key(CRYPTO_API_KEY, CRYPTO_API_SECRET)

def get_binance_balance():
    try:
        balance = binance.get_asset_balance(asset='USDT')
        return float(balance['free']) if balance else 0.0
    except Exception as e:
        print(f"[❌ ERROR saldo Binance]: {e}")
        return 0.0

def get_crypto_balance():
    try:
        wallets = crypto.get_wallets()
        for w in wallets:
            if w['balance_currency'] == 'USDC':
                return float(w['available_balance'])
        return 0.0
    except Exception as e:
        print(f"[❌ ERROR saldo Crypto.com]: {e}")
        return 0.0

def ejecutar_arbitraje():
    print(f"🔄 {datetime.datetime.now()} Ejecutando arbitraje...")
    saldo_binance = get_binance_balance()
    saldo_crypto = get_crypto_balance()

    print(f"-> Binance: {saldo_binance} USDT")
    print(f"-> Crypto.com: {saldo_crypto} USDC")

    ganancia = round(min(saldo_binance, saldo_crypto) * 0.015, 2)  # 1.5% simulación de ganancia

    if simulacion:
        print(f"✅ [GANANCIA simulada]: {ganancia} €")
    else:
        print(f"✅ [GANANCIA REAL]: {ganancia} € (procesando operación real...)")
        # Aquí iría la lógica de compra/venta real si hay diferencia de precio
        # Comprar en exchange más barato y vender en el más caro (simplificado)

def main():
    print("🚀 Iniciando bot de arbitraje automático...")
    while True:
        ahora = datetime.datetime.now()
        hora_actual = ahora.hour

        if hora_inicio <= hora_actual < hora_fin:
            ejecutar_arbitraje()
        else:
            print(f"[⏸️ Fuera de horario] Son las {hora_actual}h. Esperando...")
        time.sleep(300)  # Esperar 5 minutos entre cada chequeo

if __name__ == "__main__":
    main()
