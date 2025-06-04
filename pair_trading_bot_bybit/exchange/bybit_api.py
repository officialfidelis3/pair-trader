import ccxt
import time
import os

class BybitAPI:
    def __init__(self):
        self.exchange = ccxt.bybit({
            'apiKey': os.getenv('BYBIT_API_KEY', 'YOUR_API_KEY'),
            'secret': os.getenv('BYBIT_SECRET', 'YOUR_SECRET'),
            'enableRateLimit': True
        })

    def fetch_ohlcv(self, symbol, timeframe='1m', limit=100):
        return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def create_order(self, symbol, side, amount):
        if side == 'buy':
            return self.exchange.create_market_buy_order(symbol, amount)
        elif side == 'sell':
            return self.exchange.create_market_sell_order(symbol, amount)