import numpy as np
import time
from statsmodels.tsa.stattools import coint
import json
from datetime import datetime

class PairTradingStrategy:
    def __init__(self, api):
        self.api = api
        self.symbol_a = 'SOL/USDT'
        self.symbol_b = 'ADA/USDT'
        self.amount = 10
        self.data_file = "dashboard_data.json"

    def check_cointegration(self, prices_a, prices_b):
        score, pvalue, _ = coint(prices_a, prices_b)
        return pvalue < 0.05

    def update_dashboard(self, zscore, last_trade):
        data = {
            "zscore": round(zscore, 4),
            "symbol_a": self.symbol_a,
            "symbol_b": self.symbol_b,
            "last_trade": last_trade,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def run(self):
        while True:
            data_a = self.api.fetch_ohlcv(self.symbol_a)
            data_b = self.api.fetch_ohlcv(self.symbol_b)
            prices_a = [x[4] for x in data_a]
            prices_b = [x[4] for x in data_b]

            last_trade = "None"
            if self.check_cointegration(prices_a, prices_b):
                spread = np.array(prices_a) - np.array(prices_b)
                zscore = (spread[-1] - spread.mean()) / spread.std()
                print(f"Z-Score: {zscore}")

                if zscore > 2:
                    print("Short A, Long B")
                    self.api.create_order(self.symbol_a, 'sell', self.amount)
                    self.api.create_order(self.symbol_b, 'buy', self.amount)
                    last_trade = "Short A, Long B"
                elif zscore < -2:
                    print("Long A, Short B")
                    self.api.create_order(self.symbol_a, 'buy', self.amount)
                    self.api.create_order(self.symbol_b, 'sell', self.amount)
                    last_trade = "Long A, Short B"
            else:
                print("Pair not cointegrated")
                zscore = 0

            self.update_dashboard(zscore, last_trade)
            time.sleep(60)