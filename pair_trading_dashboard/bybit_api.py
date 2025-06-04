import os
from pybit.unified_trading import HTTP

class BybitAPI:
    def __init__(self):
        self.session = HTTP(
            api_key=os.getenv("BYBIT_API_KEY"),
            api_secret=os.getenv("BYBIT_SECRET"),
            testnet=False
        )

    def fetch_ohlcv(self, symbol, interval='1', limit=100):
        response = self.session.get_kline(
            category="linear",
            symbol=symbol.replace('/', ''),
            interval=interval,
            limit=limit
        )
        return response['result']['list'][::-1]

    def create_order(self, symbol, side, qty):
        self.session.place_order(
            category="linear",
            symbol=symbol.replace('/', ''),
            side=side.upper(),
            order_type="Market",
            qty=qty
        )