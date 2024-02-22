import json
import os
import sys
from pprint import pprint
import ccxt

# Load API credentials
with open('api.json', 'r') as file:
    credentials = json.load(file)

exchange = ccxt.bybit({
    'apiKey': credentials['apiKey'],
    'secret': credentials['secret'],
    'enableRateLimit': False,
})

exchange.load_markets()
    symbol = 'BTC/USDT'  # Ensure this symbol is available on Bybit
    market = exchange.market(symbol)
    ticker = exchange.fetch_ticker(symbol)

    price = ticker['last'] * 0.8
    amount = round(market['limits']['cost']['min'] / price, 4)

    results = []

    for i in range(0, 10):
        started = exchange.milliseconds()
        order = exchange.create_order(symbol, 'limit', 'buy', amount, price)
        ended = exchange.milliseconds()
        elapsed = ended - started
        results.append(elapsed)
        exchange.cancel_order(order['id'], symbol)
        pprint(order)
        pprint(results)

    rtt = int(sum(results) / len(results))
    print('Successfully tested 10 orders, the average round-trip time per order is', rtt, 'milliseconds')

main()
