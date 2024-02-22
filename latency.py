import ccxt
import time
import logging

# Configurazione del logger per registrare in nanosecondi
logging.basicConfig(filename='latency_log_ns.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

api_key = 'YOUR_API_KEY'
secret = 'YOUR_API_SECRET'
bybit = ccxt.bybit({
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
})

symbol = 'BTC/USDT:USDT'
amount = 0.001
price = 10000

try:
    # Inizio misurazione latenza per la creazione dell'ordine
    start_ns = time.perf_counter_ns()
    order = bybit.create_limit_buy_order(symbol, amount, price)
    end_ns = time.perf_counter_ns()
    latency_creation_ns = end_ns - start_ns
    print(f"Ordine creato in {latency_creation_ns} nanosecondi")
    logging.info(f"Order created. Latency: {latency_creation_ns} ns. Order details: {order}")

    # Inizio misurazione latenza per la cancellazione dell'ordine
    start_cancel_ns = time.perf_counter_ns()
    bybit.cancel_order(order['id'], symbol)
    end_cancel_ns = time.perf_counter_ns()
    latency_cancel_ns = end_cancel_ns - start_cancel_ns
    print(f"Ordine cancellato in {latency_cancel_ns} nanosecondi")
    logging.info(f"Order cancelled. Latency: {latency_cancel_ns} ns.")
except ccxt.BaseError as e:
    logging.error(f"CCXT Error: {e}")
    print(f"Errore CCXT: {e}")
except Exception as e:
    logging.error(f"General Error: {e}")
    print(f"Errore Generico: {e}")
